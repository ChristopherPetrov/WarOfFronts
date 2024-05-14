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

def Get_Screen_Grid(loc_x, loc_y, rect):
    return ( WIN_WIDTH - SCREEN_OFF.get_width() - WIDTH_FROM_BORDER - rect.width/2 + COORDS_X[loc_x] , 
                WIN_HEIGHT - SCREEN_OFF.get_height() - HEIGHT_FROM_BORDER - rect.height/2 + COORDS_Y[loc_y] )

def Check_Screen_Grid_Loc_X(asset):
    for loc_x in range(1, len(COORDS_X)):
        grid_coords = []
        get_touple = Get_Screen_Grid(loc_x, 0, asset)
        grid_coords += get_touple 
        print('checking and :' + str(loc_x))
        if(asset.x == grid_coords[0]):
            print("shit works" + str(loc_x))

def Enemy_Controller(enemy_count):
    if(enemy_count < 5):
        enemy = INF1.get_rect()
        # WIN.blit(INF1, Get_Screen_Grid(10, random.randrange(1,9), INF1) )
        enemy_count += 1
        Check_Screen_Grid_Loc_X(enemy)
    

def Render_Window(screen_State, number_of_enemies):
    WIN.blit(BACKGROUND, (0, 0)) # Renders the background
    
    #Handles the render between Truned ON and OFF screen
    if screen_State is False :
        WIN.blit(SCREEN_OFF, (WIN_WIDTH - SCREEN_OFF.get_width() - WIDTH_FROM_BORDER, WIN_HEIGHT - SCREEN_OFF.get_height() - HEIGHT_FROM_BORDER))
    else:
        WIN.blit(SCREEN_ON, (WIN_WIDTH - SCREEN_ON.get_width() - WIDTH_FROM_BORDER, WIN_HEIGHT - SCREEN_ON.get_height() - HEIGHT_FROM_BORDER))
        # WIN.blit(INF1, Get_Screen_Grid(1, 4, INF1))
        # WIN.blit(INF1, Get_Screen_Grid(3, 4, INF1))
        # WIN.blit(INF1, Get_Screen_Grid(3, 6, INF1))
        # WIN.blit(INF1, Get_Screen_Grid(5, 4, INF1))

        Enemy_Controller(number_of_enemies)
    

def Main():
    IS_SCREEN_ON = False
    number_of_enemies = 0

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

        Render_Window(IS_SCREEN_ON, number_of_enemies)
        
        pg.display.update()
        

    pg.quit()



if __name__ == "__main__":
    Main()

# Atribute Image by <a href="https://www.freepik.com/free-photo/vintage-rusty-scratched-wall_10746799.htm#query=rust%20overlay&position=0&from_view=keyword&track=ais_user&uuid=01c0e15f-befa-45c9-bc30-1485cd5ec620">Freepik</a>
# <a href="https://www.freepik.com/free-photo/rusty-metallic-textured-background_12335614.htm#query=rusty%20metal&position=5&from_view=keyword&track=ais_user&uuid=1ead46d0-fb9b-4c46-8437-c55b5023bf0b">Image by freepik</a>
#    <a href="https://www.freepik.com/free-photo/abstract-close-up-rusty-metallic-wallpaper_12558744.htm#query=rusty%20metal&position=11&from_view=keyword&track=ais_user&uuid=1ead46d0-fb9b-4c46-8437-c55b5023bf0b">Image by freepik</a>