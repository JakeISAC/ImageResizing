import os
from sys import platform


class Initialize:
    def __init__(self, dir_name: str = "resized_images"):
        self.__known_os = ["linux", "linux2", "darwin", "win32"]
        self.__dir_name = dir_name

    def __make_dir(self):
        current_dir = os.getcwd()
        full_path = os.path.join(current_dir, self.__dir_name)
        os.makedirs(full_path, exist_ok=True)

    def setup(self):
        if platform in self.__known_os:
            self.__make_dir()
        else:
            return Exception("Unknown OS")
