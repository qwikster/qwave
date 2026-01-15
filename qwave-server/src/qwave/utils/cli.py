import re
import sys
from typing import Optional
from shutil import get_terminal_size
from qwave.cli.logo import print_logo

def clear() -> None:
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()
    
def goto(x: int, y: int) -> str:
    return f"\x1b{y};{x}H" # i still don't know why it's backwards

def get_termcol(rgb: tuple[int, int, int], bg: bool = False) -> str:
    return f"\x1b[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m" if bg else f"\x1b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"

def display_width(s: str) -> int:
    # regex by ai
    s = re.sub(r'\x1b\[[0-9;]*m', '', s)
    return len(s)
    
def dw_text_center(text: str, size: int) -> str:
    padding = size - display_width(text)
    bump = "" if padding % 2 == 0 else " "
    return " " * (padding // 2) + text + " " * (padding // 2) + bump

def screen_center(text: str) -> str:
    x, _ = get_term_size()
    if display_width(text) >= x-1:
        raise ValueError(f"terminal size is too small! (needed: {x} cols)")
    return dw_text_center(text, x - 1)

def get_term_size() -> tuple[int, int]:
    return get_terminal_size((80, 24))

def prompt(message: str, default: Optional[str]) -> str:
    if default:
        response = input(f"{message} [Default: {default}]\n>... ").strip()
        return response if response else default
    while True:
        response = input(f"{message}\n>... ").strip()
        if response:
            return response

def prompt_yn(message: str, default: bool = True) -> bool:
    df = "Y/n" if default else "y/N"
    response = input(f"{message} [{df}]\n>... ").strip().lower()
    if not response:
        return default
    return response in ("y", "yes")

def prompt_int(message: str, default: int, min_val: Optional[int], max_val: Optional[int]) -> int:
    while True:
        response = prompt(message, str(default))
        try:
            value = int(response)
            if min_val is not None and value < min_val:
                print()
                continue
            if max_val is not None and value > max_val:
                print()
                continue
            return value
        except ValueError:
            print()