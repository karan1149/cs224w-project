import argparse
import pickle
import sklearn
from sklearn.neural_network import MLPClassifier
from collections import Counter
from sklearn.metrics import confusion_matrix

if __name__=='__main__':

	parser = argparse.ArgumentParser(description='Run classification on a dataset.')
	parser.add_argument('--data_path', help="Path to full dataset. If provided, 90 percent used for train and 10 percent used for test. Other flags must be empty.")
	parser.add_argument('--train_path',
	                    help='Path to train pkl file. Should be an array of pairs to train on.')
	parser.add_argument('--test_path',
	                    help='Path to test pkl file. Should be an array of pairs.')

	args = parser.parse_args()

	if args.data_path:
		with open(args.data_path, 'rb') as f:
			data = pickle.load(f)
		train_data = data[:int(len(data) * .9)]
		test_data = data[int(len(data) * .9):]
		assert(not args.train_path and not args.test_path)
	else:
		with open(args.train_path, 'rb') as f:
			train_data = pickle.load(f)

		with open(args.test_path, 'rb') as f:
			test_data = pickle.load(f)

	print("Loaded data...")
	print("Training examples: %d, test examples: %d" % (len(train_data), len(test_data)))

	train_data_x, train_data_y = zip(*train_data)
	test_data_x, test_data_y = zip(*test_data)

	assert(len(train_data_x[0]) == len(test_data_x[0]))

	print("Dimensionality of embeddings %d" % len(train_data_x[0]))

	clf = MLPClassifier(hidden_layer_sizes=(100,), verbose=True, early_stopping=True)

	print("Classes found in training data:")
	print(Counter(train_data_y).most_common())

	print("Classes found in test data:")
	print(Counter(test_data_y).most_common())

	print("Fitting on training data...")
	clf.fit(train_data_x, train_data_y)

	train_accuracy = clf.score(train_data_x, train_data_y)
	print("Train accuracy: %f" % train_accuracy)

	test_accuracy = clf.score(test_data_x, test_data_y)
	print("Test accuracy: %f" % test_accuracy)

	print("Train confusion matrix:")
	train_pred = clf.predict(train_data_x)
	print(confusion_matrix(train_data_y, train_pred))

	print("Test confusion matrix:")
	test_pred = clf.predict(test_data_x)
	print(confusion_matrix(test_data_y, test_pred))

