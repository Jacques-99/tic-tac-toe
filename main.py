# Example file showing a circle moving on screen
import pygame
import sys
import logging
import numpy as np
import time

class Game:
    def __init__(self) -> None:
        # Set up logging
        logging.basicConfig(
            filename='logs.log', 
            level=logging.INFO,
            format="%(asctime)s:%(filename)s - %(funcName)s:%(lineno)s - %(message)s",
            )
        
        logging.info('------ New Game Started ------')

        # pygame setup
        pygame.init()
        pygame.display.set_caption("Noice")
        self.screen = pygame.display.set_mode((720, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        #=== Screen ===#
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.col = [0,self.screen_width/3,self.screen_width*2/3]
        self.row = [0,self.screen_height/3,self.screen_height/3*2]

        #=== Text ===#
        self.font = pygame.font.Font('freesansbold.ttf',32)
        self.text = self.font.render('', True, 'green')
        self.textRect = self.text.get_rect()
        self.textRect.center = (self.screen_width / 2.8, self.screen_height / 2)

        #=== Grid ===#
        self.grid_scale = pygame.Vector2(self.screen.get_width(), self.screen.get_height())
        self.grid_img = pygame.image.load("images/grid.png").convert_alpha()
        self.grid = pygame.transform.scale(self.grid_img, self.grid_scale)

        self.matrix = [[None,None,None],[None,None,None],[None,None,None]]

        #=== Cross ===#
        self.cross_scale = pygame.Vector2(self.screen.get_width()/3, self.screen.get_height()/3)
        self.cross_img = pygame.image.load("images/cross.png").convert_alpha()
        self.cross = pygame.transform.scale(self.cross_img, self.cross_scale)

        #=== Circle ===#
        self.circle_scale = pygame.Vector2(self.screen.get_width()/3, self.screen.get_height()/3)
        self.circle_img = pygame.image.load("images/circle.png").convert_alpha()
        self.circle = pygame.transform.scale(self.circle_img, self.circle_scale)

        #=== Players ===#
        self.player1 = 0
        self.player2 = 1
        self.current_player = self.player1
        self.next_player = self.player1       

    def run(self):

        #=== Functions ===#

        def has_winning_list(ls:list):
            try:
                if sum(ls) == self.current_player*3:
                    return True
            except TypeError as e:
                pass
            return False
        
        def determine_block(pos):
            if pos > self.col[2]:
                return 2 # column 3
            elif pos < self.col[1]: 
                return 0 # column 1
            else:
                return 1 # column 2
        
        def is_victorious():
            # Check if the current player has a winning row:
            for i, row in enumerate(self.matrix):
                if has_winning_list(row):
                    logging.info(f'Player {self.current_player} won in row {i}')
                    return [True,f"row{i+1}"]
            
            # Check if the current player has a winning col:
            transposed_matrix = np.transpose(np.array(self.matrix)).tolist()

            for j, col in enumerate(transposed_matrix):
                if has_winning_list(col):
                    logging.info(f'Player {self.current_player} won in col {j}')
                    return [True,f"col{j+1}"]

            # Check if the current player has a winning diagonal:
            diagonal1=[self.matrix[0][0],self.matrix[1][1],self.matrix[2][2]]
            if has_winning_list(diagonal1):
                logging.info(f'Player {self.current_player} won in diagonal 1')
                return [True,"diagonal1"]

            diagonal2 = [self.matrix[2][0],self.matrix[1][1],self.matrix[0][2]]
            if has_winning_list(diagonal2):
                logging.info(f'Player {self.current_player} won in diagonal 2')
                return [True,"diagonal2"]
            
            return [False,None]

        def take_turn(player):
            # Get the mouse position where the user clicked:
            mouse_pos = pygame.mouse.get_pos()
            # Determine x and y coordinates of the mouse:
            x_pos = mouse_pos[0]
            y_pos = mouse_pos[1]
            # Determine the row and column the user clicked:
            column = determine_block(x_pos)
            row = determine_block(y_pos)
            
            # Determine if the block was already selected:
            if self.matrix[row][column] != None:
                illigal_move_message = self.font.render(f'illegal move!', True, 'red')
                draw_board()
                self.screen.blit(illigal_move_message,self.textRect)
                logging.info(f'Player {self.current_player+1} attepted to make an illigal move on row {row+1} and col {column+1}')
                pygame.display.update()
                time.sleep(0.8)
            else:
                # Update the matrix to display the relevent icon:
                self.matrix[row][column] = player
                logging.info(f'Player {self.current_player+1} played at row {row+1} and {column+1}')
                # Switch the turn of the player:
                self.next_player = 1-self.current_player
        
        def draw_board():
            for i, row in enumerate(self.matrix):
                for j, col in enumerate(row):
                    try:
                        if col == 1:
                            self.screen.blit(self.cross, (self.col[j],self.row[i]))
                        elif col == 0:
                            self.screen.blit(self.circle, (self.col[j],self.row[i]))
                        elif col != None:
                            raise Exception(f"Unexpected value in board at position ({i}, {j})")
                    except Exception as e:
                        logging.error(str(e))
                        raise

        def game_is_draw():
            game_completed = True
            for row in self.matrix:
                for col in row:
                    if col == None:
                        game_completed = False
                        return False
            return game_completed
        
        def end_game():
            logging.info('------ Game Ended ------')

            # Delay before exiting the game:
            time.sleep(3)
            pygame.quit()
            sys.exit()    

        def draw_line(win_row):
            a11=(self.screen_width // 6, self.screen_height // 6)
            a12=(self.screen_width // 2, self.screen_height // 6)
            a13=((self.screen_width // 6)*5,self.screen_width // 6)
            a21=(self.screen_width // 6, self.screen_height // 2)
            a23=((self.screen_width // 6)*5, self.screen_height // 2)
            a31=(self.screen_width // 6,(self.screen_width // 6)*5)
            a32=(self.screen_width // 2, (self.screen_width // 6)*5)
            a33=((self.screen_width // 6)*5, (self.screen_height // 6)*5)
            
            blue_colour = (30, 70, 150)

            if win_row == "row1":
                pygame.draw.line(self.screen, blue_colour, a11, a13 , 20)
            elif win_row == "row2":
                pygame.draw.line(self.screen, blue_colour, a21, a23 , 20)
            elif win_row == "row3":
                pygame.draw.line(self.screen, blue_colour, a31, a33 , 20)
            elif win_row == "col1":
                pygame.draw.line(self.screen, blue_colour, a11, a31 , 20)
            elif win_row == "col2":
                pygame.draw.line(self.screen, blue_colour, a12, a32 , 20)
            elif win_row == "col3":
                pygame.draw.line(self.screen, blue_colour, a13, a33 , 20)
            elif win_row == "diagonal1":
                pygame.draw.line(self.screen, blue_colour, a11, a33 , 20)
            elif win_row == "diagonal2":
                pygame.draw.line(self.screen, blue_colour, a31, a13 , 20)
            else:
                raise Exception(f"Unexpected value. Cannot draw line: {win_row}")
            
        while True:
            # Switch the turn of the player:
            self.current_player = self.next_player

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("white")
            
            # Print the grid:
            self.screen.blit(self.grid, (0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:              # pygame.QUIT event means the user clicked X to close the window
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN: # Check if the player has clicked the mouse
                    take_turn(self.current_player)
                    break

            # Draw the circles and crosses of the current board:
            draw_board()

            # Determine if the current player won
            results=is_victorious()
            if results[0] == True:
                    # Generate and display a win message:
                    win_message = self.font.render(f'Player {self.current_player + 1} Won', True, 'green')
                    
                    try:
                        draw_line(results[1])
                    except Exception as e:
                        logging.error(str(e))
                        raise

                    self.screen.blit(win_message,self.textRect)
                    pygame.display.flip()

                    end_game()          

            # Determine if the game ended in a draw:
            elif game_is_draw():
                    # Generate and display a draw message:
                    draw_message = self.font.render(f'No winner', True, 'orange')
                    self.screen.blit(draw_message,self.textRect)
                    logging.info('Game ended in a draw')
                    pygame.display.flip()
                    end_game()

            # Display the board and icons:
            pygame.display.flip()

            # Increase the delta time since the last frame:
            self.dt = self.clock.tick(60) / 1000 
                    
Game().run()