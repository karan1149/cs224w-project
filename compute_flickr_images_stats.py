import os
import pickle

def compute_flickr_edges_stats(edges_node_ids):
    num_self_edges = 0
    with open('data/flickrEdges.txt', 'r') as f:
        for line in f:
            if line.startswith("#"):
                continue
            left_node, right_node = line.split()
            edges_node_ids.add(left_node)
            edges_node_ids.add(right_node)
            if left_node == right_node:
                num_self_edges += 1
    print("%d self edges" % num_self_edges)
    print("%d nodes in edges" % len(edges_node_ids))

def compute_nus_edges_stats(nus_node_ids):
    num_self_edges = 0
    with open('data/edgeFeaturesFlickr/edgeFeaturesNUS.txt', 'r') as f:
        for line in f:
            if line.startswith("#"):
                continue
            if len(line.split()) == 2:
                continue
            left_node, right_node = line.split()[:2]

            nus_node_ids.add(left_node)
            nus_node_ids.add(right_node)
            if left_node == right_node:
                num_self_edges += 1
    print("%d self edges in nus" % num_self_edges)
    print("%d nodes in edges in nus" % len(nus_node_ids))

def compute_flickr_images_stats(images_node_ids):
    directory = 'data/flickr_images'
    subdirs = os.listdir(directory)
    num_categories = 0
    for subdir in subdirs:
      subdir_path = os.path.join(directory, subdir)
      if not os.path.isdir(subdir_path):
        continue
      num_categories += 1
      images = os.listdir(subdir_path)
      images = [img for img in images if '.jpg' in img]

      for image_name in images:
        img_id = image_name[:-4].split('_')[1]
        assert(image_name[:-4].split('_'))
        images_node_ids.add(img_id)

    print("%d categories of images" % num_categories)
    print("%d nodes in images" % len(images_node_ids))


if __name__=='__main__':
    edges_node_ids = set()
    images_node_ids = set()
    nus_node_ids = set()

    compute_flickr_edges_stats(edges_node_ids)
    compute_nus_edges_stats(nus_node_ids)
    compute_flickr_images_stats(images_node_ids)

    print("%d nodes in the intersection of images and edges" % len(edges_node_ids.intersection(images_node_ids)))
    print("%d nodes in the intersection of images and nus" % len(nus_node_ids.intersection(images_node_ids)))

    print("Now saving relevant nodes in the flickrEdges.txt file that have images")
    relevant_nodes = edges_node_ids.intersection(images_node_ids)

    with open('data/relevant_nodes_set.pkl', 'wb') as f:
        pickle.dump(relevant_nodes, f)
