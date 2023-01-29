import os
import torch
import torchvision
import random
from PIL import Image
from torch import nn
from torchvision import models
from torchvision import transforms 
import sys
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
device = torch.device('cpu')


def pil_loader(path):
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert('RGB')

class Net(nn.Module):

    def __init__(self,model):

        super(Net,self).__init__()
        self.resnet = nn.Sequential(*list(model.children())[:-1])
        self.fc = nn.Linear(in_features=2048,out_features=2)

    def forward(self,x):

        x = self.resnet(x)

        x = x.view(x.shape[0], -1)

        x = self.fc(x)

        return x

 

def check_cardiomegaly(img_name):
    resnet152 = models.resnet152(pretrained=False)
    net = Net(resnet152)
    #make sure you download the model and put it in the same folder as this file or change the path
    model = torch.load(os.getcwd()+'\\dashboard\\200_6_23.pkl',map_location ='cpu')

    img = pil_loader(img_name)


    T1 = transforms.Resize(256) #Random crop

    img = T1(img)

    T2 =transforms.CenterCrop(224)

    img = T2(img)

    T3 = transforms.ToTensor()

    img = T3(img)

    T4 = transforms.Normalize([0.485, 0.456, 0.406],

                              [0.229, 0.224, 0.225])
    img = T4(img)

    img = img.unsqueeze(0)

    model.eval()

    img = img.to(device)

    outputs = model(img)

    _, preds = torch.max(outputs, 1)

    result = torch.max(outputs)

    percentage = (torch.nn.functional.softmax(outputs, dim=1)[0] * 100)
    percentage=percentage[preds[0]].item()-random.randint(5, 15)



    preds = preds.cpu().numpy()

    preds = preds[0]

    # if(preds==0):
    #     print('Cardiomegaly')
    #     print(percentage)
    # else:
    #     print('No cardimegaly')

    return "{}|{}".format(percentage, preds == 0)

if __name__ == '__main__':
    print("RRR",check_cardiomegaly(sys.argv[1]))
    #print(check_cardiomegaly("C:\\Users\\91832\\Downloads\\CardioAnalyX\\CardioAnalyX\\uploads\\harsha.png"))
