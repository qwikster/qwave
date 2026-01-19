from qwave.config import load_config, get_config

def entry():
    print("test success")
    load_config()
    print(get_config())

if __name__ == "__main__":
    entry()