from tkinter import *
from cell import Cell, create_mine_count_label
import settings

# setting window instance
window = Tk()
window.title("Minesweeper")
window.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
window.resizable(False, False)  # the first one for blocking adjusting width, the second for height

top_frame = Frame(window, bg="green", width=settings.WIDTH, height=settings.TOP_HEIGHT)
top_frame.place(x=0, y=0)
game_frame = Frame(window, bg="#43b561", width=settings.WIDTH, height=settings.HEIGHT - settings.TOP_HEIGHT)
game_frame.place(x=0, y=settings.TOP_HEIGHT)

for column in range(settings.GRID_SIZE):
    for row in range(settings.GRID_SIZE):
        c = Cell(column, row)
        c.create_button(game_frame)
        c.cell_button.grid(column=column, row=row)

# Cell.generate_mines()
mine_count_label = create_mine_count_label(top_frame)
Cell.mines_left_label.place(x=0, y=0)
# run the game
window.mainloop()
