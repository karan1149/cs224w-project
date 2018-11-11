# https://becominghuman.ai/extract-a-feature-vector-for-any-image-with-pytorch-9717561d1d4c?fbclid=IwAR0D_5q4y4wd5jwVs7Y9dtnv7YNT9AqMtBzSb_miN0ziKtaGDNWgFkY9Zp0

import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torch.autograd import Variable
from PIL import Image
import time
import pickle
import os
import random
import operator
from scipy.spatial.distance import cosine

with open('data/relevant_nodes_set.pkl', 'rb') as f:
  relevant_nodes = pickle.load(f)

embeddings = []


def save_output(module, input, output):
    embeddings.append(output)

model = models.resnet50(pretrained=True) # change this to desired model
for param in model.parameters():
    param.requires_grad = False
model.eval()
hook = model.avgpool.register_forward_hook(save_output)

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

  num_total_images = 0
  with open('cnn_embeddings.txt', 'w') as embedding_file:   
    num_subdirs = len(subdirs)
    for subdir_idx, subdir in enumerate(subdirs):
      subdir_path = os.path.join(directory, subdir)
      if not os.path.isdir(subdir_path):
        continue

      images = os.listdir(subdir_path)
      images = [img for img in images if '.jpg' in img]

      images = [(img, img[:-4].split('_')[1]) for img in images if img[:-4].split('_')[1] in relevant_nodes]

      num_images = len(images)
      num_total_images += num_images

      if not num_images:
        continue

      print('--- SUBDIR {:>3} OUT OF {:>3}: {:<35} with {:>4} images ............ '.format(str(subdir_idx + 1), str(num_subdirs), '[%s]' % subdir, str(num_images)), end='\r', flush=True)
      begin_time = time.time()


      batch = Variable(torch.zeros(num_images, 3, 224, 224))

      for i, (img, img_id) in enumerate(images):
        assert(img_id in relevant_nodes)



        img_tensor = get_vector(os.path.join(subdir_path, img))
        batch[i] = img_tensor.data
        # model(img_tensor)
        # print('--- SUBDIR {:>3} OUT OF {:>3}: {:<35} with {:>4} images ............ {:<10}'.format(str(subdir_idx + 1), str(num_subdirs), '[%s]' % subdir, str(num_images), '[%d/%d]' % (i, num_images)), end='\r', flush=True)

        # assert(len(embeddings) == last_embeddings_len + 1)
        # last_embeddings_len += 1

        # line = img_id + ' ' + ' '.join(map(lambda x: str(x), embeddings[-1].data.numpy().flatten())) + '\n'
        # embedding_file.write(line)
      model(batch)
      assert(len(embeddings) == last_embeddings_len + 1)
      last_embeddings_len += 1

      for i in range(len(images)):
        line = img_id + ' ' + ' '.join(map(lambda x: str(x), embeddings[-1].data.numpy()[i].flatten())) + '\n'
        embedding_file.write(line)
      return

      print('--- SUBDIR {:>3} OUT OF {:>3}: {:<35} with {:>4} images ............ time: {:>10}s'.format(str(subdir_idx + 1), str(num_subdirs), '[%s]' % subdir, str(num_images), '%f' % (time.time() - begin_time)))

  print('TOTAL NUMBER OF IMAGES:', num_total_images)


def populate_embedding_map(embedding_file, embedding_map):
  values_size = -1
  with open(embedding_file, 'r') as file:
    for line in file:
      tokens = line.split()
      values = [float(num) for num in tokens[1:]]

      # Ensure all embeddings in a file are of the same size.
      assert(values_size == -1 or values_size == len(values))
      values_size = len(values)

      embedding_map[tokens[0]] = values

def find_similar_images(num_samples=1000000):
  embedding_map = {}
  similarities_map = {}

  populate_embedding_map('cnn_embeddings_partial.txt', embedding_map)

  ids = embedding_map.keys()
  for i in range(num_samples):
    id1, id2 = random.sample(ids, 2)
    similarities_map[(id1, id2)] = cosine(embedding_map[id1], embedding_map[id2])

  top10_pairs = dict(sorted(similarities_map.items(), key=operator.itemgetter(1), reverse=False)[:10])
  for ids, cosine_val in top10_pairs.items():
    print('MAX IDS: %s and %s (value = %s)' % (ids[0], ids[1], cosine_val))


save_embeddings()
# find_similar_images()





  