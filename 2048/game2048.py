import random
import copy  # 追加

class Game2048:
    def __init__(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()
        self.game_over = False

    def add_random_tile(self):
        empty_positions = [(r, c) for r in range(4) for c in range(4) if self.board[r][c] == 0]
        if empty_positions:
            r, c = random.choice(empty_positions)
            self.board[r][c] = 2 if random.random() < 0.9 else 4

    def compress(self, mat):
        new_mat = [[0] * 4 for _ in range(4)]
        for r in range(4):
            pos = 0
            for c in range(4):
                if mat[r][c] != 0:
                    new_mat[r][pos] = mat[r][c]
                    pos += 1
        return new_mat

    def merge(self, mat):
        for r in range(4):
            for c in range(3):
                if mat[r][c] == mat[r][c + 1] and mat[r][c] != 0:
                    mat[r][c] *= 2
                    self.score += mat[r][c]  # スコアを加算
                    mat[r][c + 1] = 0
        return mat

    def reverse(self, mat):
        return [row[::-1] for row in mat]

    def transpose(self, mat):
        return [list(row) for row in zip(*mat)]

    def move_left(self):
        self.board = self.compress(self.board)
        self.board = self.merge(self.board)
        self.board = self.compress(self.board)

    def move_right(self):
        self.board = self.reverse(self.board)
        self.move_left()
        self.board = self.reverse(self.board)

    def move_up(self):
        self.board = self.transpose(self.board)
        self.move_left()
        self.board = self.transpose(self.board)

    def move_down(self):
        self.board = self.transpose(self.board)
        self.move_right()
        self.board = self.transpose(self.board)

    def move(self, direction):
        if self.game_over:
            return

        prev_board = [row[:] for row in self.board]  # 現在のボードのコピー

        if direction == 'left':
            self.move_left()
        elif direction == 'right':
            self.move_right()
        elif direction == 'up':
            self.move_up()
        elif direction == 'down':
            self.move_down()

        # ボードが変化した場合のみタイルを追加
        if self.board != prev_board:
            self.add_random_tile()
            self.game_over = self.check_game_over()

    def check_game_over(self):
        # 空きタイルが存在する場合はゲームオーバーではない
        if any(0 in row for row in self.board):
            return False

        # 隣接するタイルに同じ値があればゲームオーバーではない
        for r in range(4):
            for c in range(3):
                if self.board[r][c] == self.board[r][c + 1] or self.board[c][r] == self.board[c + 1][r]:
                    return False

        return True

    def get_state(self):
        return {
            'board': self.board,
            'score': self.score,
            'game_over': self.game_over
        }

    def copy(self):
        # 現在のゲーム状態をコピーするメソッド
        new_game = Game2048()
        new_game.board = copy.deepcopy(self.board)  # ディープコピーを使用
        new_game.score = self.score
        new_game.game_over = self.game_over
        return new_game
