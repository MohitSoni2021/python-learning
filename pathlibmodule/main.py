import os

Parent = "/run/media/mohitsoni/New Volume1/1_LEARN/python"
# Directory = "TestDir"
#
# Path = os.path.join(Parent, Directory);
#
# os.mkdir(Path);
#
#
#
# def getdir(label):
#     print(f"The {label} path -> {os.getcwd()}\n\n")
#
#
# getdir("Before")
# os.chdir("../")
# getdir("After")

#listing file in a directory;

def listfiles(path):
    print(os.listdir(path));

def listfiles_with_extension(path, extension=".txt"):
    listfiles(path)
    for file in os.listdir(path):
        if file.endswith(extension):
            print(file);

def listCompListfile(path):
    print([file for file in os.listdir(path)]);

def listcompwithextension(path, extension=".txt"):
    print([file for file in os.listdir(path) if file.endswith(extension)]);

# listfiles("/run/media/mohitsoni/New Volume1/1_LEARN/python");

# listfiles_with_extension("/run/media/mohitsoni/New Volume1/1_LEARN/python", ".py")

# os.rmdir(os.path.join(Parent, "TestDir"));
# listfiles(Parent);

# listfiles(os.path.join(Parent, "modules and imports concepts"));

# listcompwithextension(os.path.join(Parent, "modules and imports concepts"), ".py");

print(os.name)