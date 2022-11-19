""" Evaluate the model on the test dataset
"""
import torch
import os
import csv
import argparse
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True # handle the case of truncated images
from torchvision import datasets, transforms

input_size = 224

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
    'extra_issues': transforms.Compose([
        transforms.Resize(input_size),
        transforms.CenterCrop(input_size),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}


def evaluate(model, dataloaders, cls_type):
    
    model.eval()   # Set model to evaluate mode
    results = dict()

    for inputs, labels in dataloaders[phase]:
        inputs = inputs.to(device)
        labels = labels.to(device)
        
        outputs = model(inputs)
        _, preds = torch.max(outputs, 1)

    for img, pred in zip(dataloaders[phase].dataset.imgs, preds):
        if cls_type == 'osm_cls':
            results[img[0]] = 'footway' if pred == 0 else 'primary'
        else:
            results[img[0]] = 'nonroad' if pred == 0 else 'road'

    # print results
    for k,v in results.items():
        print(k.split('/')[-1],v)

    # output the results into csv files
    with open(f'./{cls_type}_results.csv','w') as f:
        writer = csv.writer(f)
        if cls_type == 'osm_cls':
            writer.writerow(['image_id','highway']) # title
        else:
            writer.writerow(['image_id', 'road/non-road'])

        for key in results.keys():
            writer.writerow([key.split('/')[-1].split('.')[0],results[key]])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_size',type=int,default=256)
    parser.add_argument('--input_size',type=int,default=224)
    parser.add_argument('--phase',type=str,default='issues')
    parser.add_argument('--cls_type',type=str,default='osm_cls')
    args = parser.parse_args()

    batch_size = args.batch_size
    input_size = args.input_size
    phase = args.phase
    cls_type = args.cls_type

    model_path = ""
    data_dir = ""
    if args.cls_type == 'osm_cls':
        data_dir = './huawei_dataset'
        model_path = './checkpoints/resnet18_epoch15_0.944.pth'
    else:
        data_dir = './road_dataset'
        model_path = './checkpoints/road_cls_resnet18_epoch15_0.976.pth'

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # Create training and validation datasets
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x]) for x in [phase]}
    # Create training and validation dataloaders
    dataloaders_dict = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=batch_size, num_workers=4) for x in [phase]}

    model_ft = torch.load(model_path)
    evaluate(model_ft, dataloaders_dict,cls_type)