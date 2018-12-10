from collections import defaultdict
from collections import Counter
import os
import argparse
import operator
import random

def get_images_per_class():
  images = []

  with open('data/ImageList/ImageList.txt', 'r') as f:
    for line in f:
      images.append(line[line.rfind('_')+1:].strip())

  labels_dir = 'data/Groundtruth/AllLabels'
  labels_files = [name for name in os.listdir(labels_dir) if name.endswith('.txt') ]

  # print("Num labels is %d" % len(labels_files))

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

  animal_classes = set(['animal', 'birds', 'dog', 'cat', 'horses', 'fish', 'elk', 'cow', 'tiger', 'fox', 'whales', 'zebra'])
  plant_classes = set(['plants', 'flowers', 'tree', 'leaf', 'coral'])
  building_classes = set(['buildings', 'house', 'tower', 'temple'])
  scenery_classes = set(['sunset', 'clouds', 'lake', 'ocean', 'valley', 'sun', 'cityscape', 'moon', 'waterfall', 'rainbow'])

  five_class_images = defaultdict(list)
  for image, labels in labels_per_image.items():
    image_id = image[:image.find('.')]
    if len(set(labels) & animal_classes) > 0:
      five_class_images[image_id].append('animal')
    if 'person' in labels:
      five_class_images[image_id].append('person')
    if len(set(labels) & plant_classes) > 0:
      five_class_images[image_id].append('plant')
    if len(set(labels) & building_classes) > 0:
      five_class_images[image_id].append('building')
    if len(set(labels) & scenery_classes) > 0:
      five_class_images[image_id].append('scenery')


  person_images = set([image_id for image_id in five_class_images if five_class_images[image_id] == ['person']])
  animal_images = set([image_id for image_id in five_class_images if five_class_images[image_id] == ['animal']])
  plant_images = set([image_id for image_id in five_class_images if five_class_images[image_id] == ['plant']])
  building_images = set([image_id for image_id in five_class_images if five_class_images[image_id] == ['building']])
  scenery_images = set([image_id for image_id in five_class_images if five_class_images[image_id] == ['scenery']])
  multiple_images = set([image_id for image_id in five_class_images if len(five_class_images[image_id]) > 1])

  print('Num only person images is %d' % len(person_images))
  print('Num only animal images is %d' % len(animal_images))
  print('Num only plant images is %d' % len(plant_images))
  print('Num only building images is %d' % len(building_images))
  print('Num only scenery images is %d' % len(scenery_images))
  print('Num multiple images is %d' % len(multiple_images))

  print('person: ', random.sample(person_images, 5))
  print('animal: ', random.sample(animal_images, 5))
  print('plant: ', random.sample(plant_images, 5))
  print('building: ', random.sample(building_images, 5))
  print('scenery: ', random.sample(scenery_images, 5))
  print('multiple: ', random.sample(multiple_images, 5))

  return [person_images, animal_images, plant_images, building_images, scenery_images]

def create_subgraph(images_per_class, output_edges_filename, output_labels_filename, pick_popular_nodes=False, threshold=0):
  # num_images_per_class = min(len(person_images), len(animal_images))
  # person_images = random.sample(person_images, num_images_per_class)
  # animal_images = random.sample(animal_images, num_images_per_class)

  nodes_to_include = set()
  for images in images_per_class:
    nodes_to_include = nodes_to_include.union(images)

  # print('num_images_per_class', num_images_per_class)
  print('Number of total images in all classes = %d' % len(nodes_to_include)) # 84023 total person and animal images

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

  if pick_popular_nodes:
    node_degrees = defaultdict(int)
    for left_node, right_node in input_edges:
      if left_node in nodes_to_include and right_node in nodes_to_include:
        node_degrees[left_node] += 1
        node_degrees[right_node] += 1

    nodes_to_include = set([n for n, c in node_degrees.items() if c >= threshold])
    print("Number of popular nodes with degree %d or higher: %d" % (threshold, len(nodes_to_include)))

  edges_written = 0 
  nodes_added = set()
  with open(output_edges_filename, 'w') as f:
    for left_node, right_node in input_edges:
      if left_node in nodes_to_include and right_node in nodes_to_include:
        f.write(left_node + ' ' + right_node + '\n')
        edges_written += 1
        nodes_added.add(left_node)
        nodes_added.add(right_node)

  print("Induced graph has %d unique nodes with %d edges" % (len(nodes_added), edges_written))

  num_per_class = [len([node for node in nodes_added if node in images]) for images in images_per_class]
  print("Induced graph has " + str(num_per_class) + " images")
  # num_person = len([node for node in nodes_added if node in person_images])
  # num_animal = len([node for node in nodes_added if node in animal_images])
  # print("Induced graph has %d person images and %d animal images" % (num_person, num_animal))
  
  # Induced graph has 32899 unique nodes with 75742 edges
  # Induced graph has 18948 person images and 13951 animal images

  with open(output_labels_filename, 'w') as f:
    for node in nodes_added:
      label = '0'
      for idx, images in enumerate(images_per_class):
        if node in images:
          label = str(idx)
      f.write(node + ' ' + label + '\n')

