# based on https://github.com/Brain-Bridge-Lab/resmem/blob/master/sample.py
from resmem import ResMem, transformer
import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import numpy as np
import os
import pandas as pd
import argparse
import time

time0 = time.time()

class ImageOnlyDataset(Dataset):
    def __init__(self, loc, transform=transformer):
        self.loc = loc
        self.transform = transform
        # get all the file names
        for root, dirs, files in os.walk(loc):
            # assumes no recursive structure, so just break
            break
        self.frame = np.array(sorted(files)).reshape(-1,1)
    
    def __len__(self):
        return self.frame.shape[0]
    
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        
        img_name = self.frame[idx, 0]
        image = Image.open(f'{self.loc}/{img_name}')
        image = image.convert('RGB')
        image_x = self.transform(image)
        return [img_name, image_x]

ORDINAL = 1

parser = argparse.ArgumentParser()
parser.add_argument('--loc', type=str)
parser.add_argument('--output_dir', type=str)
parser.add_argument('--batch_size', type=int, default=32)
parser.add_argument('--num_workers', type=int, default=1)
args = parser.parse_args()
loc = args.loc
output_dir = args.output_dir
batch_size = args.batch_size
num_workers = args.num_workers

# check if cuda is available
if torch.cuda.is_available():
    print('Using GPU')
else:
    print('Did not find GPU')

# load the images
dt = ImageOnlyDataset(loc)
d_test = DataLoader(dt, batch_size=batch_size, num_workers=num_workers, pin_memory=True)

# load the model
model = ResMem(pretrained=True).cuda()

if len(d_test):
    model.eval()
    with torch.no_grad():
        preds = []
        names = []
        for batch in d_test:
            name, x = batch
            bs, c, h, w = x.size()
            pred = model.forward(x.cuda().view(-1, c, h, w)).view(bs, -1).mean(1)
            preds += pred.squeeze().tolist()
            names += name
    df = pd.DataFrame({'img_name':names, 'resmem_pred':preds})
    df.to_csv(output_dir, index=False)
else:
    print(f'No data found in {loc}')

time1 = time.time()
print(f'it took {time1 - time0} seconds')