from modules.base import BaseModule
from PIL import Image


class Storager(BaseModule):

    def _process(self, item):
        content, path = item
        content = Image.fromarray(content.astype("uint8")).convert("RGB")
        content.save(path)
