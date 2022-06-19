# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 04:
# 99314 Raquel Cardoso
# 99287 Miguel Eleutério

from ctypes import pointer
from multiprocessing.sharedctypes import Value
from re import I
import sys
from time import get_clock_info
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

class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self, n, given_board):
        self.size = n
        self.board = given_board

    def __str__(self) -> str:
        to_print = ""
        size = self.get_size()
        for i in range(size):
            line = self.get_row(i)
            for j in range(size):
                if j != size-1:
                    to_print += str(line[j]) + "\t"
                else:
                    to_print += str(line[j]) + "\n"

        return to_print

    def get_board(self):
        return self.board

    def get_size(self):
        return self.size

    def get_row(self, row: int):
        return self.board[row]

    def get_col(self, col: int):
        return [line[col] for line in self.board]

    def get_number(self, row: int, col: int):
        return self.board[row][col]

    def change_number(self, row: int, col: int, number: int):
        self.board[row][col] = number

    def adjacent_vertical_numbers(self, row: int, col: int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        return (self.board[row - 1][col] if self.get_size() > row > 0 else None, 
        self.board[row + 1][col] if 0 <= row < (self.get_size() - 1) else None)

    def adjacent_horizontal_numbers(self, row: int, col: int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.board[row][col - 1] if self.get_size() > col > 0 else None, 
        self.board[row][col + 1] if 0 <= col < (self.get_size() - 1) else None)

    def get_first_empty_position(self):
        for i in range(self.get_size()):
            for j in range(self.get_size()):
                if self.get_number(i, j) == 2:
                    return (i, j, 2)
        return None

    def get_horizontal_values(self, row: int, col: int, identifier: int):
        """Identifier:
        1 = Next 2 values; 0 = Previous 2 values; Returns None if non-existant"""
        if identifier == 1:
            return (self.board[row][col + 1] if 0 <= col < (self.get_size() - 1) else None, 
            self.board[row][col + 2] if 0 <= col < (self.get_size() - 2) else None)
        else:
            return (self.board[row][col - 1] if self.get_size() > col > 0 else None, 
            self.board[row][col - 2] if self.get_size() > col > 1 else None)

    def get_vertical_values(self, row: int, col: int, identifier: int):
        """Identifier:
        1 = Next 2 values; 0 = Previous 2 values; Returns None if non-existant"""
        if identifier == 1:
            return (self.board[row + 1][col] if 0 <= row < (self.get_size() - 1) else None, 
            self.board[row + 2][col] if 0 <= row < (self.get_size() - 2) else None)
        else:
            return (self.board[row - 1][col] if self.get_size() > row > 0 else None, 
            self.board[row - 2][col] if self.get_size() > row > 1 else None)

    def copy_board(self):
        new_board = []
        for i in range(self.get_size()):
            line = []
            for j in range(self.get_size()):
                line += [self.get_number(i, j)]
            new_board += [line]
        return new_board

    def exists(self, vector1, identifier: int):
        """Identifier:
        0 = Row; 1 = Columnn
        """
        if identifier == 0:
            for i in range(self.get_size()):
                row = self.get_row(i)
                if row == vector1:
                    return True
        if identifier == 1:
            for i in range(self.get_size()):
                col = self.get_col(i)
                if col == vector1:
                    return True
        return False

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
        n = n.rstrip('\n')
        n = int(n)

        for i in range(n):
            line = sys.stdin.readline()
            line = line.rstrip('\n')
            values = line.split('\t')
            for j in range(n):
                values[j] = int(values[j])
            board += [values]
        return Board(n, board)

    # TODO: outros metodos da classe

class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.state = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    def get_state(self):
        return self.state

    def get_size(self):
        return self.state.get_size()

    def change_number(self, row: int, col: int, number: int):
        self.state.change_number(row, col, number)

    def get_number(self, row: int, col: int):
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.state.get_number(row, col)

    def get_row(self, row: int):
        return self.state.get_row(row)

    def get_col(self, col: int):
        return self.state.get_col(col)

    def get_first_empty_position(self):
        return self.get_state().get_first_empty_position()

    def get_horizontal_values(self, row: int, col: int, identifier: int):
        return self.get_state().get_horizontal_values(row, col, identifier)

    def get_vertical_values(self, row: int, col: int, identifier: int):
        return self.get_state().get_vertical_values(row, col, identifier)

    def adjacent_horizontal_numbers(self, row: int, col: int):
        return self.get_state().adjacent_horizontal_numbers(row, col)

    def adjacent_vertical_numbers(self, row: int, col: int):
        return self.get_state().adjacent_vertical_numbers(row, col)

    def copy_board(self):
        return self.get_state().copy_board()

    def exists(self, vector1, identifier: int):
        """Identifier:
        0 = Row; 1 = Columnn
        """
        return self.get_state().exists(vector1, identifier)

    # TODO: outros metodos da classe

class Takuzu(Problem):

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        
        self.initial = TakuzuState(board)

    def actions(self, given_state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        position = given_state.get_state().get_first_empty_position()
        result = tuple()
        put = {0, 1}

        next_horizontals = given_state.get_horizontal_values(position[0], position[1], 1)
        prev_horizontals = given_state.get_horizontal_values(position[0], position[1], 0)
        next_verticals = given_state.get_vertical_values(position[0], position[1], 1)
        prev_verticals = given_state.get_vertical_values(position[0], position[1], 0)
        adjacent_verticals = given_state.adjacent_vertical_numbers(position[0], position[1])
        adjacent_horizontals = given_state.adjacent_horizontal_numbers(position[0], position[1])

        equals0, equals1 = False, False
        row = given_state.get_row(position[0])
        col = given_state.get_col(position[1])

        def same_numbers(n1, n2):
            numbers = [n1, n2]
            if n1 == n2 and 2 not in numbers and None not in numbers:
                return True
            return False
        
        if same_numbers(adjacent_verticals[0], adjacent_verticals[1]):
        #if adjacent_verticals[0] == adjacent_verticals[1] and 2 not in adjacent_verticals and None not in adjacent_verticals:
            put.discard(adjacent_verticals[0])
        
        if same_numbers(adjacent_horizontals[0], adjacent_horizontals[1]):
        #if adjacent_horizontals[0] == adjacent_horizontals[1] and 2 not in adjacent_horizontals and None not in adjacent_horizontals:
            put.discard(adjacent_horizontals[0])

        if same_numbers(next_horizontals[0], next_horizontals[1]):
        #if next_horizontals[0] == next_horizontals[1] and 2 not in next_horizontals and None not in next_horizontals:
            put.discard(next_horizontals[0])

        if same_numbers(prev_horizontals[0], prev_horizontals[1]):
        #if prev_horizontals[0] == prev_horizontals[1] and 2 not in prev_horizontals and None not in prev_horizontals:
            put.discard(prev_horizontals[0])

        if same_numbers(next_verticals[0], next_verticals[1]):
        #if next_verticals[0] == next_verticals[1] and 2 not in next_verticals and None not in next_verticals:
            put.discard(next_verticals[0])

        if same_numbers(prev_verticals[0], prev_verticals[1]):
        #if prev_verticals[0] == prev_verticals[1] and 2 not in prev_verticals and None not in prev_verticals:
            put.discard(prev_verticals[0])

        if given_state.get_row(position[0]).count(2) == 1:
            new_row1_0, new_row1_1 = row.copy(), row.copy()
            new_row1_0[position[1]], new_row1_1[position[1]] = 0, 1
            if given_state.exists(new_row1_0, 0):
                equals0 = True
            if given_state.exists(new_row1_1, 0):
                equals1 = True

        if given_state.get_col(position[1]).count(2) == 1:
            new_col1_0, new_col1_1 = col.copy(), col.copy()
            new_col1_0[position[0]], new_col1_1[position[0]] = 0, 1
            if given_state.exists(new_col1_0, 1):
                equals0 = True
            if given_state.exists(new_col1_1, 1):
                equals1 = True

        if equals0:
            put.discard(0)

        if equals1:
            put.discard(1)

        if 1 in put:
            result += ((position[0], position[1], 1),)
        if 0 in put:
            result += ((position[0], position[1], 0),)
            
        return result

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        copied_board = state.copy_board()
        copied_board[action[0]][action[1]] = action[2]

        return TakuzuState(Board(state.get_size(), copied_board))

    def goal_test(self, given_state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""

        size = given_state.get_size()

        for i in range(size):
            line1 = given_state.get_row(i)
            col1 = given_state.get_col(i)
            if (1,1,1) in line1 or (0,0,0) in line1 or 2 in line1:
                return False
            if (1,1,1) in col1 or (0,0,0) in col1 or 2 in col1:
                return False
            for j in range(i + 1, size):
                line2 = given_state.get_row(j)
                col2 = given_state.get_col(j)
                if line1 == line2 or col1 == col2:  
                    return False

        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # relatório
        pass

if __name__ == "__main__":
    # Ler tabuleiro do ficheiro 'i1.txt' (Figura 1):
    # $ python3 takuzu < i1.txt
    board = Board.parse_instance_from_stdin()

    # Criar uma instância de Takuzu:
    problem = Takuzu(board)

    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)

    print(goal_node.state.get_state(), end = "")