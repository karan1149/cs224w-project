import numpy as np
import snap


def remap_nodes(content, unique):
	nid = 0
	node_map = {} #maps original ids from 0 to num_nodes
	for elem in unique:
		node_map[elem] = nid
		nid += 1

	with open('flickrEdgesSmall_remapped.txt', 'w') as nf:
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

def generate_subgraph():
	G = snap.LoadEdgeList(snap.PUNGraph, 'flickrEdges.txt', 0, 1)
	sub_graph = snap.GetRndSubGraph(G, 15000)
	snap.SaveEdgeList(sub_graph, 'flickr_subgraph.txt')

if __name__ == '__main__':
	# generate_subgraph()
	#### read in original edge list to create node mappings to generate files
	with open('flickrEdgesSmall.txt', 'r') as f:
			content = f.readlines()
			content = [x.strip().split() for x in content if not x.startswith('#')]
			flat = [int(item) for sublist in content for item in sublist]
			unique = list(set(flat))
			unique.sort()
			remap_nodes(content, unique)

			#remap_nodes
			#generate_embedding_file(content, unique, "node2vec_subgraph_")
		
	# with open('flickrEdges.txt', 'r') as f:
	# 		content = f.readlines()
	# 		old_edges = set()
	# 		content = [x.strip() for x in content]
	# 		for edge in content:
	# 			old_edges.add(edge)

	# 		print(len(old_edges))
	# 		print(old_edges)
	# 		new_edges = [] #with weights
	# 		with open('edgeFeaturesNUS.txt') as nus:
	# 			nus.next() #skip initial line
	# 			for line in nus:
	# 				split_line = line.split()
	# 				nodes = split_line[:2]
	# 				cur_edge = " ".join(nodes)
	# 				if cur_edge in old_edges:
	# 					weights = split_line[2:]
	# 					weights = [int(x) for x in weights]
	# 					edge_weight = sum(weights)
	# 					new_edges.append((cur_edge, edge_weight))



	# 		#print(new_edges)
	# 		print(len(new_edges))

		
		









