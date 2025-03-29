import random, pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# initial configuration
plt.switch_backend('TkAgg')
plt.ion()
fig, ax = plt.subplots(figsize=(6, 6))  # window size
ax.set_xticks([])
ax.set_yticks([])
ax.set_title('Generating Sudoku...', fontsize=14, pad=10)

texts = [[ax.text(j + 0.5, 8.5 - i, '', # numbers position
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


def update_board(df, current_pos=None, is_backtrack=False):
    for i in range(9):
        for j in range(9):
            num = df.iloc[i, j]
            texts[i][j].set_text(str(num) if num != 0 else '')

            if current_pos and (i, j) == current_pos:
                color = 'red' if is_backtrack else 'blue'
                texts[i][j].set_color(color)
            else:
                texts[i][j].set_color('black' if num != 0 else 'gray')

    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.02)

def eliminate_numbers(complete_table, n):
    # Cria uma cópia para modificar
    final_table = complete_table.copy()
    positions = [(i, j) for i in range(9) for j in range(9)]

    random.shuffle(positions)
    random.seed(n)
    random.shuffle(positions)

    removed = 0
    for i, j in positions:
        if removed >= n:
            break

        if final_table.iloc[i, j] != 0:

            # Remove temporariamente
            final_table.iloc[i, j] = 0

            removed += 1

    return final_table

def number_is_valid(df, number, row, col):
    if number in df.iloc[row,:].values or number in df.iloc[:,col].values:
        return False
    row_quadrant = (row // 3) * 3
    col_quadrant = (col // 3) * 3
    quadrant = df.iloc[row_quadrant:row_quadrant + 3, col_quadrant:col_quadrant + 3]
    return number not in quadrant.values

def create_sudoku(df, position=0):
    if position >= 81:
        update_board(df)
        return True

    x  = position // 9
    y = position % 9
    current_pos = (x, y)
    if df.iloc[x, y] != 0:
        return create_sudoku(df, position + 1)

    numbers = random.sample(range(1, 10), 9)

    for num in numbers:
        if number_is_valid(df, num, x, y):
            df.iloc[x, y] = num
            update_board(df,current_pos=current_pos)
            if create_sudoku(df, position + 1):
                return True

            # Backtracking
            df.iloc[x, y] = 0  # cell reset
            update_board(df,current_pos=current_pos,is_backtrack=True)
    return False

if __name__ == "__main__":
    # create a board with zeros using NxN board
    n = 9
    df = pd.DataFrame(np.zeros((n, n), dtype=int))
    update_board(df)

    # generate sudoku
    try:
        if create_sudoku(df):
            df.to_csv("complete_table.csv", header=None, index=None)
            df = eliminate_numbers(df, 43) # CHANGE 'n' TO CHANGE THE DIFICULTY
            #   Easy -> 31 ~ 36
            #   Medium -> 37 ~ 45
            #   Hard -> 46 ~ 51+
            df.to_csv("table.csv", header=None, index=None)
        else:
            print("Error creating sudoku!")
        plt.ioff()
        plt.show()
    except KeyboardInterrupt:
        print("\nInterrupted by user!")
        plt.ioff()