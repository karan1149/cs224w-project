import argparse
import pickle
import sklearn
from sklearn.neural_network import MLPClassifer
from collections import Counter

if __name__=='__main__':

	parser = argparse.ArgumentParser(description='Run classification on a dataset.')
	parser.add_argument('train_path',
	                    help='Path to train pkl file. Should be an array of pairs to train on.')
	parser.add_argument('test_path',
	                    help='Path to test pkl file. Should be an array of pairs.')

	args = parser.parse_args()

	with open(args.train_path, 'rb') as f:
		train_data = pickle.load(f)

	with open(args.test_path, 'rb') as f:
		test_data = pickle.load(f)

	train_data_x, train_data_y = zip(*train_data)
	test_data_x, test_data_y = zip(*test_data)

	assert(len(train_data_x[0]) == len(train_data_y[0]))

	print("Dimensionality of train %d" % len(train_data_x[0]))

	clf = MLPClassifer(hidden_layer_size=(100,), verbose=True)

	print("Classes found in training data:")
	print(Counter(train_data_y, most_common=True))

	print("Classes found in test data:")
	print(Counter(test_data_y, most_common=True))

	print("Fitting on training data...")
	clf.fit(train_data_x, train_data_y)

	train_accuracy = clf.score(train_data_x, train_data_y)
	print("Train accuracy: %f" % train_accuracy)

	test_accuracy = clf.score(test_data_x, test_data_y)
	print("Test accuracy: %f" % test_accuracy)

