import matplotlib.pyplot as plt

minimum_degrees = list(range(2, 6))

resnet_results = [0.946854, 0.947473, 0.956145, 0.946508]
node2vec_results = [0.671338, 0.689827, 0.716627, 0.723626]
concat_results = [0.946854, 0.952793, 0.959518, 0.951709]
sdne_results = [0.525648, 0.532912, 0.508916, 0.491828]
concat_node2vec_sdne = [0.687996, 0.704122, 0.732048, 0.748886]

# plt.plot(minimum_degrees, resnet_results, c='red', label="ResNet-18")
plt.plot(minimum_degrees, node2vec_results, c='blue', label="Node2Vec")
# plt.plot(minimum_degrees, concat_results, c='purple', label="Node2Vec + ResNet-18")
plt.plot(minimum_degrees, sdne_results, c='orange', label="SDNE")
plt.plot(minimum_degrees, concat_node2vec_sdne, c='brown', label='Node2Vec + SDNE')
plt.ylabel("Accuracy Score")
plt.xlabel("Minimum Node Degree")
plt.title("Classification Results on Person-Animal-Plant Subgraphs")
# plt.axhline(y=0.4, linestyle=':', color="green", label='Random Chance')
plt.legend()
plt.savefig('subsets/results/person_animal_plant_concat_node2vec_sdne_subgraphs.png')

