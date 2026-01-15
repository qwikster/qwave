import sys
import yaml
from pathlib import Path
from typing import Optional
from getpass import getpass
from passlib.hash import bcrypt
from importlib.metadata import version

from qwave.utils.cli import print_logo, clear, goto, get_termcol, display_width, text_center, screen_center, get_term_size, prompt, prompt_yn, prompt_int
from qwave.database import init_db, create_tables, get_session
from qwave.models import User

col1 = get_termcol((20, 245, 170))
col2 = get_termcol((255, 73, 158))
offset = 0

def get_offset():
    return ((get_term_size()[0] // 2) - 26)

def main():
    while get_term_size()[0] <= 64:
        clear()
        input(f"{col1}Your terminal is too small!\nIt must be at least {col2}64{col1}x{col2}12{col1}.\nHit {col2}Enter{col1} to retry...")
    clear()
    
    print_logo(center = True)
    print(screen_center(f"{col1}(by {col2}@qwik{col1}, version {col2}{version("qwave")}{col1})!!"))
    print()
    print(screen_center(f"{col1}╔════════════════════════════════════════════════╗"))
    print(screen_center(f"{col1}║  Thanks for picking {col2}qWave{col1}!! you are very cool  ║"))
    print(screen_center(f"{col1}╠════════════════════════════════════════════════╣"))
    print(screen_center(f"{col1}║ {col2}Step 1{col1}: How (where) should qWave be installed? ║"))
    print(screen_center(f"{col1}╟────────────────────────────────────────────────╢"))
    print(screen_center(f"{col1}║ {col2}[1] {col1}Server install (/srv/qwave/*) {col2}(req. root!) {col1}║"))
    print(screen_center(f"{col1}║ {col2}[2] {col1}User install (~/qwave/*)                   ║"))
    print(screen_center(f"{col1}║ {col2}[3] {col1}Custom directory! {col2}(may require root!)      {col1}║"))
    print(screen_center(f"{col1}╚════════════════════════════════════════════════╝"))
    install_type = prompt_int(default = 1, min_val = 1, max_val = 3, offset = get_offset())
    
def entry():
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print(f"{col1}goodbye!{col2}")
        sys.exit(0)