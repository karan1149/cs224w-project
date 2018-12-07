import numpy as np
from argparse import ArgumentParser
import pickle
from collections import Counter

def read_embedding_file(input_file, labels):
	print("Reading embedding file %s..." % input_file)
	id_to_embed = {}
	embed_size = None
	with open(input_file, 'r') as ef:
		line_count = 0
		for line in ef:
			if not line.startswith('#'):
				content = line.split()
				image_id, embedding = content[0], [float(elem) for elem in content[1:]]
				if embed_size is None:
					embed_size = len(embedding)
					print("Embed size is {}...".format(embed_size))
				else:
					assert(embed_size == len(embedding))

				if image_id in labels:
					id_to_embed[image_id] = embedding
				line_count += 1

		print("Number of embeddings found is {}...".format(line_count))
		return id_to_embed

if __name__ == '__main__':
	parser = ArgumentParser(description='generate image dataset of embeddings')
	parser.add_argument('-embed_file', '--embed_file')
	parser.add_argument('--label_file', '-label_file', 
	                    help='labels')
	parser.add_argument('--dataset_file', '-dataset_file', 
	                    help='labels')
	parser.add_argument('-concat_file', '--concat_file')

	args = parser.parse_args()

	labels = {}
	with open(args.label_file, 'r') as f:
		for line in f:
			image_id, label_str = line.split()
			labels[image_id] = int(label_str)

	print("Total number of labels in label file {}...".format(len(labels)))
	print("Distribution of loaded labels:")

	print(Counter(labels.values()).most_common())

	id_to_embed = read_embedding_file(args.embed_file, labels)
	if args.concat_file:
		id_to_embed_concat = read_embedding_file(args.concat_file, labels)
	output_labels = []
	embed_labels = [] #tuples of (embed, label)

	skipped_due_to_concatenation = 0

	for image_id in id_to_embed:
		if args.concat_file and image_id not in id_to_embed_concat:
			skipped_due_to_concatenation += 1
			continue
		embedding = id_to_embed[image_id]
		if args.concat_file:
			embedding = embedding + id_to_embed_concat[image_id]
		embed_labels.append((embedding, labels[image_id]))
		output_labels.append(labels[image_id])

	print("Distribution of labels in dataset:")
	print(Counter(output_labels).most_common())
	print("Number of tuples in dataset is {}".format(len(embed_labels)))
	print("Dimensionality of embeddings in dataset is %d..." % len(embed_labels[0][0]))
	if args.concat_file:
		print("Number of tuples skipped due to concatenation file is %d" % skipped_due_to_concatenation)

	pickle.dump(embed_labels, open(args.dataset_file, 'wb'))

    
