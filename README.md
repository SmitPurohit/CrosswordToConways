# CrosswordToConways

-Takes in either a .puz file or the date of a New Yorker crossword and plays Conway's Game of Life on that crossword, outputting to a gif

Install reqs with:

```pip install -r requirements.txt```

Run with:

```python ./crosswordToConways.py -h``` to see all options

```python ./crosswordToConways.py -f <file_name.puz>``` to run this with a .puz file in the same directory

```python ./crosswordToConways.py -d <YYYY/MM/DD> ``` to run this with the New Yorker crossword from that date in YYYY/MM/DD) format

Add ```-o <output_file.gif>``` to output the gif to a specific file

Press Space after the pygame window pops up

## Examples

New Yorker (2023/12/06)
![](https://github.com/SmitPurohit/CrosswordToConways/blob/main/examples/NY2023-12-06.gif)

