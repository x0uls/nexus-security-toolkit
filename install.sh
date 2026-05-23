#!/bin/bash

# Terminate script immediately if any individual command fails
set -e

# Define terminal UI styling colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RESET='\033[0m'

echo -e "${CYAN}[*] Initializing Nexus Security Toolkit Installation...${RESET}"

# 1. Establish the workspace tracking directory path
TARGET_DIR="$HOME/nexus-security-toolkit"
echo -e "${CYAN}[*] Creating deployment environment directory at: ${TARGET_DIR}${RESET}"
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

# 2. Retrieve project source files directly from the master GitHub repository
echo -e "${CYAN}[*] Streaming core application frame files...${RESET}"
curl -sSL -O https://raw.githubusercontent.com/x0uls/nexus-security-toolkit/main/scanner.py

# Create a minimal main.py to handle menu transitions seamlessly if it doesn't exist
if [ ! -f "main.py" ]; then
    echo -e "${CYAN}[*] Generating menu pipeline controller...${RESET}"
    cat << 'EOF' > main.py
import os
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    while True:
        clear_screen()
        print("=" * 50)
        print("         NEXUS SECURITY TOOLKIT CONTROLLER        ")
        print("=" * 50)
        print(" [1] Run Multi-Threaded Port Scanner & Auditor")
        print(" [2] Exit Toolkit")
        print("=" * 50)
        
        choice = input(" > ").strip()
        if choice == '1':
            clear_screen()
            try:
                import scanner
                scanner.main()
            except ImportError:
                print("\n[!] Error: Core scanner components missing in runtime path.")
                input("\nPress Enter to return to menu...")
        elif choice == '2':
            clear_screen()
            print("[*] Exiting Nexus Security Toolkit. Stay secure.")
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
EOF
fi

# 3. Handle Python dependency environment deployment
echo -e "${CYAN}[*] Verifying package management tools and dependencies...${RESET}"
if command -v pip3 &> /dev/null; then
    pip3 install --user rich paramiko > /dev/null 2>&1 || pip3 install rich paramiko > /dev/null 2>&1
elif command -v pip &> /dev/null; then
    pip install --user rich paramiko > /dev/null 2>&1 || pip install rich paramiko > /dev/null 2>&1
else
    echo -e "${YELLOW}[!] Warning: Python pip manager not detected. Please install 'rich' and 'paramiko' packages manually.${RESET}"
fi

# 4. Finalize script execution permissions
chmod +x main.py

echo -e "\n${GREEN}[+] Nexus Security Toolkit successfully deployed!${RESET}"
echo -e "To launch your control dashboard, execute: ${GREEN}python3 $TARGET_DIR/main.py${RESET}\n"