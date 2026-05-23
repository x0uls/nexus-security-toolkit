# Define terminal UI styling colors using native PowerShell console routing
$Green  = "Green"
$Cyan   = "Cyan"
$Yellow = "Yellow"

Write-Host "[*] Initializing Nexus Security Toolkit Installation..." -ForegroundColor $Cyan

# 1. Establish the workspace tracking directory path
$TargetDir = "$HOME\nexus-security-toolkit"
Write-Host "[*] Creating deployment environment directory at: $TargetDir" -ForegroundColor $Cyan
if (-not (Test-Path -Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir | Out-Null
}
Set-Location -Path $TargetDir

# 2. Retrieve project source files directly from the master GitHub repository
Write-Host "[*] Streaming core application frame files..." -ForegroundColor $Cyan
try {
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/x0uls/nexus-security-toolkit/main/scanner.py" -OutFile "scanner.py" -UseBasicParsing
} catch {
    Write-Host "[!] Error: Failed to download scanner.py from GitHub repository." -ForegroundColor Red
    Exit
}

# Create a minimal main.py to handle menu transitions seamlessly if it doesn't exist
if (-not (Test-Path -Path "main.py")) {
    Write-Host "[*] Generating menu pipeline controller..." -ForegroundColor $Cyan
    $MainPyContent = @"
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
"@
    Set-Content -Path "main.py" -Value $MainPyContent
}

# 3. Handle Python dependency environment deployment
Write-Host "[*] Verifying package management tools and dependencies..." -ForegroundColor $Cyan

# Test for standard python environment access to pip
$PipCheck = Get-Command pip -ErrorAction SilentlyContinue
$Pip3Check = Get-Command pip3 -ErrorAction SilentlyContinue

if ($Pip3Check) {
    Start-Process pip3 -ArgumentList "install --user rich paramiko" -NoNewWindow -Wait -RedirectStandardOutput $null -RedirectStandardError $null
} elseif ($PipCheck) {
    Start-Process pip -ArgumentList "install --user rich paramiko" -NoNewWindow -Wait -RedirectStandardOutput $null -RedirectStandardError $null
} else {
    Write-Host "[!] Warning: Python pip manager not detected. Please install 'rich' and 'paramiko' packages manually." -ForegroundColor $Yellow
}

# 4. Finalize script execution output
Write-Host ""
Write-Host "[+] Nexus Security Toolkit successfully deployed!" -ForegroundColor $Green
Write-Host "To launch your control dashboard, execute: python $TargetDir\main.py" -ForegroundColor $Green
Write-Host ""