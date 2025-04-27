import sys

import time, math
import lib.stddraw as stddraw
from lib.color import Color
from point import Point
import numpy as np


class GameGrid:
    def __init__(self, grid_h, grid_w):
        self.grid_height = grid_h
        self.grid_width = grid_w
        self.tile_matrix = np.full((grid_h, grid_w), None)
        self.current_tetromino = None
        self.game_over = False
        self.game_won = False
        self.score = 0
        self.doubled = False
        self.quadrupled = False
        self.empty_cell_color = Color(54, 15, 80)
        self.line_color = Color(138 , 43, 226)
        self.boundary_color = Color(186, 85, 211)
        self.line_thickness = 0.002
        self.box_thickness = 10 * self.line_thickness
        self.animating_tiles = {}
        self.blink_duration = 0.4
        self.blink_highlight = Color(255, 87, 34)
        self.blink_scale_amt = 0.15

    def display(self):
        stddraw.clear(self.empty_cell_color)
        self.draw_grid()
        if self.current_tetromino is not None:
            self.current_tetromino.draw()
        self.draw_boundaries()
        self.draw_score()
        stddraw.show(0)

    def draw_grid(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.tile_matrix[row][col] is not None:
                    self.tile_matrix[row][col].draw(Point(col, row))
        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
        start_x, end_x = -0.5, self.grid_width - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5
        for x in np.arange(start_x + 1, end_x, 1):  
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1): 
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()  

    def draw_boundaries(self):
        stddraw.setPenColor(self.boundary_color)  # using boundary_color
        stddraw.setPenRadius(self.box_thickness)
        pos_x, pos_y = -0.5, -0.5
        stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
        stddraw.setPenRadius()


    def is_occupied(self, row, col):
        if not self.is_inside(row, col):
            return False  
        return self.tile_matrix[row][col] is not None

    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True
    
    def update_grid(self, tiles_to_lock, blc_position):
        self.current_tetromino
        n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
        for col in range(n_cols):
            for row in range(n_rows):
                if tiles_to_lock[row][col] is not None:
                   pos = Point()
                   pos.x = blc_position.x + col
                   pos.y = blc_position.y + (n_rows - 1) - row
                   if self.is_inside(pos.y, pos.x):
                      self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
                   else:
                       self.game_over = True
        self.clear_and_move_down_rows()
        return self.game_over               



    def draw_score(self):
        stddraw.setFontSize(28)
        stddraw.setPenColor(stddraw.YELLOW)
        stddraw.setFontFamily("Arial")
        score_pos_x = self.grid_width - 2
        score_pos_y = self.grid_height - 1
        stddraw.text(score_pos_x, score_pos_y, "score: " + str(self.score))

    def update_score(self, points):
        self.score += points 
        if self.score >= 200 and not self.doubled:
            self.double_tiles_value() 
            self.doubled = True  

        elif self.score >= 16000 and not self.quadrupled:
            self.double_tiles_value()
            self.quadrupled = True 


    def delete_free_tiles_and_update_score(self):
        for col in range(self.grid_width): 
            conqat = [False] * self.grid_height 
            for row in range(self.grid_height - 1, -1, -1):
                if self.tile_matrix[row][col] is not None:
                    if row == self.grid_height - 1 or conqat[row + 1]: 
                        conqat[row] = True
                    else:
                        self.update_score(self.tile_matrix[row][col].number)
                        self.tile_matrix[row][col] = None


    def clear_and_move_down_rows(self):
        rows_cleared = 0
        for row in range(self.grid_height):
            if all(self.tile_matrix[row]):  
                rows_cleared += 1
            elif rows_cleared > 0:  
                self.tile_matrix[row - rows_cleared] = self.tile_matrix[row].copy()
                self.tile_matrix[row] = [None] * self.grid_width 

        self.score += rows_cleared * 100

    def merge_tiles(self):
        for col in range(self.grid_width):
            row = 0  
            while row < self.grid_height - 1: 
                current_tile = self.tile_matrix[row][col]
                above_tile = self.tile_matrix[row + 1][col]

                if current_tile is not None and above_tile is not None:
                    if current_tile.number == above_tile.number:
                        merged_number = current_tile.number * 2
                        current_tile.number = merged_number
                        self.tile_matrix[row + 1][col] = None  
                        self.update_score(merged_number)  

                        for r in range(row + 1, self.grid_height - 1):
                            self.tile_matrix[r][col] = self.tile_matrix[r + 1][col]
                        self.tile_matrix[self.grid_height - 1][col] = None
                row += 1  
        self.check_win()



    def label_components(self):
        label_count = 1
        labels = {}

        for col in range(self.grid_width):
            for row in range(self.grid_height):
                if self.tile_matrix[row][col] is not None and (row, col) not in labels:
                    self.flood_fill(row, col, label_count, labels)
                    label_count += 1
        return labels


    def flood_fill(self, row, col, label, labels):
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            if (r, c) not in labels and self.tile_matrix[r][c] is not None:
                labels[(r, c)] = label
                if r > 0: stack.append((r - 1, c))
                if r < self.grid_height - 1: stack.append((r + 1, c))
                if c > 0: stack.append((r, c - 1))
                if c < self.grid_width - 1: stack.append((r, c + 1))


    def move_down_components(self, labels):
        for label in set(labels.values()):
            component = [loc for loc, lbl in labels.items() if lbl == label]
            min_row = min(r for r, c in component)
            if min_row == 0 or all(self.tile_matrix[r - 1][c] is not None for r, c in component):
                continue
            for r, c in component:
                self.tile_matrix[r][c], self.tile_matrix[r - 1][c] = None, self.tile_matrix[r][c]



    def double_tiles_value(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.tile_matrix[row][col] is not None: 
                    self.tile_matrix[row][col].number *= 2
                    self.tile_matrix[row][col].update_colors()


    def check_win(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.tile_matrix[row][col] is not None and self.tile_matrix[row][col].number == 2048:
                    self.game_won = True
                    self.draw_game_won()
                    return True
        return False 

    def draw_game_won(self):
        while True:
            stddraw.clear(self.empty_cell_color)
            stddraw.setFontSize(30)
            stddraw.setFontFamily("Arial")
            stddraw.setPenColor(stddraw.YELLOW)
            stddraw.text(self.grid_width / 2, self.grid_height / 2 + 3, "Congratulations! You reached 2048!")

            button_width = self.grid_width / 4
            button_height = 2
            button_spacing = 3

            restart_button_x = self.grid_width / 2 - button_width / 2
            restart_button_y = self.grid_height / 2 - button_spacing
            stddraw.setPenColor(Color(25, 255, 228))
            stddraw.filledRectangle(restart_button_x, restart_button_y, button_width, button_height)
            stddraw.setPenColor(Color(31, 160, 239))
            stddraw.text(restart_button_x + button_width / 2, restart_button_y + button_height / 2, "Restart")

            exit_button_x = self.grid_width / 2 - button_width / 2
            exit_button_y = self.grid_height / 2 - 2 * button_spacing
            stddraw.setPenColor(Color(25, 255, 228))
            stddraw.filledRectangle(exit_button_x, exit_button_y, button_width, button_height)
            stddraw.setPenColor(Color(31, 160, 239))
            stddraw.text(exit_button_x + button_width / 2, exit_button_y + button_height / 2, "Exit")

            stddraw.show(50)

            if stddraw.mousePressed():
                mx, my = stddraw.mouseX(), stddraw.mouseY()

                if restart_button_x <= mx <= restart_button_x + button_width and restart_button_y <= my <= restart_button_y + button_height:
                    print("Restart button clicked.")
                    self.reset_game()
                    break

                elif exit_button_x <= mx <= exit_button_x + button_width and exit_button_y <= my <= exit_button_y + button_height:
                    print("Exit button clicked.")

    def reset_game(self):
        self.game_over = False
        self.game_won = False
        self.score = 0
        self.tile_matrix = np.full((self.grid_height, self.grid_width), None)
        self.display()  


pass