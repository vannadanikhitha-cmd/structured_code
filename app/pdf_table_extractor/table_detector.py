from transformers import (
    DetrImageProcessor,
    TableTransformerForObjectDetection
)
from PIL import Image
import torch


class TableDetector:

    def __init__(self):
        #Loads image preprocessing pipeline
        #using pre-trained Table Transformer (TATR) model
        self.processor = (DetrImageProcessor.from_pretrained("microsoft/table-transformer-detection"))
        #Loads the actual AI model
        self.model = (TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection"))

    def detect(self, image):
        #Converts OpenCV/Numpy image into PIL image
        pil_img = Image.fromarray(image)
        #Resize the image
        #create pytorch tensor
        inputs = self.processor(images=pil_img,return_tensors="pt")
        #unpacks the directory
        outputs = self.model(**inputs)
        #[-1] will convert img size in reverse like height, width
        results = (self.processor.post_process_object_detection(outputs,threshold=0.6,target_sizes=torch.tensor([pil_img.size[::-1]]))[0])

        tables = []

        for box in results["boxes"]:
            #convert Torch Tensor to list 
            tables.append(box.tolist())

        return tables