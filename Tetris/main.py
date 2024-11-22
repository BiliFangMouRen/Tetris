import pygame
import random
import os

# 初始化Pygame
pygame.init()

# 窗口大小
screen_width = 800
screen_height = 600
game_width = 300  # 游戏区域宽度
game_height = 600  # 游戏区域高度
block_size = 30  # 方块大小

# 创建窗口
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('俄罗斯方块')

# 游戏区域
top_left_x = (screen_width - game_width) // 2
top_left_y = screen_height - game_height

# 定义形状
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# 创建方块类
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

# 创建游戏网格
def create_grid(locked_positions={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

# 转换形状格式
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

# 检查是否有有效空间
def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

# 检查是否游戏结束
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

# 获取随机形状
def get_shape():
    return Piece(5, 0, random.choice(shapes))

# 绘制文本中间
def draw_text_middle(text, size, color, surface):
    font_path = os.path.join(os.getcwd(), '苹方字体.ttf')
    font = pygame.font.Font(font_path, size)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + game_width/2 - (label.get_width() / 2), top_left_y + game_height/2 - label.get_height()/2))

# 绘制网格
def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+game_width, sy+ i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + game_height))

# 清除满行
def clear_rows(grid, locked, surface):
    inc = 0
    rows_to_clear = []

    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            rows_to_clear.append(i)
            inc += 1

    if inc > 0:
        # 闪烁效果
        for i in range(5):  # 闪烁次数
            for row in rows_to_clear:
                pygame.draw.rect(surface, (255, 255, 255, 128), (top_left_x, top_left_y + row * block_size, game_width, block_size))
            pygame.display.update()
            pygame.time.delay(100)

            for row in rows_to_clear:
                pygame.draw.rect(surface, (0, 0, 0), (top_left_x, top_left_y + row * block_size, game_width, block_size))
            pygame.display.update()
            pygame.time.delay(100)

        for row in rows_to_clear:
            for j in range(len(grid[row])):
                try:
                    del locked[(j, row)]
                except:
                    continue

        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < rows_to_clear[0]:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc

# 绘制下一个形状
def draw_next_shape(shape, surface):
    font_path = os.path.join(os.getcwd(), '苹方字体.ttf')
    font = pygame.font.Font(font_path, 30)
    label = font.render('下一个', 1, (255,255,255))

    sx = top_left_x + game_width + 50
    sy = top_left_y + game_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))

# 更新分数
def update_score(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

# 获取最高分
def max_score():
    if not os.path.exists('scores.txt'):
        with open('scores.txt', 'w') as f:
            f.write('0')

    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score

# 绘制窗口
def draw_window(surface, grid, score=0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font_path = os.path.join(os.getcwd(), '苹方字体.ttf')
    font = pygame.font.Font(font_path, 60)
    label = font.render('俄罗斯方块', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + game_width / 2 - (label.get_width() / 2), 30))

    # 当前得分
    font = pygame.font.Font(font_path, 30)
    label = font.render('得分: {}'.format(score), 1, (255, 255, 255))

    sx = top_left_x + game_width + 50
    sy = top_left_y + game_height/2 - 100

    surface.blit(label, (sx + 20, sy + 160))

    # 最高得分
    label = font.render('最高分: {}'.format(max_score()), 1, (255, 255, 255))

    sx = top_left_x - 200
    sy = top_left_y + 200

    surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    draw_grid(surface, grid)
    pygame.display.update()

# 主循环
def main():
    global grid

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.27

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            score += clear_rows(grid, locked_positions, screen) * 10

        draw_window(screen, grid, score)
        draw_next_shape(next_piece, screen)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle("GAME OVER", 80, (255,255,255), screen)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)

# 主菜单
def main_menu():
    run = True
    while run:
        screen.fill((0,0,0))
        draw_text_middle('按任意键开始', 60, (255, 255, 255), screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()

main_menu()
