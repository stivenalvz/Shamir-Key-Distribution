import mnemonic
import bip32utils
import hashlib
import base58
from bech32 import bech32_encode, convertbits
from hdwallet import BIP84HDWallet
from hdwallet.cryptocurrencies import BitcoinMainnet
from mnemonic import Mnemonic
from shamir_mnemonic import combine_mnemonics, generate_mnemonics
from shamir_mnemonic.utils import MnemonicError
from ecdsa import SigningKey, SECP256k1
from eth_hash.auto import keccak

def DireccionEthereum(private_key_hex):
    # Convierte la clave privada hexadecimal a bytes
    private_key_bytes = bytes.fromhex(private_key_hex)

    # Usa ecdsa para generar la clave pública a partir de la clave privada
    private_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    public_key = private_key.get_verifying_key().to_string()

    # Crea el hash Keccak-256 de la clave pública
    keccak_hash = keccak(public_key)

    # La dirección Ethereum es los últimos 20 bytes del hash Keccak-256
    eth_address = '0x' + keccak_hash[-20:].hex()

    return eth_address

def DireccionTron(private_key_hex):    
    # Convierte la clave privada hexadecimal a bytes
    private_key_bytes = bytes.fromhex(private_key_hex)

    # Usa ecdsa para generar la clave pública a partir de la clave privada
    private_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    public_key = private_key.get_verifying_key().to_string()

    # Hash Keccak-256 de la clave pública
    keccak_hash = keccak(public_key)

    # Tron utiliza el prefijo 0x41 en lugar del prefijo de Ethereum 0x
    tron_address_hex = '41' + keccak_hash[-20:].hex()

    # Convertir la dirección a bytes
    tron_address_bytes = bytes.fromhex(tron_address_hex)

    # Calcular el checksum (primeros 4 bytes del hash SHA256 del hash SHA256 de la dirección)
    sha256_1 = hashlib.sha256(tron_address_bytes).digest()
    sha256_2 = hashlib.sha256(sha256_1).digest()
    checksum = sha256_2[:4]

    # Añadir el checksum a la dirección y codificarla en Base58
    tron_address_with_checksum = tron_address_bytes + checksum
    tron_address_base58 = base58.b58encode(tron_address_with_checksum).decode()

    return tron_address_base58

def crearPalabrasShamir(entropy,gruposMinimos,deCantidad,sobreTotal):
    mnemo = Mnemonic("english")
    master_secret = mnemo.to_entropy(entropy)
    try:
        mnemonics = generate_mnemonics(
            group_threshold=gruposMinimos, 
            groups=[(deCantidad, sobreTotal)], 
            master_secret=master_secret
        )
        
        return mnemonics[0]     
            
    except MnemonicError as e:
        return 'Error al generar  mnemonics'


def restaurarPalabrasShamir(arrayMenemonic):
    try:
        mnemo = Mnemonic("english")
        recovered_mnemonic = combine_mnemonics(arrayMenemonic)
        recovered_seed_words = mnemo.to_mnemonic(recovered_mnemonic)
        return recovered_seed_words
    except MnemonicError as e:
        return 'Error al restaurar mnemonics'


