from parseCrossword import parse_crossword_file
from parseCrossword import parse_crossword_url
import pygame
import getopt, sys
from utilities import num_neighbors
import numpy as np
import imageio
import re

def crossword_to_conways(input_option, output_option, input_type):

    #Get values for the grid
    try:
        if not input_type:
            print("Enter an input type")
            return
        
        if input_type == "url":
            #Make sure the date is in YYYY/MM/DD 
            date_pattern = re.compile(r'^\d{4}/\d{2}/\d{2}$')
            if date_pattern.match(input_option):
                print(f"Getting New Yorker Crossword for date {input_option}")
            else:
                print(f"{input_option} is not in the correct format.")
                return
            
            try:
                result = parse_crossword_url(f"https://www.newyorker.com/puzzles-and-games-dept/crossword/{input_option}")
            except:
                print(f"{input_option} is either not a valid date or there is no New Yorker Crossword for that date")
                return
            
        if input_type == "file":
            result = parse_crossword_file(input_option)

    except FileNotFoundError:
        return
    
    puzzle_width, puzzle_height, grid = result
    image_arr = []
    image_store = {}
    
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

    maxOscillations = 5 #Total number of periods an oscillation will run for
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
        updated = [] #Updated holds a tuple of (row, col, new_val)

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
        frame = np.uint8(x3).T #Transpose bc for some reason this gets rotated
        frame_store = tuple(tuple(x) for x in frame)
        if frame_store in image_store:
            image_store[frame_store] += 1
            if image_store[frame_store] >= maxOscillations:
                break
        else:
            image_store[frame_store] = 1
        image_arr.append(frame)
        if len(updated) == 0:
            running = False

        clock.tick(60)  # limits FPS to 1
        
    pygame.quit()

    if input_type=="file":
        #Remove the last 4 characters (.puz) to get the filename for the gif
        output_path = input_option[:-3] + "gif"
    if input_type=="url":
        input_option = input_option.replace("/", "-")
        output_path = "NY" + input_option + ".gif"
    if output_option != "":
        output_path = output_option
    
    
    # Save the list of images as a GIF
    imageio.mimwrite(output_path, image_arr, duration=500, loop=0)  # Set the duration between frames in milliseconds


if __name__ == "__main__":
    argumentList = sys.argv[1:]
 
    # Options
    options = "hf:d:o:"
 
    # Long options
    long_options = ["Help", "File=", "Date=", "Output="]
    
    input_option = ""
    output_option = ""

    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        # checking each argument
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-h", "--Help"):
                print("Run with -f <name>.puz or -d YYYY/MM/DD")
                print("Specify output file with -o (must be a .gif)")
                
            elif currentArgument in ("-f", "--File"):
                print ("Using file:", currentValue)
                if currentValue[-4:] == ".puz":
                    input_option = currentValue
                    input_type = "file"
                else:
                    print("Enter a valid .puz file")
                    sys.exit

            elif currentArgument in ("-d", "--Date"):
                print("Using date: ", currentValue)
                input_option = currentValue
                input_type = "url"

            elif currentArgument in ("-o", "--Output"):
                if currentValue[-4:] == ".gif":
                    print("Outputting to: ", currentValue)
                    output_option = currentValue

                else:
                    print("Enter a valid gif file")
                    sys.exit()
                
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))

    if(input_option):
        crossword_to_conways(input_option, output_option, input_type)