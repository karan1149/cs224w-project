from collections import defaultdict
from collections import Counter
import os
import operator
import random

# Num labels is 81
# Top labels:
  # Labels_sky.txt 74190
  # Labels_clouds.txt 54087
  # Labels_person.txt 51577
  # Labels_water.txt 35264
  # Labels_animal.txt 33887
  # Labels_grass.txt 22561
  # Labels_buildings.txt 17835
  # Labels_window.txt 15051
  # Labels_plants.txt 14345
  # Labels_lake.txt 13392
  # Labels_ocean.txt 11307
  # Labels_road.txt 9524
  # Labels_flowers.txt 8605
  # Labels_sunset.txt 8418
  # Labels_reflection.txt 7875
  # Labels_rocks.txt 6327
  # Labels_vehicle.txt 6099
  # Labels_snow.txt 5404
  # Labels_tree.txt 5352
  # Labels_beach.txt 5239
  # Labels_mountain.txt 5099

# 1: 79214 --> covers 80/81 labels
# 2: 52640
# 3: 33063
# 4: 20607
# 5: 12206
# 6: 6723
# 7: 3263
# 8: 1213
# 9: 323
# 10: 77
# 11: 10
# 12: 2
# 13: 1

images = []

with open('data/ImageList/ImageList.txt', 'r') as f:
  for line in f:
    images.append(line[line.rfind('_')+1:].strip())

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

    # num_ones = sum(1 for line in enumerate(f) if line == '1\n')
    # num_images_per_label[labels_file] = num_ones

sorted_labels = sorted(num_images_per_label.items(), key=operator.itemgetter(1), reverse=True)
for label, num_images in sorted_labels:
  print label, num_images, random.sample(images_per_label[label], 5)

labels_per_image = defaultdict(list)

for label in images_per_label:
  for image in images_per_label[label]:
    labels_per_image[image].append(label)

print(Counter([len(labels_per_image[image]) for image in labels_per_image], most_common=True))

# num_unary_images_ = defaultdict(int)
# for image in labels_per_image:
#   if len(labels_per_image[image]) == 1:


print(Counter([labels_per_image[image][0] for image in labels_per_image if len(labels_per_image[image]) == 1]))

unary_images = set()
for image in labels_per_image:
  if len(labels_per_image[image]) == 1:
    unary_images.add(image)

unary_images_per_label = defaultdict(list)

for image in unary_images:
  unary_images_per_label[labels_per_image[image][0]].append(image)

for label in unary_images_per_label:
  if len(unary_images_per_label[label]) > 5:
    print(label, random.sample(unary_images_per_label[label], 5))

