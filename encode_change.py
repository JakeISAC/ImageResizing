from PIL import Image
import os


class EncodeChange:
    def __init__(self, image_path: str, new_encoding: str, output_dir: str = ""):
        self.__image_path = image_path
        self.__new_encoding = new_encoding
        self.__output_dir = output_dir
        self.__save_path = None
        if output_dir != "":
            self.__save_folder = output_dir
        else:
            self.__save_folder = os.path.dirname(self.__image_path)

    def change_image_encoding(self):
        filename, extension = os.path.splitext(os.path.basename(self.__image_path))
        if extension == self.__new_encoding:
            return

        new_file_name = filename + "." + self.__new_encoding
        self.__save_path = os.path.join(self.__save_folder, new_file_name)

        photo = Image.open(self.__image_path)
        photo.save(self.__save_path)

    def get_path(self) -> str:
        if self.__save_path is not None:
            return str(self.__image_path)
        else:
            raise NotADirectoryError


def change_directory_images_encoding(dir_path: str, new_encoding: str, output_dir: str = ""):
    if output_dir == "":
        current_dir = os.getcwd()
        full_path = os.path.join(current_dir, "changed_images")
        output_dir = full_path
        os.makedirs(full_path, exist_ok=True)

    for filename in os.listdir(dir_path):
        full_image_path = os.path.join(dir_path, filename)
        change_encode = EncodeChange(full_image_path, new_encoding, output_dir)
        change_encode.change_image_encoding()
