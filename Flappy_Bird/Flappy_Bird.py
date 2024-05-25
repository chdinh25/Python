import pygame, sys, random

# Function to control floors movement
# Create 2 floors to keep the floor running at the bottom of the play screen
def flooring():
    # 1st floor
    playscreen.blit(floor,(floor_x_pos, 650))
    # 2nd floor will start from the x-axis of the first floor and adding the play screen width
    playscreen.blit(floor,(floor_x_pos + width, 650))

# Function to create pipes
def create_pipe():
    # Use random() to pick the random height from pipe_height
    random_pipe_pos = random.choice(pipe_height)
    # Create the bottom pipes
    bottom_pipe = pipe_column.get_rect(midtop = (500, random_pipe_pos))
    # Create the top pipe, 700 is distance between top and bottom pipes
    top_pipe = pipe_column.get_rect(midtop = (500, random_pipe_pos - 700))
    return bottom_pipe, top_pipe

# Function to control pipes movement
def pipe_movement(pipes):
	for pipe in pipes :
        # Move pipes to the left
		pipe.centerx -= 5
	return pipes

# Function to draw pipes on the play screen
def piping(pipes):
    for pipe in pipes:
        # Use if to check if pipe.bottom >= 600, pygame will recognize as bottom_pipe
        if pipe.bottom >= 600 : 
            playscreen.blit(pipe_column, pipe)
        # If not, pygame will recognize as top_pipes and flip the picture of the pipes
        else:
            # Since pipes need to be flip vertically, the y-axis is True and x-axis is False
            flip_pipe = pygame.transform.flip(pipe_column, False, True)
            playscreen.blit(flip_pipe, pipe)

# Function to check the collisions 
def collision_check(pipes):
    for pipe in pipes:
        # Use colliderect(0 to check collision)
        if bird_rectangle.colliderect(pipe):
            # Add hit sound
            hit_sound.play()
            return False
    # Use if to check if the bird over the ceiling(0) or under the floor(650)
    if bird_rectangle.top <= -75 or bird_rectangle.bottom >= 650:
            return False
    return True 

# Function to make the bird more lively
def rotate_bird(bird1):
	new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 3, 1)
	return new_bird

# Function to control the bird animation
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rectangle = new_bird.get_rect(center = (100, bird_rectangle.centery))
    return new_bird, new_bird_rectangle

# Function to display the score
def score_output(game_state):
    # Use if statement to check if the game state is "active" or "over"
    if game_state == 'active':
        current_score = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rectangle = current_score.get_rect(center = (216, 100))
        playscreen.blit(current_score, score_rectangle)
    if game_state == 'over':
        current_score = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rectangle = current_score.get_rect(center = (216, 100))
        playscreen.blit(current_score, score_rectangle)

        high_current_score = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rectangle = high_current_score.get_rect(center = (216, 630))
        playscreen.blit(high_current_score, high_score_rectangle)

# Function to update the highest score as new highest is reached
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

# Adjust all the sound to suit for the pygame
pygame.mixer.pre_init(frequency = 44100, size = -16, channels = 2, buffer = 512)
pygame.init()

# Set width and height of the play screen
width = 432
height = 768
playscreen = pygame.display.set_mode((width, height))
# Set SPF for the game
clock = pygame.time.Clock()
# Set font for the game
game_font = pygame.font.Font('font.ttf', 33)

# Initialize all the variables for the game
gravity = 0.4
bird_movement = 0
game_active = True
score = 0
high_score = 0

# Insert background, use load() to load photo from the system
background = pygame.image.load('packages/background-night.png').convert()
# Scale background 2 time to fix the window since the original photo is 2 times smaller
background = pygame.transform.scale2x(background)

# Insert floor, use load() to load photo from the system
floor = pygame.image.load('packages/floor.png').convert()
# Scale floor 2 time to fix the window since the original photo is 2 times smaller
floor = pygame.transform.scale2x(floor)
# Initialize the floor x-axis position to 0
floor_x_pos = 0

