# Use a pipeline as a high-level helper
from transformers import pipeline
from PIL import Image
import pandas as pd
import torch
import time

semantic_segmentation = pipeline("image-segmentation", model="facebook/maskformer-swin-large-coco", 
                                 device=torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

image_path = "test.jpeg"
image = Image.open(image_path)

t1 = time.time()
results = semantic_segmentation(image)
print("computation time :", time.time() - t1)

print(f"pipeline device : {semantic_segmentation.device}")

df = pd.DataFrame(results)
print(df)

for i, mask in enumerate(df['mask']):
    mask.save(f"{i}.png")