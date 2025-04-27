################################################################################
#                                                                              #
# The main program of Tetris 2048 Base Code                                    #
#                                                                              #
################################################################################

import lib.stddraw as stddraw  # for creating an animation with user interactions
from lib.picture import Picture  # used for displaying an image on the game menu
################################################################################
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
################################################################################


from tetromino import Tetromino  # this class is for modeling the tetrominoes
from game_grid import GameGrid  # this class is for modeling the game grid
import time
import random  # random was used for creating tetrominoes with random shapes



def start(speed=None):
    # set the dimensions of the game grid
    grid_h, grid_w = 20, 12

    # set the size of the drawing canvas (the displayed window)

    canvas_h, canvas_w = 40 * grid_h, 40 * grid_w
    stddraw.setCanvasSize(canvas_w, canvas_h)
    # set the scale ofs the coordinate system for the drawing canvas
    stddraw.setXscale(-0.5, grid_w - 0.5)
    stddraw.setYscale(-0.5, grid_h - 0.5)

    # set the game grid dimension values stored and used in the Tetromino class
    Tetromino.grid_height = grid_h
    Tetromino.grid_width = grid_w
    # create the game grid
    grid = GameGrid(grid_h, grid_w)
    if speed is None:
        speed = display_game_menu(grid_h, grid_w)

    while True:
        lastfalltime = time.time()
        current_tetromino = create_tetromino()
        grid.current_tetromino = current_tetromino
        paused = False

        # create the first tetromino to enter the game grid

        # by using the create_tetromino function defined below

        # display a simple menu before opening the game
        # by using the display_game_menu function defined below

        # the main game loop
        while True:

            # check for any user interaction via the keyboard
            if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
                key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
                # if the left arrow key has been pressed
                if key_typed == 'p':
                    paused = not paused

                if not paused:
                    if key_typed == "left":
                        # move the active tetromino left by one
                        current_tetromino.move(key_typed, grid)
                    # if the right arrow key has been pressed
                    elif key_typed == "right":
                        # move the active tetromino right by one
                        current_tetromino.move(key_typed, grid)
                    # if the down arrow key has been pressed
                    elif key_typed == "down":
                        # move the active tetromino down by one
                        # (soft drop: causes the tetromino to fall down faster)
                        current_tetromino.move(key_typed, grid)
                    elif key_typed == 'up':  # Assuming 'up' arrow is for rotation
                        current_tetromino.rotate(grid)
                    elif key_typed == 's':
                        while current_tetromino.move("down",
                                                     grid):  # Move the tetromino down until it can't move further
                            pass

                # clear the queue of the pressed keys for a smoother interaction
                stddraw.clearKeysTyped()
                labels = grid.label_components()
                grid.move_down_components(labels)

            if not paused:

                current_time = time.time()
                if (current_time - lastfalltime) * 1000 >= speed:
                    success = current_tetromino.move("down", grid)
                    grid.merge_tiles()
                    lastfalltime = current_time

                    if not success:
                        tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
                        game_over = grid.update_grid(tiles, pos)
                        if game_over:
                            stddraw.clear()  # Clear the canvas

                            stddraw.setPenColor(stddraw.VIOLET)
                            stddraw.filledRectangle(0, 0, grid_w, grid_h)

                            stddraw.setFontSize(40)
                            stddraw.setPenColor(stddraw.BLACK)
                            stddraw.text(grid_w / 2, grid_h / 2, "Game Over")
                            speed = restart_button_display(grid_h, grid_w)  # Capture fall speed from restart

                            stddraw.show()

                            return speed  # end the game loop

                        current_tetromino = create_tetromino()
                        grid.current_tetromino = current_tetromino

                    grid.display()

                    if grid.check_win():
                        grid.draw_game_won()
            else:
                # Display a pause screen or simply do nothing
                stddraw.text(canvas_w / 2, canvas_h / 2, "Game Paused")
                stddraw.show(100)  # Update the display to show the paused message


def restart_button_display(grid_h, grid_w):
    
    text_color = Color(31, 160, 239)
    button_color = Color(25, 255, 228)
    button_x, button_y = 0, 0
    button_w, button_h = 6, 2
    


    

    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_x, button_y, button_w, button_h)
    stddraw.setPenColor(text_color)
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(20)
    stddraw.text(button_x + button_w / 2, button_y + button_h / 2, "Restart")

    while True:
        stddraw.show(50)
        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if button_x <= mouse_x <= button_x + button_w and button_y <= mouse_y <= button_y + button_h:
                stddraw.clear()
                # Call display_game_menu and return the speed
                return display_game_menu(grid_h, grid_w)


def create_tetromino():
    # the type (shape) of the tetromino is determined randomly
    tetromino_types = ['L', 'Z', 'O', '.', 'T', 'I', 'J', 'S']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    # create and return the tetromino
    tetromino = Tetromino(random_type)
    return tetromino


def display_game_menu(grid_height, grid_width):
    # Define colors used for the menu
    text_color = Color(138, 43, 226)
    background_color = Color(54, 15, 80)
    button_color = Color(186, 185, 200)
    

    # Clear the drawing canvas to the background color
    stddraw.clear(background_color)

    # Load and display the game menu image
    current_dir = os.path.dirname(os.path.realpath(__file__))
    img_file = current_dir + "/images/menu_image.png"
    img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
    image_to_display = Picture(img_file)
    stddraw.picture(image_to_display, img_center_x, img_center_y)

    # Display the start game button and wait for a click
    button_w, button_h = grid_width - 1.5,4
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(15)
    stddraw.setPenColor(text_color)
    stddraw.text(img_center_x, button_blc_y + 3, "Click Here to start Tetris 2048, use 'p' to pause the game")
    
    stddraw.text(img_center_x, button_blc_y + 1.5, "Use right and left keys to move, 'up' key to rotate, 's' to hard drop")

    while True:
        stddraw.show(50)
        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if button_blc_x <= mouse_x <= button_blc_x + button_w and button_blc_y <= mouse_y <= button_blc_y + button_h:
                break  # Exit the loop when the start button is clicked

    # Display difficulty selection and wait for a choice
    button_w, button_h = grid_width / 3, 1
    button_y = 2
    difficulties = {
        "Easy": grid_width * 0.19 - button_w / 2,
        "Medium": grid_width * 0.44 - button_w / 2,
        "Hard": grid_width * 0.75 - button_w / 2
    }
    for difficulty, button_x in difficulties.items():
        stddraw.setPenColor(button_color)
        stddraw.filledRectangle(button_x, button_y, button_w, button_h)
        stddraw.setPenColor(text_color)
        stddraw.text(button_x + button_w / 2, button_y + button_h / 2, difficulty)

    difficulty_choice = None
    while difficulty_choice is None:
        stddraw.show(50)
        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            for difficulty, button_x in difficulties.items():
                if button_x <= mouse_x <= button_x + button_w and button_y <= mouse_y <= button_y + button_h:
                    difficulty_choice = difficulty
                    break

    # Return the fall speed associated with the selected difficulty
    speed = {"Easy": 1000, "Medium": 500, "Hard": 250}[difficulty_choice]
    return speed


if __name__ == '__main__':
    speed = None  # Initialize with None or a default value
    while True:
        speed = start(speed)  # Pass the current speed to start
        if speed == "exit":
            print("Exiting the game.")
            break
        elif speed == "restart":
            print("Restarting...")
            speed = None  # Reset if needed, or handle accordingly
            continue
