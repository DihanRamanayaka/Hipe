# purr_ai_cli.py
import os
import time
import requests
from colorama import Fore, Style, init

init(autoreset=True)

API_URL = "https://text.pollinations.ai/"
BOT_NAME = "Hipe"
VERSION = "v0.9.0"

# === Tokyo-Night palette ===
C = {
    "border": Fore.LIGHTBLACK_EX,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "white": Fore.LIGHTWHITE_EX,
    "blue": Fore.LIGHTBLUE_EX,
    "dim": Fore.LIGHTBLACK_EX
}

# === Copilot-style banner ===
LOGO = f"""{C['magenta']} 
██╗  ██╗██╗██████╗ ███████╗     █████╗ ██╗
██║  ██║██║██╔══██╗██╔════╝    ██╔══██╗██║
███████║██║██████╔╝█████╗      ███████║██║
██╔══██║██║██╔═══╝ ██╔══╝      ██╔══██║██║
██║  ██║██║██║     ███████╗    ██║  ██║██║
╚═╝  ╚═╝╚═╝╚═╝     ╚══════╝    ╚═╝  ╚═╝╚═╝
                                          

{C['white']}{BOT_NAME} {C['dim']} - A helpful assistant in your terminal
{C['dim']}────────────────────────────────────────────
"""

def clear(): 
    os.system("cls" if os.name == "nt" else "clear")

def slow_print_in_box_line(text, width, left_border, right_border, delay=0.005):
    """
    Print a single line inside borders with a typing effect.
    `width` is the max content width (not including padding).
    left_border/right_border are strings already colored (like '│  ' and '  │').
    """
    # print left border and initial padding
    print(left_border, end="", flush=True)
    # type the text
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    # pad the rest of the line
    remaining = width - len(text)
    if remaining > 0:
        print(" " * remaining, end="", flush=True)
    # print right border and newline
    print(right_border)

def draw_bot_box_typing(title, text, char_delay=0.002, line_delay=0.035):
    """Draw a Co-style bordered box with typing animation for the content."""
    # split into lines and compute width
    lines = []
    for line in str(text).split("\n"):
        # wrap long lines at 80 chars to keep terminal friendly
        if len(line) <= 80:
            lines.append(line)
        else:
            # naive wrap
            for i in range(0, len(line), 80):
                lines.append(line[i:i+80])
    width = max(len(line) for line in lines) if lines else 0

    border = C["border"]
    blue = C["blue"]
    white = C["white"]

    top = border + "┌" + "─" * (width + 4) + "┐"
    header = f"{border}│ {blue}{title}{' ' * (width - len(title) + 3)}{border}│"
    spacer = border + "│" + " " * (width + 4) + "│"
    bottom = border + "└" + "─" * (width + 4) + "┘" + Style.RESET_ALL

    print(top)
    print(header)
    print(spacer)
    # each content line: print left border + two spaces, then type text, pad, then right border
    left_border = border + "│  " + white
    right_border = "  " + border + "│"
    for ln in lines:
        slow_print_in_box_line(ln, width, left_border, right_border, delay=char_delay)
        time.sleep(line_delay)
    print(bottom)

def get_reply(prompt):
    """Fetch a reply from Pollinations.ai (GET)."""
    try:
        r = requests.get(API_URL + prompt, timeout=15)
        if r.status_code == 200:
            return r.text.strip()
        return f"({BOT_NAME} Error) Status {r.status_code}"
    except Exception as e:
        return f"({BOT_NAME} Error) {e}"

def intro():
    clear()
    print(LOGO)
    print(f"{C['dim']}{VERSION}\n")
    print(C["white"] + "Welcome to Hipe — improved terminal assistant.\n")
    print(C["dim"] + "Press Ctrl+C or type 'exit' to quit.\n")

def main():
    intro()
    # keep a simple history list (strings). This script prints history sequentially,
    # so for long sessions consider paging or truncation.
    history = []

    while True:
        # bottom chat bar: bot icon then prompt
        try:
            user_input = input(C["cyan"] + "User ❯ " + Style.RESET_ALL).strip()
        except (KeyboardInterrupt, EOFError):
            print()  # newline
            user_input = "exit"

        if user_input.lower() in ("exit", "quit"):
            draw_bot_box_typing(BOT_NAME, "Goodbye — see you soon!", char_delay=0.003, line_delay=0.02)
            break

        # Show user message plainly (no box) to match your request
        print()
        print(C["white"] + "User ❯ " + C["dim"] + user_input + Style.RESET_ALL)
        history.append(("user", user_input))
        print()

        # show a small "thinking" indicator (dim)
        print(C["dim"] + "Thinking...", end="\r")
        reply = get_reply(user_input)
        # clear the thinking line
        print(" " * 60, end="\r")

        # print bot reply in a boxed style with typing
        draw_bot_box_typing(BOT_NAME, reply, char_delay=0.0025, line_delay=0.03)
        history.append(("bot", reply))
        print()

if __name__ == "__main__":
    main()
