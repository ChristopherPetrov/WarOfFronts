from typing import Self
import pygame as pg
import os
import random

pg.init()

# Creates and sets the display to 1600x900 with diplay.set_mode
WIN_WIDTH, WIN_HEIGHT = 1600, 900
WIN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

#Variables:
FPS = 60 # Uses time.Clock to lock Main() refreshes per second
COORDS_X = [0, 129, 198, 267, 336, 405, 474, 543, 612, 681, 750]
COORDS_Y = [0, 139, 186, 233, 280, 327, 374, 421, 468]

HEIGHT_FROM_BORDER, WIDTH_FROM_BORDER = 25, 15

has_move_started = False
move_enemy_event = pg.USEREVENT + 3
add_enemy_event = pg.USEREVENT + 2
ENEMIES = []
ENEMIES_COUNT = 0

DROP_BOMB = False
bomb_drop_event = pg.USEREVENT + 1
bomb_exploding_event = pg.USEREVENT + 4
IS_BOMB_DROPPED = False
IS_BOMB_EXPLODING = False
BOMB_STATE = 0


# A function to quickly get a file:
def getFile(fileName):
    return pg.image.load(os.path.join('Assets',fileName))

#Image variables:
BACKGROUND = getFile('BG-1600.png')
SCREEN_ON, SCREEN_OFF = getFile('ScreenOn.png'), getFile('ScreenOff.png')
INF1 = pg.transform.scale(getFile('Inf1.png'), (40, 40))
EXPLO = pg.transform.scale(getFile('Explosion.png'), (40, 40))
BOMB = [pg.transform.scale(getFile('Bomb1.png'), (40, 40)), pg.transform.scale(getFile('Bomb1.png'), (30, 30)), pg.transform.scale(getFile('Bomb1.png'), (20, 20))]

def Get_Screen_Grid(loc_x, loc_y, obj):
    return ( WIN_WIDTH - SCREEN_OFF.get_width() - WIDTH_FROM_BORDER - obj.rect.width/2 + COORDS_X[loc_x] , 
                WIN_HEIGHT - SCREEN_OFF.get_height() - HEIGHT_FROM_BORDER - obj.rect.height/2 + COORDS_Y[loc_y] )

class Infantry(pg.sprite.Sprite):
    def __init__(self, image, position = (0, 0) ):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()

        x, y = position
        self.grid_x = x
        self.grid_y = y

        self.grid_positions = Get_Screen_Grid(x, y, self )
        self.rect.x = self.grid_positions[0]
        self.rect.y = self.grid_positions[1]


    def set_pos(self, new_grid_position): # Input will be (grid_x, grid_y) (FE: 9,1)
        x, y = new_grid_position
        self.grid_x, self.grid_y = x, y
        
        self.grid_positions = Get_Screen_Grid(x, y, self )
        self.rect_x = int(self.grid_positions[0])
        self.rect_y = int(self.grid_positions[1])

class Bomb(pg.sprite.Sprite):
    def __init__(self, bomb_images, explosion_image, impact_locations):
        super().__init__()
        self.bomb_images = bomb_images
        self.explosion_image = explosion_image
        self.rect = explosion_image.get_rect()

        x, y = impact_locations
        self.impact_grid = (x, y)
        self.impact_coords = Get_Screen_Grid(x, y, self)
        self.impact_splash_grid = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        self.impact_splash_coords = [self.impact_coords ,Get_Screen_Grid(x + 1, y, self), Get_Screen_Grid(x - 1, y, self), Get_Screen_Grid(x, y + 1, self), Get_Screen_Grid(x, y - 1, self)]
        
def drop_bomb(location, enemies_list):
    global ENEMIES_COUNT
    global IS_BOMB_DROPPED
    global IS_BOMB_EXPLODING

    bomb = Bomb(BOMB, EXPLO, location)
    
    if BOMB_STATE <= len(BOMB) and BOMB_STATE is not 0:
        print(f'Printing Bomb: {BOMB_STATE}')
        WIN.blit(BOMB[BOMB_STATE-1], bomb.impact_coords)

    if IS_BOMB_DROPPED is False:
        IS_BOMB_DROPPED = not IS_BOMB_DROPPED
        pg.time.set_timer(bomb_drop_event, 50)


    if IS_BOMB_EXPLODING is True:
        for splash_loc in bomb.impact_splash_coords:
            WIN.blit(bomb.explosion_image,splash_loc)
        for splash_loc in bomb.impact_splash_coords:
            for enemy in enemies_list:
                if(enemy.grid_positions == splash_loc):
                    print('Enemy Bombarded')
                    enemies_list.remove(enemy)
                    ENEMIES_COUNT -= 1
    

