from paddleocr import PaddleOCR


class OCREngine:

    def __init__(self):
        #Creates a PaddleOCR object
        self.ocr = PaddleOCR(use_angle_cls=True,lang="en")

    def extract(self, image):

        result = self.ocr.ocr(image)

        words = []

        if not result or not result[0]:
            return words

        for line in result[0]:
            #create bbox for each word /header
            words.append({"bbox": line[0],"text": line[1][0]})

        return words