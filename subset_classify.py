import os

base_command = "python generate_dataset.py --embed_file %s --label_file %s --dataset_file %s && python classify.py --data_path %s | tee %s"

resnet_path = "embeddings/resnet18_embeddings.txt"
node2vec_path = "embeddings/node2vec_person_animal_plant_embedding_q0.01.txt"

for i in range(2, 13):
	resnet_dataset_path = "classification_datasets/person_animal_plant_subset_" + str(i) + "_resnet18.pkl"
	curr_command = base_command % (resnet_path, "subsets/person_animal_plant_popular_" + str(i) + "_labels.txt", resnet_dataset_path, resnet_dataset_path, "subsets/results/resnet_" + str(i) + '.txt')
	print(curr_command + '\n')
	os.system(curr_command)

	node2vec_dataset_path = "classification_datasets/person_animal_plant_subset_" + str(i) + "_node2vec_q_0_01.pkl"
	curr_command = base_command % (node2vec_path, "subsets/person_animal_plant_popular_" + str(i) + "_labels.txt", node2vec_dataset_path, node2vec_dataset_path, "subsets/results/node2vec_" + str(i) + '.txt')
	print(curr_command + '\n')
	os.system(curr_command)


