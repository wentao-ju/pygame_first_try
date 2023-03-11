import pygame, sys
from random import randint, choice

#using Sprite class for visible gaming objects, return Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #load player images
        #.convert_alpha() can make the image fits Pygame better and eliminate white color surrounding the image
        player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1,player_walk2]  #create the list to store two walking images of the player
        self.player_index = 0  #initial the list index
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80,300))  #locate the player image
        self.gravity = 0  #initial gravity to zero

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()  #get the key input
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:  #if the key is space and player is on the ground
            self.gravity = -18  #throw the player image up
            self.jump_sound.play()  #play jump sound

    def apply_gravity(self):  #fall state after jump
        self.gravity += 0.8
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:  #check if the player should stand on the ground
            self.rect.bottom = 300
    
    def animation_state(self):  #for jump and walk animations
        if self.rect.bottom < 300:  #for jump state
            self.image = self.player_jump  #show jump image
        else:
            self.player_index += 0.1  #increase index 0.1 per frame
            if self.player_index >= len(self.player_walk):  #set index to 0 if index over the length of the list
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]  #walk image switch every 10 frames

    def update(self):  #update for each frame
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        #there are two types of Obstacle: fly and snail
        if type == 'fly':
            fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame1,fly_frame2]
            self.y_position = 200  #locate the bottom of fly image
        else:
            snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1,snail_frame2]
            self.y_position = 300  #locate the bottom of snail image
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]

        #spawning obstacle at random location
        self.rect = self.image.get_rect(midbottom=(randint(900,1100),self.y_position))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destory(self):
        if self.rect.x < -100:  #if the obstacle out of the screen, remove it
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 5  #the movement speed of each obstacle is 5 pixel per frame from left
        self.destory()  

def display_score():
    #get_ticks() return the running time scince pygame.init() in ms
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surface = text_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surface.get_rect(center=(400,50))
    screen.blit(score_surface,score_rect)

    return current_time

def collision_sprite():  #return boolean for game_active state
    #.spritecollide() detects the collision between two Sprite groups
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()  #if collides, initial obstacle as empty
        return False
    else:
        return True


pygame.init()  #initial pygame, this is the mandatory function, and it should run at very first
screen = pygame.display.set_mode((800,400))  #game window
pygame.display.set_caption('Pygame Tutorial')  #game window title
clock = pygame.time.Clock()

text_font = pygame.font.Font('font/Pixeltype.ttf', 50)  #load text font
game_active = False  #initial game running state as False
start_time = 0  #initial statrting time as zero
score = 0  #initial game score as 0
bg_music = pygame.mixer.Sound('audio/music.wav')  #load game bgm
bg_music.play(loops=-1)  #play the bgm, and loop it forever
bg_music.set_volume(0.3)

#since we need only one player, the player is a single-group
player = pygame.sprite.GroupSingle()
player.add(Player())
#since we need multiple obstacles, the obstacle is a group
obstacle_group = pygame.sprite.Group()

#ingame background
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

#intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand= pygame.transform.rotozoom(player_stand,0,2)  #rescaled the image
player_stand_rect = player_stand.get_rect(center=(400,200))

game_name = text_font.render('Pixel Runner',False,(111,196,169))
game_name_rect = game_name.get_rect(center=(400,80))
game_message = text_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center=(400,330))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:  #let the game running indefinitely unless quit
    for event in pygame.event.get():  #get user actions
        if event.type == pygame.QUIT:  
            pygame.quit()
            sys.exit()  #exit the program completely
        
        if game_active:
            if event.type == obstacle_timer:
                #choice() is to choose a member in the sequence randomly
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
        else:  #if game is not start
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  #check if the user press the space key
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)  #to make current_time=0 (check the function display_score)
        
    if game_active:
        #image are displayed by blit() in order
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()

        player.draw(screen)  #display the player on the screen
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:  #if game over
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        score_message = text_font.render(f'Your score: {score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center=(400,330))
        screen.blit(game_name,game_name_rect)
        if score == 0:  #which means the game never start yet, show the welcome message
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit (score_message,score_message_rect)

    pygame.display.update()  #for each frame, update the screen
    clock.tick(60)  #limit the fps (or the while loop) to 60 frame (times) per second