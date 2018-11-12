from compute_embedding_similarity import populate_embedding_map
import argparse
from scipy.spatial.distance import cosine
import random
import operator
import pickle
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Find similar images by embeddings')

parser.add_argument('input_file', help='Input CNN embeddings txt file.')
parser.add_argument('--samples', type=int, default=10000, help='Number of samples to run.')

args = parser.parse_args()

embedding_map = {}
similarities_map = {}

populate_embedding_map(args.input_file, embedding_map)

with open('data/relevant_nodes_set.pkl', 'rb') as f:
	relevant_nodes = pickle.load(f)

ids = embedding_map.keys()
for i in tqdm(range(args.samples)):
  id1, id2 = random.sample(ids, 2)
  while id1 not in relevant_nodes or id2 not in relevant_nodes:
  	id1, id2 = random.sample(ids, 2)
  similarities_map[(id1, id2)] = cosine(embedding_map[id1], embedding_map[id2])

top10_pairs = sorted(similarities_map.items(), key=operator.itemgetter(1), reverse=False)[:10]
for ids, cosine_val in top10_pairs:
  print('MAX IDS: %s and %s (value = %s)' % (ids[0], ids[1], cosine_val))