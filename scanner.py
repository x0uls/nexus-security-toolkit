import socket
import sys
import random
import threading
from concurrent.futures import ThreadPoolExecutor
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import ipaddress
import paramiko

import main as main_menu

console = Console()

def scan_single_port(ip, port, open_ports_list, scan_timeout, lock):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(scan_timeout)
        result = s.connect_ex((ip, port))
        if result == 0:
            console.print(f"  [[bold bright_green]+[/bold bright_green]] Port [bold cyan]{port}[/bold cyan] is open.")
            with lock:
                open_ports_list.append(port)
        s.close()
    except Exception:
        pass

def grab_service_banner(ip, port, banner_timeout):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(banner_timeout)
        s.connect((ip, port))

        if port in [80, 443, 8080, 8443, 5000, 9080]:
            s.sendall(b"HEAD / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        else:
            s.sendall(b"\r\n")

        s.settimeout(1.0)
        raw_response = s.recv(1024)
        s.close()

        banner = raw_response.decode('utf-8', errors='ignore').strip()
        banner = banner.replace("\r", "").replace("\n", " | ")
        return banner if banner else ""

    except socket.timeout:
        return ""
    except Exception:
        return "[dim red]Failed to establish stream handshake[/dim red]"

def run_active_probing_checks(ip, open_ports):
    probes_log = []
    web_ports = [p for p in open_ports if p in [80, 443, 5000, 9080, 28385, 28390]]
    for port in web_ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.5)
            s.connect((ip, port))
            s.sendall(b"GET /../../../../etc/passwd HTTP/1.1\r\nHost: localhost\r\n\r\n")
            res = s.recv(512).decode('utf-8', errors='ignore')
            s.close()
            if "root:" in res or ("HTTP/1.1 200 OK" in res and "passwd" in res):
                probes_log.append(f"[bold red]• [CRITICAL] Active Path Traversal Confirmed on Port {port}![/bold red]")
            else:
                probes_log.append(f"[dim green]✓ Port {port} responded safely to malformed pathing payload.[/dim green]")
        except Exception:
            pass
    return probes_log

def run_authenticated_os_audit(ip):
    console.print("\n[bold yellow]OPTIONAL:[/bold yellow] [bold white]Run Authenticated Internal System Audit?[/bold white] (y/N)")
    if input(" > ").strip().lower() != 'y':
        return "[dim white]Authenticated OS verification skipped by user.[/dim white]"

    console.print("[bold green]SSH Username:[/bold green]")
    username = input(" > ").strip()
    console.print("[bold green]SSH Password/Passphrase:[/bold green]")
    password = input(" > ").strip()

    console.print(f"\n[bold yellow]STATUS:[/bold yellow] Establishing credentialed SSH handshake to {ip}...")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password, timeout=4.0)
        _, stdout, _ = ssh.exec_command("uname -a; echo '---'; dpkg -l | grep -E 'openssh|nginx|apache' | head -n 3")
        audit_results = stdout.read().decode('utf-8').strip()
        ssh.close()
        if audit_results:
            return f"[bold bright_green]AUTHENTICATED OS METADATA RETRIEVED:[/bold bright_green]\n{audit_results}"
        return "[bold yellow]Authenticated connection established, but target shell returned blank environment logs.[/bold yellow]"
    except Exception as e:
        return f"[bold red]AUTHENTICATION SCAN FAILURE:[/bold red] Secure connection rejected -> {str(e)}"

def prompt_float(label, hint, default):
    console.print(f"\n[bold green]{label}[/bold green]")
    console.print(f"[dim white] {hint}[/dim white]")
    try:
        val = input(" > ").strip()
        return float(val) if val else default
    except ValueError:
        console.print(f"[bold yellow]Invalid input. Defaulting to {default}.[/bold yellow]")
        time.sleep(1.0)
        return default

