import os

# main directory
APP_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))

CONFIG_PATH = os.path.expanduser(os.getenv("GAS_MONITOR_CONFIG", "~/.gasMonitor"))

def config(*fileName):
    return os.path.join(CONFIG_PATH, *fileName)