# Computes the correlation for similarity between random pairs of images for two different
# sets of embeddings. Embeddings files must have the following space-separated format for each line:
# image_id 0.23 -1.2 4.5 6.7... 5.6\n
import argparse
import random
from scipy.spatial.distance import cosine
from scipy.stats import spearmanr
from scipy.stats import pearsonr
import numpy as np

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

def compute_embedding_similarity(embedding_file1, embedding_file2, samples=10000):
	print("Computing similarity for files %s and %s using %d samples..." % (embedding_file1, embedding_file2, samples))
	embeddings1 = {}
	embeddings2 = {}

	populate_embedding_map(embedding_file1, embeddings1)
	populate_embedding_map(embedding_file2, embeddings2)

	assert(sorted(embeddings1.keys()) == sorted(embeddings2.keys()))

	ids = sorted(embeddings1.keys())

	assert(len(embeddings1[ids[0]]) == len(embeddings1[ids[0]]))

	similarities1 = []
	similarities2 = []

	for i in range(samples):
		id1 = random.choice(ids)

		while True:
			id2 = random.choice(ids)
			if id2 != id1:
				break

		similarities1.append(cosine(embeddings1[id1], embeddings1[id2]))
		similarities2.append(cosine(embeddings2[id1], embeddings2[id2]))

	assert(len(similarities1) == len(similarities2) and len(similarities1) == samples)

	pearson = pearsonr(np.asarray(similarities1), np.asarray(similarities2))
	spearman = spearmanr(np.asarray(similarities1), np.asarray(similarities2))

	print("Pearson correlation: %f" % pearson[0])
	print("Spearman correlation: %f" % spearman[0])

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Compare two sets of embeddings.')

	parser.add_argument('embedding_file1', help='Path to first embedding file.')
	parser.add_argument('embedding_file2', help='Path to second embedding file.')
	parser.add_argument('--samples', help='Number of samples to run in computing similarity. Default 10,000.', type=int, default=10000)

	args = parser.parse_args()

	compute_embedding_similarity(args.embedding_file1, args.embedding_file2, samples=args.samples)