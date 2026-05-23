# Nexus Security Toolkit

A multi-threaded port scanner with banner grabbing capabilities. Quickly scan networks and identify open ports with service information.

## Features

- 🚀 **Multi-threaded scanning** - Fast port scanning using concurrent threads
- 🎯 **Banner grabbing** - Automatically detects service information on open ports
- 🎨 **Rich UI** - Beautiful terminal interface with colored output
- 🔍 **Flexible port ranges** - Scan single ports or ranges
- ⚡ **Configurable timeout** - Adjust scan speed and accuracy

## Requirements

- Python 3.7+
- `socket` (built-in)
- `paramiko` (for SSH support)
- `rich` (for terminal UI)
- `ipaddress` (built-in)
- `concurrent.futures` (built-in)
- `threading` (built-in)

## Installation

### Prerequisites

Ensure you have Python 3.7 or higher installed. [Download Python](https://www.python.org/downloads/)

### Linux/macOS

```bash
# Clone the repository
git clone https://github.com/x0uls/nexus-security-toolkit.git
cd nexus-security-toolkit

# Install dependencies
pip install -r requirements.txt

# Run the toolkit
python main.py
```

### Windows

#### Using PowerShell (irm)
```powershell
irm https://raw.githubusercontent.com/x0uls/nexus-security-toolkit/main/install.ps1 | iex
```

#### Using curl (PowerShell 7+)
```powershell
curl -sSL https://raw.githubusercontent.com/x0uls/nexus-security-toolkit/main/install.ps1 | powershell -NoProfile -
```

#### Manual Installation
```powershell
# Clone the repository
git clone https://github.com/x0uls/nexus-security-toolkit.git
cd nexus-security-toolkit

# Install dependencies
pip install -r requirements.txt

# Run the toolkit
python main.py
```

### macOS (Homebrew)

```bash
brew tap x0uls/nexus-security-toolkit
brew install nexus-security-toolkit
```

## Quick Start

1. **Start the toolkit:**
   ```bash
   python main.py
   ```

2. **Select an option from the menu:**
   - Option `1` - Multi-Threaded Port Scanner
   - Option `2` - Exit Toolkit

3. **Enter target information when prompted:**
   - Target IP address
   - Port range (e.g., `80-443` or `22`)
   - Number of threads (default: 100)
   - Timeout per port (default: 1 second)

## Usage Examples

### Scan common web ports
```
Target IP: 192.168.1.100
Port range: 80-443
Threads: 50
Timeout: 1
```

### Scan all SSH and common services
```
Target IP: 10.0.0.50
Port range: 22,80,443,3306,5432
Threads: 100
Timeout: 2
```

## Configuration

### Adjustable Parameters

- **Threads**: Increase for faster scans (higher CPU usage)
- **Timeout**: Lower for faster scans (may miss slow services), higher for accuracy
- **Port ranges**: Specify individual ports or ranges (e.g., `1-1024` or `80,443,8080`)

## Dependencies

Install all required packages:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install paramiko
pip install rich
```

## Troubleshooting

### "Module not found" error
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
```

### Permission denied on Linux/macOS
```bash
# Make scripts executable
chmod +x main.py
```

### Slow scanning
- Increase the number of threads
- Decrease the timeout value
- Check your network connectivity

### High CPU usage
- Reduce the number of threads
- Increase the timeout value

## Legal Notice

This toolkit is intended for authorized security testing and network administration only. Unauthorized port scanning may be illegal in your jurisdiction. Always obtain proper authorization before scanning networks you do not own or have explicit permission to test.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

**Version:** 1.0.0  
**Last Updated:** May 2026
