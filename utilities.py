#Get the number of neighbors for a row, column on a grid
def num_neighbors(grid, r,c):
    count = 0

    for x in [-1,0,1]:
        for y in [-1,0,1]:
            #Only need to check for 0 bound check, the other is taken care of by the try catch
            if not (y,x) == (0,0) and r+y >= 0 and c+x >= 0:
                try:
                    if grid[r+y][c+x] == 1:
                        count += 1
                except:
                    continue
    return count