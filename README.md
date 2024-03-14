# Quick Start guide 
### Install Prerequisite

- Python version: 3.8.+ 
 
### Steps

- Install dependencies: `$pip3 install -r requirements.txt`
- Update the configuration in `config.py` file, (by default values which  are mentioned in requirement would be considered)
- Run the simulation: `$make simulate`

## Project Structure

Application parts are:
```
terminal-simulator
├── main.py # simulation logic
├── .env # Environment variables
├── .gitignore # Specifies files to ignore in version control.
├── Makefile # application level commands
├── README.md  # Documentation and instructions for the project.
├── requirements.txt # Python dependencies for the application.
```