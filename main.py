import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
import scanner

console = Console()

MENU_OPTIONS = {
    "1": "Multi-Threaded Port Scanner",
    "2": "Exit Toolkit",
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_homepage():
    clear_screen()

    title = Text("Nexus Security Toolkit", style="bold green blink")
    subtitle = Text("\n")
    for key, label in MENU_OPTIONS.items():
        subtitle.append("[", style="cyan")
        subtitle.append(key, style="white")
        subtitle.append(f"] {label}\n", style="cyan")

    console.print(Panel(
        Text.assemble(title, subtitle),
        title="[ SYSTEM READY ]",
        border_style="green",
        padding=(1, 5)
    ))

def main_menu():
    actions = {
        "1": lambda: (clear_screen(), console.print(Panel("MODULE LOADED: MULTI-THREADED PORT SCANNER", style="bold cyan")), scanner.main()),
        "2": lambda: (clear_screen(), console.print("Exiting Nexus Security Toolkit. Goodbye!", style="bold red"), sys.exit(0)),
    }

    try:
        while True:
            display_homepage()
            choice = Prompt.ask("\n> Option")
            action = actions.get(choice)
            if action:
                action()
    except KeyboardInterrupt:
        clear_screen()
        console.print("\nExiting Nexus Security Toolkit. Goodbye!", style="bold red")
        sys.exit(0)

if __name__ == "__main__":
    main_menu()