class Node:
    def __init__(self,state,parent=None,cost=0):
        self.state = state
        self.parent = parent
        self.cost = cost
def generic_search(graph,start,goal,fringe):
    fringe.push(Node(start),0)
    visited = {}
    nodes_expanded = 0
    while not fringe.is_empty():
        node = fringe.pop()
        nodes_expanded += 1
        if node.state == goal:
            path=[]
            curr=node
            while curr:
                path.append(curr.state)
                curr=curr.parent
            return path[::-1],node.cost,nodes_expanded #目标节点溯源
        if node.state not in visited or node.cost < visited[node.state]:
            visited[node.state]=node.cost
            for neighbor,weight in graph.get(node.state,[]): #没有邻居直接跳过
                new_cost = node.cost + weight
                fringe.push(Node(neighbor,node,new_cost),new_cost)
    return None,0,nodes_expanded









