import asyncio
from pyppeteer import launch
import requests
from bs4 import BeautifulSoup

def parse_crossword_file(filename: str):
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
    
    return (puzzle_width, puzzle_height, grid)


def parse_crossword_url(url: str):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    iframes = soup.find_all('iframe')
    links = [iframe.get('data-src') for iframe in iframes if iframe.get('data-src')]
    async def get_page_html(url):
        browser = await launch(headless=True)
        page = await browser.newPage()
        await page.goto(url, waitUntil='domcontentloaded')
        
        # Wait for a short time to ensure all dynamic content is loaded (you might need to adjust this)
        await asyncio.sleep(2)
        
        # Get the rendered HTML content
        html = await page.content()
        
        await browser.close()
        return html

    url = links[0]
    html_content = asyncio.get_event_loop().run_until_complete(get_page_html(url))

    # Now 'html_content' contains the rendered HTML of the page
    #print(html_content.encode('utf-8'))
    soup = BeautifulSoup(html_content, 'html.parser')
    crossword_div = soup.find('div', {'class': 'crossword horizontally-centered'})
    grid = []
    row = []
    width = 0
    height = 0
    for box in crossword_div.find_all('div'):
        deets = box.get('class')
        if len(deets) > 1:
            color = deets[1]
            if color == "letter":
                row.append(0)
            else:
                row.append(1)
            if len(grid) == 0:
                width+=1
        else:
            if deets[0] == "endRow":
                grid.append(row)
                row = []
    height = len(grid)
    return (width,height,grid)
    
    