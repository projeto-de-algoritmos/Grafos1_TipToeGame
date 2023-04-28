#cria estrutura de dados para o grafo com matriz de adjacencia
class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.adj_matrix = [[0] * num_vertices for _ in range(num_vertices)]
        self.visited = [False] * num_vertices
    
    def add_edge(self, v1, v2):
        self.adj_matrix[v1][v2] = 1
        self.adj_matrix[v2][v1] = 1
    
    def remove_edge(self, v1, v2):
        self.adj_matrix[v1][v2] = 0
        self.adj_matrix[v2][v1] = 0
    
    def clear_visited(self):
        self.visited = [False] * self.num_vertices
    
    #tranforma matriz em grafo
    def matrix_to_graph(self, matrix):
        element = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] != 7:
                    # checa se é possivel ir para a direita, esquerda, cima ou baixo
                    if i+1 < len(matrix) and matrix[i+1][j] != 7:
                        self.add_edge(element, len(matrix[i])+element)
                    if j+1 < len(matrix[i]) and matrix[i][j+1] != 7:
                        self.add_edge(element, element+1)
                    if i-1 >= 0 and matrix[i-1][j] != 7:
                        self.add_edge(element, element-len(matrix[i]))
                    if j-1 >= 0 and matrix[i][j-1] != 7:
                        self.add_edge(element, element-1)
                if matrix[i][j] != 7:
                    self.add_edge(element, element)
                element += 1

    # cria caminho entre dois pontos usando busca em profundidade
    def dfs(self, start, end):
        self.visited[start] = True
        if start in end:
            return [start]
        for v in range(self.num_vertices):
            if self.adj_matrix[start][v] == 1 and not self.visited[v]:
                path = self.dfs(v, end)
                if path:
                    return [start] + path
        return None
    
    # transforma caminho em lista de coordenadas
    def path_to_coordinates(self, path, matrix):
        coordinates = []
        for i in path:
            coordinates.append(self.index_to_coordinates(i, matrix))
        return coordinates
    
    # transforma indice em coordenadas
    def index_to_coordinates(self, index, matrix):
        row = int(index) // len(matrix)
        column = index % len(matrix)
        return (row, column)
    
    # transforma coordenadas em indice
    def coordinates_to_index(self, coordinates, matrix):
        return coordinates[0]*len(matrix) + coordinates[1]
    
    # transforma caminho em lista de movimentos
    def path_to_moves(self, path=[], matrix=[[]]):
        moves = []
        if path != None:
            for i in range(len(path)-1):
                moves.append(self.get_move(path[i], path[i+1], matrix))
        return moves

    # retorna movimento entre dois pontos
    def get_move(self, start, end, matrix):
        start = self.index_to_coordinates(start, matrix)
        end = self.index_to_coordinates(end, matrix)
        if start[0] == end[0]:
            if start[1] > end[1]:
                return [-1, 0]
            else:
                return [1, 0]
        else:
            if start[0] > end[0]:
                return [0, -1]
            else:
                return [0, 1]