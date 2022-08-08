import pandas as pd
from random import randint

####################################################################################################

class game_obs():

    def __init__(self, pieces_b={}, pieces_r={}):

        self.board = pd.DataFrame(['']*8 for i in range(8))
        self.check_mate = 0
        self.turn = 'b'

        if pieces_b != {}: self.pieces_b = pieces_b

        else:
            self.pieces_b = {
                'Rb70': piece('R', 'b', (7, 0)),
                'Rb77': piece('R', 'b', (7, 7)),
                'Bb72': piece('B', 'b', (7, 2)),
                'Bb75': piece('B', 'b', (7, 5)),
                'Nb71': piece('N', 'b', (7, 1)),
                'Nb76': piece('N', 'b', (7, 6)),
                'Qb73': piece('Q', 'b', (7, 3)),
                'Kb74': piece('K', 'b', (7, 4)),
                'Pb60': piece('P', 'b', (6, 0)),
                'Pb61': piece('P', 'b', (6, 1)),
                'Pb62': piece('P', 'b', (6, 2)),
                'Pb63': piece('P', 'b', (6, 3)),
                'Pb64': piece('P', 'b', (6, 4)),
                'Pb65': piece('P', 'b', (6, 5)),
                'Pb66': piece('P', 'b', (6, 6)),
                'Pb67': piece('P', 'b', (6, 7))
            }

        if pieces_r != {}: self.pieces_r = pieces_r

        else:
            self.pieces_r = {
                'Rr00': piece('R', 'r', (0, 0)),
                'Rr07': piece('R', 'r', (0, 7)),
                'Br02': piece('B', 'r', (0, 2)),
                'Br05': piece('B', 'r', (0, 5)),
                'Nr01': piece('N', 'r', (0, 1)),
                'Nr06': piece('N', 'r', (0, 6)),
                'Qr03': piece('Q', 'r', (0, 3)),
                'Kr04': piece('K', 'r', (0, 4)),
                'Pr10': piece('P', 'r', (1, 0)),
                'Pr11': piece('P', 'r', (1, 1)),
                'Pr12': piece('P', 'r', (1, 2)),
                'Pr13': piece('P', 'r', (1, 3)),
                'Pr14': piece('P', 'r', (1, 4)),
                'Pr15': piece('P', 'r', (1, 5)),
                'Pr16': piece('P', 'r', (1, 6)),
                'Pr17': piece('P', 'r', (1, 7)),
            }

        self.pieces = {**self.pieces_b, **self.pieces_r}

    def place_pieces(self, print_pieces=True):

        self.filled_squares_b = {(i.row, i.col) for i in self.pieces_b.values()}
        self.filled_squares_r = {(i.row, i.col) for i in self.pieces_r.values()}
        self.filled_squares = self.filled_squares_b.union(self.filled_squares_r)

        self.kings_pos = {(i.row, i.col) for i in self.pieces.values() if i.value == 'K'}

        if print_pieces:
            self.board = pd.DataFrame([''] * 8 for i in range(8))
            for i in self.pieces.values(): self.board.iloc[i.row, i.col] = i.id1

    def compute_legal_moves(self):

        for i in self.pieces.values(): i.compute_moves(self)

    def move_piece(self, initial_pos, final_pos, info=False, respect_turn=True, print_pieces=True):

        for i in self.pieces.values():
            if (i.row, i.col) == initial_pos:
                piece = i
                break;
        else: raise ValueError('No existe ninguna pieza en {}'.format(initial_pos))

        piece.move(self, final_pos, info, respect_turn, print_pieces)

    def undo(self, print_pieces=True, print_checks=True):

        self.pieces[self.last_piece].undo_move(self, print_pieces, print_checks)

    def change_turn(self, turn=None):

        if turn != None: self.turn = turn

        if self.turn == 'b': self.turn = 'r'
        elif self.turn == 'r': self.turn = 'b'

    def check_if_check(self):

        self.check = 0

        for i in self.pieces.values():
            if any(x in i.prelegal_moves for x in self.kings_pos):
                self.check = 1
                break

    def check_if_checkmate(self, print_pieces=False, print_checks=True):

        if self.check == 1:

            if self.turn == 'b': pieces_sc = self.pieces_b
            else: pieces_sc = self.pieces_r

            self.check_mate, aux = 1, {}
            for i in pieces_sc:
                new_legal_moves = []
                for movement in pieces_sc[i].legal_moves:
                    pieces_sc[i].move(self, movement, respect_turn=False, real=False)
                    if self.check == 0:
                        self.check_mate = 0
                        new_legal_moves.append(movement)
                    self.check = 1
                    self.undo(print_pieces, print_checks)
                aux[i] = new_legal_moves

            for i in aux: pieces_sc[i].legal_moves = aux[i]
            self.real = True

            if print_checks:
                if self.check_mate: print('Check mate!')
                else: print('Check!')

    def select_piece(self, stgy='random', info=False):

        if stgy == 'random':

            if self.turn == 'b': valid_pieces = self.pieces_b.values()
            else: valid_pieces = self.pieces_r.values()

            valid_pieces2 = [i for i in valid_pieces if len(i.legal_moves) > 0]
            piece = valid_pieces2[randint(0, len(valid_pieces2)-1)]

            if info: print('Se selecciona al azar la pieza de {}'.format((piece.row, piece.col)))

            return piece

        if stgy == 'pro1':

            if self.turn == 'b':
                valid_pieces = self.pieces_b.values()
                s2 = self.filled_squares_r
            else:
                valid_pieces = self.pieces_r.values()
                s2 = self.filled_squares_b

            valid_pieces2 = [i for i in valid_pieces if len(i.legal_moves) > 0]

            better_pieces = []
            for piece in valid_pieces2:
                s1 = set(piece.legal_moves)
                s3 = s1.intersection(s2)
                if s3 != set(): better_pieces.append(piece)

            if better_pieces != []:
                piece = better_pieces[randint(0, len(better_pieces)-1)]
                if info:
                    print('Se selecciona a conciencia la pieza de {}'\
                    .format((piece.row, piece.col)))

            else:
                piece = valid_pieces2[randint(0, len(valid_pieces2) - 1)]
                if info:
                    print('Se selecciona al azar la pieza de {}'.format((piece.row, piece.col)))

            return piece

    def display_board(self):

        display(self.board.style.set_table_styles(
        [{'selector': '*', 'props': [('background-color', 'beige'),
        ('border-color', 'black'), ('border-width', '1px'),
        ('border-style', 'solid'), ('width', '30px'), ('text-align', 'center')]},
        {'selector': 'th', 'props': [('background-color', '#ffe3a9')]}])\
        .applymap(piece_color).applymap(background_color))


