# Computes the correlation for similarity between random pairs of images for two different
# sets of embeddings. Embeddings files must have the following space-separated format for each line:
# image_id 0.23 -1.2 4.5 6.7... 5.6\n
import argparse
import random
from scipy.spatial.distance import cosine
from scipy.stats import spearmanr
from scipy.stats import pearsonr
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

def get_total_lines(embedding_file):
	lines = 0
	with open(embedding_file, 'r') as f:
		for line in f:
			lines += 1
	return lines

def populate_embedding_map(embedding_file, embedding_map):
	print("Populating embedding map from %s..." % embedding_file)
	values_size = -1
	with open(embedding_file, 'r') as file:
		for line in tqdm(file, total=get_total_lines(embedding_file)):
			tokens = line.split()
			values = [float(num) for num in tokens[1:]]

			# Ensure all embeddings in a file are of the same size.
			assert(values_size == -1 or values_size == len(values))
			if values_size == -1:
				values_size = len(values)
			values_size = len(values)

			embedding_map[tokens[0]] = values
	print("Dimensionality of embeddings is %d..." % values_size)

def get_file_basename(filename):
	return os.path.splitext(os.path.basename(filename))[0]

def get_file_title(filename):
	return os.path.splitext(os.path.basename(filename))[0].replace("_", " ").title()

def compute_embedding_similarity(embedding_file1, embedding_file2, samples=10000):
	print("Computing similarity for files %s and %s using %d samples..." % (embedding_file1, embedding_file2, samples))
	embeddings1 = {}
	embeddings2 = {}

	populate_embedding_map(embedding_file1, embeddings1)
	populate_embedding_map(embedding_file2, embeddings2)

	print("Finished populating embedding maps. Now sampling...")

	if sorted(embeddings1.keys()) != sorted(embeddings2.keys()):
		print("WARNING: Keys are not the same for embeddings")
		print("Embedding file 1 has %d ids" % len(embeddings1.keys()))
		print("Embedding file 2 has %d ids" % len(embeddings2.keys()))
		embeddings1_ids = set(embeddings1.keys())
		embeddings2_ids = set(embeddings2.keys())
		ids = list(embeddings1_ids.intersection(embeddings2_ids))
		print("Embedding intersection has %d ids" % len(ids))
	else:
		ids = sorted(embeddings1.keys())
		print("Embedding has %d ids" % len(ids))

	similarities1 = []
	similarities2 = []

	for i in tqdm(range(samples)):
		id1 = random.choice(ids)

		while True:
			id2 = random.choice(ids)
			if id2 != id1:
				break

		similarities1.append(min(max(cosine(embeddings1[id1], embeddings1[id2]), 0), 1))
		similarities2.append(min(max(cosine(embeddings2[id1], embeddings2[id2]), 0), 1))

	assert(len(similarities1) == len(similarities2) and len(similarities1) == samples)

	pearson = pearsonr(np.asarray(similarities1), np.asarray(similarities2))
	spearman = spearmanr(np.asarray(similarities1), np.asarray(similarities2))

	print("Pearson correlation: %f" % pearson[0])
	print("Spearman correlation: %f" % spearman[0])

	plt.scatter(similarities1, similarities2, s=1)
	plt.title("Distances of " + get_file_title(embedding_file1) + " vs. " + get_file_title(embedding_file2))
	plt.xlabel("Distance according to " + get_file_title(embedding_file1))
	plt.ylabel("Distance according to " + get_file_title(embedding_file2))
	leg1 = Rectangle((0, 0), 0, 0, alpha=0.0)
	plt.legend([leg1], ['Pearson = %.3f\nSpearman = %.3f' % (pearson[0], spearman[0])], handlelength=0)
	plt.savefig('plots/' + get_file_basename(embedding_file1) + "__" + get_file_basename(embedding_file2) + '.png')

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Compare two sets of embeddings.')

	parser.add_argument('embedding_file1', help='Path to first embedding file.')
	parser.add_argument('embedding_file2', help='Path to second embedding file.')
	parser.add_argument('--samples', help='Number of samples to run in computing similarity. Default 10,000.', type=int, default=10000)

	args = parser.parse_args()

	compute_embedding_similarity(args.embedding_file1, args.embedding_file2, samples=args.samples)