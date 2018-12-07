import numpy as np
from argparse import ArgumentParser
import pickle
from collections import Counter

def read_embedding_file(input_file, labels):
	id_to_embed = {}
	embed_labels = [] #tuples of (embed, label)
	embed_size = None
	with open(input_file, 'r') as ef:
		line_count = 0
		for line in ef:
			if not line.startswith('#'):
				content = line.split()
				image_id, embedding = content[0], [float(elem) for elem in content[1:]]
				if embed_size is None:
					embed_size = len(embedding)
					print("embed_size is {}".format(embed_size))
				else:
					assert(embed_size == len(embedding))

				if image_id in labels:
					id_to_embed[image_id] = embedding
				line_count += 1

		print("number of embeddings {}".format(line_count))
		return id_to_embed

	for image_id in id_to_embed:
		embed_labels.append((id_to_embed[image_id], labels[image_id]))
		output_labels.append(labels[image_id])

	print(Counter(output_labels, most_common=True)
	print("embed_labels length {}".format(len(embed_labels)))

	pickle.dump(open(args.dataset_file, 'wb'), embed_labels))

if __name__ == '__main__':
	parser = ArgumentParser(description='generate image dataset of embeddings')
	parser.add_argument('-embed_file', '--embed_file')
	parser.add_argument('--label_file', '-label_file', 
	                    help='labels')
	parser.add_argument('--dataset_file', '-dataset_file', 
	                    help='labels')
	parser.add_argument('-concat_file', '--concat_file')

	args = parser.parse_args()
	labels = pickle.load(open(args.label_file, 'rb'))
	print("number of labels {}".format(len(labels)))
	print(Counter(labels.values(), most_common=True))
	id_to_embed = read_embedding_file(args.embed_file, labels)
	output_labels = []

    	






