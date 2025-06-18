import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import torch
from torchvision import models, transforms
import urllib
import json

# Load pretrained model
model = models.resnet50(pretrained=True)
model.eval()

# Load ImageNet labels
url = 'https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt'
imagenet_classes = urllib.request.urlopen(url).read().decode().splitlines()

# Image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# Generate descriptive sentence
def generate_sentence(label):
    label = label.lower()
    if 'person' in label:
        return "A person is standing on the road."
    elif 'dog' in label:
        return "A dog is sitting or walking around."
    elif 'car' in label or 'vehicle' in label:
        return "A car is parked or driving on the road."
    elif 'cat' in label:
        return "A cat is resting nearby."
    elif 'tree' in label:
        return "A tree is visible in the scene."
    elif 'building' in label:
        return "A building can be seen in the background."
    elif 'road' in label:
        return "A road is visible."
    else:
        return f"It appears to be a {label}."

# GUI setup
def load_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    image = Image.open(file_path).convert('RGB')
    image_resized = image.resize((224, 224))
    tk_image = ImageTk.PhotoImage(image_resized)
    panel.config(image=tk_image)
    panel.image = tk_image

    # Transform and predict
    input_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor)
        predicted_idx = output.argmax(1).item()
        predicted_label = imagenet_classes[predicted_idx]

    sentence = generate_sentence(predicted_label)
    label_result.config(text=sentence)

# Create GUI
root = tk.Tk()
root.title("Image Classifier with Description")
root.geometry("500x500")

btn_load = tk.Button(root, text="Load Image", command=load_image)
btn_load.pack(pady=10)

panel = tk.Label(root)
panel.pack()

label_result = tk.Label(root, text="", font=("Arial", 14), wraplength=480)
label_result.pack(pady=10)

root.mainloop()
