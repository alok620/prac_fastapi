import json
import base64
import io
import pickle
from PIL import Image

with open('app/images/generated.png', mode='rb') as file:
    img = file.read()
img = base64.encodebytes(img).decode('utf-8')

img = base64.b64decode(img)

print(img)


img = Image.open(io.BytesIO(img))
img.show()

