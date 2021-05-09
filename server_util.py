from os import path, mkdir, listdir, unlink
from shutil import rmtree

app_root = path.dirname(path.abspath(__file__))

DATA = "input"

SHELL = "shell_scripts"

# Temp
SKULL_STRIP = f'{DATA}/temp/skull_strip'
DENOISE = f'{DATA}/temp/denoise'
BAIS_COR = f'{DATA}/temp/bias_cor'
TEMP_OUTPUT = f'{DATA}/temp/output'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def create_folders():
    input_folder = path.join(app_root, 'input')
    if not path.exists(input_folder):
        mkdir(input_folder)
        mkdir(path.join(input_folder, "nii"))
        mkdir(path.join(input_folder, "img"))
        mkdir(SKULL_STRIP)
        mkdir(DENOISE)
        mkdir(BAIS_COR)
        mkdir(TEMP_OUTPUT)

    output_folder = path.join(app_root, 'output')
    if not path.exists(output_folder):
        mkdir(output_folder)
        mkdir(path.join(output_folder, "nii"))
        mkdir(path.join(output_folder, "img"))


def delete_contents(folder_path):
    folder = folder_path
    for filename in listdir(folder):
        file_path = path.join(folder, filename)
        try:
            if path.isfile(file_path) or path.islink(file_path):
                unlink(file_path)
            elif path.isdir(file_path):
                rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s : %s' % (file_path, e))

    rmtree(folder)


def supported_file(filename):
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext == "nii":
        return True
    else:
        return False