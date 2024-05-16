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

ENEMIES = []
ENEMIES_COUNT = 0

# A function to quickly get a file:
def getFile(fileName):
    return pg.image.load(os.path.join('Assets',fileName))

#Image variables:
BACKGROUND = getFile('BG-1600.png')
SCREEN_ON, SCREEN_OFF = getFile('ScreenOn.png'), getFile('ScreenOff.png')
INF1 = pg.transform.scale(getFile('Inf1.png'), (40, 40))


# def Get_Screen_Grid(loc_x, loc_y, asset):
#     return ( WIN_WIDTH - SCREEN_OFF.get_width() - WIDTH_FROM_BORDER - asset.get_width()/2 + COORDS_X[loc_x] , 
#                 WIN_HEIGHT - SCREEN_OFF.get_height() - HEIGHT_FROM_BORDER - asset.get_height()/2 + COORDS_Y[loc_y] )
def Get_Screen_Grid(loc_x, loc_y, obj):
    return ( WIN_WIDTH - SCREEN_OFF.get_width() - WIDTH_FROM_BORDER - obj.rect.width/2 + COORDS_X[loc_x] , 
                WIN_HEIGHT - SCREEN_OFF.get_height() - HEIGHT_FROM_BORDER - obj.rect.height/2 + COORDS_Y[loc_y] )

class Infantry(pg.sprite.Sprite):
    def __init__(self, image, position = (0, 0) ):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        x, y = position
        
        self.grid_x = x
        self.grid_y = y

        self.grid_positions = Get_Screen_Grid(x, y, self )
        self.rect.x = self.grid_positions[0]
        self.rect.y = self.grid_positions[1]


    def set_pos(self, new_grid_position): # Input will be (grid_x, grid_y) (FE: 9,1)
        x, y = new_grid_position

        self.grid_x, self.grid_y = x, y

        # print('START OF SET_POS DEBUG:')
        # print(f'New Grid Coods: x: {x}, y: {y}')
        self.grid_positions = Get_Screen_Grid(x, y, self )
        
        self.rect_x = int(self.grid_positions[0])
        self.rect_y = int(self.grid_positions[1])


# def Check_Screen_Grid_Loc_X(asset):
#     for loc_x in range(1, len(COORDS_X)):
        
#         grid_coords = []
#         get_touple = Get_Screen_Grid(loc_x, 0, asset)
#         grid_coords += get_touple 
        
#         #print(f'Asset: {asset.rect.x}, grid_coords {grid_coords[0]}')
        
#         if(asset.rect.x == grid_coords[0]):
#             print(f'Location found: {loc_x}')
#             return loc_x
    
    print('No location found!')
    return False

def handle_enemy_movement(enemies_list):
    for obj in enemies_list:
        global ENEMIES_COUNT
        #obj_grid_x = Check_Screen_Grid_Loc_X(obj)

        #Future Proof: Exeption Handle for 'Check_Screen_Grid_Loc_X' == 0 

        # Exeption handle: Enemy going out of bounds
        if(obj.grid_x <= 1):
            #Temporary Solution which will be migrated to Event
            print('-1 Health')
            enemies_list.remove(obj)
            ENEMIES_COUNT -= 1
            return
        
        # print('START OF HANDLE ENEMY MOVEMENT DEBUG:')
        # print(f'Obj Grid X: {obj.grid_x}, will be: {obj.grid_x - 1}')    
        # print(f'Obj Grid Y:{obj.grid_y}')
        obj.set_pos((obj.grid_x - 1,obj.grid_y))


def Enemy_Controller():
    global ENEMIES_COUNT
    if(ENEMIES_COUNT < 5):
        enemy = Infantry(INF1, (10 ,random.randrange(1, 9)))
        ENEMIES.append(enemy)
        ENEMIES_COUNT += 1
        
    

def Render_Window(Screen_State):
    WIN.blit(BACKGROUND, (0, 0)) # Renders the background
    
    #Handles the render between Truned ON and OFF screen
    if Screen_State is False :
        WIN.blit(SCREEN_OFF, (WIN_WIDTH - SCREEN_OFF.get_width() - WIDTH_FROM_BORDER, WIN_HEIGHT - SCREEN_OFF.get_height() - HEIGHT_FROM_BORDER))
    else:
        WIN.blit(SCREEN_ON, (WIN_WIDTH - SCREEN_ON.get_width() - WIDTH_FROM_BORDER, WIN_HEIGHT - SCREEN_ON.get_height() - HEIGHT_FROM_BORDER))
        handle_enemy_movement(ENEMIES)
        Enemy_Controller()
        
        for enemy in ENEMIES:
            WIN.blit(enemy.image, enemy.grid_positions)

    

def Main():
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
            

        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_a]:
            print('K')

        Render_Window(IS_SCREEN_ON)
        
        pg.display.update()
        pg.time.delay(3000)
        

    pg.quit()



if __name__ == "__main__":
    Main()

# Atribute Image by <a href="https://www.freepik.com/free-photo/vintage-rusty-scratched-wall_10746799.htm#query=rust%20overlay&position=0&from_view=keyword&track=ais_user&uuid=01c0e15f-befa-45c9-bc30-1485cd5ec620">Freepik</a>
# <a href="https://www.freepik.com/free-photo/rusty-metallic-textured-background_12335614.htm#query=rusty%20metal&position=5&from_view=keyword&track=ais_user&uuid=1ead46d0-fb9b-4c46-8437-c55b5023bf0b">Image by freepik</a>
#    <a href="https://www.freepik.com/free-photo/abstract-close-up-rusty-metallic-wallpaper_12558744.htm#query=rusty%20metal&position=11&from_view=keyword&track=ais_user&uuid=1ead46d0-fb9b-4c46-8437-c55b5023bf0b">Image by freepik</a>