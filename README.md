# Chainwave - Bitcoin Vanity Address Generator

#### Developed by: Stiven Alvarez
#### GitHub: [stivenalvz](https://github.com/stivenalvz)
#### City: Medellín, Colombia
#### Recording Date: May 11, 2025

#### Video Demo: [Watch the Demo](https://www.youtube.com/watch?v=H2vSpDp7vos)

## Description

**Chainwave** is a desktop application that allows users to generate Bitcoin vanity addresses and distribute recovery phrases using the Shamir mnemonic scheme. The application is designed to be intuitive and secure, facilitating the management of cryptocurrency keys and addresses.

### Main Features

- **Vanity Address Generation**: Creates personalized Bitcoin addresses that start with a specific prefix.
- **Phrase Distribution**: Uses the Shamir scheme to split recovery phrases into parts, allowing for secure recovery.
- **User-Friendly Interface**: Designed to facilitate navigation and use of the application.

## Technologies Used

- **Language**: Python
- **Framework**: Eel for the graphical interface, using a small HTML file
- **QR Code Generation**: To visualize Bitcoin addresses
- **File Management**: To save and retrieve keys and phrases

## Project Structure

- `project.py`: Main entry point of the application.
- `web/`: Contains static files and HTML templates.
- `address.txt`: File to store generated addresses.
- `wordlist.txt`: List of words for the Shamir scheme.
- `requirements.txt`: List of dependencies needed to run the project.

## Installation and Usage

### Option 1: Manual Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/stivenalvz/Shamir-Key-Distribution.git
   cd Shamir-Key-Distribution
   ```

2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python project.py
   ```

4. A graphical interface will open, allowing you to easily interact with the application.