from urllib import request
import re


class ImageUrlSpider:
    url = "http://www.jituwang.com/tuku"
    image_type = "nvxingnvren"
    root_pattern = r'<div class="anPic">([\s\S]+?)</div>'
    image_pattern = r'<img src="([\s\S]+?)" alt="([\s\S]+?)"/>'

    @classmethod
    def __fetch_content(cls, page):
        r = request.urlopen(f'{cls.url}/{cls.image_type}/list_{page}.html')
        htmls = r.read()
        # htmls = str(htmls, 'utf-8')
        htmls = str(htmls, 'gbk')
        return htmls

    @classmethod
    def __analysis(cls, htmls):
        list_html = re.findall(cls.root_pattern, htmls)
        anchors = []
        for html in list_html:
            info = re.findall(cls.image_pattern, html)
            image: str = info[0][0]
            title: str = info[0][1]
            if image.startswith("http://"):
                anchor = {
                    'image': image.strip(),
                    'title': title.strip(),
                }
                anchors.append(anchor)
        return anchors

    @staticmethod
    def __show(anchors):
        for index in range(0, len(anchors)):
            anchor = anchors[index]
            print(f'{anchor["title"]}:{anchor["image"]}')

    @staticmethod
    def __write(anchors):
        fo = open("./images.txt", "w")
        for index in range(0, len(anchors)):
            anchor = anchors[index]
            fo.write(f'{anchor["image"]}\n')
        fo.close()

    @classmethod
    def go(cls):
        all_anchors = []

        for page in range(1, 10):
            htmls = cls.__fetch_content(page)
            anchors = cls.__analysis(htmls)
            all_anchors.extend(anchors)

        cls.__show(all_anchors)
        cls.__write(all_anchors)


if __name__ == '__main__':
    ImageUrlSpider.go()