def main():
    while True:
        console.print("[bold green]Target IP Address[/bold green]")
        console.print("[dim white] Tip: Press Enter on a blank line to return to main menu[/dim white]")
        try:
            input_ip = input(" > ").strip()
        except (KeyboardInterrupt, EOFError):
            main_menu.clear_screen()
            return

        if not input_ip:
            main_menu.clear_screen()
            return

        try:
            ipaddress.ip_address(input_ip)
            break
        except ValueError:
            console.print(f"\n[bold red]ERROR:[/bold red] '[bold yellow]{input_ip}[/bold yellow]' is not a valid IPv4 or IPv6 address.\n")

    scan_timeout = prompt_float("Port Scan Timeout (Seconds)", "Default: 0.05 for LAN, increase for weak Wi-Fi", 0.05)
    banner_timeout = prompt_float("Service Banner Timeout (Seconds)", "Default: 2.0 — increase for high-latency targets", 2.0)

    console.print(f"\n[bold yellow]STATUS:[/bold yellow] Starting scanning operation on [bold cyan]{input_ip}[/bold cyan]...")

    ports = list(range(1, 65537))
    random.shuffle(ports)

    open_ports = []
    lock = threading.Lock()
    start_time = time.time()

    executor = ThreadPoolExecutor(max_workers=500)
    try:
        futures = executor.map(lambda port: scan_single_port(input_ip, port, open_ports, scan_timeout, lock), ports)
        for _ in futures:
            pass
    except KeyboardInterrupt:
        executor.shutdown(wait=False, cancel_futures=True)
        sys.exit(0)
    finally:
        executor.shutdown(wait=False)

    end_time = time.time()
    total_duration = end_time - start_time

    open_ports.sort()

    table = Table(box=None, expand=True, show_header=True, border_style="dim white")
    table.add_column("Port", style="bold cyan", width=14, justify="left")
    table.add_column("Service Banner Identification Response String", style="white", justify="left")

    if open_ports:
        console.print("\n[bold yellow]STATUS:[/bold yellow] Extracting service banners sequentially...\n")
        for port in open_ports:
            console.print(f" [dim white]• Interrogating port {port}...[/dim white]")
            banner = grab_service_banner(input_ip, port, banner_timeout)
            display_banner = banner.strip() if banner and banner.strip() else "[dim white]Connected (No string returned)[/dim white]"
            table.add_row(f"Port {port}", display_banner)
    else:
        table.add_row("None", "No open ports identified across the target spectrum.")

    console.print("\n[bold yellow]STATUS:[/bold yellow] Deploying active behavioral security probes...")
    active_probe_findings = run_active_probing_checks(input_ip, open_ports)
    active_render_output = "\n".join(active_probe_findings) if active_probe_findings else "[dim green]✓ All exposed interfaces parsed safely against testing suites.[/dim green]"

    authenticated_results_string = run_authenticated_os_audit(input_ip)

    console.print("\n[dim green]────────────────────────────────────────────────────────────[/dim green]")

    summary_text = (
        f"Target IP:          [bold white]{input_ip}[/bold white]\n"
        f"Ports Scanned:      [bold white]65,536[/bold white]\n"
        f"Total Active Open:  [bold bright_green]{len(open_ports)}[/bold bright_green]\n"
        f"Time Elapsed:       [bold yellow]{total_duration:.2f} seconds[/bold yellow]\n\n"
        f"[bold green]SERVICE MAP DETECTED[/bold green]\n"
        f"────────────────────────────────────────────────────────────────────────────────"
    )

    master_layout = Table(box=None, expand=True, show_header=False)
    master_layout.add_column("Container")
    master_layout.add_row(summary_text)
    master_layout.add_row(table)
    master_layout.add_row("\n[bold red]ACTIVE BEHAVIORAL NETWORK PROBE FEEDBACK[/bold red]\n────────────────────────────────────────────────────────────────────────────────")
    master_layout.add_row(active_render_output)
    master_layout.add_row("\n[bold blue]INTERNAL TRUSTED CREDENTIALED SYSTEM AUDIT RESULTS[/bold blue]\n────────────────────────────────────────────────────────────────────────────────")
    master_layout.add_row(authenticated_results_string)

    console.print(Panel(master_layout, title="[bold bright_green]DUAL-ENGINE AUDIT COMPLETE[/bold bright_green]", border_style="bright_green", padding=(1, 2)))

    console.print("\n[dim white]Press Enter to return to the main menu...[/dim white]")
    try:
        input()
    except (KeyboardInterrupt, EOFError):
        pass
    main_menu.clear_screen()

if __name__ == "__main__":
    main()