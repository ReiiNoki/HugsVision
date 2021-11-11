import json

import torch
from torchvision import transforms

from PIL import Image

class TorchVisionClassifierInference:

  transformTorchVision = transforms.Compose([
      transforms.Resize((224,224),interpolation=Image.NEAREST),
      transforms.ToTensor(),
      # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
  ])

  """
  🤗 Constructor for the image classifier trainer of TorchVision
  """
  def __init__(self, model_path: str, transform=transformTorchVision):

    self.model_path = model_path if model_path.endswith("/") else model_path + "/"
    self.transform = transform
    
    self.model = torch.load(self.model_path + "best_model.pth", map_location="cuda:0")

    self.config = json.load(open(self.model_path + "config.json", "r"))

    print("Model loaded!")

  """
  Arguments
  ---------
  img: Pillow Image
  """
  def predict_image(self, img):
    
    img = self.transform(img)
    img = torch.unsqueeze(img, 0)

    # Predict and get the corresponding label identifier
    pred = self.model(img)

    # Get label index
    _, predicted_class_idx = torch.max(pred, 1)

    # Get string label from index
    label = self.config["id2label"][str(predicted_class_idx.item())]
    
    return label

  """
  Arguments
  ---------
  img_path: str
  """
  def predict(self, img_path: str):  
    return self.predict_image(img=Image.open(img_path))
