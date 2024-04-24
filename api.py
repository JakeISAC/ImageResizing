import resizing as resize
import encode_change as encode
import argparse


class RequestHandler:
    parser = argparse.ArgumentParser(description='Process some requests.')

    def __init__(self):
        # base requests
        self.parser.add_argument("--resize-auto", action="store_true",
                                 help="Perform auto resizing. The return is a base64 encode of the resized image. "
                                      "** Required filedes: "
                                      "--image-path "
                                      ", Optional fields: "
                                      "--save-image "
                                      "--output-dir-resizing **")
        self.parser.add_argument("--resize-manual", action="store_true",
                                 help="Perform manual resizing. The return is a base64 encode of the resized image. "
                                      "If no parameters are provided the operation will default to basic_resize() "
                                      "** Required fields: "
                                      "--image-path "
                                      ", Optional fields: "
                                      "--name "
                                      "--encode "
                                      "--new-width "
                                      "--new-height "
                                      "--super-resolution "
                                      "--output-dir-resizing "
                                      "--save-image **")
        self.parser.add_argument("--resize-auto-super", action="store_true",
                                 help="Perform auto super resizing. The return is a base64 encode of the resized "
                                      "image. "
                                      "** Required fields: "
                                      "--image-path "
                                      ", Optional fields: "
                                      "--save-image "
                                      "--output-dir-resizing **")
        self.parser.add_argument("--resize-auto-basic", action="store_true",
                                 help="Perform auto basic resizing. The return is a base64 encode of the resized image. " 
                                      "** Required fields: "
                                      "--image-path "
                                      ", Optional fields: "
                                      "--save-image "
                                      "--output-dir-resizing **")
        self.parser.add_argument("--resize-dir", action="store_true",
                                 help="Perform auto directory resizing. The return is a base64 encode of the resized "
                                      "image "
                                      "** Required fields: "
                                      "--image-dir-path "
                                      ", Optional fields: "
                                      "--save-image "
                                      "--output-dir-resizing **")
        self.parser.add_argument("--change-encode", action="store_true",
                                 help="Change the image encoding. The return is a path where the images were saved."
                                      "image. "
                                      "** Required fields: "
                                      "--image-path "
                                      "--encode "
                                      ", Optional fields: "
                                      "--output-dir-encode **")
        self.parser.add_argument("--change-encode-dir", action="store_true",
                                 help="Change the encode of all images in a dir. The return is a base64 encode of the "
                                      "resized image. "
                                      "** Required fields: "
                                      "--image-dir-path "
                                      "--encode"
                                      ", Optional fields: "
                                      "--output-dir-encode **")

        self.parser.add_argument("--image-path", type=str,
                                 help="Path to the image to be processed")
        self.parser.add_argument("--output-dir-resizing", default="", type=str,
                                 help="Path to the output folder for the resized image."
                                      "If you want to use the default encode one please leave blank.")
        self.parser.add_argument("--save-image", type=bool, default=False,
                                 help="Boolean determining if the images is to be saved.")
        # flags manual resize
        self.parser.add_argument("--name", type=str, default="image", help="Name of the file")
        self.parser.add_argument("--encode", type=str, default="png", help="Encoding format of the image")
        self.parser.add_argument("--new-width", type=int, default=1920, help="New width for the image")
        self.parser.add_argument("--new-height", type=int, default=1080, help="New height for the image")
        self.parser.add_argument("--super-resolution", type=bool, default=False,
                                 help="Apply super resolution to the image")

        self.parser.add_argument("--image-dir-path", type=str,
                                 help="Path to a directory containing images to be resized")

        self.parser.add_argument("--output-dir-encode", type=str, default="",
                                 help="Directory to save the output image file")

    def handle_request(self) -> str:
        args = self.parser.parse_args()

        if args.resize_auto:
            print(self.__handle_resize_auto(args))
        elif args.resize_manual:
            print(self.__handel_resize_manual(args))
        elif args.resize_auto_super:
            print(self.__handel_resize_auto_super(args))
        elif args.resize_auto_basic:
            print(self.__handel_resize_auto_basic(args))
        elif args.resize_dir:
            print(self.__handel_resize_dir(args))
        elif args.change_encode:
            path = self.__handel_change_image_encode(args)
            return f"The image have been saved at:\n{path}"
        elif args.change_encode_dir:
            path = self.__handel_change_encode_dir(args)
            return f"The images have been saved at:\n{path}"
        else:
            return "Command unknown. Can not process"

    @staticmethod
    def __handle_resize_auto(args) -> str:
        resize_auto = resize.ImageResizing(args.image_path, args.output_dir_resizing, args.save_image)
        return resize_auto.auto()

    @staticmethod
    def __handel_resize_manual(args) -> str:
        resize_manual = resize.ImageResizing(args.image_path, args.output_dir_resizing, args.save_image)
        return resize_manual.manual_resize(args.name, args.encode, args.new_width, args.new_height,
                                           args.super_resolution)

    @staticmethod
    def __handel_resize_auto_super(args) -> str:
        resize_auto_super = resize.ImageResizing(args.image_path, args.output_dir_resizing, args.save_image)
        return resize_auto_super.automatic_super_resize()

    @staticmethod
    def __handel_resize_auto_basic(args) -> str:
        resize_auto_basic = resize.ImageResizing(args.image_path, args.output_dir_resizing, args.save_image)
        return resize_auto_basic.automatic_basic_resize()

    @staticmethod
    def __handel_resize_dir(args) -> [str]:
        return resize.resize_images_in_dir(args.image_dir_path, args.output_dir_resizing, args.save_image)

    @staticmethod
    def __handel_change_image_encode(args) -> str:
        change_encode = encode.EncodeChange(args.image_path, args.encode, args.output_dir_encode)
        change_encode.change_image_encoding()
        return change_encode.get_path()

    @staticmethod
    def __handel_change_encode_dir(args) -> str:
        result = encode.change_directory_images_encoding(args.image_dir_path, args.encode, args.output_dir_encode)
        return result
