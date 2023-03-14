import os
from resmem import ResMem, transformer
from PIL import Image
import pandas as pd
import argparse
import time

time0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument('--loc', type=str)
parser.add_argument('--output_dir', type=str)
args = parser.parse_args()
loc = args.loc
output_dir = args.output_dir

# get all the file names
for root, dirs, files in os.walk(loc):
    # assumes no recursive structure, so just break
    break

model = ResMem(pretrained=True)
model.eval()

preds = []
names = []
for f in sorted(files):
    img = Image.open(f'{root}/{f}')
    img.convert('RGB')
    image_x = transformer(img)
    c, h, w = image_x.size()
    prediction = model(image_x.view(-1, c, h, w))
    preds.append(prediction.detach().numpy().item())
    names.append(f)

df = pd.DataFrame({'img_name':names, 'resmem_pred':preds})
df.to_csv(output_dir, index=False)

time1 = time.time()
print(f'it took {time1 - time0} seconds')