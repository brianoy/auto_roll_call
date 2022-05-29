"""
!brew install zbar
!pip install pyqrcode
!pip install pyzbar

from PIL import Image
from pyzbar.pyzbar import decode
data = decode(Image.open('horn.png'))
print(data[0][0].decode("utf-8"))
"""
#from PIL import Image
from pyzbar.pyzbar import decode
def qr_code_decode(pic):
    try:
        data = decode(pic)
        info = data[0][0].decode("utf-8")
    except IndexError:
        info = ""
    return info



