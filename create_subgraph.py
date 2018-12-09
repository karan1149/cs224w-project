import os
import argparse
import random
from collections import defaultdict
import pickle

# Creates an induced subgraph from input_edges_filename with number of nodes
# equal to size. Note that some nodes may be isolated, so they might not show
# up in edge list.
def create_subgraph(input_edges_filename, output_edges_filename, size, pick_popular_nodes=False, relevant_nodes=None):
	print("Creating induced subgraph from %s, saving to %s, number of nodes is %d..." % (input_edges_filename, output_edges_filename, size))
	if pick_popular_nodes:
		print("Choosing subgraph based on degrees in original input graph...")
	input_edges = []
	input_nodes = set()

	node_degrees = defaultdict(int)

	self_edges = 0

	if relevant_nodes:
		with open(relevant_nodes, 'rb') as f:
			relevant_nodes_set = pickle.load(f)

		print("Loaded relevant nodes set with size %d..." % len(relevant_nodes_set))

	with open(input_edges_filename, 'r') as f:
		for line in f:
			if line.startswith('#'):
				continue

			assert(len(line.split()) == 2)
			left_node, right_node = line.split()

			assert(int(left_node) > 0)
			assert(int(right_node) > 0)
			input_edges.append((left_node, right_node))

			if relevant_nodes_set is None or left_node in relevant_nodes_set:
				input_nodes.add(left_node)
			if relevant_nodes_set is None or right_node in relevant_nodes_set:
				input_nodes.add(right_node)

			if left_node == right_node:
				self_edges += 1

			if args.pick_popular_nodes:
				node_degrees[left_node] += 1
				node_degrees[right_node] += 1

	input_nodes = list(input_nodes)

	if args.pick_popular_nodes:
		nodes_to_include = sorted([(c, n) for n, c in node_degrees.items()], reverse=True)[:size]

		input_nodes = [n for c, n in nodes_to_include]
	
	nodes_to_include = set(random.sample(input_nodes, size))

	assert(len(nodes_to_include) == size)
	print('Input graph has %d nodes and %d edges, including %d self-edges' % (len(input_nodes), len(input_edges), self_edges))

	if len(set(input_edges)) != len(input_edges):
		print('Warning: Input graph has %d unique edges. Some edges are dups' % len(set(input_edges)))

	edges_written = 0
	nodes_added = set()
	with open(output_edges_filename, 'w') as f:
		for left_node, right_node in input_edges:
			if left_node in nodes_to_include and right_node in nodes_to_include:
				f.write(left_node + ' ' + right_node + '\n')
				edges_written += 1
				nodes_added.add(left_node)
				nodes_added.add(right_node)

	print("Induced graph has %d unique nodes with %d edges" % (len(nodes_added), edges_written))

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Create a subgraph of a graph.')

	parser.add_argument('input_edges_filename', help='Path to input edge file.')
	parser.add_argument('output_edges_filename', help='Path to output edge file.')
	parser.add_argument('size', help='Size of subgraph.', type=int,)
	parser.add_argument('--pick_popular_nodes', help='If passed, graph includes only the nodes with highest degree in input graph', action='store_true')
	parser.add_argument('--relevant_nodes', help='Pickle file containing a list of nodes. Only these nodes will be included in final result.')

	args = parser.parse_args()

	create_subgraph(args.input_edges_filename, args.output_edges_filename, args.size, args.pick_popular_nodes, args.relevant_nodes)