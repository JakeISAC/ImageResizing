"""
Before running the code you will need to install the following:
- pip3 install opencv-python opencv-contrib-python
- pip3 install numpy
- pip3 install pillow
"""
from api import RequestHandler
from initialize import Initialize


if __name__ == "__main__":
    Initialize().setup()
    handler = RequestHandler()
    handler.handle_request()
