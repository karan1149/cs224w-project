# https://becominghuman.ai/extract-a-feature-vector-for-any-image-with-pytorch-9717561d1d4c?fbclid=IwAR0D_5q4y4wd5jwVs7Y9dtnv7YNT9AqMtBzSb_miN0ziKtaGDNWgFkY9Zp0

import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torch.autograd import Variable
from PIL import Image
import os

embeddings = []

def save_output(module, input, output):
    embeddings.append(output)

model = models.resnet50(pretrained=True)
for param in model.parameters():
    param.requires_grad = False
model.eval()
hook = model.layer4[0].conv2.register_forward_hook(save_output)

scaler = transforms.Resize((224, 224))
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
to_tensor = transforms.ToTensor()

def get_vector(image_name):
    img = Image.open(image_name)
    img_tensor = Variable(normalize(to_tensor(scaler(img))).unsqueeze(0))
    return img_tensor


def save_embeddings(directory='data/flickr_images'):
  subdirs = os.listdir(directory)
  last_embeddings_len = len(embeddings)

  num_images = 0
  with open('cnn_embeddings.txt', 'w') as embedding_file:   
    for subdir in subdirs:
      subdir_path = os.path.join(directory, subdir)
      if not os.path.isdir(subdir_path):
        continue

      images = os.listdir(subdir_path)
      images = [img for img in images if '.jpg' in img]

      num_images += len(images)

      # batch = torch.zeros(len(images), 3, 224, 224)

      for i, img in enumerate(images):
        img_tensor = get_vector(os.path.join(subdir_path, img))
        # batch[i] = img_tensor
        model(img_tensor)
        print embeddings[-1].size()

        assert(len(embeddings) == last_embeddings_len + 1)
        last_embeddings_len += 1

        img_id = img[:-4].split('_')[1]
        # line = img_id + ' '.join()

      # print batch[0].data
      # model(batch)
      # print embeddings[-1].size


  print num_images
save_embeddings()





  