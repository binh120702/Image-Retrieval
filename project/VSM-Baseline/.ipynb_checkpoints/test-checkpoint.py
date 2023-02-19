import feature_extractor
from PIL import Image 

data_path = '../data/oxbuild_images-v1/all_souls_000000.jpg'

tmp = Image.open(data_path) 

print(tmp)