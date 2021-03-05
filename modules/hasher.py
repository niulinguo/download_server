from modules.base import BaseModule
from scipy import signal
from PIL import Image
import hashlib


class Hasher(BaseModule):

    def _process(self, item):
        cov = [[[0.1], [0.05], [0.1]]]
        img = signal.convolve(item, cov)
        img = Image.fromarray(img.astype("uint8")).convert("RGB")
        md5 = hashlib.md5(str(img).encode("utf-8")).hexdigest()
        return md5
