import fitz
import cv2
import numpy as np


class PDFLoader:

    def __init__(self, dpi=200):
        self.dpi = dpi

    def load_pdf(self, pdf_path):

        doc = fitz.open(pdf_path)

        pages = []

        for page in doc:
            #enlarge pages before converting into images
            mat = fitz.Matrix(self.dpi / 72,self.dpi / 72)
            #convert pdf pages into images
            pix = page.get_pixmap(matrix=mat,alpha=False)
            #convert raw bytes to numpy array
            img = np.frombuffer(pix.samples,dtype=np.uint8)
            #reshape into image
            img = img.reshape(pix.height,pix.width,pix.n)

            if pix.n == 4:
                #convert RGBA to BGR
                img = cv2.cvtColor(img,cv2.COLOR_RGBA2BGR)

            pages.append(img)

        return pages