import requests
from PIL import ImageFile
import numpy as np
from modules.base import BaseModule


class Downloader(BaseModule):

    def _process(self, url):
        response = requests.get(url)
        content = response.content
        parser = ImageFile.Parser()
        parser.feed(content)
        img = parser.close()
        img = np.array(img)
        return img
