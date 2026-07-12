import os.path
from pathlib import Path;

print(Path.cwd());

homedir = Path.home();
print(homedir);

Parentdir = "/run/media/mohitsoni/New Volume1/1_LEARN/python"
parentpath = Path(Parentdir);

print(parentpath);

# print(Path(os.path.join(Parentdir, "")))
print(os.listdir(parentpath));