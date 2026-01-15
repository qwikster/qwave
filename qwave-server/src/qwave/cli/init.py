import sys
import yaml
from pathlib import Path
from typing import Optional
from getpass import getpass
from passlib.hash import bcrypt

from qwave.utils.cli import print_logo, clear, goto, get_termcol, display_width, dw_text_center, screen_center, get_term_size, prompt, prompt_yn, prompt_int
from qwave.database import init_db, create_tables, get_session
from qwave.models import User


            
def entry():
    print_logo()