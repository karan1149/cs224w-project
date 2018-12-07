from collections import defaultdict
from collections import Counter
import os
import operator
import random


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

sorted_labels = sorted(num_images_per_label.items(), key=operator.itemgetter(1), reverse=True)
# for label, num_images in sorted_labels:
#   print label, num_images, random.sample(images_per_label[label], 5)

labels_per_image = defaultdict(list)

for label in images_per_label:
  for image in images_per_label[label]:
    labels_per_image[image].append(label[label.find('_')+1:label.find('.')])

# print(Counter([len(labels_per_image[image]) for image in labels_per_image], most_common=True))

def unary_binary_analysis():
  print(Counter([labels_per_image[image][0] for image in labels_per_image if len(labels_per_image[image]) <= 2]))

  unary_images = set()
  for image in labels_per_image:
    if len(labels_per_image[image]) <= 2:
      unary_images.add(image)

  unary_images_per_label = defaultdict(list)

  for image in unary_images:
    unary_images_per_label[labels_per_image[image][0]].append(image)

  for label in unary_images_per_label:
    if len(unary_images_per_label[label]) > 5:
      print(label, random.sample(unary_images_per_label[label], 5))

# def animal_person_analysis():
animal_classes = {'animal', 'birds', 'dog', 'cat', 'horses', 'fish', 'elk', 'cow', 'tiger', 'fox', 'whales', 'zebra'}

person_animal_images = defaultdict(list)
for image, labels in labels_per_image.items():
  image_id = image[:image.find('.')]
  if len(set(labels) & animal_classes) > 0:
    person_animal_images[image_id].append('animal')
  if 'person' in labels:
    person_animal_images[image_id].append('person')

person_images = set([image_id for image_id in person_animal_images if person_animal_images[image_id] == ['person']])
animal_images = set([image_id for image_id in person_animal_images if person_animal_images[image_id] == ['animal']])
both_images = set([image_id for image_id in person_animal_images if len(person_animal_images[image_id]) == 2])

print('Num only person images is %d' % len(person_images))
print('Num only animal images is %d' % len(animal_images))
print('Num both images is %d' % len(both_images))

print('person: ', random.sample(person_images, 5))
print('animal: ', random.sample(animal_images, 5))
print('both: ', random.sample(both_images, 5))

def create_subgraph(person_images, animal_images):
  # num_images_per_class = min(len(person_images), len(animal_images))
  # person_images = random.sample(person_images, num_images_per_class)
  # animal_images = random.sample(animal_images, num_images_per_class)

  nodes_to_include = person_images.union(animal_images)
  # print('num_images_per_class', num_images_per_class)
  print(len(nodes_to_include))

  input_edges = []
  input_nodes = set()

  with open('data/flickrEdges.txt', 'r') as f:
    for line in f:
      if line.startswith('#'):
        continue

      assert(len(line.split()) == 2)
      left_node, right_node = line.split()

      assert(int(left_node) > 0)
      assert(int(right_node) > 0)
      input_edges.append((left_node, right_node))

  edges_written = 0 
  nodes_added = set()
  with open('person_animal_edges.txt', 'w') as f:
    for left_node, right_node in input_edges:
      if left_node in nodes_to_include and right_node in nodes_to_include:
        f.write(left_node + ' ' + right_node + '\n')
        edges_written += 1
        nodes_added.add(left_node)
        nodes_added.add(right_node)

  print("Induced graph has %d unique nodes with %d edges" % (len(nodes_added), edges_written))

  num_person = len([node for node in nodes_added if node in person_images])
  num_animal = len([node for node in nodes_added if node in animal_images])

  print("Induced graph has %d person images and %d animal images" % (num_person, num_animal))

create_subgraph(person_images, animal_images)

# animal_person_analysis()


###################### GENERAL LABEL ANALYSIS #####################

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

#################### UNARY (OR BINARY) IMAGE ANALYSIS #####################

# Label counts for unary images:
# 'Labels_person.txt': 31617 +++
# 'Labels_animal.txt': 10463 +++
# 'Labels_sky.txt': 5008 -
# 'Labels_window.txt': 3586 -
# 'Labels_water.txt': 2672 +...
# 'Labels_flowers.txt': 2528 +++
# 'Labels_food.txt': 2246 +++
# 'Labels_toy.txt': 1927 - 
# 'Labels_grass.txt': 1808 .. 
# 'Labels_clouds.txt': 1784 - 
# 'Labels_plants.txt': 1741 +
# 'Labels_buildings.txt': 1482 +++
# 'Labels_road.txt': 1200
# 'Labels_sign.txt': 767
# 'Labels_snow.txt': 615
# 'Labels_tree.txt': 516
# 'Labels_vehicle.txt': 500
# 'Labels_nighttime.txt': 468
# 'Labels_rocks.txt': 452
# 'Labels_statue.txt': 420
# 'Labels_leaf.txt': 417
# 'Labels_temple.txt': 407
# 'Labels_computer.txt': 375
# 'Labels_military.txt': 334
# 'Labels_fire.txt': 301
# 'Labels_wedding.txt': 289
# 'Labels_book.txt': 286
# 'Labels_sand.txt': 253
# 'Labels_street.txt': 246
# 'Labels_tower.txt': 217
# 'Labels_plane.txt': 208
# 'Labels_ocean.txt': 203

# Label counts for images with 1 or 2 labels:
# 'Labels_person.txt': 41639 +
# 'Labels_sky.txt': 15358
# 'Labels_animal.txt': 13996 +
# 'Labels_water.txt': 6947
# 'Labels_flowers.txt': 5900 + 
# 'Labels_window.txt': 5185
# 'Labels_grass.txt': 4530
# 'Labels_buildings.txt': 4252 + 
# 'Labels_road.txt': 2633
# 'Labels_food.txt': 2246 +
# 'Labels_plants.txt': 2045
# 'Labels_toy.txt': 1998
# 'Labels_birds.txt': 1884+
# 'Labels_clouds.txt': 1866
# 'Labels_rocks.txt': 1247
# 'Labels_tree.txt': 1082
# 'Labels_leaf.txt': 1018
# 'Labels_vehicle.txt': 887
# 'Labels_sign.txt': 816
# 'Labels_ocean.txt': 803