def handle_enemy_movement(enemies_list):
    global has_move_started
    for enemy in enemies_list:
        global ENEMIES_COUNT

        # Exeption handle: Enemy going out of bounds
        if(enemy.grid_x <= 1):
            #Temporary Solution which will be migrated to Event
            print('-1 Health')
            enemies_list.remove(enemy)
            ENEMIES_COUNT -= 1
            return
        
        enemy.set_pos((enemy.grid_x - 1,enemy.grid_y))
    has_move_started = False


def Enemy_Controller():
    global ENEMIES_COUNT
    if(ENEMIES_COUNT < 5):
        ENEMIES_COUNT += 1
        pg.time.set_timer(add_enemy_event, 3000)
        
    

def Render_Window(Screen_State):
    global ENEMIES
    global BOMB_STATE
    global BOMB
    global DROP_BOMB
    global has_move_started
    
    WIN.blit(BACKGROUND, (0, 0)) # Renders the background
    
    #Handles the render between Truned ON and OFF screen
    if Screen_State is False :
        WIN.blit(SCREEN_OFF, (WIN_WIDTH - SCREEN_OFF.get_width() - WIDTH_FROM_BORDER, WIN_HEIGHT - SCREEN_OFF.get_height() - HEIGHT_FROM_BORDER))
    else:
        WIN.blit(SCREEN_ON, (WIN_WIDTH - SCREEN_ON.get_width() - WIDTH_FROM_BORDER, WIN_HEIGHT - SCREEN_ON.get_height() - HEIGHT_FROM_BORDER))
        
        if has_move_started is False:
            has_move_started = not has_move_started
            pg.time.set_timer(move_enemy_event, 3000)
        Enemy_Controller()
        for enemy in ENEMIES:
            WIN.blit(enemy.image, enemy.grid_positions)
        
        
        if DROP_BOMB is True:
            drop_bomb((7, 5), ENEMIES) 
    

def Main():
    global BOMB_STATE
    global IS_BOMB_DROPPED
    global IS_BOMB_EXPLODING
    global DROP_BOMB
    global ENEMIES
    IS_SCREEN_ON = False
    clock = pg.time.Clock()
    
    run = True
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            #If user clicks the X (pg.QUIT event.type) the loop stops
            if event.type == pg.QUIT:
                run = False
                

            #Changes the state of IS_SCREEN_DOWN to the opposite on clicking 'F'
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    IS_SCREEN_ON = not IS_SCREEN_ON
                if event.key == pg.K_COMMA: # easy to use debug function
                    print('This is debug:')
                    print(WIN_WIDTH)
                    print(SCREEN_ON.get_width())
                    print('Debug End')
                if event.key == pg.K_SPACE and IS_BOMB_DROPPED is False and IS_BOMB_EXPLODING is False:
                    DROP_BOMB = True
                    
            
            if event.type == add_enemy_event:
                enemy = Infantry(INF1, (10 ,random.randrange(1, 9)))
                ENEMIES.append(enemy)
                
            if event.type == move_enemy_event:
                handle_enemy_movement(ENEMIES)

            if event.type == bomb_drop_event:
                BOMB_STATE += 1
                if BOMB_STATE <= len(BOMB) + 1:
                    pg.time.set_timer(bomb_drop_event, 1000)
                    if BOMB_STATE + 1 > len(BOMB) + 1:
                        BOMB_STATE = 0
                        IS_BOMB_DROPPED = False
                        IS_BOMB_EXPLODING = True  
                        pg.time.set_timer(bomb_exploding_event, 3000)
            
            if event.type == bomb_exploding_event:
                
                IS_BOMB_EXPLODING = False
                DROP_BOMB = False
                    


        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_a]:
            print('K')

        Render_Window(IS_SCREEN_ON)
        
        pg.display.update()
        

    pg.quit()



if __name__ == "__main__":
    Main()

# Atribute Image by <a href="https://www.freepik.com/free-photo/vintage-rusty-scratched-wall_10746799.htm#query=rust%20overlay&position=0&from_view=keyword&track=ais_user&uuid=01c0e15f-befa-45c9-bc30-1485cd5ec620">Freepik</a>
# <a href="https://www.freepik.com/free-photo/rusty-metallic-textured-background_12335614.htm#query=rusty%20metal&position=5&from_view=keyword&track=ais_user&uuid=1ead46d0-fb9b-4c46-8437-c55b5023bf0b">Image by freepik</a>
#    <a href="https://www.freepik.com/free-photo/abstract-close-up-rusty-metallic-wallpaper_12558744.htm#query=rusty%20metal&position=11&from_view=keyword&track=ais_user&uuid=1ead46d0-fb9b-4c46-8437-c55b5023bf0b">Image by freepik</a>