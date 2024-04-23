from transformers import pipeline
from PIL import Image
import torch
import base64
import json
from io import BytesIO
import logging

def img_to_base64(image):
    im_file = BytesIO()
    image.save(im_file, format="JPEG")
    im_bytes = im_file.getvalue()
    im_b64 = base64.b64encode(im_bytes)
    return im_b64

def init():
    global semantic_segmentation
    semantic_segmentation = pipeline("image-segmentation", model="facebook/maskformer-swin-large-coco", 
                                    device=torch.device('cuda' if torch.cuda.is_available() else 'cpu'))
    logging.info(f"pipeline device : {semantic_segmentation.device}")
    logging.info("Init complete")

def run(raw_data):
    logging.info("model : request received")
    data = json.loads(raw_data)
    image = Image.open(BytesIO(base64.b64decode(data['img'])))
    results = semantic_segmentation(image)
    for i,j in enumerate(results):
        img = j['mask']
        wef = img_to_base64(img)
        results[i]['mask'] = wef.decode("utf-8")
    logging.info("Request processed")
    return results