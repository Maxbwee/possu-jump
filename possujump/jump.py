# importing different libraries
import pygame
import random

# initialize pygame
pygame.init()

# game window
# Capital letters because these will be constants in the game 
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# create game window
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Possu Jump')

# setting framerate of the game
clock = pygame.time.Clock()
FPS = 60

# game variables

SCROLL_START = 200
GRAVITY = 1
MAX_PLATFORMS = 10
scroll = 0
bg_scroll = 0
game_over = False
score = 0

# define colors
WHITE = (255, 255, 255)

# font for game
font_small = pygame.font.SysFont('lucidaconsole', 20)
font_big = pygame.font.SysFont('lucidaconsole', 24)

# prints a list of available fonts with pygame
# print(pygame.font.get_fonts())

# load game images
possu_img = pygame.image.load('possujump/assets/possu.png').convert_alpha()
gamebg_image = pygame.image.load('possujump/assets/possubg.png').convert_alpha()
platform_img = pygame.image.load('possujump/assets/possuplatform.png').convert_alpha()

# function to output game over text with
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))

# function for drawing the background for the game
def draw_bg(bg_scroll):
     window.blit(gamebg_image, (0, 0 + bg_scroll))
     window.blit(gamebg_image, (0, -600 + bg_scroll))


# player character
class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(possu_img, (80,80))
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False
    
    # Draw method needs a self argument always
    def move(self):
        # reset variables
        # changes in the delta variables of the x and y coordinates
        scroll = 0
        dx = 0
        dy = 0

        # keyboard input for moving the possu
        key = pygame.key.get_pressed()
        
        if key[pygame.K_a]:
            dx = -10
            self.flip = True
        if key[pygame.K_d]:
            dx = 10
            self.flip = False


        # gravity that pulls the character down increases gravity by 1 each game loop
        self.vel_y += GRAVITY
        dy += self.vel_y

        # collision to make sure the character doesn't go off the screen left and right
        if self.rect.left + dx  < 0:
            dx = 0 - self.rect.left

        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        #check jumping on platforms and collision in y direction
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if the player is above the platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20


        # check if the player is at the top of the screen
        # if the player moves up the screen everything else moves down with -dy variable
        if self.rect.top <= SCROLL_START:
            # if player is jumping
            if self.vel_y < 0:
                scroll = -dy
            
        # updates the position of the character.
        # controls the vertical position of the player
        self.rect.x += dx
        # will freeze the players position on the screen dy - dy
        self.rect.y += dy + scroll      
            
        return scroll

    def draw(self):
        window.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 20, self.rect.y - 25))
        pygame.draw.rect(window, WHITE, self.rect, 2)

# Making the platforms for the game
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_img, (width, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self, scroll):
        # updating the platforms vertical position
        self.rect.y += scroll

        # check if the platforms are still in the game window
        # gets rid of platforms that leave the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# The character possu is an instance of the Player() class
possu = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

# create platform groups 
platform_group = pygame.sprite.Group()

# create starting platforms
platform = Platform(SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT - 50, 100)
platform_group.add(platform)

# Keeps game running
run = True

while run:

    clock.tick(FPS)

    if game_over == False:

        scroll = possu.move()

        # print(scroll) checking if the game recognizes the scroll
        
        # draw background
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll)

        # generate platforms
        # to generate platforms you need x , y and width
        if len(platform_group) < MAX_PLATFORMS:
            # platform width between 40 and 60 pixels
            p_width = random.randint(40, 60)
            # platform x coordinate 
            p_x = random.randint(0, SCREEN_WIDTH - p_width)
            # platform y coordinate
            p_y = platform.rect.y - random.randint(80, 120)
            platform = Platform(p_x, p_y, p_width)
            platform_group.add(platform)
        
        # update platforms
        # update starts empty but platform_group and call the method
        platform_group.update(scroll)
        #draw player character and platforms
        platform_group.draw(window)
        possu.draw()
        
        # check if the game ends = player falls off the screen
        if possu.rect.top > SCREEN_HEIGHT:
            game_over = True

        # Check if python recognizes game over
        # the console logs false if the player is on the screen
        # and logs True if the player falls off the screen
        # = Game over
        # print (game_over)
    else:
        draw_text('GAME OVER POSSU!', font_big, WHITE, 90, 200)
        draw_text('SCORE: ' + str(score), font_big, WHITE, 130, 250)
        draw_text('PRESS SPACE TO PLAY AGAIN', font_big, WHITE, 40, 300)
        key = pygame.key.get_pressed()
        if key [pygame.K_SPACE]:
            # reset the game
            game_over = False
            score = 0
            scroll = 0
            # reset possu
            possu.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
            # reset platforms
            platform_group.empty()
            # create starting platforms
            platform = Platform(SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT - 50, 100)
            platform_group.add(platform)

    # pygame event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update the game window
    pygame.display.update()

pygame.quit()