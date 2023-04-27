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
                self.add_edge(element, element)
                element += 1