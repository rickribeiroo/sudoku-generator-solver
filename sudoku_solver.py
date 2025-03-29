import pandas as pd
import matplotlib.pyplot as plt

# initial config
plt.switch_backend('TkAgg')
plt.ion()
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xticks([])
ax.set_yticks([])
ax.set_title('Solving Sudoku...', fontsize=14, pad=10)

# visuals
texts = [[ax.text(j + 0.5, 8.5 - i, '',
                  ha='center',
                  va='center',
                  fontsize=14) for j in range(9)] for i in range(9)]

# draw grid
for i in range(10):
    lw = 2 if i % 3 == 0 else 0.5
    ax.axhline(i, color='black', lw=lw)
    ax.axvline(i, color='black', lw=lw)
# limit adjustments
ax.set_xlim(0, 9)
ax.set_ylim(0, 9)
plt.tight_layout()

def update_board(df):
    for i in range(9):
        for j in range(9):
            num = df.iloc[i, j]
            texts[i][j].set_text(str(num) if num != 0 else '')
            texts[i][j].set_color('black' if num != 0 else 'gray')
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.02)

class box:
    number = int
    possible_numbers = []
    position = []
    def __init__(self, row, col, number = 0, possible_numbers = []):
        self.possible_numbers = possible_numbers
        self.number = number
        self.position = [row, col]
    def __repr__(self):
        return f"pos {self.position} -> {self.possible_numbers}"

def number_is_valid(df, number, row, col):
    if number in df.iloc[row,:].values or number in df.iloc[:,col].values:
        return False
    row_quadrant = (row // 3) * 3
    col_quadrant = (col // 3) * 3
    quadrant = df.iloc[row_quadrant:row_quadrant + 3, col_quadrant:col_quadrant + 3]
    return number not in quadrant.values

def get_quadrant(df, row, col):
    quad_row = 3 * (row // 3)
    quad_col = 3 * (col // 3)
    return df.iloc[quad_row:quad_row + 3, quad_col:quad_col + 3].values.flatten()

def select_possible_numbers(df):
    solver_positions = []
    all_numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    for row in range(9):
        for col in range(9):
            print(row,col)
            if df.iloc[row, col] == 0:
                used_in_row = set(df.iloc[row, :])
                used_in_col = set(df.iloc[:, col])
                used_in_quad = set(get_quadrant(df, row, col))
                used_numbers = used_in_row | used_in_col | used_in_quad

                possible_numbers = list(all_numbers - used_numbers)
                print(used_numbers)
                solver_positions.append(box(row, col, possible_numbers=possible_numbers))
    # sort by possible numbers
    solver_positions.sort(key=lambda x: len(x.possible_numbers))
    return solver_positions

def solver(df, solver_positions, position=0):
    print(position)
    if position >= len(solver_positions):
        update_board(df)
        return True
    # box position (x,y) in table
    cell = solver_positions[position]
    x, y = cell.position[0], cell.position[1]

    for num in list(cell.possible_numbers):
        if number_is_valid(df, num, x, y):
            previous_state = {
                'cell_value': df.iloc[x, y],
                'removed_from': []
            }

            df.iloc[x, y] = num
            update_board(df)
            texts[x][y].set_color('blue')
            fig.canvas.draw()
            plt.pause(0.1)

            # remove cell numbers (temporally)
            related_cells = [
                c for c in solver_positions
                if (c.position[0] == x or c.position[1] == y or
                    (c.position[0] // 3 == x // 3 and c.position[1] // 3 == y // 3))
            ]

            for related in related_cells:
                if num in related.possible_numbers:
                    previous_state['removed_from'].append(related)
                    related.possible_numbers.remove(num)

            solver_positions_sorted = sorted(
                solver_positions[position + 1:],
                key=lambda cell: len(cell.possible_numbers))

            new_positions = solver_positions[:position + 1] + solver_positions_sorted

            if solver(df, new_positions, position + 1):
                return True
            df.iloc[x, y] = previous_state['cell_value']

            texts[x][y].set_color('red')
            update_board(df)
            plt.pause(0.2)
            texts[x][y].set_color('black')

            for related in previous_state['removed_from']:
                if num not in related.possible_numbers:
                    related.possible_numbers.append(num)
            solver_positions.sort(key=lambda cell: len(cell.possible_numbers))
    return False


if __name__ == "__main__":
    df = pd.read_csv("table.csv", header=None)
    update_board(df)

    solver_positions = select_possible_numbers(df)
    try:
        if solver(df, solver_positions):
            print("Solution found!")
            df.to_csv("solution.csv", header=None, index=None)
            plt.ioff()
            plt.show()
        else:
            print("No solution found!")
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário!")
        plt.ioff()