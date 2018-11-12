import numpy as np

def remap_nodes(content, unique):
	nid = 0
	node_map = {} #maps original ids from 0 to num_nodes
	for elem in unique:
		node_map[elem] = nid
		nid += 1

	with open('flickrEdges_remapped.txt', 'w') as nf:
		for elem in content:
			nf.write("{} {}\n".format(node_map[int(elem[0])], node_map[int(elem[1])]))

def generate_embedding_file(content, unique, embed_prefix):
	node_map = {} #maps 0 to num_nodes to original ids
	nid = 0
	for elem in unique:
		node_map[nid] = elem
		nid += 1

	embeddings = np.load("{}_embedding.dat".format(embed_prefix))
	with open("{}_embed_file".format(embed_prefix), 'w') as f:
		for nid in range(len(unique)):
			orig_id = str(node_map[nid])
			embed_vector = embeddings[nid]
			embed_string = " ".join([str(elem) for elem in embed_vector])
			f.write(orig_id + " " + embed_string + "\n")


if __name__ == '__main__':
	#### read in original edge list to create node mappings to generate files
	with open('flickrEdges.txt', 'r') as f:
		content = f.readlines()
		content = [x.strip().split() for x in content]
		flat = [int(item) for sublist in content for item in sublist]
		unique = list(set(flat))
		unique.sort()

		#remap_nodes
		generate_embedding_file(content, unique, "sdne")
		
