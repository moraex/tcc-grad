"""
modulo que define as funções que podem ser usadas
por diferentes arquivos.
"""
import os


class ReadFile:

    def read(self, file_path):
        with open(file_path, "r") as f:
            return f.readlines()


class WriteFile:

    def write(self, file_path, data):
        with open(file_path, "w") as f:
            f.writelines(''.join(data))


class OSPath:
    path = None
    file_name = None
    file_extension = None
    full = None

    def __init__(self, full_path) -> None:
        self.full = full_path
        self.path, file = os.path.split(full_path)
        self.file_name = file.split(".")[0]
        self.file_extension = ".".join(file.split(".")[1:])
