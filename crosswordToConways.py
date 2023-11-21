from parseCrossword import parse_crossword
import pygame
import sys
from utilities import num_neighbors
import numpy as np
import imageio

def crossword_to_conways():

    #Get values for the grid
    try:
        result = parse_crossword(sys.argv[1])
    except FileNotFoundError:
        return
    puzzle_width, puzzle_height, grid = result
    image_arr = []
    #Set up pygame
    pygame.init()
    pygame.display.set_caption("Conway Crossword")

    screen = pygame.display.set_mode((puzzle_width*20+2, puzzle_height*20+2))

    clock = pygame.time.Clock()
    running = True

    #Draw the lines for the crossword
    pygame.draw.rect(screen,"white",(1,1,puzzle_width*20,puzzle_height*20)) 
    for _ in range(20, puzzle_width*20+1,20):
        pygame.draw.rect(screen,"black",(_,1,1,puzzle_height*20)) 
    for _ in range(20, puzzle_height*20+1,20):
        pygame.draw.rect(screen,"black",(1,_,puzzle_width*20,1))   
    pygame.display.flip()

    #Start paused, space button unpauses
    paused = True
    #Drawing loop
    while running:

        #poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
        
        
        # Draw the boxes
        for r in range(puzzle_height):
            for c in range(puzzle_width):
                if grid[r][c] == 1:
                    pygame.draw.rect(screen,"black",(c*20+1,r*20+1,19,19)) 
                else:
                    pygame.draw.rect(screen,"white",(c*20+1,r*20+1,19,19)) 
        pygame.display.flip()
        
        if paused:
            continue
        
        #Calculate next board
        updated = []
        for r in range(puzzle_height):
            for c in range(puzzle_width):
                neighbors = num_neighbors(grid, r,c) 
                if grid[r][c] == 1:
                    if neighbors < 2 or neighbors > 3:
                        updated.append((r,c,0))
                else:
                    if neighbors == 3:
                        updated.append((r,c,1))
        for update in updated:
            grid[update[0]][update[1]] = update[2]
        
        #Save image for gif creation later
        x3 = pygame.surfarray.pixels2d(screen)
        image_arr.append(np.uint8(x3).T) #Transpose bc for somereason this gets rotated

        if len(updated) == 0:
            running = False
        clock.tick(1)  # limits FPS to 1
        
    pygame.quit()

    #Remove the last 4 characters (.puz) to get the filename for the gif
    output_path = sys.argv[1][:-3] + "gif"
    
    # Save the list of images as a GIF
    imageio.mimwrite(output_path, image_arr, duration=500)  # Set the duration between frames in milliseconds

if __name__ == "__main__":
    crossword_to_conways()