if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Create a subgraph of specific classes.')

  parser.add_argument('output_edges_filename', help='Path to output edge file.')
  parser.add_argument('output_labels_filename', help='Path to output labels file.')
  parser.add_argument('--pick_popular_nodes', help='If passed, graph includes only the nodes with highest degree in input graph', action='store_true')
  # parser.add_argument('--threshold', help='If passed, graph is induced on only the nodes degree >= threshold', type=int)

  args = parser.parse_args()

  images = get_images_per_class()

  create_subgraph(images, args.output_edges_filename, args.output_labels_filename, args.pick_popular_nodes, 6)


######### FIVE CLASSES: PERSON, ANIMAL, PLANT, BUILDING, SCENERY #########
# Num only person images is 44507
# Num only animal images is 27524
# Num only plant images is 14868
# Num only building images is 9698
# Num only scenery images is 41755
# Num multiple images is 30882
# person:  ['406614736', '64521836', '576646360', '144923191', '462513389']
# animal:  ['268880929', '426050083', '267667783', '295891759', '1166195900']
# plant:  ['188588652', '1636020', '470965108', '313446417', '63251322']
# building:  ['318511913', '1932058673', '278447782', '2250534430', '2705545455']
# scenery:  ['171832451', '1083548335', '489039399', '819163623', '358051944']
# multiple:  ['2402924745', '201570088', '2614077241', '173274210', '353858116']
# Number of total images in all classes = 138352
# Number of popular nodes with degree 5 or higher: 26476
# Induced graph has 26474 unique nodes with 97206 edges
# Induced graph has [7075, 5890, 3253, 1662, 8594] images


######### SUBGRAPH STATISTICS FOR NODES WITH DEGREE ABOVE THRESHOLD #########
# THRESHOLD = 1 (DEGREES ARE 2 OR HIGHER)
# Number of popular nodes with degree above 1: 37813
# Induced graph has 37812 unique nodes with 107887 edges
# Induced graph has [17270, 12198, 8344] images

# THRESHOLD = 2 (DEGREES ARE 3 OR HIGHER)
# Number of popular nodes with degree above 2: 30079
# Induced graph has 30078 unique nodes with 92819 edges
# Induced graph has [13172, 10116, 6790] images

# THRESHOLD = 3 (DEGREES ARE 4 OR HIGHER)
# Number of popular nodes with degree above 3: 20756
# Induced graph has 20747 unique nodes with 66731 edges
# Induced graph has [8437, 7401, 4909] images

# THRESHOLD = 4 (DEGREES ARE 5 OR HIGHER)
# Number of popular nodes with degree above 4: 13473
# Induced graph has 13451 unique nodes with 42461 edges
# Induced graph has [5181, 4980, 3290] images

# THRESHOLD = 5 (DEGREES ARE 6 OR HIGHER)
# Number of popular nodes with degree above 5: 8835
# Induced graph has 8792 unique nodes with 25939 edges
# Induced graph has [3340, 3215, 2237] images

# THRESHOLD = 6 (DEGREES ARE 7 OR HIGHER)
# Number of popular nodes with degree above 6: 6447
# Induced graph has 6379 unique nodes with 17930 edges
# Induced graph has [2394, 2332, 1653] images

# Number of popular nodes with degree 8 or higher: 5023
# Induced graph has 4947 unique nodes with 13390 edges
# Induced graph has [1840, 1791, 1316] images

######### PERSON ANIMAL PLANTS ###############
# Num only person images is 49557
# Num only animal images is 31295
# Num only plant images is 21855
# Num multiple images is 4730
# person:  ['2234988534', '1294791520', '151969699', '265651015', '2264532142']
# animal:  ['184197341', '738946180', '406848538', '435526016', '2040069882']
# plant:  ['2488534064', '751873865', '2613199529', '334566577', '524677648']
# multiple:  ['495299325', '422997101', '152833664', '1522639939', '86847692']
# Number of total images in all classes: 102707
# Induced graph has 42174 unique nodes with 112229 edges
# Induced graph has [19720, 13277, 9177] images

######### PERSON ANIMAL ############
# Num only person images is 50017
# Num only animal images is 34006
# Num both images is 1559
# ('person: ', ['279733730', '2315582981', '161634252', '2678358533', '1804881117'])
# ('animal: ', ['2689553007', '2308672664', '2649004764', '2742179333', '2449263849'])
# ('both: ', ['2738469546', '710427749', '2539263822', '556965755', '283590026'])
# 84023
# Induced graph has 32899 unique nodes with 75742 edges
# Induced graph has 18948 person images and 13951 animal images



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












