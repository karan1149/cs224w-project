from collections import defaultdict
from collections import Counter
import os
import operator
import random

images = []

with open('data/ImageList/ImageList.txt', 'r') as f:
  for line in f:
    images.append(line[line.rfind('_')+1 : line.find('.')].strip())
print('Number of total images %d' % len(images))

labels_dir = 'data/Groundtruth/AllLabels'
labels_files = [name for name in os.listdir(labels_dir) if name.endswith('.txt') ]

print("Num labels is %d" % len(labels_files))

num_images_per_label = defaultdict(int)
images_per_label = defaultdict(list)
for labels_file in labels_files:
  with open(os.path.join(labels_dir, labels_file), 'r') as f:
    for i, line in enumerate(f):
      if line == '1\n':
        num_images_per_label[labels_file] += 1
        images_per_label[labels_file].append(images[i])

labels_per_image = defaultdict(list)

for label in images_per_label:
  for image in images_per_label[label]:
    labels_per_image[image].append(label[label.find('_')+1:label.find('.')])

popular_images = set([])
with open('data/flickrEdgesMostPopularRelevant40k.txt', 'r') as f:
  for line in f:
    popular_images.update(line.split())

print(random.sample(popular_images,10))

print(Counter([len(labels_per_image[image]) for image in popular_images]))

unary_images = {image : labels_per_image[image] for image in popular_images if len(labels_per_image[image]) == 1}

print(random.sample(unary_images.items(), 10))

