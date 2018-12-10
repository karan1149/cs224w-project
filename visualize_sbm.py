# import snap
from matplotlib import pyplot as plt
import numpy as np


def get_adj_matrix(labels_file, edges_file, num_classes, smb_file):
  image_ids = [{} for _ in range(num_classes)] # index 0 = person, index 1 = animal
  num_images = [0 for _ in range(num_classes)] # index 0 = person, index 1 = animal

  with open(labels_file, 'r') as f:
    for line in f:
      assert(len(line.split()) == 2)
      image_id, label = line.split()[0], int(line.split()[1])
      image_ids[label][image_id] = num_images[label]
      num_images[label] += 1

  num_images_in_prev_classes = 0
  for i in range(1, num_classes):
    num_images_in_prev_classes += num_images[i-1]
    for image_id, new_id in image_ids[i].items():
      image_ids[i][image_id] = new_id + num_images_in_prev_classes

  print("Creating combined map to new ordered ids... ")
  combined_id_map = {}
  for image_id_map in image_ids:
    combined_id_map.update(image_id_map)

  print("Creating adjacency matrix...")
  A = np.ones((sum(num_images), sum(num_images)))

  # G = snap.LoadEdgeList(snap.PUNGraph, edges_file, 0, 1)
  # for edge in G.Edges
  with open(edges_file, 'r') as f:
    for line in f:
      assert(len(line.split()) == 2)
      node1, node2 = line.split()
      id1, id2 = combined_id_map[node1], combined_id_map[node2]
      A[id1][id2] = 0
      A[id2][id1] = 0

  plt.imshow(A, cmap='binary')
  plt.savefig(smb_file, dpi=1000)
  plt.clf()


get_adj_matrix('person_animal_plant_labels.txt', 'person_animal_plant_edges.txt', 3, 'visualize_person_animal_plant_sbm_1000.png')

def compute_clustering_coeff(edges_file):
  G = snap.LoadEdgeList(snap.PUNGraph, edges_file, 0, 1)
  clustering_coeff = snap.GetClustCf(G, 1000)
  print("clustering_coeff of %s subgraph: %f" % (edges_file[:edges_file.find('.')], clustering_coeff))

# compute_clustering_coeff('person_animal_edges.txt')
