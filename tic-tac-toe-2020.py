import pygame as pg

pg.init()

# Board properties
width = 7
height = 7
win_length = 4

print(f"Win length is {win_length} tiles\nwidth {width} tiles\nheight {height} tiles")

board = [width * [0] for h in range(height)]
spots = width * height
player = 1

# Window
win_width, win_height = 1280, 720  # Starting resolution
win_info = pg.display.Info()

# Info details
bar = [260, 50]  # px
font = pg.font.SysFont('trebuchetms', 40)
bar_text = font.render("Player 1's turn", False, (255, 255, 255))
bar_text_width, bar_text_height = bar_text.get_rect()[2:4]

# Tile creation
tile_color = {0: (255, 255, 255), 1: (255, 0, 0), -1: (0, 0, 255)}
tile_size = win_width // width if min([win_width/width, (win_height - bar[1])/height]) == win_width/width \
                else (win_height - bar[1]) // height
tile_margin = round(tile_size * 0.1) if round(tile_size * 0.1) > 1 else 1
tile_size = round(tile_size * 0.9) if round(tile_size * 0.9) > 1 else 1

hover = []
hover_tile = pg.Surface((tile_size, tile_size))
hover_tile.set_alpha(128)
hover_tile.fill(tile_color[player])

# Window again
win_width = tile_size * width + tile_margin * (width + 1)
win_width = bar[0] if bar[0] > win_width else win_width
win_height = tile_size * height + tile_margin * (height + 1) + bar[1]
win = pg.display.set_mode([win_width, win_height], pg.RESIZABLE)
resized = False


# Algorithms to detect if a player has won
def horizontal(p):
    for y in range(height):
        count = 0
        for x in range(width):
            count = count + 1 if board[y][x] == p else 0
            if count == win_length:
                return True
    return False


def vertical(p):
    for x in range(width):
        count = 0
        for y in range(height):
            count = count + 1 if board[y][x] == p else 0
            if count == win_length:
                return True
    return False


def bslash(p):
    for x in range(width - win_length + 1):
        count = 0
        for d in range(min([width - x, height])):
            count = count + 1 if board[d][x + d] == p else 0
            if count == win_length:
                return True
    for y in range(1, height - win_length + 1):
        count = 0
        for d in range(min([width, height - y])):
            count = count + 1 if board[y + d][d] == p else 0
            if count == win_length:
                return True
    return False


def slash(p):
    for x in range(width - win_length + 1):
        count = 0
        for d in range(min([width - x, height])):
            count = count + 1 if board[d][width-1 - x - d] == p else 0
            if count == win_length:
                return True
    for y in range(1, height - win_length + 1):
        count = 0
        for d in range(min([width, height - y])):
            count = count + 1 if board[y + d][width-1 - d] == p else 0
            if count == win_length:
                return True
    return False


def fullTest(p):
    if any([horizontal(p), vertical(p), bslash(p), slash(p)]):
        return True

# Drawing tiles and text
def draw():
    win.fill((0, 0, 0))
    # generate tiles
    for x in range(width):
        for y in range(height):
            pg.draw.rect(win, tile_color[board[y][x]],
                         (tile_margin + x * (tile_margin + tile_size),
                          tile_margin + y * (tile_margin + tile_size) + bar[1],
                          tile_size, tile_size))
    # Hover tile
    if hover:
        win.blit(hover_tile, (tile_margin + hover[1] * (tile_margin + tile_size),
                              tile_margin + hover[0] * (tile_margin + tile_size) + bar[1]))

    # Draw text
    win.blit(bar_text, ((win_width - bar_text_width)//2, (bar[1] - bar_text_height)//2))


# Setup
game = True
end = False
# Main
while not end:
    if game:
        # Interaction
        # check if player is hovering above playing area
        mouse_x, mouse_y = pg.mouse.get_pos()
        if 0 < mouse_x < win_width and bar[1] < mouse_y < win_height:
            # check if player is hovering above free spot
            row = int((mouse_y - bar[1]) / (win_height - bar[1]) * height)
            col = int(mouse_x / win_width * width)
            if not board[row][col]:
                hover = [row, col]

                # Check for actual input
                if pg.mouse.get_pressed()[0]:
                    # update board position
                    board[row][col] = player
                    spots -= 1
                    # check if board is full
                    if not spots:
                        # Game over
                        bar_text = font.render("It's a Tie!",
                                               False, (255, 255, 255))
                        bar_text_width, bar_text_height = bar_text.get_rect()[2:4]
                        hover = []
                        game = False
                    # check if player has won
                    elif fullTest(player):
                        # Game Over
                        bar_text = font.render("Player" + ("1" if player == 1 else "2") + " won!",
                                               False, (255, 255, 255))
                        bar_text_width, bar_text_height = bar_text.get_rect()[2:4]
                        hover = []
                        game = False
                    # move to next turn
                    else:
                        player *= -1

                        hover_tile.fill(tile_color[player])
                        bar_text = font.render("Player " + ("1" if player == 1 else "2") + "'s turn",
                                               False, (255, 255, 255))
            else:
                hover = []

    # Other property updates
    for event in pg.event.get():

        if event.type == pg.QUIT:
            game = False
            end = True

        # Window resizing
        elif event.type == pg.VIDEORESIZE:
            if not resized:
                win_width, win_height = event.size
                tile_size = win_width // width if min([win_width/width, (win_height - bar[1])/height]) == win_width/width \
                    else (win_height - bar[1]) // height
                tile_margin = round(tile_size * 0.1) if round(tile_size * 0.1) > 1 else 1
                tile_size = round(tile_size * 0.9) if round(tile_size * 0.9) > 1 else 1
                hover_tile = pg.transform.scale(hover_tile, (tile_size, tile_size))

                # Window again
                win_width = tile_size * width + tile_margin * (width + 1)
                win_width = bar[0] if bar[0] > win_width else win_width
                win_height = tile_size * height + tile_margin * (height + 1) + bar[1]
                win = pg.display.set_mode([win_width, win_height], pg.RESIZABLE)
                resized = True
            else:
                resized = False

    # Update screen
    draw()
    pg.display.update()

pg.quit()  # Perfect.
