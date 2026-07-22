import random
import os
import sys
from datetime import datetime

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
    empties = squares * 4 // 9  
    for p in random.sample(range(squares), empties):
        board[p // side][p % side] = 0
        
    return board

def get_board_and_manage_date():
    """Checks the calendar date. Generates a fresh board if a new day has arrived."""
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    
    if not os.path.exists("date.txt") or not os.path.exists("state.txt"):
        with open("date.txt", "w") as f:
            f.write(today_str)
        return generate_board()
    
    with open("date.txt", "r") as f:
        last_saved_date = f.read().strip()
        
    if last_saved_date != today_str:
        with open("date.txt", "w") as f:
            f.write(today_str)
        return generate_board()
        
    try:
        with open("state.txt", "r") as f:
            lines = f.read().splitlines()
            return [[int(n) for n in line.split()] for line in lines]
    except:
        return generate_board()

def create_svg(board):
    """Generates a newspaper sketch style layout with inverted black background and white lines."""
    svg_width = 440
    svg_height = 500
    start_x = 40
    start_y = 90
    cell_size = 40

    svg = f"""<svg xmlns="http://w3.org" viewBox="0 0 {svg_width} {svg_height}" width="100%">
    <defs>
        <style>
            @import url('https://googleapis.com');
            .bg {{ fill: #0d1117; }}
            .header-text {{ font-family: 'Courier Prime', monospace; font-size: 13px; fill: #ffffff; letter-spacing: 1px; text-anchor: middle; }}
            .sub-header {{ font-family: 'Courier Prime', monospace; font-size: 8px; fill: #8b949e; text-decoration: underline; text-anchor: middle; }}
            .grid-bg {{ fill: #0d1117; stroke: #ffffff; stroke-width: 1.5px; }}
            .cell-thin {{ stroke: #ffffff; stroke-width: 0.75; fill: transparent; cursor: pointer; }}
            .cell-thin:hover {{ fill: rgba(255, 255, 255, 0.08); }}
            .cell-thick {{ stroke: #ffffff; stroke-width: 2.5; stroke-linecap: square; pointer-events: none; }}
            .number {{ font-family: 'Courier Prime', monospace; font-weight: bold; font-size: 22px; fill: #ffffff; text-anchor: middle; dominant-baseline: central; pointer-events: none; }}
            .footer-text {{ font-family: 'Courier Prime', monospace; font-size: 7px; fill: #57606a; text-anchor: middle; }}
        </style>
    </defs>
    
    <!-- Dark Canvas Background -->
    <rect width="{svg_width}" height="{svg_height}" class="bg" />

    <!-- Newspaper Header Elements -->
    <text x="220" y="42" class="header-text">A PUZZLE A DAY KEEPS THE WRINKLES AWAY.</text>
    <text x="220" y="58" class="sub-header">participate in the program</text>

    <!-- Main Grid Frame -->
    <rect x="{start_x}" y="{start_y}" width="360" height="360" class="grid-bg" />
    """

    # Grid Cell Layout Loops
    for r in range(9):
        for c in range(9):
            x = start_x + (c * cell_size)
            y = start_y + (r * cell_size)
            val = board[r][c]
            
            # Invisible clickable target anchor link
            svg += f'<a href="https://github.com">\n'
            svg += f'  <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" class="cell-thin" />\n'
            svg += f'</a>\n'
            
            if val != 0:
                svg += f'<text x="{x + cell_size/2}" y="{y + cell_size/2}" class="number">{val}</text>\n'

    # Thick Major Newspaper Blocks Boundaries
    for i in range(4):
        pos = i * cell_size * 3
        svg += f'<line x1="{start_x + pos}" y1="{start_y}" x2="{start_x + pos}" y2="{start_y + 360}" class="cell-thick" />\n'
        svg += f'<line x1="{start_x}" y1="{start_y + pos}" x2="{start_x + 360}" y2="{start_y + pos}" class="cell-thick" />\n'

    # Fine Print Branding Credits Bottom Text
    svg += f"""
    <text x="220" y="470" class="footer-text">© 2026 Puzzle Ad Genius™ All Rights Reserved.</text>
    <text x="220" y="482" class="footer-text">Puzzle no. 098805349</text>
    </svg>"""
    return svg

if __name__ == "__main__":
    board = get_board_and_manage_date()
    
    with open("state.txt", "w") as f:
        for row in board:
            f.write(" ".join(map(str, row)) + "\n")
            
    svg_content = create_svg(board)
    with open("sudoku.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("Inverted sketch grid updated successfully!")
