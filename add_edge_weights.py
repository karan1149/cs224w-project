import argparse

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Add edge weights to an edgelist.')

	parser.add_argument('input_edges_filename', help='Path to input edge file.')
	parser.add_argument('output_edges_filename', help='Path to output edge file.')
	parser.add_argument('edge_features_filename', help='Path to edge features file.')

	args = parser.parse_args()

	input_edges = set()

	with open(args.input_edges_filename, 'r') as f:
		for line in f:
			if line.startswith('#'):
				continue
			left_node, right_node = line.split()
			assert((left_node, right_node) not in input_edges)
			assert((right_node, left_node) not in input_edges)
			assert(left_node != right_node)

			input_edges.add((left_node, right_node))
	print("%d edges found in input file..." % len(input_edges))

	found = 0
	not_found = 0
	total = 0
	seen = set()
	with open(args.output_edges_filename, 'w') as w:
		with open(args.edge_features_filename, 'r') as r:
			for line in r:
				tokens = line.split()
				if len(tokens) == 2:
					print("Skipping first line...")
					continue
				assert(len(tokens) == 9)

				left_node, right_node = tokens[:2]

				assert((left_node, right_node) not in seen)
				seen.add((left_node, right_node))
				if (left_node, right_node) in input_edges:
					nodes_string = left_node + ' ' + right_node
					found += 1
				elif (right_node, left_node) in input_edges:
					nodes_string = right_node + ' ' + left_node
					found += 1
				else:
					not_found += 1
					continue

				weight = 1 + sum(int(i) for i in tokens[2:])

				w.write(nodes_string + ' ' + str(weight) + '\n')
	print("%d lines in edge features found, %d not found" % (found, not_found))



