import random
import os
import sys

def generate_board():
    """Generates a valid, partially filled Sudoku puzzle board."""
    base  = 3
    side  = base * base
    def pattern(r, c): return (base * (r % base) + r // base + c) % side
    def shuffle(s): return random.sample(s, len(s)) 
    
    r_base = range(base) 
    rows  = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)] 
    cols  = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]
    nums  = shuffle(range(1, side + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    
    squares = side * side
    empties = squares * 4 // 9  # Removes around 36 numbers for a clean playable setup
    for p in random.sample(range(squares), empties):
        board[p // side][p % side] = 0
        
    return board

def read_current_board():
    """Reads the state of the active board if it exists, otherwise builds a new one."""
    if os.path.exists("state.txt"):
        try:
            with open("state.txt", "r") as f:
                lines = f.read().splitlines()
                return [[int(n) for n in line.split()] for line in lines]
        except:
            return generate_board()
    return generate_board()

def create_svg(board, selected_cell=None):
    """Generates an aesthetic, neon dark-theme interactive SVG."""
    svg_width = 440
    svg_height = 460
    start_x = 40
    start_y = 50
    cell_size = 40

    svg = f"""<svg xmlns="http://w3.org" viewBox="0 0 {svg_width} {svg_height}" width="100%">
    <defs>
        <style>
            @import url('https://googleapis.com');
            .bg {{ fill: #0d1117; rx: 16px; }}
            .grid-bg {{ fill: #161b22; stroke: #30363d; stroke-width: 1px; rx: 8px; }}
            .cell-thin {{ stroke: #30363d; stroke-width: 1; fill: transparent; cursor: pointer; }}
            .cell-thin:hover {{ fill: rgba(88, 166, 255, 0.1); }}
            .cell-thick {{ stroke: #bc8cff; stroke-width: 2.5; stroke-linecap: round; pointer-events: none; }}
            .number {{ font-family: 'Share Tech Mono', monospace; font-weight: bold; font-size: 20px; fill: #adbac7; text-anchor: middle; dominant-baseline: central; pointer-events: none; }}
            .selected {{ fill: rgba(188, 140, 255, 0.25); stroke: #bc8cff; stroke-width: 1.5; }}
        </style>
    </defs>
    <rect width="{svg_width}" height="{svg_height}" class="bg" />
    <rect x="{start_x}" y="{start_y}" width="360" height="360" class="grid-bg" />
    """

    # Render Grid Cells
    for r in range(9):
        for c in range(9):
            x = start_x + (c * cell_size)
            y = start_y + (r * cell_size)
            val = board[r][c]
            
            is_sel = (selected_cell == (r, c))
            cell_cls = "cell-thin selected" if is_sel else "cell-thin"
            
            # Wrap cell in an anchor tag so users can click to select coordinates
            svg += f'<a href="https://github.com{r}&amp;col={c}">\n'
            svg += f'  <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" class="{cell_cls}" />\n'
            svg += f'</a>\n'
            
            if val != 0:
                svg += f'<text x="{x + cell_size/2}" y="{y + cell_size/2}" class="number">{val}</text>\n'

    # Thick Block Dividers
    for i in range(4):
        pos = i * cell_size * 3
        svg += f'<line x1="{start_x + pos}" y1="{start_y}" x2="{start_x + pos}" y2="{start_y + 360}" class="cell-thick" />\n'
        svg += f'<line x1="{start_x}" y1="{start_y + pos}" x2="{start_x + 360}" y2="{start_y + pos}" class="cell-thick" />\n'

    svg += "</svg>"
    return svg

if __name__ == "__main__":
    # Check if a move was submitted via automated workflow dispatch flags
    args = sys.argv[1:]
    board = read_current_board()
    
    # Save active layout updates
    with open("state.txt", "w") as f:
        for row in board:
            f.write(" ".join(map(str, row)) + "\n")
            
    svg_content = create_svg(board)
    with open("sudoku.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
