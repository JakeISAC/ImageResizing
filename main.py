"""
Before running the code you will need to install the following:
- pip3 install opencv-python opencv-contrib-python
- pip3 install numpy
- pip3 install pillow
"""

from PIL import Image
import cv2
import numpy as np
import os
from sys import platform

acceptable_extensions = [".png", ".jpg", ".jpeg", ".webp", ".tiff"]


def make_dir(file_name):
    current_dir = os.getcwd()
    if not os.path.isdir(current_dir + file_name):
        os.mkdir(current_dir + file_name)


def setup():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        make_dir("/resized_images")
    elif platform == "win32":
        make_dir("\\resized_images")
    else:
        return Exception("Unknown OS")


def format_name(file_name: str) -> (str, str):
    file = ""
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        file = "/" + file_name + "/"
    elif platform == "win32":
        file = "\\" + file_name + "\\"

    return file


class ImageResizing:
    def __init__(self, image_path, save_folder=""):
        self.__image_loaded = False
        self.__image_path = image_path
        self.__image = {
            "image": np.array(0),
            "width": -1,
            "height": -1,
            "file_name": "",
            "file_extension": ""
        }
        self.__target_resolution = (1920, 1080)
        if save_folder != "":
            self.__save_folder = save_folder
        else:
            self.__save_folder = os.getcwd() + format_name("resized_images")

    @property
    def get_original_image(self):
        if self.__image_loaded:
            return self.__image
        else:
            return "Image was not loaded yet"

    def __load_image(self, acceptable_extension_input: [] = None) -> None:
        if acceptable_extension_input is None:
            global acceptable_extensions
            acceptable_extension_input = acceptable_extensions

        # load image and calculate the parameters
        im = cv2.imread(self.__image_path)

        if im is not None:
            width, height, _ = im.shape
            # update image
            self.__image["image"] = im
            self.__image["width"] = width
            self.__image["height"] = height
            # get file name and extension
            filename, extension = os.path.splitext(os.path.basename(self.__image_path))
            self.__image["file_name"] = filename
            self.__image["file_extension"] = extension
            # mark image as loaded
            self.__image_loaded = True

            # check to avoid any errors that might result in a severe crash
            # (happened to me a couple of times while coding this)
            if self.__image["file_extension"].lower() not in acceptable_extension_input:
                raise "File format can not be processed"

    """
        Recommended for images with dimensions larger than 1920x1080
    """

    def automatic_basic_resize(self) -> None:
        if not self.__image_loaded:
            self.__load_image()

        # resize the image
        new_image = cv2.resize(self.__image["image"], self.__target_resolution, interpolation=cv2.INTER_LINEAR)

        # save the image
        save_path = os.path.join(self.__save_folder,
                                 (self.__image["file_name"] + "_" + "basic" + self.__image["file_extension"]))
        cv2.imwrite(save_path, new_image)

    """
        Recommended for images which have dimensions smaller than 1920x1080
    """

    def automatic_super_resize(self) -> None:
        if not self.__image_loaded:
            self.__load_image()

        '''
            In order to upsample where the result is an image with dimensions of 1920x1080 first we need to resize the
            image using the basic upscaling technique to 960x540. The image will be later upsampled to the desired
            resolution using the FSRCNN model.
        '''
        input_size = (self.__target_resolution[0] // 2, self.__target_resolution[1] // 2)
        new_image = cv2.resize(self.__image["image"], input_size, interpolation=cv2.INTER_LINEAR)

        # load the model and set parameters
        model = cv2.dnn_superres.DnnSuperResImpl.create()
        model.readModel('models/FSRCNN_x2.pb')
        model.setModel("fsrcnn", 2)

        # upsample the image
        result = model.upsample(new_image)

        # save the image
        save_path = os.path.join(self.__save_folder,
                                 (self.__image["file_name"] + "_" + "super" + self.__image["file_extension"]))
        cv2.imwrite(save_path, result)

    def manual_resize(self, name: str = "image", encode: str = "png", new_width: int = 1920, new_height: int = 1080,
                      super_resolution: bool = False) -> None:
        if not self.__image_loaded:
            self.__load_image()

        if super_resolution:
            input_size = (new_width // 2, new_height // 2)
            new_image = cv2.resize(self.__image["image"], input_size, interpolation=cv2.INTER_LINEAR)

            # load the model and set parameters
            # EDSR is much better than FSCRNN but sometimes takes longer to compute
            model = cv2.dnn_superres.DnnSuperResImpl.create()
            model.readModel('models/EDSR_x2.pb')
            model.setModel("edsr", 2)

            # upsample the image
            result = model.upsample(new_image)

            # save the image
            save_path = os.path.join(self.__save_folder, (name + "." + encode))
            cv2.imwrite(save_path, result)
        else:
            # resize the image
            input_size = (new_width, new_height)
            new_image = cv2.resize(self.__image["image"], input_size, interpolation=cv2.INTER_LINEAR)

            # save the image
            save_path = os.path.join(self.__save_folder, (name + "." + encode))
            cv2.imwrite(save_path, new_image)

    """
        auto() is simply using specifications that I defined above the functions above. 
        
        Note:
            I defined specifications for this like that, because I run the code on multiple images 
            that the client gave us and there is not a lot visible difference between basic and super resizing
            on those images. But, because super_resize basically 'recreates' an image the image looks smoother and
            a bit more pleasant, but I have no idea that matters to us, 
    """

    def auto(self) -> None:
        if not self.__image_loaded:
            self.__load_image()

        if self.__image["width"] < 1920 or self.__image["height"] < 1080:
            self.automatic_super_resize()
        else:
            self.automatic_basic_resize()


def resize_images_in_dir(dir_path):
    for x in os.listdir(dir_path):
        image_resizing = ImageResizing(os.path.join(dir_path, x))
        image_resizing.auto()


# ---------------------------------------------------------------------
# additional functions to convert images to different encodes if necessary

class EncodeChange:
    def __init__(self, image_path: str, new_encoding: str, output_dir: str):
        self.__image_path = image_path
        self.__new_encoding = new_encoding
        self.__output_dir = output_dir

    def change_image_encoding(self):
        dir_file = self.__output_dir if self.__output_dir else os.path.dirname(self.__image_path)
        filename, _ = os.path.splitext(os.path.basename(self.__image_path))

        new_file_name = filename + "." + self.__new_encoding

        photo = Image.open(self.__image_path)
        photo.save(os.path.join(dir_file, new_file_name))


def change_directory_images_encoding(dir_path: str, new_encoding: str, output_dir: str = ""):
    for filename in os.listdir(dir_path):
        full_image_path = os.path.join(dir_path, filename)
        change_encode = EncodeChange(full_image_path, new_encoding, output_dir)
        change_encode.change_image_encoding()


if __name__ == "__main__":
    setup()
    image = ImageResizing("photos/IMG_0649.JPG")
    image.automatic_super_resize()
