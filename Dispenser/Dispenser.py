from Server.config import NODES
import requests
node_index = 0
REPLICATION_COUNT = 2


def select_node():
    global node_index
    start_index = node_index
    nodes = []
    chosen = 0

    while (chosen < REPLICATION_COUNT):
        try:
            response = requests.get(f"{NODES[node_index]}/health", timeout=5)
            
            if response.status_code == 200:
                selected = NODES[node_index]
                node_index = (node_index + 1) % len(NODES)
                nodes.append(selected)
                
        except:
            pass
        node_index = (node_index + 1) % len(NODES)
        if node_index == start_index:
            raise Exception("All nodes are down!")
            break

    if (chosen == REPLICATION_COUNT) :
        return nodes
    else :
        return "error"

