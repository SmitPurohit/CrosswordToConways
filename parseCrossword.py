def parse_crossword(filename: str):
    width_index = 0x2C
    height_index = 0x2D
    puzzle_offset = 0x34

    #Load file + set width,height, and the crossword grid
    file_content: str

    try:
        with open(filename, 'rb') as file:
            file_content = file.read()
    except FileNotFoundError as e:
        print(f"{e}")
        raise FileNotFoundError
    puzzle_width = file_content[width_index] 
    puzzle_height = file_content[height_index]
    puzzle_size = (puzzle_width*puzzle_height)
    puzzle = file_content[puzzle_offset+puzzle_size:puzzle_offset+2*puzzle_size].decode('ascii')
    grid = [[0 for _ in range(puzzle_width)] for _ in range(puzzle_height)]

    for r in range(puzzle_height):
        for c in range(puzzle_width):
            grid[r][c] = 0 if puzzle[c+r*puzzle_height] ==  '-' else 1
    
    return puzzle_width, puzzle_height, grid



