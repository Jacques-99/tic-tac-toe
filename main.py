# Example file showing a circle moving on screen
import pygame
import sys

class Game:
    def __init__(self) -> None:
        # pygame setup
        pygame.init()
        pygame.display.set_caption("Noice")
        self.screen = pygame.display.set_mode((720, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.player_pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)

        #=== Screen ===#
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.col = [0,self.screen_width/3,self.screen_width*2/3]
        self.row = [0,self.screen_height/3,self.screen_height/3*2]

        #=== Grid ===#
        self.grid_scale = pygame.Vector2(self.screen.get_width(), self.screen.get_height())
        self.grid_img = pygame.image.load("images/grid2.png").convert_alpha()
        self.grid = pygame.transform.scale(self.grid_img, self.grid_scale)

        self.matrix = [[2,2,2],[2,2,2],[2,2,2]]

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

    def run(self):
        while True:
            
            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("black")
            
            self.screen.blit(self.grid, (0,0))

            # self.matrix = [[1,0,1],[0,1,1],[1,0,0]]

            for row in range(len(self.matrix)):
                for col in range(len(self.matrix[row])):
                    if self.matrix[row][col] == 1:
                        self.screen.blit(self.cross, (self.col[col],self.row[row]))
                    elif self.matrix[row][col] == 0:
                        self.screen.blit(self.circle, (self.col[col],self.row[row]))
                    else: 
                        pass

            def determine_pos(pos):
                if pos > self.col[2]:
                    return 2 # column 3
                elif pos < self.col[1]: 
                    return 0 # column 1
                else:
                    return 1 # column 2

            # poll for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # pygame.QUIT event means the user clicked X to close your window
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    print(f"Player {self.current_player} clicked mouse at {mouse_pos}")

                    x_pos = mouse_pos[0]
                    print(x_pos)
                    y_pos = mouse_pos[1]
                    print(y_pos)
                    column = determine_pos(x_pos)
                    row = determine_pos(y_pos)
                    
                    self.matrix[row][column] = self.current_player
                    print(self.matrix)
                    self.current_player = 1-self.current_player

            
            # check if current player has won the game:
                # find cross product of matrix with [1,1,1]
                    # if the result contains a 3 it means player2 won with a row
                    # if the result contains a 0 it means player1 won with a row
                
                # find the transpose of the matrix
                    # if the result contains a 3 it means player2 won with a column
                    # if the result contains a 0 it means player1 won with a column

                # check if there's a winning combo in one of the diagonals


            # flip() the display to put your work on screen
            pygame.display.flip()
            pygame.display.update()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(60) / 1000         

Game().run()