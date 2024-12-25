from ultralytics import YOLO

import torch
class Trianer:
    def start(self,config):
    
        # Load a pre-trained model
        self.model = config.get_model()  # or use 'yolov5s.pt' for YOLOv5
    
        # Training parameters
        self.data = config.DATASET_YAML  # Path to your dataset YAML file
        self.epochs = config.epochs          # Number of epochs to train for
        self.batch = config.batch          # Batch size
        self.img_size = 640        # Image size
    
        # Fine-tune the model
        if torch.cuda.is_available():
            self.model.model.to('cuda')  # Move model to GPU
            
        self.model.train(data=self.data, epochs=self.epochs, batch=self.batch, imgsz=self.img_size)
    
        # Save the fine-tuned model
        self.model.save(f'{config.SESSION_NAME}.pt')
    