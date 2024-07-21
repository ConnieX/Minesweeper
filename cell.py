from tkinter import Button, Label, messagebox
from ctypes import cdll
import random
import settings
import itertools
import sys


def create_mine_count_label(location):
    Cell.mines_left_label = Label(location, text=f"Mines left: {Cell.mines_left}", bg='green')


class Cell:
    all = []
    first_click = True
    mines_left = settings.MINE_COUNT
    mines_left_label = None
    cells_left = settings.GRID_SIZE ** 2 - settings.MINE_COUNT

    def __init__(self, x, y, is_mine=False):
        self.x = x
        self.y = y
        self.is_mine = is_mine
        self.cell_button = None
        self.cell_number = 0
        self.opened = False
        self.mine_candidate = False
        Cell.all.append(self)

    def create_button(self, location):
        self.cell_button = Button(location, width=3, height=2, bg='#43b561', activebackground='#91e6a7')
        self.cell_button.bind('<Button-1>', self.left_click_actions)  # <Button-1> is left click
        self.cell_button.bind('<Button-3>', self.right_click_actions)  # <Button-3> is right click

    def left_click_actions(self, event):
        if Cell.first_click:
            self.generate_mines(self.x, self.y)
            Cell.first_click = False
        if self.mine_candidate:
            return
        if self.is_mine:
            self.kaboom()
        else:
            self.show_cell()
        if Cell.cells_left == 0:
            messagebox.showinfo("WINNER", "You discovered all mines! You win.")
            sys.exit()

    def right_click_actions(self, _):
        if not self.mine_candidate:
            self.mine_candidate = True
            self.cell_button.configure(bg='orange')
            Cell.mines_left -= 1
            Cell.mines_left_label.configure(text=f"Mines left: {Cell.mines_left}")
        else:
            self.mine_candidate = False
            self.cell_button.configure(bg='#43b561')
            Cell.mines_left += 1
            Cell.mines_left_label.configure(text=f"Mines left: {Cell.mines_left}")


    def kaboom(self):
        # interrupt a game and display a message that player lost
        self.cell_button.configure(bg='red')
        messagebox.showinfo("Game Over", "You clicked on a mine! Game Over.")
        sys.exit()

    def show_cell(self):
        self.cell_button.configure(text=self.cell_number)
        self.opened = True
        Cell.cells_left -= 1

        if self.cell_button.cget('bg') == 'orange':
            Cell.mines_left += 1
            Cell.mines_left_label.configure(text=f"Mines left: {Cell.mines_left}")

        self.cell_button.configure(bg='#91e6a7')
        if self.cell_number == 0:
            positions = [[x, y] for x, y in
                         (itertools.product([self.x - 1, self.x, self.x + 1], [self.y - 1, self.y, self.y + 1]))
                         if settings.GRID_SIZE > x >= 0 and settings.GRID_SIZE > y >= 0]
            for cell_pos in positions:
                surrounding_cell = self.get_cell_by_position(cell_pos[0], cell_pos[1])
                if not surrounding_cell.opened:
                    surrounding_cell.show_cell()

    def get_cell_by_position(self, x, y):
        return Cell.all[x * settings.GRID_SIZE + y]

    @staticmethod
    def generate_mines(banned_x, banned_y):
        banned_positions = [[x, y] for x, y in
                            (itertools.product([banned_x - 1, banned_x, banned_x + 1],
                                               [banned_y - 1, banned_y, banned_y + 1]))
                            if settings.GRID_SIZE > x >= 0 and settings.GRID_SIZE > y >= 0]
        available_cells = [cell for cell in Cell.all if [cell.x, cell.y] not in banned_positions]
        picked_cells = random.sample(available_cells, settings.MINE_COUNT)
        for cell in picked_cells:
            cell.is_mine = True
            positions = [[x, y] for x, y in
                         (itertools.product([cell.x - 1, cell.x, cell.x + 1], [cell.y - 1, cell.y, cell.y + 1]))
                         if settings.GRID_SIZE > x >= 0 and settings.GRID_SIZE > y >= 0]
            for cell_pos in positions:
                updated_cell = cell.get_cell_by_position(cell_pos[0], cell_pos[1])
                updated_cell.cell_number += 1

    # redefine how cell is represented
    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
