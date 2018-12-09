# import snap
from matplotlib import pyplot as plt
import numpy as np


def get_adj_matrix(labels_file, edges_file):
  image_ids = [{}, {}] # index 0 = person, index 1 = animal
  num_images = [0, 0] # index 0 = person, index 1 = animal

  with open(labels_file, 'r') as f:
    for line in f:
      assert(len(line.split()) == 2)
      image_id, label = line.split()[0], int(line.split()[1])
      image_ids[label][image_id] = num_images[label]
      num_images[label] += 1

  for image_id, new_id in image_ids[1].items():
    image_ids[1][image_id] = new_id + num_images[0]

  print("Creating combined map to new ordered ids... ")
  person_ids, animal_ids = image_ids
  combined_id_map = {**person_ids, **animal_ids}

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
  plt.savefig('visualize_person_animal_sbm_5000.png', dpi=1000)
  plt.clf()


get_adj_matrix('person_animal_labels.txt', 'person_animal_edges.txt')

def compute_clustering_coeff(edges_file):
  G = snap.LoadEdgeList(snap.PUNGraph, edges_file, 0, 1)
  clustering_coeff = snap.GetClustCf(G, 1000)
  print("clustering_coeff of %s subgraph: %f" % (edges_file[:edges_file.find('.')], clustering_coeff))

# compute_clustering_coeff('person_animal_edges.txt')
