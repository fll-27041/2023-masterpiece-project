#!/usr/bin/env python
import pygame
import math
import RPi.GPIO as GPIO

pygame.font.init()

# Defining variables used in programs
screen_width = 1024
screen_height = 768
draw_grid = True
screen = pygame.display.set_mode([screen_width, screen_height])
running = True
grid_size = 99
offset_x = 117
offset_y = 135
board = pygame.image.load("images//masterpiece-board.png").convert()
board_height = 478
board = pygame.transform.scale(board, (screen_width, board_height))
boxbot = pygame.image.load("images//robot-boxbot.png").convert()
boxbot = pygame.transform.scale(boxbot, (60, 90))
spawn_positions_x = [0, 1, 6, 7]
spawn_positions_y = [2, 3]
boxbot_grid_x = -1.0
boxbot_grid_y = -1.0
velocity_x = 0
velocity_y = 0
maxvelocity = grid_size
fight_back_font = pygame.font.Font('fonts/fightback.ttf', 50)
delta_x = 0
delta_y = 0
code = ''
velocity_decay = .99
recording = False
recorded_points = []

GPIO_X_0 = 36
GPIO_X_1 = 38
GPIO_X_2 = 40
GPIO_Y_0 = 37
GPIO_Y_1 = 35

def is_in_square(screen_x, screen_y, grid_x, grid_y):
    screen_grid_start_x = grid_x * grid_size + offset_x
    screen_grid_end_x = screen_grid_start_x + grid_size

    screen_grid_start_y = grid_y * grid_size + offset_y
    screen_grid_end_y = screen_grid_start_y + grid_size

    # print(f"Checking if {screen_x} > {screen_grid_start_x} and {screen_x} < {screen_grid_end_x}")
    if screen_x > screen_grid_start_x and screen_x < screen_grid_end_x: 
        if screen_y > screen_grid_start_y and screen_y < screen_grid_end_y:
            return True
        
    return False

def get_grid(screen_x, screen_y):
    for y in range (0, 4):
        for x in range(0, 8):
            if is_in_square(screen_x, screen_y, x, y):
                return (x, y)
    print("MISS")
    return (-1, -1)

def convert_binary(grid_x, grid_y):
    return ('{0:03b}'.format(grid_x), '{0:02b}'.format(grid_y))
    # return bin(grid_x)[2:], bin(grid_y)[2:]    
                # binary_x = str(binary[0])[2:]
                # binary_y = str(binary[1])[2:]
    # return (bin(grid_x), bin(grid_y))

def write_python_file():
    # Convert all recorded points into a path
    lines_of_code = []
    for i in range(len(recorded_points) - 1):
        old_x = recorded_points[i][0]
        old_y = recorded_points[i][1]
        new_x = recorded_points[i + 1][0]
        new_y = recorded_points[i + 1][1]
        display_move_code(old_x, old_y, new_x, new_y)
        lines_of_code.append(code)
        lines_of_code.append(code)

    return

def update_bot():
    global boxbot_grid_y
    global velocity_x
    global boxbot_grid_x
    global velocity_y

    boxbot_grid_y += 0.01 * velocity_y
    velocity_y *= velocity_decay
    boxbot_grid_x += 0.01 * velocity_x
    velocity_x *= velocity_decay

def display_move_code(old_x, old_y, new_x, new_y):
    global code
    delta_x = (new_x - old_x)
    delta_y = (new_y - old_y)
    #compute hypotenuse of delta_x and delta_y
    delta_distance = (math.sqrt((delta_x ** 2) + (delta_y ** 2)))

    #this is what we want to output
    str_distance = delta_distance * 304
    code = f"r.robot.straight(\"{str_distance:.2f}\")"
    print("We updated code to " + code)

def draw_bot(grid_x, grid_y):
    screen_x = grid_x * grid_size + offset_x + 20
    screen_y = grid_y * grid_size + offset_y + 5
    screen.blit(boxbot, (screen_x, screen_y))

def setup_gpio():   
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_X_0, GPIO.OUT)
    GPIO.setup(GPIO_X_1, GPIO.OUT)
    GPIO.setup(GPIO_X_2, GPIO.OUT)
    GPIO.setup(GPIO_Y_0, GPIO.OUT)
    GPIO.setup(GPIO_Y_1, GPIO.OUT)

    GPIO.output(GPIO_X_0, GPIO.LOW)
    GPIO.output(GPIO_X_1, GPIO.LOW)
    GPIO.output(GPIO_X_2, GPIO.LOW)
    GPIO.output(GPIO_Y_0, GPIO.LOW)
    GPIO.output(GPIO_Y_1, GPIO.LOW)


