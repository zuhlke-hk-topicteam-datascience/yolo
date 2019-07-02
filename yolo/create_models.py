import os
from .utils import utils
from .models import *
from PIL import Image
from torchvision.transforms import Compose, Resize, ToTensor
from einops import rearrange
from einops.layers.torch import Rearrange
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import NullLocator
import random


def filedir():
    return os.path.dirname(os.path.realpath(__file__))


class Model:

    def __init__(self,
                 device="cpu",
                 iou_thres=0.5,
                 conf_thres=0.8,
                 nms_thres=0.5,
                 img_size=416,
                 ):

        self.device = device
        self.iou_thres = iou_thres
        self.conf_thres = conf_thres
        self.nms_thres = nms_thres
        self.img_size = img_size
        self.classes = None
        self.model = None

        if self._should_download():
            self._download_weights()
        self._load_model()
        self._load_classes()

    def predict(self, img):
        """
        Args:
            x: a PIL Image
        Returns:
            dictionary of class predictions
        """
        x = self.pil_to_tensor(img)
        y = self.model(x)
        detections = utils.non_max_suppression(y, self.conf_thres, self.nms_thres)[0]

        if detections is not None:
            detections = utils.rescale_boxes(
                detections, self.img_size, list(img.size))
            return [{
                "x1": float(x1),
                "x2": float(x2),
                "y1": float(y1),
                "y2": float(y2),
                "prob": float(conf),
                "class_prob": float(cls_conf),
                "class": self.classes[int(cls_pred)],
            } for x1, y1, x2, y2, conf, cls_conf, cls_pred in detections]
        else:
            return []

    def _should_download(self):
        NotImplementedError()

    def _download_weights(self):
        NotImplementedError()

    def _load_model(self):
        NotImplementedError()

    def _load_classes(self):
        NotImplementedError()

    def pil_to_tensor(self, x):
        transforms = Compose([
            Resize((self.img_size, self.img_size)),
            ToTensor(),
            Rearrange("c h w -> () c h w")
        ])

        return transforms(x)


class Yolo(Model):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _should_download(self):
        return not os.path.isfile("weights/yolov3.weights")

    def _download_weights(self):
        cmd = f"weights/download_yolov3.sh"
        os.system(cmd)

    def _load_model(self):
        cfg = os.path.join(filedir(), "config/yolov3.cfg")
        weights = os.path.join(filedir(), "weights/yolov3.weights")
        self.model = Darknet(cfg).to(self.device)
        self.model.load_darknet_weights(weights)
        self.model.eval()

    def _load_classes(self):
        path = os.path.join(filedir(), "config/coco.names")
        self.classes = utils.load_classes(path)
