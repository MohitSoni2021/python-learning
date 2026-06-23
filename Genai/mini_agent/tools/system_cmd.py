import os

def run_command(cmd : str):
    res = os.system(cmd)
    return res