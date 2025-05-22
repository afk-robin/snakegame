import pygame
import random
from sys import exit
pygame.init()

width, height= 800 , 640  
g_a_height= 600
cell_size= 20

bg_color= (162,166,0)
snake_color= (0,255,0)
head_color= (0,0,0)
food_color= (255,0,0)
text_color= (255,255,255)
tile_color= (50,50,50)

screen  = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def get_random_position(snake_color):
    while True:
        x=random.randint(0,(width - cell_size)// cell_size)*cell_size
        y=random.randint(0,(g_a_height - cell_size)// cell_size)*cell_size
        if (x,y) not in snake_color:
            return (x,y)
        
def draw_score(score,high_score):
    score_surface = font.render(f"Score: {score} High Score: {high_score}",True,text_color)
    screen.blit(score_surface,(10, g_a_height+5))

def draw_game_over():
    tile_width,tile_height = 400,100
    tile_x = (width-tile_width) // 2
    tile_y = (g_a_height-tile_height) // 2
    pygame.draw.rect(screen, tile_color,(tile_x,tile_y,tile_width,tile_height),border_radius=10)
    game_over_text = font.render("GAME OVER!",True, text_color)
    restart_text = font.render("Press R to Restart or ESC to Quit", True, text_color)
    screen.blit(game_over_text, (tile_x+ (tile_width-game_over_text.get_width()) // 2 , tile_y + 20 ))
    screen.blit(restart_text, (tile_x+ (tile_width-restart_text.get_width()) // 2 , tile_y + 60 ))

snake = [(100,100) , (80,100) , (60,100)]
direction = (cell_size,0)
food_position = get_random_position(snake)
score = 0
high_score = 0
speed = 10
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    snake = [(100,100) , (80,100) , (60,100)]
                    direction = (cell_size,0)
                    food_position = get_random_position(snake)
                    score = 0
                    speed = 10
                    game_over = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            else:
                if event.key == pygame.K_UP and direction !=(0 , cell_size):
                    direction = (0 , -cell_size )
                elif event.key == pygame.K_DOWN and direction !=(0 , -cell_size):
                    direction = (0 , cell_size )
                elif event.key == pygame.K_LEFT and direction !=( cell_size, 0):
                    direction = (-cell_size , 0)
                elif event.key == pygame.K_RIGHT and direction !=(-cell_size, 0):
                    direction = (cell_size , 0)
    if not game_over:
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if (new_head in snake) or (new_head[0]< 0 or new_head[0]>= width or new_head[1]< 0 or new_head[1]>= g_a_height):
            game_over = True
            if score > high_score:
                high_score = score
            continue
        snake.insert(0, new_head)

        if new_head == food_position:
            score += 10
            food_position = get_random_position(snake)
            if score % 50 == 0:
                speed += 1
        else:
            snake.pop()
        screen.fill((0, 0, 0))
        game_surface = pygame.Surface((width, g_a_height))
        game_surface.fill(bg_color)
        screen.blit(game_surface,(0, 0))

        pygame.draw.circle(screen, food_color, (food_position[0] + cell_size // 2, food_position[1] + cell_size // 2), cell_size // 2)

        for i,segment in enumerate(snake):
            color = head_color if i == 0 else snake_color
            pygame.draw.rect(screen, color, pygame.Rect(segment[0],segment[1], cell_size , cell_size))

        draw_score(score,high_score)
    else:
        draw_game_over()
    pygame.display.update()
    clock.tick(speed)