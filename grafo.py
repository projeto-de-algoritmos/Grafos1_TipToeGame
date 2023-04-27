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
    
    # transforma tabuleiro em grafo
    def createGrafo(self, board):
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    self.add_edge(i, j)
                elif board[i][j] == 1:
                    self.remove_edge(i, j)
        return self.adj_matrix
    
    # dfs
    def dfs(self, v):
        path = []
        self.visited[v] = True
        for i in range(self.num_vertices):
            if self.adj_matrix[v][i] == 1 and not self.visited[i]:
                path.append([v, i])
                self.dfs(i)
        return path
