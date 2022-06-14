# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 04:
# 99314 Raquel Cardoso
# 99287 Miguel Eleutério

from re import I
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
from utils import vector_add


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

    def __str__(self) -> str:
        to_print = ""
        for i in range(self.size):
            col = self.get_col(i)
            for j in range(self.size):
                to_print += str(col[j]) + "\t"

    def get_size(self):
        return self.size

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

#wtf

class Takuzu(Problem):

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        for i in range(self.board.get_size()):
            for j in range(self.board.get_size()):
                if self.board.get_number(i, j) == 2:
                    # testar c 1/0 e ver se cumpre todas: se sim -> meter se não -> meter o outro
                    # se n for possivel concluir se cumpre em alguma, testar a prox, se tbm nao -> meter ambas
                    actions += [i, j, 0]
                    actions += [i, j, 1]
                    
        return actions

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        self.board.change_number(action[0], action[1], action[2])
        return self.board

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # nao ha linhas e colunas iguais 
        # nao ha 3 numeros iguais seguidos horizontalmente ou verticalmente

        #verificar q nao ha 2 no tabuleiro,
        # nao há diferença maior q 1

        board = self.board
        size = board.get_size()
        one_count = 0
        zero_count = 0
        for i in range(size):
            line1 = board.get_row(i)
            col1 = board.get_col(i)
            for j in range(i, size):
                line2 = board.get_row(j)
                col2 = board.get_col(j)
                if line1 == line2 or col1 == col2:                
                    return False
            if (1,1,1) in line1 or (0,0,0) in line1 or 2 in line1:
                return False
            if (1,1,1) in col1 or (0,0,0) in col1 or 2 in col1:
                return False
            one_count += line1.count(1)
            zero_count += line1.count(0)

        if abs(one_count - zero_count) > 1:
            return False

        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # Ler tabuleiro do ficheiro 'i1.txt' (Figura 1):
    # $ python3 takuzu < i1.txt
    board = Board.parse_instance_from_stdin()

    # Criar uma instância de Takuzu:
    problem = Takuzu(board)

    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)

    # Verificar se foi atingida a solução
    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board, sep="")
