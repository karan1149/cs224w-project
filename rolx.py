import argparse
import snap
from collections import defaultdict
def write_concat_file(embeddings, output_name):
	with open(output_name, 'w') as f:
		for elem in embeddings:
			embeddings[elem] = [str(x) for x in embeddings[elem]]
			embed_string = " ".join(embeddings[elem])
			f.write(str(elem) + " " + embed_string + "\n")

def get_embeddings(embed_file):
	embeddings = defaultdict(list)
	with open(embed_file, 'r') as f:
		for line in f:
			content = line.split()
			image_id, embedding = int(content[0]), [float(elem) for elem in content[1:]]
			embeddings[image_id] = embedding

	return embeddings

def get_neighbors(edge_list):
	neighbors = defaultdict(set)
	with open(edge_list, 'r') as f:
		for line in f:
			content = line.split()
			src, dest = content[0], content[1]
			neighbors[int(src)].add(int(dest))
			neighbors[int(dest)].add(int(src))


	return neighbors

def rolx(cur_embeddings, neighbors, num_iters):
	for i in range(num_iters):
		new_embeddings = defaultdict(list)
		for image_id in cur_embeddings:
			nbrs = neighbors[image_id]
			nbrs_embed = [cur_embeddings[nbr] for nbr in nbrs]
			mean_nbrs = [sum(x)/len(nbrs) for x in zip(*nbrs_embed)]
			new_embeddings[image_id] = cur_embeddings[image_id] + mean_nbrs
			#print(len(new_embeddings[image_id]))
			assert(len(new_embeddings[image_id]) == 2 * len(cur_embeddings[image_id]))

		cur_embeddings = new_embeddings

	return cur_embeddings

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Compare two sets of embeddings.')

	parser.add_argument('--embedding_file', help='Path to embedding file.')
	parser.add_argument('--num_iters', type=int, default=2, help='number of iterations to run Rolx')
	parser.add_argument('--edge_list', help='Path to edge edge_list')
	parser.add_argument('--output_name', help='output_file_name')

	args = parser.parse_args()
	neighbors = get_neighbors(args.edge_list)
	embeddings = get_embeddings(args.embedding_file)
	final_embeddings = rolx(embeddings, neighbors, args.num_iters)
	write_concat_file(final_embeddings, args.output_name)


		







