# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 04:
# 99314 Raquel Cardoso
# 99287 Miguel Eleutério

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self, size, board):
        self.size = size
        self.board = board

    def get_number(self, row: int, col: int):
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def change_number(self, row: int, col: int, number: int):
        self.board[row][col] = number

    def adjacent_vertical_numbers(self, row: int, col: int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        return (self.board[row - 1][col] if row != 0 else None, self.board[row + 1][col] if row != (self.size - 1) else None)
        

    def adjacent_horizontal_numbers(self, row: int, col: int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.board[row][col - 1] if col != 0 else None, self.board[row][col + 1] if col != (self.size - 1) else None)

    def get_row(self, row: int):
        return self.board[row]

    def get_col(self, col: int):
        return (line[col] for line in self.board)


    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """
        board = []
        n = sys.stdin.readline()

        for i in range(n):
            line = sys.stdin.readline()
            line = line.rstrip('\n')
            values = line.split('\t')
            values = map(int, values)
            board += values
        return self(n, board)

    # TODO: outros metodos da classe


class Takuzu(Problem):

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        for i in range(n):
            for j in range(n):
                if self.board.get_number(i, j) == 2:
                    actions += [i, j, 0]
                    actions += [i, j, 1]
                    
        return actions

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        available_actions = self.actions(self, state)
        if action in available_actions:
            self.board.change_number(action[0], action[1], action[2])
        return self.board

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        
        #verificar q nao ha 2 no tabuleiro, q nao há diferença maior q 1
        # q nao linhas e colunas iguais e q nao ha 3 numeros iguais seguidos horziontalmente ou verticalmente

        #faz a função banger miguel !!!!!!!!!!!!!!!!!!!
        '''
        count_zero = 0
        count_one = 0
        rows = []
        cols = []

        for i in range(self.board.size):
            row = self.board.get_row(i)
            for k in range(self.board.size):
                if self.board.get_number(i, k) == 0:
                    count_zero += 1
            
            
            #ver se há linhas iguais
            if len(rows) == 0:
                rows += row
            else:
                for j in range(len(rows)):
                    if row == rows[j]:
                        return False'''
        


    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
