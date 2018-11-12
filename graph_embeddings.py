import matplotlib.pyplot as plt
from time import time

from gem.utils      import graph_util, plot_util
from gem.evaluation import visualize_embedding as viz
from gem.evaluation import evaluate_graph_reconstruction as gr

from gem.embedding.hope     import HOPE
from gem.embedding.node2vec import node2vec
from gem.embedding.sdne     import SDNE
from argparse import ArgumentParser


if __name__ == '__main__':
    ''' Sample usage
    python run_karate.py -node2vec 1
    '''
    parser = ArgumentParser(description='Graph Embedding Experiments on Flickr Graph')
    parser.add_argument('-node2vec', '--node2vec', action='store_true',
                        help='whether to run node2vec')
    parser.add_argument('--hope', '-hope', action='store_true',
                        help='whether to run HOPE')
    parser.add_argument('--sdne', '-sdne', action='store_true',
                        help='whether to run SDNE')
    
    args = parser.parse_args()

    # File that contains the edges. Format: source target
    # Optionally, you can add weights as third column: source target weight
    edge_f = 'flickrEdges_remapped.txt'
    # Specify whether the edges are directed
    isDirected = False

    # Load graph
    G = graph_util.loadGraphFromEdgeListTxt(edge_f, directed=isDirected)

    models = []
    # Load the models you want to run
    if args.hope:
        models.append(HOPE(d=2, beta=0.01))

    if args.node2vec:
        models.append(
            node2vec(d=128, max_iter=1, walk_len=80, num_walks=10, con_size=10, ret_p=1, inout_p=5)
        )

    if args.sdne:
        models.append(SDNE(d=128, beta=10, alpha=.2, nu1=1e-6, nu2=1e-6, K=3,n_units=[50, 15,], rho=0.3, n_iter=1, xeta=0.01,n_batch=200,
                        modelfile=['enc_model.json', 'dec_model.json'],
                        weightfile=['enc_weights.hdf5', 'dec_weights.hdf5']))

    # For each model, learn the embedding and evaluate on graph reconstruction and visualization
    for embedding in models:
        print ('Num nodes: %d, num edges: %d' % (G.number_of_nodes(), G.number_of_edges()))
        t1 = time()
        # Learn embedding - accepts a networkx graph or file with edge list
        Y, t = embedding.learn_embedding(graph=G, edge_f=None, is_weighted=False, no_python=True)
        print (embedding._method_name+':\n\tTraining time: %f' % (time() - t1))
        print(Y)
        Y.dump("sdne_embedding.dat")
        # Evaluate on graph reconstruction
        # MAP, prec_curv, err, err_baseline = gr.evaluateStaticGraphReconstruction(G, embedding, Y, None)
        # #---------------------------------------------------------------------------------
        # print(("\tMAP: {} \t preccision curve: {}\n\n\n\n"+'-'*100).format(MAP,prec_curv[:5]))
        # #---------------------------------------------------------------------------------
        # Visualize
        # viz.plot_embedding2D(embedding.get_embedding(), di_graph=G, node_colors=None)
        # plt.show()
        # plt.clf()
