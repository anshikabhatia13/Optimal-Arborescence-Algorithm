class List:
    def __init__(self):
        self.items = []
        self.capacity = 4
        self.size = 0

    def list_init(self):
        self.capacity = 4
        self.size = 0
        self.items = []

    def list_size(self):
        return self.size

    def list_resize(self, capacity):
        self.items = self.items[:capacity]
        self.capacity = capacity

    def list_add(self, item):
        if self.capacity == self.size:
            self.list_resize(self.capacity * 2)
        self.items.append(item)
        self.size += 1

    def list_set(self, index, item):
        if 0 <= index < self.size:
            self.items[index] = item

    def list_get(self, index):
        if 0 <= index < self.size:
            return self.items[index]
        else:
            return None

    def list_max(self):
        max_index = 0
        for i in range(1, self.size):
            if self.items[i] > self.items[max_index]:
                max_index = i
        return max_index

    def list_delete(self, index):
        if 0 <= index < self.size:
            self.items.pop(index)
            self.size -= 1
            if self.size > 0 and self.size == self.capacity // 4:
                self.list_resize(self.capacity // 2)

    def list_free(self):
        self.items = []

class Stack:
    def __init__(self):
        self.items = []
        self.capacity = 4
        self.size = 0

    def stack_init(self):
        self.capacity = 4
        self.size = 0
        self.items = []

    def stack_resize(self, capacity):
        self.items = self.items[:capacity]
        self.capacity = capacity

    def stack_push(self, item):
        if self.capacity == self.size:
            self.stack_resize(self.capacity * 2)
        self.items.append(item)
        self.size += 1

    def stack_top(self):
        return self.items[self.size - 1]

    def stack_pop(self):
        self.items.pop()
        self.size -= 1
        if self.size > 0 and self.size == self.capacity // 4:
            self.stack_resize(self.capacity // 2)

    def stack_free(self):
        self.items = []

def min_arborescence(graph, vertices, root):
    def create_f_star(graph, vertices, root):
        f_star = [-1] * vertices
        for v in range(vertices):
            if v == root - 1:
                continue
            for u in range(vertices):
                if graph[u][v] != -1:
                    if f_star[v] == -1:
                        f_star[v] = u
                    else:
                        if graph[u][v] <= graph[f_star[v]][v]:
                            f_star[v] = u
        return f_star

    def check_cycle(vertices, root, chosen_edges):
        for v in range(vertices):
            if v == root - 1:
                continue
            else:
                current = v
                while True:
                    if chosen_edges[current] == -1:
                        break
                    elif chosen_edges[current] == v:
                        return v + 1
                    else:
                        current = chosen_edges[current]
        return 0

    def find_cycle(vertices, cycle_start, chosen_edges):
        found_cycle = [cycle_start]
        current = cycle_start
        while True:
            if chosen_edges[current] == -1:
                print("ERROR IN check_cycle")
                break
            elif chosen_edges[current] == cycle_start:
                found_cycle.append(cycle_start)
                break
            else:
                current = chosen_edges[current]
                found_cycle.append(current)
        return found_cycle

    def compress_graph(graph, vertices, root, min_edges, in_cycle, cycle_size, cycle_begin, new_root, map_g_to_gdash, map_gdash_to_g):
        new_vertices = vertices - cycle_size + 1
        new_graph = [[-1] * new_vertices for _ in range(new_vertices)]
        map_g_to_gdash = [-1] * vertices
        map_gdash_to_g = [-1] * new_vertices

        curr = 0
        for i in range(vertices):
            if in_cycle[i] == 1:
                map_g_to_gdash[i] = new_vertices - 1
                map_gdash_to_g[new_vertices - 1] = cycle_begin
            else:
                map_g_to_gdash[i] = curr
                map_gdash_to_g[curr] = i
                curr += 1
        new_root[0] = map_g_to_gdash[root - 1] + 1

        for u in range(vertices):
            for v in range(vertices):
                if v != root - 1:
                    u_in_cycle = in_cycle[u]
                    v_in_cycle = in_cycle[v]
                    min_edge_weight = graph[min_edges[v]][v]

                    if not u_in_cycle and not v_in_cycle:
                        if graph[u][v] != -1:
                            new_graph[map_g_to_gdash[u]][map_g_to_gdash[v]] = graph[u][v] - min_edge_weight

                    elif u_in_cycle and v_in_cycle:
                        pass

                    else:
                        if graph[u][v] != -1:
                            if new_graph[map_g_to_gdash[u]][map_g_to_gdash[v]] == -1:
                                new_graph[map_g_to_gdash[u]][map_g_to_gdash[v]] = graph[u][v] - min_edge_weight
                            else:
                                if graph[u][v] - min_edge_weight < new_graph[map_g_to_gdash[u]][map_g_to_gdash[v]]:
                                    new_graph[map_g_to_gdash[u]][map_g_to_gdash[v]] = graph[u][v] - min_edge_weight
        return new_graph

    def decompress_arborescence(graph, vertices, vertices_dash, f_star, in_cycle, arbro_dash, g_dash_to_g):
        arbro = [-1] * vertices
        for i in range(vertices_dash):
            if arbro_dash[i] != -1:
                if in_cycle[g_dash_to_g[i]] == 0 and in_cycle[g_dash_to_g[arbro_dash[i]]] == 0:
                    arbro[g_dash_to_g[i]] = g_dash_to_g[arbro_dash[i]]
                elif in_cycle[g_dash_to_g[i]] == 1:
                    connector_to_tree = g_dash_to_g[arbro_dash[i]]
                    best_weight = 1e8
                    current_node = g_dash_to_g[i]
                    best_node = current_node
                    itr = 0
                    while True:
                        if current_node == g_dash_to_g[i] and itr > 0:
                            break
                        if graph[connector_to_tree][current_node] != -1:
                            if graph[connector_to_tree][current_node] < best_weight:
                                best_weight = graph[connector_to_tree][current_node]
                                best_node = current_node
                        current_node = f_star[current_node]
                        itr += 1
                    if best_node == -1:
                        print("ERROR IN DECOMPRESSING!")
                        exit(0)
                    arbro[best_node] = connector_to_tree

        for i in range(vertices):
            if arbro[i] == -1:
                arbro[i] = f_star[i]
        return arbro

    min_arbo_array = []
    f_star = create_f_star(graph, vertices, root)
    cycle_exists = check_cycle(vertices, root, f_star)
    if cycle_exists == 0:
        min_arbo_array = f_star
    else:
        cycle = find_cycle(vertices, cycle_exists - 1, f_star)
        cycle_size = 0
        for i in range(1, vertices):
            if cycle[i] == cycle[0]:
                cycle_size = i
                break
        in_cycle = [0] * vertices
        for i in range(vertices):
            if i < cycle_size:
                in_cycle[cycle[i]] = 1
        root_dash = [0]
        map2_new = [-1] * vertices
        map_from_new = [-1] * (vertices - cycle_size + 1)
        graph_dash = compress_graph(graph, vertices, root, f_star, in_cycle, cycle_size, cycle_exists - 1, root_dash, map2_new, map_from_new)
        min_arbo_array_dash = min_arborescence(graph_dash, vertices - cycle_size + 1, root_dash[0])
        min_arbo_array = decompress_arborescence(graph, vertices, vertices - cycle_size + 1, f_star, in_cycle, min_arbo_array_dash, map_from_new)
    return min_arbo_array

# Example usage:
# Replace this with your actual graph data
def help():
    print("\n-------------------------------------------------------")
    print("\n        Methods to execute program:")
    print("(1) algo help")
    print("                      or")
    print("(2) algo <testFile.txt>")
    print("                      or")
    print("(3) algo <number of vertices> <number of edges> <root node>\n")

    print("\n        Details of each method:")
    print("(1) Will print this help message.")
    print("(2) Will start the program, guidelines for which are-")
    print("          |- <testFile.txt> should be in the directory 'test'.")
    print("          |- Vertex numbers are 1-indexed.")
    print("          |- For guidelines on the format of testFile, see README.")
    print("(3) Will start the program, guidelines for which are-")
    print("          |- Both <number of vertices> and <number of edges> should be positive integers.")
    print("          |- <root node> value should be less than <number of vertices>.")
    print("          |- The program will further ask for details of each directed edge in the format <starting node> <ending node> <weight of edge>.")
    print("             Values of <starting node> and <ending node> should be less than <root node>.")
    print("             Values of <weight of edge> should be positive real numbers.")
    print("          |- Vertex numbers are 1-indexed.")
    print("PROGRAM WILL TERMINATE IF-")
    print("ALL VERTICES ARE NOT REACHABLE FROM <root node>,")
    print("                      or")
    print("ANY OTHER SITUATION WHERE ARBRORESCENCE DOESN'T EXIST.")
    print("\n-------------------------------------------------")




def main():
    import sys

    N, M, R = 0, 0, 0
    graph = []

    if len(sys.argv) < 2:  # Wrong arguments
        print("NOT ENOUGH ARGUMENTS!\nSee help-")
        help()
        sys.exit(1)

    if len(sys.argv) == 2:  # Help or input via file
        if sys.argv[1] == "help":
            # Help
            help()
            sys.exit(0)
        else:
            # Input via file
            file_name = sys.argv[1]
            full_file_name = "../test/" + file_name
            try:
                with open(full_file_name, "r") as fp:
                    N, M, R = map(int, fp.readline().split())
                    if N < 1 or M < 0:
                        print("INVALID NUMBER OF VERTICES({}) OR NUMBER OF EDGES({})!\nSee help-".format(N, M))
                        help()
                        sys.exit(1)

                    if R > N or R < 1:
                        print("INVALID VALUE OF ROOT NODE({})!\nSee help-".format(R))
                        help()
                        sys.exit(1)

                    graph = [[-1] * N for _ in range(N)]

                    for _ in range(M):
                        start, end, weight = map(int, fp.readline().split())
                        if start > N or start < 1 or end > N or end < 1:
                            print("INVALID VALUE OF <starting node> OR <ending node>!\nSee help-")
                            help()
                            sys.exit(1)
                        if weight < 0:
                            print("WEIGHT VALUE SHOULD BE >= 0!\nSee help-")
                            help()
                            sys.exit(1)

                        if start == end or end == R:
                            continue
                        if graph[start - 1][end - 1] == -1:
                            graph[start - 1][end - 1] = weight
                        elif weight < graph[start - 1][end - 1]:
                            graph[start - 1][end - 1] = weight
            except FileNotFoundError:
                # File not found
                print("FILE NOT FOUND! MAKE SURE FILE IS IN 'TEST' DIRECTORY.\nSee help-")
                help()
                sys.exit(1)

    elif len(sys.argv) == 4:  # Input via command line
        N, M, R = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])

        if N < 1 or M < 0:
            print("INVALID NUMBER OF VERTICES({}) OR NUMBER OF EDGES({})!\nSee help-".format(N, M))
            help()
            sys.exit(1)

        if R > N or R < 1:
            print("INVALID VALUE OF ROOT NODE({})!\nSee help-".format(R))
            help()
            sys.exit(1)

        graph = [[-1] * N for _ in range(N)]

        for edge in range(M):
            print("For edge {}:".format(edge + 1), end=' ')
            start, end, weight = map(int, input().split())
            if start > N or start < 1 or end > N or end < 1:
                print("INCORRECT VALUE OF <starting node> OR <ending node>!\nSee help-")
                help()
                sys.exit(1)
            if weight < 0:
                print("WEIGHT VALUE SHOULD BE >= 0!\nSee help-")
                help()
                sys.exit(1)

            if start == end or end == R:
                continue
            if graph[start - 1][end - 1] == -1:
                graph[start - 1][end - 1] = weight
            elif weight < graph[start - 1][end - 1]:
                graph[start - 1][end - 1] = weight

    else:  # Wrong arguments
        print("TOO MANY ARGUMENTS!\nSee help-")
        help()
        sys.exit(1)

    # Perform BFS on the graph here.
    # If not connected, exit the program with an error message to the user.

    # Your code for finding the minimum arborescence would be here.

    # print("Chosen edges in the minimum arborescence are:")
    # for i in range(N):
    #     if graph[i] == -1:
    #         pass
    #     else:
    #         print("{} -> {}".format(min_arbrorescence[i] + 1, i + 1))
    # # Your code for finding the minimum arborescence should be here.

# Call your min_arborescence function to get the result
    min_arborescence_result = min_arborescence(graph, N, R)

    print("Chosen edges in the minimum arborescence are:")
    for i in range(N):
        if min_arborescence_result[i] == -1:
            pass
        else:
            print("{} -> {}".format(min_arborescence_result[i] + 1, i + 1))

if __name__ == "__main__":
    main()
