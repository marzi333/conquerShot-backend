import torch
from torchvision import transforms
from PIL import Image

input_size = 224
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

data_transforms = {
    'train': transforms.Compose([
        transforms.RandomResizedCrop(input_size),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Resize(input_size),
        transforms.CenterCrop(input_size),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'issues': transforms.Compose([
        transforms.Resize(input_size),
        transforms.CenterCrop(input_size),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'custom': transforms.Compose([
        transforms.Resize(input_size),
        transforms.CenterCrop(input_size),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

def pil_loader(path: str) -> Image.Image:
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert('RGB')

def evaluate_single_img(img_path,cls_type='osm_cls'):
    # load single image
    img = pil_loader(img_path)
    img = data_transforms['issues'](img)
    img = img.to(device)
    img = img.unsqueeze(0)
    # load model
    results = []
    model_ft = None
    if cls_type == 'osm_cls':
        model_ft = torch.load('./checkpoints/resnet18_epoch15_0.944.pth')
        results = ['footway','primary']
    else:
        model_ft = torch.load('./checkpoints/road_cls_resnet18_epoch15_0.976.pth')
        results = ['nonroad','road']
    model_ft.eval()
    outputs = model_ft(img)
    _, preds = torch.max(outputs, 1)
    return results[0] if preds == 0 else results[1]