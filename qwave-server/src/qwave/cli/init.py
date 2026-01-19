import os
import sys
import yaml
from time import sleep
from pathlib import Path
from elevate import elevate
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

def logo():
    clear()
    print_logo(center = True)
    print(screen_center(f"{col1}(by {col2}@qwik{col1}, version {col2}{version("qwave")}{col1})!!"))
    print()

def get_offset():
    return ((get_term_size()[0] // 2) - 26)

def prompt_box(title: str, lines: list) -> None:
    logo()
    print(screen_center(f"{col1}╔════════════════════════════════════════════════╗"))
    print(screen_center(f"{col1}║ {text_center(title, 46)} ║"))
    print(screen_center(f"{col1}╠════════════════════════════════════════════════╣"))
    for i in lines:
        ln = display_width(i)
        print(screen_center(f"{col1}║ " + i + " "*(46 - ln) + " ║"))
    print(screen_center(f"{col1}╚════════════════════════════════════════════════╝"))

def title_box(title: str) -> None:
    logo()
    print(screen_center(f"{col1}╔════════════════════════════════════════════════╗"))
    print(screen_center(f"{col1}║ {text_center(title, 46)} ║"))
    print(screen_center(f"{col1}╚════════════════════════════════════════════════╝"))

def install_type() -> Path:
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

    if install_type == 1:
        data_dir = Path("/srv/qwave")
        title_box(f"{col2}Installer will restart as root!{col1}")
        sleep(0.75 if os.geteuid() != 0 else 0)
        elevate(graphical = False)
        
    elif install_type == 2:
        data_dir = Path.home() / "qwave"
        
    elif install_type == 3:
        data_dir = Path(prompt("Config path?", "/srv/qwave", get_offset()))
        title_box(f"{col2}Installer will restart as root!{col1}")
        sleep(0.75 if os.geteuid() != 0 else 0)
        elevate(graphical = False)
        
    if not data_dir.parent.exists():
        try:
            data_dir.parent.mkdir(parents = True, exist_ok = True)
        except PermissionError:
            print(f"\n{col2}Permission denied! Please run the installer as root ({col1}sudo{col2})")
            sys.exit(1)
    
    if os.geteuid() != 0 and install_type != 2:
        print(screen_center(f"\n{col2}Permission denied! Please run the installer as root ({col1}sudo{col2})"))
        sys.exit(1)
        
    return data_dir

def configure_server(data_dir):
    config = {}
    logo()
    title_box("Pick a cool or unique name for your server!!")
    config["server_name"] = prompt(default = "qWave", offset = get_offset())
    title_box(f"Server IP? (pick {col2}0.0.0.0{col1} if unsure!)")
    config["host"] = prompt(default = "0.0.0.0", offset = get_offset())
    title_box("Pick a port to connect to qWave's web client.")
    config["port"] = prompt_int(default = 4269, min_val = 1024, max_val = 49151, offset = get_offset())

    prompt_box("Bitrate for files to be transcoded to:", lines = [
        "I recommend one of the following:",
        f"{col2}64kbps{col1}: Minimum filesize but sounds poor",
        f"{col2}128k{col1}: Okay for low-end speakers",
        f"{col2}196k{col1}: Decent standard file size (default)",
        f"{col2}256k{col1}: High definition audio!",
        f">> {col2}qWave does not support lossless audio :({col1}"])
    config["opus_bitrate"] = prompt_int(f"You shouldn't ever change this!\n{" " * get_offset()}", 196, 32, 256, get_offset())

    title_box(f"Max file upload size? ({col2}MB{col1})")
    config["max_upload_size_mb"] = prompt_int(default = 256, min_val = 8, max_val = 8192, offset = get_offset())
    prompt_box(f"Enable metadata lookup via {col2}MusicBrainz{col1}?", ["(Free, no API key)", f"{col2}!{col1} This will send {col2}all file names and metadata{col1}", "to MusicBrainz's servers on file upload."])
    config["musicbrainz_enabled"] = prompt_yn(None, True, get_offset())
    prompt_box(f"Enable Content ID via {col2}acoustid.org{col1}?", [f"{col2}!{col1} Requires a free API key", f"{col2}!{col1} This will send {col2}files without metadata/info{col1}", "to their servers on upload."])
    config["acoustid_enabled"] = prompt_yn(None, False, get_offset())
    
    if config["acoustid_enabled"]:
        title_box("Register: https://acoustid.org/api-key")
        config["acoustid_api_key"] = prompt("", offset = get_offset())
    else:
        config["acoustid_api_key"] = None
        
    prompt_box("Review your final settings:", [
        f"Name: {col2}{config["server_name"]}{col1}",
        f"IP: {col2}{config["host"]}{col1}",
        f"Port: {col2}{config["port"]}{col1}",
        f"Location: {col2}{data_dir}{col1}",
        f"Bitrate: {col2}{config["opus_bitrate"]}{col1}",
        f"Max upload: {col2}{config["max_upload_size_mb"]}{col1}",
        f"Musicbrainz: {col2}{config["musicbrainz_enabled"]}{col1}",
        f"AcoustID: {col2}{config["acoustid_enabled"]}{col1}",
    ])
    print(screen_center("(Wait 2s...)"))
    sleep(2)
    cont = prompt_yn("Does this look right to you?", True, get_offset())
    if cont:
        return config
    else:
        sys.exit(0)


def create_config(data_dir, config):
    logo()
    title_box("writing config...")
    data_dir.mkdir(parents = True, exist_ok = True)
    config_data = {
        'server_name':   config['server_name'],
        'host':          config['host'],
        'port':          config['port'],
        'database_path': str(data_dir / "qwave.db"),
        'music_dir':     str(data_dir / "music"),
        'temp_dir':      str(data_dir / "temp"),
        'opus_bitrate':  config['opus_bitrate'],
        'max_upload_size_mb': config['max_upload_size_mb'],
        'acoustid_enabled':   config['acoustid_enabled'],
        'acoustid_api_key':   config['acoustid_api_key'],
        'musicbrainz_enabled': config['musicbrainz_enabled'],
        'theme_primary_color': str("#14F5AA"),
        'theme_secondary_color': str("#FF499E"),
        'logo_url': None,
        'background_url': None,
    }
    
    with open(data_dir / "qwave.ini", 'w') as f:
        f.write("# qWave server config\n\n")
        yaml.dump(config_data, f, default_flow_style = False, sort_keys = False)
        
    title_box(f"{col2}✓{col1}config written!")


def dbinit():
    pass


def main():
    while get_term_size()[0] <= 64:
        clear()
        input(f"{col1}Your terminal is too small!\nIt must be at least {col2}64{col1}x{col2}12{col1}.\nHit {col2}Enter{col1} to retry...")
    logo()
    
    if not sys.platform.startswith("linux"):
        print(f"{col2}qWave is ONLY supported on Linux!!\nI appreciate the enthusiasm, but Windows support is just not something I can do right now.")
        sys.exit(1)
    
    data_dir = install_type()
    
    if data_dir.exists():
        print(f"{col2}{data_dir}{col1} already exists!!\nPlease clear it manually if you are sure you want to overwrite it.")
        sys.exit(0)
    
    config = configure_server(data_dir)
    create_config(data_dir, config)
    database_url = f"sqlite:///{data_dir / 'qwave.db'}"
    
    dbinit(database_url)
    
    
def entry():
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print(f"{col1}goodbye!{col2}")
        sys.exit(0)
        
         