def light_up_grid(grid_x, grid_y): 
    # grid_x is a value from 0 to 7
    # grid_y is a value from 0 to 3

    # We will use these pins.
    # pins are numbered 1 to 40.
    # pin 1 and 2 are the top row.
    # 3 and 4 are next.  
    # 
    # PIN 39 is ground.
    # PIN 2 is 5V power 
    # PIN 1 is 3v3 power
    # PIN 36 (GPIO 19) is x bit 0 [ORANGE]
    # PIN 38 (GPIO 20) is x bit 1 [RED]
    # PIN 40 (GPIO 21) is x bit 2 [WHITE]
    # PIN 37 (GPIO 26) is y bit 0 [GREY]
    # PIN 35 (GPIO 19) is y bit 1 [YELLOW]
    (bin_x, bin_y) = convert_binary(int(grid_x), int(grid_y))
    
    if bin_x[2] == '1':
        print("GPIO_X_0 to HIGH")
        GPIO.output(GPIO_X_0, GPIO.HIGH)
    else:
        GPIO.output(GPIO_X_0, GPIO.LOW)
    if bin_x[1] == '1':
        print("GPIO_X_1 to HIGH")
        GPIO.output(GPIO_X_1, GPIO.HIGH)
    else:
        GPIO.output(GPIO_X_1, GPIO.LOW)
    if bin_x[0] == '1':
        print("GPIO_X_2 to HIGH")
        GPIO.output(GPIO_X_2, GPIO.HIGH)
    else:
        GPIO.output(GPIO_X_2, GPIO.LOW)
    if bin_y[1] == '1':
        print("GPIO_Y_0 to HIGH")
        GPIO.output(GPIO_Y_0, GPIO.HIGH)
    else:
        GPIO.output(GPIO_Y_0, GPIO.LOW)
    if bin_y[0] == '1':
        print("GPIO_Y_1 to HIGH")
        GPIO.output(GPIO_Y_1, GPIO.HIGH)
    else:
        GPIO.output(GPIO_Y_1, GPIO.LOW)                      

    # there are 8 pins that are hooked up to the rasperry bio

    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(4,GPIO.OUT)
    #GPIO.output(4,GPIO.LOW)
    #count = 0    


def game_loop():
    boxbot_spawned = False
    
    global code
    global velocity_x
    global velocity_y
    global boxbot_grid_x
    global boxbot_grid_y
    global draw_grid
    global recording
    global recorded_points

    clock = pygame.time.Clock()

    clicked_grid = []
    while running:
        for event in pygame.event.get():
            # This is the code to close when the user hits the X in the upper right
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    print("Great!")
                    velocity_y -= 0.1
                    if velocity_y > maxvelocity:
                        velocity_y = maxvelocity
                    print(f"velocity_y {velocity_y}")
                if event.key == pygame.K_a:
                    velocity_x -= 0.05
                    if abs(velocity_x) > maxvelocity:
                        velocity_x = - maxvelocity
                if event.key == pygame.K_s:
                    velocity_y += 0.05
                    if abs(velocity_y) > maxvelocity:
                        velocity_y = - maxvelocity
                if event.key == pygame.K_d:
                    velocity_x += 0.05
                    if abs(velocity_x) > maxvelocity:
                        velocity_x = maxvelocity
                if event.key == pygame.K_g:
                    draw_grid = not draw_grid
                if event.key == pygame.K_SPACE:
                    if recording == False:
                        recording = True
                        recorded_points = []
                    elif recording == True:
                        write_python_file()
                        recording = False
                

            if event.type == pygame.MOUSEBUTTONUP:
                
                #binary coversion code

                pos = pygame.mouse.get_pos()

                clicked_grid = get_grid(pos[0], pos[1])
                if clicked_grid is not (-1, -1):
                    print(f"Got this grid {clicked_grid} for this position {pos}")
                    binary = convert_binary(clicked_grid[0], clicked_grid[1])
                    print(f"Binary version {binary}")

                    if boxbot_spawned is False:
                        # If the click is in the home area, make the boxbot show up
                        if clicked_grid[0] in spawn_positions_x and clicked_grid[1] in spawn_positions_y:                        
                            boxbot_spawned = True

                    display_move_code(boxbot_grid_x, boxbot_grid_y, clicked_grid[0], clicked_grid[1])
                    boxbot_grid_x = clicked_grid[0]
                    boxbot_grid_y = clicked_grid[1]

                    light_up_grid(boxbot_grid_x, boxbot_grid_y)

                    if recording:
                        recorded_points.append((boxbot_grid_x, boxbot_grid_y))

                    
        screen.fill((125, 0, 125))
        screen.blit(board, (0, 90))
        if boxbot_spawned:
            update_bot()
            # light_up_grid(boxbot_grid_x, boxbot_grid_y)

            draw_bot(boxbot_grid_x, boxbot_grid_y)
            #make a picture of the code
            code_surface = fight_back_font.render(code, False, (111, 196, 169))
            #get rect
            code_rect = code_surface.get_rect(center = (screen_width / 2, screen_height / 2 + 250))
            screen.blit(code_surface, code_rect)


        if draw_grid:
            for y in range (0, 5):
                    # print(f"Drawing line {y} at height {y * grid_size}")
                    pygame.draw.line(screen, (0, 255, 0), 
                                (0, offset_y + y * grid_size),  
                                (screen_width, offset_y + y * grid_size),
                                1)
            for x in range(0, 9):
                pygame.draw.line(screen, (0, 255, 0), 
                            (offset_x + x * grid_size, 0),  
                                (offset_x + x * grid_size, screen_height),
                                1)
        
        if recording:
            recording_surface = fight_back_font.render("RECORDING", False, (111, 196, 169))
            
            # Draw the list of nodes
            for i in range(len(recorded_points) - 1):
                old_x = recorded_points[i][0]
                old_y = recorded_points[i][1]
                new_x = recorded_points[i + 1][0]
                new_y = recorded_points[i + 1][1]
                pygame.draw.line(screen, (255, 0, 0), (old_x * 99, old_y * 99), (new_x * 99, new_y * 99))
            
            #get rect
            recording_rect = recording_surface.get_rect(center = (screen_width / 2, screen_height / 2 -320))
            screen.blit(recording_surface, recording_rect)


        pygame.display.flip()
        clock.tick(60)

        # count = count + 1
        # if count % 2 == 0:
        #     GPIO.output(4,GPIO.HIGH)
        # else:
        #     GPIO.output(4,GPIO.LOW)
        # time.sleep(1 / 0.5)
        
#this is where main code begins
pygame.init()
pygame.key.set_repeat(100, 50)
setup_gpio()
game_loop()
pygame.quit()
