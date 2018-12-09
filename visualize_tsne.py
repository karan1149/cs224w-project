from argparse import ArgumentParser
from compute_embedding_similarity import populate_embedding_map
from generate_dataset import populate_label_map
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import random
import numpy as np

if __name__=="__main__":
	parser = ArgumentParser(description='Generate visualization of graph')
	parser.add_argument('-embed_file', '--embed_file', help='Embedding txt file', required=True)
	parser.add_argument('--label_file', '-label_file', 
	                    help='Labels txt', required=True)
	parser.add_argument('--output_file', '-output_file', required=True)
	parser.add_argument('--samples', type=int, help="Number of elements to sample from embeddings.")
	parser.add_argument('--title', help="Title for the plot")
	parser.add_argument('--labels', help="Comma-separated labels")

	args = parser.parse_args()

	embedding_map = {}

	populate_embedding_map(args.embed_file, embedding_map)
	print("Number of embeddings found is %d" % len(embedding_map))

	labels = {}

	populate_label_map(args.label_file, labels)
	print("Number of labels found is %d" % len(labels))

	intersection_ids = list(set(embedding_map.keys()).intersection(set(labels.keys())))

	print("Number of images in intersection is %d" % len(intersection_ids))

	if args.samples and len(intersection_ids) > args.samples:
		print("Samping %d nodes..." % args.samples)
		intersection_ids = random.sample(intersection_ids, args.samples)


	intersection_labels = [labels[image_id] for image_id in intersection_ids]
	max_label = max(intersection_labels)

	print("Max label found is %d" % max_label)
	print("Assuming labels are sequential...")

	embedding_X = [embedding_map[image_id] for image_id in intersection_ids]

	tsne = TSNE(n_components=2, random_state=0)

	embedding_2d = tsne.fit_transform(embedding_X)

	colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'w', 'orange', 'purple']

	labels = [str(i) for i in range(max_label + 1)]

	if args.labels:
		labels = args.labels.split(',')

	for i in range(max_label + 1):
		mask = np.array([x == i for x in intersection_labels], dtype=bool)
		plt.scatter(embedding_2d[mask, 0], embedding_2d[mask, 1], c=colors[i], label=labels[i], s=4)

	if args.title:
		plt.title(args.title)

	plt.legend()
	plt.savefig(args.output_file)