# Create the birds, and use convert() to load objects faster
bird_down = pygame.transform.scale2x(pygame.image.load('packages/bird-down.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('packages/bird-mid.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('packages/bird-up.png').convert_alpha())
# Create a list to store all values of bird
bird_list= [bird_down, bird_mid, bird_up]
# Initialize the list index to 0 since the list index start at 0
bird_index = 0
bird = bird_list[bird_index]

# Create a rectangle around the bird so pygame can recognize as the bird get hits
# The position is 100 from the left edge and middle of the height
bird_rectangle = bird.get_rect(center = (100, height/2))

# Create timer for bird, bird flap every 0.1s
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 100)

# Insert pipes
pipe_column = pygame.image.load('packages/pipe.png').convert()
pipe_column = pygame.transform.scale2x(pipe_column)
pipe_list = []

# Create the timer for pipes to create random pipe after the amount of time, in this case is 1.2s
random_pipe = pygame.USEREVENT
pygame.time.set_timer(random_pipe , 1200) 

# Declare list pipe_height to hold all the heights of pipes
pipe_height = [200, 300, 400]

# Insert ending background
game_over_message = pygame.transform.scale2x(pygame.image.load('packages/message.png').convert_alpha())
game_over_rectangle = game_over_message.get_rect(center=(216,384))

# Insert sounds
flap_sound = pygame.mixer.Sound('sounds/wing.wav')
hit_sound = pygame.mixer.Sound('sounds/hit.wav')
score_sound = pygame.mixer.Sound('sounds/point.wav')
score_sound_countdown = 100

# Use while loop to keep the window game open
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            #fix error: video system not initialized
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # Use if to check if SpaceBar iss hit and game is active
            if event.key == pygame.K_SPACE and game_active:
                # Set bird_movement to 0, so the bird do not under any force atm
                bird_movement = 0
                # -10 since the bird need to go up as SpaceBar is hit
                bird_movement = -10
                # Insert sound
                flap_sound.play()
            # If SpaceBar is hit and the game is not active
            if event.key == pygame.K_SPACE and game_active == False:
                # Start a new game as SpaceBAr is hit again
                game_active = True 
                # Clear all the pipe_list from the previous game play
                pipe_list.clear()
                # Reset the bird, set the bird's position to 100 from the left edge and middle of the height
                bird_rectangle.center = (100, height/2)
                # Reset bird movement
                bird_movement = 0 
                # Reset score
                score = 0 
        if event.type == random_pipe :
            pipe_list.extend(create_pipe())
        
        # Use if to control bird flap, to switch between up, mid and down bird 
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0 
            bird, bird_rectangle = bird_animation()    

    # Add background to play screen        
    playscreen.blit(background,(0, 0))
    if game_active:
        # Add gravity to the bird movement
        bird_movement += gravity
        rotated_bird = rotate_bird(bird) 
        # Add bird_movement to the y-axis od the rectangle to pull the bird downward      
        bird_rectangle.centery += bird_movement
        # Add bird to play screen
        playscreen.blit(rotated_bird, bird_rectangle)
        # Call collision_check() to check collision 
        game_active= collision_check(pipe_list)
        # Pipes
        # Take all pipe_list as parameter, move it to the left and return new pipe_list
        pipe_list = pipe_movement(pipe_list)
        # Add pipes to the play screen by calling piping()
        piping(pipe_list)
        score += 0.01
        score_output('active')

        # Scored sound
        score_sound_countdown -= 1
        # Use if statement to check if scored, play sound
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        playscreen.blit(game_over_message, game_over_rectangle)
        high_score = update_score(score, high_score)
        score_output('over')

    # Floor movement
    floor_x_pos -= 1
    flooring()
    # Use if statement to keep the floor running. As the 2nd floor is almost finished,
    # the 1st floor will fill up and keep running
    if floor_x_pos <= -width:
        floor_x_pos = 0
    
    pygame.display.update()
    # Set SPF for the game
    clock.tick(120)