import random
import os

def generate_board():
    """Generates a valid, partially filled Sudoku puzzle board."""
    # A standard base layout for puzzle generation
    base  = 3
    side  = base * base

    def pattern(r, c): return (base * (r % base) + r // base + c) % side
    def shuffle(s): return random.sample(s, len(s)) 
    
    r_base = range(base) 
    rows  = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)] 
    cols  = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]
    nums  = shuffle(range(1, side + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    
    # Randomly remove elements to create the puzzle (adjust difficulty here)
    squares = side * side
    empties = squares * 5 // 9  # Removes roughly 45-50 numbers
    for p in random.sample(range(squares), empties):
        board[p // side][p % side] = 0
        
    return board

def create_svg(board):
    """Generates an aesthetic, neon dark-theme SVG string."""
    svg_width = 440
    svg_height = 500
    start_x = 40
    start_y = 90
    cell_size = 40

    # Start constructing the SVG layout
    svg = f"""<svg xmlns="http://w3.org" viewBox="0 0 {svg_width} {svg_height}" width="100%" height="100%">
    <defs>
        <style>
            @import url('https://googleapis.com');
            .bg {{ fill: #0d1117; rx: 16px; }}
            .title {{ font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 22px; fill: url(#title-grad); }}
            .subtitle {{ font-family: 'Share Tech Tech', sans-serif; font-size: 11px; fill: #8b949e; letter-spacing: 2px; }}
            .grid-bg {{ fill: #161b22; stroke: #30363d; stroke-width: 1px; rx: 8px; }}
            .cell-thin {{ stroke: #30363d; stroke-width: 1; }}
            .cell-thick {{ stroke: #58a6ff; stroke-width: 2.5; stroke-linecap: round; }}
            .number {{ font-family: 'Poppins', sans-serif; font-weight: 600; font-size: 18px; fill: #adbac7; text-anchor: middle; dominant-baseline: central; }}
            .fixed-num {{ fill: #ff7b72; font-weight: 700; }}
        </style>
        <linearGradient id="title-grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#58a6ff" />
            <stop offset="100%" stop-color="#bc8cff" />
        </linearGradient>
    </defs>

    <!-- Canvas Background -->
    <rect width="{svg_width}" height="{svg_height}" class="bg" />

    <!-- Header Content -->
    <text x="40" y="48" class="title">SUDOKU OF THE DAY</text>
    <text x="40" y="68" class="subtitle">AUTOMATED DAILY PUZZLE</text>

    <!-- Inner Grid Board Backdrop -->
    <rect x="{start_x}" y="{start_y}" width="360" height="360" class="grid-bg" />
    """

    # Render Board Cells and Values
    for r in range(9):
        for c in range(9):
            x = start_x + (c * cell_size)
            y = start_y + (r * cell_size)
            val = board[r][c]
            
            # Draw individual cells border lines
            svg += f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="none" class="cell-thin" />\n'
            
            # Place values (Colorize initial puzzle seeds uniquely)
            if val != 0:
                is_fixed = random.choice([True, False, True]) # Adds stylistic visual variety
                num_class = "number fixed-num" if is_fixed else "number"
                svg += f'<text x="{x + cell_size/2}" y="{y + cell_size/2}" class="{num_class}">{val}</text>\n'

    # Render Thick Major Subgrid Boundaries (3x3 blocks)
    for i in range(4):
        pos = i * cell_size * 3
        # Vertical Major Lines
        svg += f'<line x1="{start_x + pos}" y1="{start_y}" x2="{start_x + pos}" y2="{start_y + 360}" class="cell-thick" />\n'
        # Horizontal Major Lines
        svg += f'<line x1="{start_x}" y1="{start_y + pos}" x2="{start_x + 360}" y2="{start_y + pos}" class="cell-thick" />\n'

    svg += "\n</svg>"
    return svg

if __name__ == "__main__":
    puzzle_board = generate_board()
    svg_content = create_svg(puzzle_board)
    
    # Save output to image file
    with open("sudoku.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("Successfully generated clean sudoku.svg file!")
