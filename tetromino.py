from tile import Tile  # used for modeling each tile on the tetrominoes
from point import Point  # used for tile positions
import copy as cp  # the copy module is used for copying tiles and positions
import random  # the random module is used for generating random values
import numpy as np  # the fundamental Python module for scientific computing

# A class for modeling tetrominoes with 7 different types as I, O, Z, S, L, J and T
class Tetromino:
   # the dimensions of the game grid (defined as class variables)
   grid_height, grid_width = None, None
   tetromino_types = ['I', 'O', 'Z', 'S', 'L', 'J', 'T']

   # A constructor for creating a tetromino with a given shape (type)
   def __init__(self, shape):
      self.type = shape  # set the type of this tetromino
      # determine the occupied (non-empty) cells in the tile matrix based on
      # the shape of this tetromino (see the documentation given with this code)
      occupied_cells = []
      if self.type == 'I':
         n = 4  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino I in its initial rotation state
         occupied_cells.append((1, 0))  # (column_index, row_index)
         occupied_cells.append((1, 1))
         occupied_cells.append((1, 2))
         occupied_cells.append((1, 3))
      elif self.type == 'O':
         n = 2  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino O in its initial rotation state
         occupied_cells.append((0, 0))  # (column_index, row_index)
         occupied_cells.append((1, 0))
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
      elif self.type == 'Z':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino Z in its initial rotation state
         occupied_cells.append((0, 1))  # (column_index, row_index)
         occupied_cells.append((1, 1))
         occupied_cells.append((1, 2))
         occupied_cells.append((2, 2))
      elif self.type == 'J':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino J in its initial rotation state
         occupied_cells.append((0, 0))  # (column_index, row_index)
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
         occupied_cells.append((2, 1))
      elif self.type == 'L':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino L in its initial rotation state
         occupied_cells.append((2, 0))  # (column_index, row_index)
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
         occupied_cells.append((2, 1))
      elif self.type == 'S':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino S in its initial rotation state
         occupied_cells.append((1, 0))  # (column_index, row_index)
         occupied_cells.append((2, 0))
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
      elif self.type == 'T':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino T in its initial rotation state
         occupied_cells.append((1, 0))  # (column_index, row_index)
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
         occupied_cells.append((2, 1))
      # create a matrix of numbered tiles based on the shape of this tetromino
      self.tile_matrix = np.full((n, n), None)
      # create the four tiles (minos) of this tetromino and place these tiles
      # into the tile matrix
      for col_index, row_index in occupied_cells:
         # assign a random number (2 or 4) to each tile in the tetromino
         self.tile_matrix[row_index][col_index] = Tile(random.choice([2, 4]))
      # initialize the position of this tetromino (as the bottom left cell in
      # the tile matrix) with a random horizontal position above the game grid
      self.bottom_left_cell = Point()
      self.bottom_left_cell.y = Tetromino.grid_height - 1
      self.bottom_left_cell.x = random.randint(0, Tetromino.grid_width - n)

   # A method that computes and returns the position of the cell in the tile
   # matrix specified by the given row and column indexes
   def get_cell_position(self, row, col):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      position = Point()
      # horizontal position of the cell
      position.x = self.bottom_left_cell.x + col
      # vertical position of the cell
      position.y = self.bottom_left_cell.y + (n - 1) - row
      return position

   # A method to return a copy of the tile matrix without any empty row/column,
   # and the position of the bottom left cell when return_position is set
   def get_min_bounded_tile_matrix(self, return_position=False):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      # determine rows and columns to copy (omit empty rows and columns)
      min_row, max_row, min_col, max_col = n - 1, 0, n - 1, 0
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] is not None:
               if row < min_row:
                  min_row = row
               if row > max_row:
                  max_row = row
               if col < min_col:
                  min_col = col
               if col > max_col:
                  max_col = col
      # copy the tiles from the tile matrix of this tetromino
      copy = np.full((max_row - min_row + 1, max_col - min_col + 1), None)
      for row in range(min_row, max_row + 1):
         for col in range(min_col, max_col + 1):
            if self.tile_matrix[row][col] is not None:
               row_ind = row - min_row
               col_ind = col - min_col
               copy[row_ind][col_ind] = cp.deepcopy(self.tile_matrix[row][col])
      # return just the matrix copy when return_position is not set (as True)
      # the argument return_position defaults to False when a value is not given
      if not return_position:
         return copy
      # otherwise return the position of the bottom left cell in copy as well
      else:
         blc_position = cp.copy(self.bottom_left_cell)
         blc_position.translate(min_col, (n - 1) - max_row)
         return copy, blc_position

   # A method for drawing the tetromino on the game grid
   def draw(self):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      for row in range(n):
         for col in range(n):
            # draw each occupied cell as a tile on the game grid
            if self.tile_matrix[row][col] is not None:
               # get the position of the tile
               position = self.get_cell_position(row, col)
               # draw only the tiles that are inside the game grid
               if position.y < Tetromino.grid_height:
                  self.tile_matrix[row][col].draw(position)

   # A method for moving this tetromino in a given direction by 1 on the grid
   def move(self, direction, game_grid):
      # check if this tetromino can be moved in the given direction by using
      # the can_be_moved method defined below
      if not (self.can_be_moved(direction, game_grid)):
         return False  # the tetromino cannot be moved in the given direction
      # move this tetromino by updating the position of its bottom left cell
      if direction == "left":
         self.bottom_left_cell.x -= 1
      elif direction == "right":
         self.bottom_left_cell.x += 1
      else:  # direction == "down"
         self.bottom_left_cell.y -= 1
      return True  # a successful move in the given direction

   # A method that is used for rotating every tetromino in clock-wise direction by 90 degree
   def rotate(self, game_grid):
      # skip rotation for the 'O' shape since it looks the same after rotation
      if self.type == 'O':
         return False
      # create a temporary rotated version of the tile matrix (90 degrees clockwise)
      rotated_matrix = np.rot90(self.tile_matrix, -1)
      n = len(rotated_matrix)
      # check if the rotated tetromino would fit on the grid without collisions
      for row in range(n):
         for col in range(n):
            if rotated_matrix[row][col] is not None:
               pos = self.get_cell_position(row, col)
               # check if the position is inside the grid and not occupied
               if not game_grid.is_inside(pos.y, pos.x) or game_grid.is_occupied(pos.y, pos.x):
                  return False  # rotation not possible due to collision or out of bounds
      # if all positions are valid, update the tile matrix to the rotated one
      self.tile_matrix = rotated_matrix
      return True  # rotation successful

   # A method for checking if this tetromino can be moved in a given direction
   def can_be_moved(self, direction, game_grid):
      n = len(self.tile_matrix)
      if direction == "rotate":
         # simulate rotation to check if it would be valid
         rotated_matrix = np.rot90(self.tile_matrix, -1)
         for row in range(n):
            for col in range(n):
               if rotated_matrix[row][col] is not None:
                  pos = self.get_cell_position(row, col)
                  # check if the new position after rotation is valid
                  if not game_grid.is_inside(pos.y, pos.x) or game_grid.is_occupied(pos.y, pos.x):
                     return False  # rotation would cause collision or go out of bounds
         return True  # rotation is safe
      # initialize movement offsets
      dx, dy = 0, 0
      if direction == "left":
         dx = -1  # move left (decrease x)
      elif direction == "right":
         dx = 1  # move right (increase x)
      elif direction == "down":
         dy = -1  # move down (decrease y)
      # check if each tile can move to the new position
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] is not None:
               pos = self.get_cell_position(row, col)
               new_x = pos.x + dx
               new_y = pos.y + dy
               # check if the new position is inside the grid and not occupied
               if not game_grid.is_inside(new_y, new_x) or game_grid.is_occupied(new_y, new_x):
                  return False  # movement would cause collision or go out of bounds
      return True  # movement is safe
