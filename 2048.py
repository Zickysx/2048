import tkinter as tk
import random

SIZE = 4
CELL_SIZE = 100
BACKGROUND_COLOR = "#bbada0"
EMPTY_CELL_COLOR = "#cdc1b4"

COLORS = {
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e"
}


class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048")

        self.score = 0

        self.main_frame = tk.Frame(
            root,
            bg=BACKGROUND_COLOR,
            bd=10
        )
        self.main_frame.grid()

        self.cells = []
        self.board = [[0] * SIZE for _ in range(SIZE)]

        self.create_grid()
        self.add_new_tile()
        self.add_new_tile()
        self.update_grid()

        self.root.bind("<Key>", self.handle_keys)

    def create_grid(self):
        for row in range(SIZE):
            row_cells = []

            for col in range(SIZE):
                frame = tk.Frame(
                    self.main_frame,
                    bg=EMPTY_CELL_COLOR,
                    width=CELL_SIZE,
                    height=CELL_SIZE
                )
                frame.grid(row=row, column=col, padx=5, pady=5)

                label = tk.Label(
                    frame,
                    text="",
                    bg=EMPTY_CELL_COLOR,
                    justify=tk.CENTER,
                    font=("Arial", 24, "bold"),
                    width=4,
                    height=2
                )
                label.pack(expand=True, fill="both")

                row_cells.append(label)

            self.cells.append(row_cells)

    def add_new_tile(self):
        empty = []

        for row in range(SIZE):
            for col in range(SIZE):
                if self.board[row][col] == 0:
                    empty.append((row, col))

        if not empty:
            return

        row, col = random.choice(empty)
        self.board[row][col] = 2 if random.random() < 0.9 else 4

    def update_grid(self):
        for row in range(SIZE):
            for col in range(SIZE):
                number = self.board[row][col]

                if number == 0:
                    self.cells[row][col].configure(
                        text="",
                        bg=EMPTY_CELL_COLOR
                    )
                else:
                    self.cells[row][col].configure(
                        text=str(number),
                        bg=COLORS.get(number, "#3c3a32"),
                        fg="white" if number > 4 else "black"
                    )

        self.root.update_idletasks()

    def compress(self, row):
        new_row = [num for num in row if num != 0]
        new_row += [0] * (SIZE - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(SIZE - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                row[i + 1] = 0
                self.score += row[i]
        return row

    def move_left(self):
        changed = False

        new_board = []

        for row in self.board:
            compressed = self.compress(row)
            merged = self.merge(compressed)
            final = self.compress(merged)

            new_board.append(final)

            if final != row:
                changed = True

        self.board = new_board
        return changed

    def move_right(self):
        self.board = [row[::-1] for row in self.board]
        changed = self.move_left()
        self.board = [row[::-1] for row in self.board]
        return changed

    def transpose(self):
        self.board = [list(row) for row in zip(*self.board)]

    def move_up(self):
        self.transpose()
        changed = self.move_left()
        self.transpose()
        return changed

    def move_down(self):
        self.transpose()
        changed = self.move_right()
        self.transpose()
        return changed

    def handle_keys(self, event):
        key = event.keysym

        moved = False

        if key == "Left":
            moved = self.move_left()

        elif key == "Right":
            moved = self.move_right()

        elif key == "Up":
            moved = self.move_up()

        elif key == "Down":
            moved = self.move_down()

        if moved:
            self.add_new_tile()
            self.update_grid()

            if self.check_win():
                self.show_message("Ты победил!")

            elif self.check_game_over():
                self.show_message("Игра окончена!")

    def check_win(self):
        for row in self.board:
            if 2048 in row:
                return True
        return False

    def check_game_over(self):
        for row in range(SIZE):
            for col in range(SIZE):

                if self.board[row][col] == 0:
                    return False

                if col < SIZE - 1 and self.board[row][col] == self.board[row][col + 1]:
                    return False

                if row < SIZE - 1 and self.board[row][col] == self.board[row + 1][col]:
                    return False

        return True

    def show_message(self, text):
        popup = tk.Toplevel()
        popup.title("2048")

        label = tk.Label(
            popup,
            text=text,
            font=("Arial", 20)
        )
        label.pack(padx=20, pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()