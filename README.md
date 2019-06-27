# Yolo



Example usage


```python

from yolo import Yolo
from PIL import Image

path "<path to a image>"
img = Image.open(path)

model = Yolo()
y = model.predict(img)



```

Downloading model weights depends on  `wget` so if you may need to install with `brew install wget`


# Todo

* Add Darknet and YoloTiny
* Don't depend on wget for download
* Add plots to draw predicted bounding boxes
