import pygame
pygame.init()
from random import randint

def move(snake, direction):
    if direction == 0:
        snake.append((snake[-1][0], snake[-1][1]+1))
    elif direction == 1:
        snake.append((snake[-1][0]+1, snake[-1][1]))
    elif direction == 2:
        snake.append((snake[-1][0], snake[-1][1]-1))
    elif direction == 3:
        snake.append((snake[-1][0]-1, snake[-1][1]))
    snake.pop(0)

def draw(surface, snake, tile_size, food):
    w,h = surface.get_size()
    for i in range(w//tile_size+1):
        pygame.draw.line(surface, (50,50,50), ((i+1)*tile_size,0), ((i+1)*tile_size, h))
    for i in range(h//tile_size):
        pygame.draw.line(surface, (50,50,50), (0,(i+1)*tile_size), (w,(i+1)*tile_size))

    prev_pos = snake[0]
    for s in snake:
        if s is prev_pos:
            pygame.draw.rect(surface, (0,150,0), ((s[0]*tile_size+1, s[1]*tile_size+1), (tile_size-1, tile_size-1)))
        else:
            if prev_pos[0] < s[0]:
                pygame.draw.rect(surface, (0,150,0), ((s[0]*tile_size, s[1]*tile_size+1), (tile_size, tile_size-1)))
            elif prev_pos[0] > s[0]:
                pygame.draw.rect(surface, (0,150,0), ((s[0]*tile_size+1, s[1]*tile_size+1), (tile_size, tile_size-1)))
            elif prev_pos[1] > s[1]:
                pygame.draw.rect(surface, (0,150,0), ((s[0]*tile_size+1, s[1]*tile_size+1), (tile_size-1, tile_size)))
            elif prev_pos[1] < s[1]:
                pygame.draw.rect(surface, (0,150,0), ((s[0]*tile_size+1, s[1]*tile_size), (tile_size-1, tile_size)))
        prev_pos = s
    pygame.draw.rect(surface, (150,0,0), ((food[0]*tile_size+1, food[1]*tile_size+1), (tile_size-1, tile_size-1)))

def update(snake, direction, sizex, sizey, food,m=True):
    if m:
        move(snake, direction)
    if snake[-1][0] == -1:
        return True
    if snake[-1][0] == sizex:
        return True
    if snake[-1][1] == -1:
        return True
    if snake[-1][1] == sizey:
        return True

    if snake.count(snake[-1]) != 1:
        return True
    if snake[-1] == food:
        return False
    return None

def new_food(snake, sizex, sizey):
    x, y = randint(0, sizex-1), randint(0, sizey-1)
    for i in range(20):
        if (x,y) not in snake:
            break
        x, y = randint(0, sizex-1), randint(0, sizey-1)
    return x,y

def game_loop():
    SCREEN = pygame.display.set_mode((800,600))

    direction = 0
    tile_size = 20
    sizex = SCREEN.get_width()//tile_size
    sizey = SCREEN.get_height()//tile_size
    snake = [(randint(0,sizex-5), randint(0,sizey-5))]

    food = new_food(snake, sizex, sizey)
    score = 0
    font = pygame.font.SysFont(None, 50)
    txt = font.render("0", True, (255,255,255))

    C = pygame.time.Clock()
    while True:
        SCREEN.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_RIGHT:
                    direction = 1
                elif event.key == pygame.K_UP:
                    direction = 2
                elif event.key == pygame.K_DOWN:
                    direction = 0
                elif event.key == pygame.K_LEFT:
                    direction = 3

        a = update(snake, direction, sizex, sizey, food)
        if a:
            return
        elif a == False:
            snake.append(food)
            food = new_food(snake, sizex, sizey)
            score += 1
            txt = font.render(str(score), True, (255,255,255))
        draw(SCREEN, snake, tile_size, food)
        SCREEN.blit(txt, (sizex*tile_size-50,10))
        pygame.display.update()
        C.tick(10)

def generate_path(sizex, sizey):
    begin = (0,0)
    path = [begin]
    return path

def ia():
    SCREEN = pygame.display.set_mode((800,600))

    print(generate_path(20,20))

    direction = 0
    tile_size = 20
    sizex = SCREEN.get_width()//tile_size
    sizey = SCREEN.get_height()//tile_size
    snake = [(0,0) for i in range(1)]

    path = [(0,0)]

#     #sizex et sizey pairs
#     path.append((path[-1][0]+1, path[-1][1]))
#     path.append((path[-1][0], path[-1][1]+1))
#     for i in range((sizey//2)//2):
#         for x in range((sizex//2)-1):
#             path.append((path[-1][0]+1, path[-1][1]))
#             path.append((path[-1][0], path[-1][1]-1))
#             path.append((path[-1][0]+1, path[-1][1]))
#             path.append((path[-1][0], path[-1][1]+1))
#         for j in range(2):
#             path.append((path[-1][0], path[-1][1]+1))
#         for x in range((sizex//2)-1):
#             path.append((path[-1][0]-1, path[-1][1]))
#             path.append((path[-1][0], path[-1][1]-1))
#             path.append((path[-1][0]-1, path[-1][1]))
#             path.append((path[-1][0], path[-1][1]+1))
#         for j in range(2):
#             path.append((path[-1][0], path[-1][1]+1))
#     path.pop(len(path)-1)
#     path.pop(len(path)-1)
#     path.append((path[-1][0]-1, path[-1][1]))
#     for i in range(sizey-2):
#         path.append((0,sizey-2-i))
#         print(path[-1])


    for i in range(1,sizex):
        for j in range(0,sizey-1):
            if i % 2 == 0:
                path.append((i,sizey-j-2))
            else:
                path.append((i,j))
    for i in range(sizex):
        path.append((sizex-1-i,sizey-1))
    for i in range(sizey-2):
        path.append((0,sizey-2-i))

    step = 1

    food = new_food(snake, sizex, sizey)
    score = 0
    font = pygame.font.SysFont(None, 50)
    txt = font.render("0", True, (255,255,255))

    l = len(path)-1
    length = l+1
#     l = min(100, l)
    print(len(path),l)

    speed = 37464
    mode = True
    C = pygame.time.Clock()
    while True:
        SCREEN.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_s:
                    mode = not mode
                    if speed == 37464:
                        speed = 20
                    else:
                        speed = 37464
#                 elif event.key == pygame.K_RIGHT:
#                     direction = 1
#                 elif event.key == pygame.K_UP:
#                     direction = 2
#                 elif event.key == pygame.K_DOWN:
#                     direction = 0
#                 elif event.key == pygame.K_LEFT:
#                     direction = 3

        snake.append(path[step])
        u = update(snake, direction, sizex, sizey, food,m=False)
        snake.pop(0)

        a,b = snake[-1]
        pos = None
        for i in range(l):
            x,y = path[(step+1+i)%length]
            if (x,y) in snake:
                break
            elif (x,y) == food:
                break
            if i > 0 and ((max(x,a)-min(x,a) == 1 and max(y,b)-min(y,b) == 0) or (max(x,a)-min(x,a) == 0 and max(y,b)-min(y,b) == 1)):
                for j in range(10):
                    if (path[(step+1+i+j)%length] in snake):
                        a = False
                if a:
                    pos = (step+i)%length#step = (step+i)%len(path)
                break
                #print((x,y),(a,b),food)
        if pos is not None:
            step = pos


        if u:
            return
        elif u == False:
            snake.insert(0, food)
            food = new_food(snake, sizex, sizey)
            score += 1
            txt = font.render(str(score), True, (255,255,255))
        if not mode or step%2==0:
            draw(SCREEN, snake, tile_size, food)
            SCREEN.blit(txt, (sizex*tile_size-50,10))
            pygame.display.update()
        C.tick(speed)
        step += 1
        step %= length

def main():
    SCREEN = pygame.display.set_mode((800,600))

    font = pygame.font.SysFont(None, 100)
    txt = font.render("Press a key ...", True, (255,255,255))

    x, y = SCREEN.get_rect().center
    w,h = txt.get_size()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                else:
                    #game_loop()
                    ia()

        SCREEN.fill((0,0,0))
        SCREEN.blit(txt, (x-w/2, y-h/2))
        pygame.display.update()

if __name__ == "__main__":
    main()