class piece ():

    def __init__(self, value, color, position):

        self.value = value
        self.color = color

        self.row = position[0]
        self.col = position[1]

        self.id1 = value + color
        self.id2 = value + color + str(position[0]) + str(position[1])

        self.first_movement = True

    def compute_moves(self, obs):

        if self.value == 'R':

            natural_moves = set([(i, self.col) for i in range(8)]
            + [(self.row, i) for i in range(8)])
            intersections = natural_moves.intersection(obs.filled_squares)

            try: n = max([i[0] for i in intersections if (i[1] == self.col) and (i[0] < self.row)])
            except: n = 0
            try: s = min([i[0] for i in intersections if (i[1] == self.col) and (i[0] > self.row)])
            except: s = 7
            try: w = max([i[1] for i in intersections if (i[0] == self.row) and (i[1] < self.col)])
            except: w = 0
            try: e = min([i[1] for i in intersections if (i[0] == self.row) and (i[1] > self.col)])
            except: e = 7

            if self.color == 'b': filled_squares_sc = obs.filled_squares_b
            else: filled_squares_sc = obs.filled_squares_r

            prelegal_moves = {i for i in natural_moves.difference(filled_squares_sc)
            if n <= i[0] <= s and w <= i[1] <= e}

            legal_moves = prelegal_moves.difference(obs.kings_pos)

            natural_moves = list(natural_moves)
            prelegal_moves = list(prelegal_moves)
            legal_moves = list(legal_moves)

            natural_moves.sort()
            prelegal_moves.sort()
            legal_moves.sort()

            self.natural_moves = natural_moves
            self.prelegal_moves = prelegal_moves
            self.legal_moves = legal_moves

        elif self.value == 'B':

            pre_natural_moves = [(self.row + i, self.col + i) for i in range(1, 8)] \
            + [(self.row + i, self.col - i) for i in range(1, 8)] \
            + [(self.row - i, self.col + i) for i in range(1, 8)] \
            + [(self.row - i, self.col - i) for i in range(1, 8)]

            natural_moves = set([i for i in pre_natural_moves if 0 <= i[0] <= 7 and 0 <= i[1] <= 7])
            intersections = natural_moves.intersection(obs.filled_squares)

            try: nw = max([i for i in intersections if (i[0] < self.row) and (i[1] < self.col)])
            except: nw = (0, 0)
            try: ne = max([i for i in intersections if (i[0] < self.row) and (i[1] > self.col)])
            except: ne = (0, 7)
            try: sw = min([i for i in intersections if (i[0] > self.row) and (i[1] < self.col)])
            except: sw = (7, 0)
            try: se = min([i for i in intersections if (i[0] > self.row) and (i[1] > self.col)])
            except: se = (7, 7)

            if self.color == 'b': filled_squares_sc = obs.filled_squares_b
            else: filled_squares_sc = obs.filled_squares_r

            prelegal_moves = {i for i in natural_moves.difference(filled_squares_sc)
            if not (i[0] < nw[0] and i[1] < nw[1]) and not (i[0] < ne[0] and i[1] > ne[1])
            and not (i[0] > sw[0] and i[1] < sw[1]) and not (i[0] > se[0] and i[1] > se[1])}

            legal_moves = prelegal_moves.difference(obs.kings_pos)

            natural_moves = list(natural_moves)
            prelegal_moves = list(prelegal_moves)
            legal_moves = list(legal_moves)

            natural_moves.sort()
            prelegal_moves.sort()
            legal_moves.sort()

            self.natural_moves = natural_moves
            self.prelegal_moves = prelegal_moves
            self.legal_moves = legal_moves

        elif self.value == 'N':

            pre_natural_moves = [
                (self.row + 2, self.col + 1), (self.row + 2, self.col - 1),
                (self.row - 2, self.col + 1), (self.row - 2, self.col - 1),
                (self.row + 1, self.col + 2), (self.row - 1, self.col + 2),
                (self.row + 1, self.col - 2), (self.row - 1, self.col - 2)
            ]

            natural_moves = set([i for i in pre_natural_moves if 0 <= i[0] <= 7 and 0 <= i[1] <= 7])

            if self.color == 'b': filled_squares_sc = obs.filled_squares_b
            else: filled_squares_sc = obs.filled_squares_r

            prelegal_moves = {i for i in natural_moves.difference(filled_squares_sc)}

            legal_moves = prelegal_moves.difference(obs.kings_pos)

            natural_moves = list(natural_moves)
            prelegal_moves = list(prelegal_moves)
            legal_moves = list(legal_moves)

            natural_moves.sort()
            prelegal_moves.sort()
            legal_moves.sort()

            self.natural_moves = natural_moves
            self.prelegal_moves = prelegal_moves
            self.legal_moves = legal_moves

        elif self.value == 'Q':

            pre_natural_moves = [(self.row + i, self.col + i) for i in range(1, 8)] \
            + [(self.row + i, self.col - i) for i in range(1, 8)] \
            + [(self.row - i, self.col + i) for i in range(1, 8)] \
            + [(self.row - i, self.col - i) for i in range(1, 8)] \
            + [(i, self.col) for i in range(8)] + [(self.row, i) for i in range(8)]

            natural_moves = set([i for i in pre_natural_moves if 0 <= i[0] <= 7 and 0 <= i[1] <= 7])
            intersections = natural_moves.intersection(obs.filled_squares)

            try: n = max([i[0] for i in intersections if (i[1] == self.col) and (i[0] < self.row)])
            except: n = 0
            try: s = min([i[0] for i in intersections if (i[1] == self.col) and (i[0] > self.row)])
            except: s = 7
            try: w = max([i[1] for i in intersections if (i[0] == self.row) and (i[1] < self.col)])
            except: w = 0
            try: e = min([i[1] for i in intersections if (i[0] == self.row) and (i[1] > self.col)])
            except: e = 7
            try: nw = max([i for i in intersections if (i[0] < self.row) and (i[1] < self.col)])
            except: nw = (0, 0)
            try: ne = max([i for i in intersections if (i[0] < self.row) and (i[1] > self.col)])
            except: ne = (0, 7)
            try: sw = min([i for i in intersections if (i[0] > self.row) and (i[1] < self.col)])
            except: sw = (7, 0)
            try: se = min([i for i in intersections if (i[0] > self.row) and (i[1] > self.col)])
            except: se = (7, 7)

            if self.color == 'b': filled_squares_sc = obs.filled_squares_b
            else: filled_squares_sc = obs.filled_squares_r

            prelegal_moves = {i for i in natural_moves.difference(filled_squares_sc)
            if not (i[0] < n and i[1] == self.col) and not (i[0] > s and i[1] == self.col)
            and not (i[1] < w and i[0] == self.row) and not (i[1] > e and i[0] == self.row)
            and not (i[0] < nw[0] and i[1] < nw[1]) and not (i[0] < ne[0] and i[1] > ne[1])
            and not (i[0] > sw[0] and i[1] < sw[1]) and not (i[0] > se[0] and i[1] > se[1])}

            legal_moves = prelegal_moves.difference(obs.kings_pos)

            natural_moves = list(natural_moves)
            prelegal_moves = list(prelegal_moves)
            legal_moves = list(legal_moves)

            natural_moves.sort()
            prelegal_moves.sort()
            legal_moves.sort()

            self.natural_moves = natural_moves
            self.prelegal_moves = prelegal_moves
            self.legal_moves = legal_moves

        elif self.value == 'K':

            pre_natural_moves = [
                (self.row + 1, self.col), (self.row + 1, self.col - 1),
                (self.row + 1, self.col + 1), (self.row - 1, self.col),
                (self.row - 1, self.col - 1), (self.row - 1, self.col + 1),
                (self.row, self.col + 1), (self.row, self.col - 1)
            ]

            natural_moves = set([i for i in pre_natural_moves if 0 <= i[0] <= 7 and 0 <= i[1] <= 7])

            if self.color == 'b': filled_squares_sc = obs.filled_squares_b
            else: filled_squares_sc = obs.filled_squares_r

            prelegal_moves = {i for i in natural_moves.difference(filled_squares_sc)}

            legal_moves = prelegal_moves.difference(obs.kings_pos)

            natural_moves = list(natural_moves)
            prelegal_moves = list(prelegal_moves)
            legal_moves = list(legal_moves)

            natural_moves.sort()
            prelegal_moves.sort()
            legal_moves.sort()

            self.natural_moves = natural_moves
            self.prelegal_moves = prelegal_moves
            self.legal_moves = legal_moves

        elif self.value == 'P':

            if self.color == 'b':
                pre_natural_moves1 = {(self.row - 1, self.col)}
                pre_natural_moves2 = {(self.row - 1, self.col - 1), (self.row - 1, self.col + 1)}

            else:
                pre_natural_moves1 = {(self.row + 1, self.col)}
                pre_natural_moves2 = {(self.row + 1, self.col - 1), (self.row + 1, self.col + 1)}

            if self.first_movement:
                if self.color == 'b':
                    pre_natural_moves1 = pre_natural_moves1.union({(self.row - 2, self.col)})
                else:
                    pre_natural_moves1 = pre_natural_moves1.union({(self.row + 2, self.col)})

            natural_moves1 = {i for i in pre_natural_moves1 if 0 <= i[0] <= 7 and 0 <= i[1] <= 7}
            natural_moves2 = {i for i in pre_natural_moves2 if 0 <= i[0] <= 7 and 0 <= i[1] <= 7}

            if self.color == 'b':
                filled_squares_pro = obs.filled_squares\
                .union({(i[0] - 1, i[1]) for i in obs.filled_squares if i!= (self.row, self.col)})
                filled_squares_dc = obs.filled_squares_r
            else:
                filled_squares_pro = obs.filled_squares\
                .union({(i[0] + 1, i[1]) for i in obs.filled_squares if i!= (self.row, self.col)})
                filled_squares_dc = obs.filled_squares_b

            prelegal_moves =set([i for i in natural_moves1.difference(filled_squares_pro)] \
            + [i for i in natural_moves2.intersection(filled_squares_dc)])

            legal_moves = prelegal_moves.difference(obs.kings_pos)

            natural_moves = list(natural_moves1) + list(natural_moves2)
            prelegal_moves = list(prelegal_moves)
            legal_moves = list(legal_moves)

            natural_moves.sort()
            prelegal_moves.sort()
            legal_moves.sort()

            self.natural_moves = natural_moves
            self.prelegal_moves = prelegal_moves
            self.legal_moves = legal_moves

    def generate_piece_name(self, capital=True):

        if self.value == 'R': nombre = 'La torre'
        elif self.value == 'B': nombre = 'El alfil'
        elif self.value == 'N': nombre = 'El caballo'
        elif self.value == 'Q': nombre = 'La dama'
        elif self.value == 'K': nombre = 'El rey'
        elif self.value == 'P': nombre = 'El peón'

        if capital == False: nombre = nombre.lower()

        return nombre

    def select_move(self, obs, stgy='random'):

        if stgy == 'random':
            new_position = self.legal_moves[randint(0, len(self.legal_moves) - 1)]

        elif stgy == 'pro1':

            s1 = set(self.legal_moves)
            if self.color == 'b': s2 = obs.filled_squares_r
            else: s2 = obs.filled_squares_b
            s3 = s1.intersection(s2)

            if s3 != set():
                lista = list(s3)
                new_position = lista[randint(0, len(lista)-1)]

        return new_position

    def move(self, obs, new_position, info=False, print_pieces=True,
    print_checks=True, respect_turn=True, real=True):

        if respect_turn and self.color != obs.turn:
            raise ValueError('Esa pieza no puede moverse, es el turno de las del otro color.')

        old_position = (self.row, self.col)
        if new_position not in self.legal_moves:
            raise ValueError('Ese no es un movimiento legal.')

        if self.color == 'b':

            if new_position not in obs.filled_squares_r:
                obs.lmwac = False
                if info: print('{} de {} se ha movido a {}'\
                .format(self.generate_piece_name(), old_position, new_position))

            else:
                obs.lmwac = True
                piece_cap = [i for i in obs.pieces_r if
                (obs.pieces[i].row, obs.pieces[i].col) == new_position][0]
                if info: print('{} de {} ha capturado {} de {}'\
                .format(self.generate_piece_name(), old_position,
                obs.pieces_r[piece_cap].generate_piece_name(False), new_position))

                obs.cap_piece_name = piece_cap
                obs.cap_piece_object = obs.pieces_r[piece_cap]
                obs.pieces_r = dict(((i, obs.pieces_r[i]) for i in obs.pieces_r if i != piece_cap))
                obs.pieces = {**obs.pieces_b, **obs.pieces_r}

        elif self.color == 'r':

            if new_position not in obs.filled_squares_b:
                obs.lmwac = False
                if info: print('{} de {} se ha movido a {}'\
                .format(self.generate_piece_name(), old_position, new_position))

            else:
                obs.lmwac = True
                piece_cap = [i for i in obs.pieces_b if
                (obs.pieces[i].row, obs.pieces[i].col) == new_position][0]
                if info: print('{} de {} ha capturado {} de {}'\
                .format(self.generate_piece_name(), old_position,
                obs.pieces_b[piece_cap].generate_piece_name(False), new_position))

                obs.cap_piece_name = piece_cap
                obs.cap_piece_object = obs.pieces_b[piece_cap]
                obs.pieces_b = dict(((i, obs.pieces_b[i]) for i in obs.pieces_b if i != piece_cap))
                obs.pieces = {**obs.pieces_b, **obs.pieces_r}

        obs.last_piece = list(obs.pieces.keys())[list(obs.pieces.values()).index(self)]
        obs.last_position = old_position
        obs.last_first_movement = self.first_movement

        self.row, self.col = new_position[0], new_position[1]
        if self.first_movement: self.first_movement = False

        obs.change_turn(self.color)
        obs.place_pieces(print_pieces)
        obs.compute_legal_moves()
        obs.check_if_check()
        if real: obs.check_if_checkmate(print_pieces, print_checks)

    def undo_move(self, obs, print_pieces=True, print_checks=True):

        self.row, self.col = obs.last_position[0], obs.last_position[1]
        self.first_movement = obs.last_first_movement

        if obs.lmwac == True:

            if obs.cap_piece_object.color == 'b':
                obs.pieces_b[obs.cap_piece_name] = obs.cap_piece_object
            elif obs.cap_piece_object.color == 'r':
                obs.pieces_r[obs.cap_piece_name] = obs.cap_piece_object

            obs.pieces = {**obs.pieces_b, **obs.pieces_r}

        obs.change_turn(self.color)
        obs.place_pieces(print_pieces)
        obs.compute_legal_moves()


class agent():

    def __init__(self, color, stgy_selection='random', stgy_move='random', info=False):

        self.color = color
        self.stgy_selection = stgy_selection
        self.stgy_move = stgy_move
        self.info = info

    def play(self, obs):

        if self.color == obs.turn:

            piece = obs.select_piece(self.stgy_selection, self.info)
            new_position = piece.select_move(obs, self.stgy_move)
            piece.move(obs, new_position, info=self.info)

        else: print('No puedes jugar ahora, no es tu turno')


def piece_color(value):

    if value == '': color = 'beige'
    else: color = 'black'

    return 'color: %s' % color


def background_color(value):

    if value == '': color = 'beige'
    elif value[-1] == 'b': color = '#ade9ff'
    elif value[-1] == 'r': color = '#ffadad'

    return 'background-color: %s' % color

