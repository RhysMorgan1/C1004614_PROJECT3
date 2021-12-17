import random
import sys
import os
import time
import argparse
from progress import Progress
import networkx as net

Graph = net.DiGraph()           ##creates new directed graph


def load_graph(args):
    """Load graph from text file
    Parameters:
    args -- arguments named tuple
    Returns:
    A dict mapling a URL (str) to a list of target URLs (str).
    """
    # Iterate through the file line by line
    for line in args.datafile:

        # And split each line into two URLs
        print(line)    ## USED FOR TESTING TO SEE WHAT LINE IS BEING PRINTED
        node, target = line.split()
        print(node)     ##USED FOR TESTING
        print(target)   ##USED FOR TESTING
        Graph.add_node(node)        ## ADDS NODE TO THE GRAPH
        Graph.add_node(target)      ## ADDS ANOTHER NODE TO THE GRAPH
        Graph.add_edges_from(node, target)      ##CREATES A DIRECTED EDGE FROM THE NODE TO THE GRAPH
        return Graph
        raise RuntimeError("This function is not implemented yet.")


def print_stats(Graph):
        NoOfNodes = Graph.number_of_nodes()     ##ASSIGNS NUMBER OF NODES TO THE VARIABLE
        NoOfEdge = Graph.number_of_edges()      ##ASSIGNS NUMBER OF EDGES TO THE VARIABLE

        print("Number of nodes =" + NoOfNodes)  ##PRINTS VALUES
        print("Number of edges =" + NoOfEdge)

        """Print number of nodes and edges in the given graph"""
        raise RuntimeError("This function is not implemented yet.")


def stochastic_page_rank(graph, args):
    """Stochastic PageRank estimation
    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple
    Returns:
    A dict that assigns each page its hit frequency
    This function estimates the Page Rank by counting how frequently
    a random walk that starts on a random node will after n_steps end
    on each node of the given graph.
    """
    HitCount = {Graph.nodes, 0}             ## Initialises all nodes to have a Hit count of 0
    for node in Graph:                      ## Goes through each node
        for i in range(args.repeats):       ##Selects number of repeats based of user input in the console
            CurrentNode = random.choice(node)   ##Selects the next node to be a random node
            for j in range(args.steps):         ##Selects the number of steps the walker is to make
                CurrentNode = random.choice(CurrentNode)
            HitCount[CurrentNode] += 1/args.repeats     ##Determines the new hit count and sets it to the CurrentNode
    return HitCount



    raise RuntimeError("This function is not implemented yet.")


def distribution_page_rank(graph, args):
    """Probabilistic PageRank estimation
    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple
    Returns:
    A dict that assigns each page its probability to be reached
    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.
    """
    NodeProb = {}       ##initialises the current probability dict
    NextProb = {}       ##initialises the next probability dict
    NodeProb[Graph.node] = 1 / Graph.number_of_nodes()          ##makes probability of current node being selected
    for i in range(args.steps):         ##uses number of walker steps selected by user in console
        NextProb[Graph.node, 0]         ##sets each next node to 0
        for node in Graph:              ## for loop to go through each node
            Probability = NodeProb      ##Creates probability variable
            for Graph.adj in Graph:     ##Goes through each connected node
                NextProb[Graph.adj] += Probability          ##Probability calculation
                NodeProb[Graph.node] = NextProb[Graph.adj]  ##Sets this to be the current nodes prbability
    return NodeProb



    raise RuntimeError("This function is not implemented yet.")


parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")


if __name__ == '__main__':
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    graph = load_graph(args)

    print_stats(graph)

    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    time = stop - start

    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:args.number]))
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")
