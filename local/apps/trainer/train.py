import torch
import os
from shared.config import settings

from ultralytics import YOLO
class Trianer:
    def start(self):
    
        # Load a pre-trained model
        self.model = YOLO(settings.model_path)
        # self.model = Model.load_vision()  # or use 'yolov5s.pt' for YOLOv5
        
        # Training parameters
        self.data = settings.dataset_yaml  # Path to your dataset YAML file
        self.epochs = settings.epochs          # Number of epochs to train for
        self.batch = settings.batch          # Batch size
        self.img_size = settings.model_imge_size        # Image size
    
        # Fine-tune the model
        if torch.cuda.is_available():
            self.model.to('cuda')  # Move model to GPU
            

        self.model.train(data=self.data, epochs=self.epochs, batch=self.batch, imgsz=self.img_size)
    
        # Save the fine-tuned model
        self.model.save(f'{settings.session_name}.pt')
    