# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 04:
# 99314 Raquel Cardoso
# 99287 Miguel Eleutério

from re import I
import sys
from turtle import pos
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
        size = self.get_size()
        for i in range(size):
            line = self.get_row(i)
            for j in range(size):
                if j != size-1:
                    to_print += str(line[j]) + "\t"
                elif i == size-1:
                    to_print += str(line[j])
                else:
                    to_print += str(line[j]) + "\n"

        return to_print

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
        return (self.board[row - 1][col] if self.size > row > 0 else None, 
        self.board[row + 1][col] if 0 <= row < (self.size - 1) else None)

    def adjacent_horizontal_numbers(self, row: int, col: int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.board[row][col - 1] if self.size > col > 0 else None, 
        self.board[row][col + 1] if 0 <= col < (self.size - 1) else None)

    def get_row(self, row: int):
        return self.board[row]

    def get_col(self, col: int):
        return (line[col] for line in self.board)

    def get_first_empty_positions(self):

        for i in range(self.size):
            for j in range(self.size):
                if self.get_number(i, j) == 2:
                    return (i, j, 2)
        return None

    def get_horizontal_values(self, row: int, col: int, identifier: int):
        """Identifier:
        1 = Next 2 values; 0 = Previous 2 values; Returns None if non-existant"""
        if identifier == 1:
            return (self.board[row][col + 1] if 0 <= col < (self.size - 1) else None, 
            self.board[row][col + 2] if 0 <= col < (self.size - 2) else None)
        else:
            return (self.board[row][col - 1] if self.size > col > 0 else None, 
            self.board[row][col - 2] if self.size > col > 1 else None)

    def get_vertical_values(self, row: int, col: int, identifier: int):
        """Identifier:
        1 = Next 2 values; 0 = Previous 2 values; Returns None if non-existant"""
        if identifier == 1:
            return (self.board[row + 1][col] if 0 <= row < (self.size - 1) else None, 
            self.board[row + 2][col] if 0 <= row < (self.size - 2) else None)
        else:
            return (self.board[row - 1][col] if self.size > row > 0 else None, 
            self.board[row - 2][col] if self.size > row > 1 else None)

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
        position = self.board.get_first_empty_position()
        result = ()

        next_horizontals = self.board.get_horizontal_values(position[0], position[1], 1)
        prev_horizontals = self.board.get_horizontal_values(position[0], position[1], 0)
        next_verticals = self.board.get_vertical_values(position[0], position[1], 1)
        prev_verticals = self.board.get_vertical_values(position[0], position[1], 0)

        if next_horizontals[0] == prev_horizontals[0] != None:
            result += (position[0], position[1], abs(next_horizontals[0] - 1))
        elif next_verticals[0] == prev_verticals[0] != None:
            result += (position[0], position[1], abs(next_verticals[0] - 1))
        elif next_horizontals[0] == next_horizontals[1] != None:
            result += (position[0], position[1], abs(next_horizontals[0] - 1))
        elif prev_horizontals[0] == prev_horizontals[1] != None:
            result += (position[0], position[1], abs(prev_horizontals[0] - 1))
        elif next_verticals[0] == next_verticals[1] != None:
            result += (position[0], position[1], abs(next_verticals[0] - 1))
        elif prev_verticals[0] == prev_verticals[1] != None:
            result += (position[0], position[1], abs(prev_verticals[0] - 1))
        else:
            result += (position[0], position[1], 0)
            result += (position[0], position[1], 1)

        return result

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
            if (1,1,1) in line1 or (0,0,0) in line1 or 2 in line1:
                return False
            if (1,1,1) in col1 or (0,0,0) in col1 or 2 in col1:
                return False
            for j in range(i + 1, size):
                line2 = board.get_row(j)
                col2 = board.get_col(j)
                if line1 == line2 or col1 == col2:                
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
