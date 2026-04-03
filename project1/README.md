# Blind Search

​	This project implements basic uninformed search using the data structures of **graph, stack, queue, and priority queue**. It supports **Depth-First Search (DFS)**, **Breadth-First Search (BFS)**, and **Uniform-Cost Search (UCS)**. The system is capable of visualizing specified directed or undirected graphs, reading graph data from an external file (`graph_data.txt`), and presenting search results via a web-based interface in HTML format.

## Source Code's Description:

The source code mainly consists of three parts:

- ### **Implementation of Three Uninformed Search Algorithms**

The fringe for all three algorithms in this project is stored using a list, which respectively emulates the data structures of stack, queue, and priority queue (min-heap). Three classes are defined in this module, each encapsulating the corresponding search strategy logic.

- ### **General Uninformed Search Framework**

This module defines the graph node attributes and standard search interfaces. When invoking the search function, a graph object, start node, goal node, and search fringe are required as input parameters. The adoption of a generic uninformed search framework facilitates the implementation and integration of different search algorithms.

- ### **Dynamic Interactive Visualization of Search Results**

The **pyvis** library is utilized to achieve dynamic interactive visualization of search results in this section. The `save_visual_graph` function renders the graph structure, search path, and algorithm-related information into an HTML file. This module supports both directed and undirected graph visualization, enabling intuitive comparison of search efficiency and path outcomes across different algorithms.

## Usage:

### Install

```sh
pip install pyvis networkx
```

**Note**

- Python 3.10 is required.

### Running

``` sh
python src/main.py
```

## Contact:

If you have any questions or suggestions, feel free to contact:

- [Haoyang Chi](https://xinhao-deng.github.io/) (+86 13133513475)