def crearDireccion(palabras,gruposMinimos,deCantidad,sobreTotal):
    if palabras == 12:
        bytesAleatorios = 128
    elif palabras == 24:
        bytesAleatorios = 256    
    else:
        raise ValueError("Número de palabras debe ser 12 o 24")

    # 1. Generar una frase semilla aleatoria
    mnemo = mnemonic.Mnemonic("english")
    seed_phrase = mnemo.generate(strength=bytesAleatorios)  # Genera una frase semilla con 128 o 256 bits de entropía
    Shamir = crearPalabrasShamir(seed_phrase,gruposMinimos,deCantidad,sobreTotal)

    
    # 2. Generar la semilla (clave privada maestra) desde la frase semilla
    seed = mnemo.to_seed(seed_phrase)

    # 3. Usar BIP-32 para derivar la clave privada y dirección pública utilizando las rutas BIP-44, BIP-49, y BIP-84

    # BIP-44: Legacy (P2PKH)
    bip44_key = bip32utils.BIP32Key.fromEntropy(seed).ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
    public_key_44 = bip44_key.PublicKey()
    private_key_44 = bip44_key.PrivateKey()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(public_key_44).digest())
    legacy_address = base58.b58encode_check(b'\x00' + ripemd160.digest()).decode()

    # BIP-49: SegWit (P2SH-P2WPKH)
    bip49_key = bip32utils.BIP32Key.fromEntropy(seed).ChildKey(49 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
    public_key_49 = bip49_key.PublicKey()
    private_key_49 = bip49_key.PrivateKey()
    ripemd160_seg = hashlib.new('ripemd160')
    ripemd160_seg.update(hashlib.sha256(public_key_49).digest())
    script_pub_key = b'\x00\x14' + ripemd160_seg.digest()
    hashed_script_pub_key = hashlib.new('ripemd160', hashlib.sha256(script_pub_key).digest()).digest()
    segwit_address = base58.b58encode_check(b'\x05' + hashed_script_pub_key).decode()

    # Clave privada y pública para BIP84 (Native SegWit)
    # BIP-84: Native SegWit (Bech32)
    bip84_key = bip32utils.BIP32Key.fromEntropy(seed).ChildKey(84 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
    public_key_84 = bip84_key.PublicKey()
    private_key_bip84 = bip84_key.PrivateKey()
    
    wallet_segwit = BIP84HDWallet(cryptocurrency=BitcoinMainnet)
    wallet_segwit.from_private_key(private_key=private_key_bip84.hex())
    address_segwit_native = wallet_segwit.address()
    
    direccionEthereum = DireccionEthereum(private_key_44.hex())
    direccionTron = DireccionTron(private_key_44.hex())
    
    # Retornar todos los resultados en una lista
    return {
        'seed_phrase': seed_phrase,
        'legacy': {
            'private_key': private_key_44.hex(),
            'address': legacy_address
        },
        'segwit': {
            'private_key': private_key_49.hex(),
            'address': segwit_address
        },
        'native_segwit': {
            'private_key': private_key_bip84.hex(),
            'address': address_segwit_native
        },
        'ethereum': {
            'private_key': private_key_44.hex(),
            'address': direccionEthereum
        },
        'tron': {
            'private_key': private_key_44.hex(),
            'address': direccionTron
        },
        'shamir':Shamir
    }

def recuperarWallet(seed_phrase,gruposMinimos,deCantidad,sobreTotal):

    # 1. Generar la semilla (clave privada maestra) desde la frase semilla
    mnemo = mnemonic.Mnemonic("english")
    seed = mnemo.to_seed(seed_phrase)
    Shamir = crearPalabrasShamir(seed_phrase,gruposMinimos,deCantidad,sobreTotal)
    # 2. Usar BIP-32 para derivar la clave privada y dirección pública utilizando la ruta BIP-44
    bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
    
    # Clave privada y pública para BIP44 (Legacy)
    bip44_account_key_obj = bip32_root_key_obj.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
    public_key_bip44 = bip44_account_key_obj.PublicKey()
    private_key_bip44 = bip44_account_key_obj.PrivateKey()
    
    # Dirección Legacy (P2PKH)
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(public_key_bip44).digest())
    hashed_public_key_bip44 = ripemd160.digest()
    legacy_address = base58.b58encode_check(b'\x00' + hashed_public_key_bip44).decode()

    # Clave privada y pública para BIP49 (SegWit)
    bip49_account_key_obj = bip32_root_key_obj.ChildKey(49 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
    public_key_bip49 = bip49_account_key_obj.PublicKey()
    private_key_bip49 = bip49_account_key_obj.PrivateKey()
    
    # Dirección SegWit (P2SH-P2WPKH)
    ripemd160_seg = hashlib.new('ripemd160')
    ripemd160_seg.update(hashlib.sha256(public_key_bip49).digest())
    hashed_public_key_bip49 = ripemd160_seg.digest()
    script_pub_key_bip49 = b'\x00\x14' + hashed_public_key_bip49
    hashed_script_pub_key_bip49 = hashlib.new('ripemd160', hashlib.sha256(script_pub_key_bip49).digest()).digest()
    segwit_address = base58.b58encode_check(b'\x05' + hashed_script_pub_key_bip49).decode()

    # Clave privada y pública para BIP84 (Native SegWit)
    # BIP-84: Native SegWit (Bech32)
    bip84_key = bip32utils.BIP32Key.fromEntropy(seed).ChildKey(84 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
    public_key_84 = bip84_key.PublicKey()
    private_key_bip84 = bip84_key.PrivateKey()
    
    wallet_segwit = BIP84HDWallet(cryptocurrency=BitcoinMainnet)
    wallet_segwit.from_private_key(private_key=private_key_bip84.hex())
    address_segwit_native = wallet_segwit.address()
    
    direccionEthereum = DireccionEthereum(private_key_bip44.hex())
    direccionTron = DireccionTron(private_key_bip44.hex())

    return {
        'seed_phrase': seed_phrase,
        'legacy': {
            'private_key': private_key_bip44.hex(),
            'address': legacy_address
        },
        'segwit': {
            'private_key': private_key_bip49.hex(),
            'address': segwit_address
        },
        'native_segwit': {
            'private_key': private_key_bip84.hex(),
            'address': address_segwit_native
        },
        'ethereum': {
            'private_key': private_key_bip44.hex(),
            'address': direccionEthereum
        },
        'tron': {
            'private_key': private_key_bip44.hex(),
            'address': direccionTron
        }
        ,'shamir':Shamir
    }


def recuperarWalletShamir(arrayShamir,gruposMinimos,deCantidad,sobreTotal):
    seed_phrase = restaurarPalabrasShamir(arrayShamir)

    # 1. Generar la semilla (clave privada maestra) desde la frase semilla
    mnemo = mnemonic.Mnemonic("english")
    seed = mnemo.to_seed(seed_phrase)

    Shamir = crearPalabrasShamir(seed_phrase,gruposMinimos,deCantidad,sobreTotal)
    # 2. Usar BIP-32 para derivar la clave privada y dirección pública utilizando la ruta BIP-44
    bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
    
    # Clave privada y pública para BIP44 (Legacy)
    bip44_account_key_obj = bip32_root_key_obj.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
    public_key_bip44 = bip44_account_key_obj.PublicKey()
    private_key_bip44 = bip44_account_key_obj.PrivateKey()
    
    # Dirección Legacy (P2PKH)
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(public_key_bip44).digest())
    hashed_public_key_bip44 = ripemd160.digest()
    legacy_address = base58.b58encode_check(b'\x00' + hashed_public_key_bip44).decode()

    # Clave privada y pública para BIP49 (SegWit)
    bip49_account_key_obj = bip32_root_key_obj.ChildKey(49 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
    public_key_bip49 = bip49_account_key_obj.PublicKey()
    private_key_bip49 = bip49_account_key_obj.PrivateKey()
    
    # Dirección SegWit (P2SH-P2WPKH)
    ripemd160_seg = hashlib.new('ripemd160')
    ripemd160_seg.update(hashlib.sha256(public_key_bip49).digest())
    hashed_public_key_bip49 = ripemd160_seg.digest()
    script_pub_key_bip49 = b'\x00\x14' + hashed_public_key_bip49
    hashed_script_pub_key_bip49 = hashlib.new('ripemd160', hashlib.sha256(script_pub_key_bip49).digest()).digest()
    segwit_address = base58.b58encode_check(b'\x05' + hashed_script_pub_key_bip49).decode()

    # Clave privada y pública para BIP84 (Native SegWit)
    # BIP-84: Native SegWit (Bech32)
    bip84_key = bip32utils.BIP32Key.fromEntropy(seed).ChildKey(84 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
    public_key_84 = bip84_key.PublicKey()
    private_key_bip84 = bip84_key.PrivateKey()
    
    wallet_segwit = BIP84HDWallet(cryptocurrency=BitcoinMainnet)
    wallet_segwit.from_private_key(private_key=private_key_bip84.hex())
    address_segwit_native = wallet_segwit.address()
    
    direccionEthereum = DireccionEthereum(private_key_bip44.hex())
    direccionTron = DireccionTron(private_key_bip44.hex())

    return {
        'seed_phrase': seed_phrase,
        'legacy': {
            'private_key': private_key_bip44.hex(),
            'address': legacy_address
        },
        'segwit': {
            'private_key': private_key_bip49.hex(),
            'address': segwit_address
        },
        'native_segwit': {
            'private_key': private_key_bip84.hex(),
            'address': address_segwit_native
        },
        'ethereum': {
            'private_key': private_key_bip44.hex(),
            'address': direccionEthereum
        },
        'tron': {
            'private_key': private_key_bip44.hex(),
            'address': direccionTron
        },
        'shamir':Shamir
    }
    