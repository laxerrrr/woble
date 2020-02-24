"""
 __      __         _       _        
 \ \    / /  ___   | |__   | |   ___ 
  \ \/\/ /  / _ \  | '_ \  | |  / -_)
   \_/\_/   \___/  |_.__/  |_|  \___|

    Made with PySDL2
    
    by Xavier Savoie and Ian Dauphinée

"""
import os #Used to get current directory
import sys #Used to exit
import struct #Used to check if system is 32 bit or 64 bit
import time #Used for time.sleep to regulate FPS
import gc #Used to fetch all objects in program


pythonversion = (struct.calcsize("P") * 8)
contents = (os.listdir(os.getcwd()))
if (pythonversion == 32) :
    sdlname = "SDL2-2.0.10-win32-x86"
elif (pythonversion == 64) :
    sdlname = "SDL2-2.0.10-win32-x64"

SDL2PATH = (os.getcwd() + "\\" + sdlname)

if "main.py" and sdlname in contents : #Solely for development
    os.environ["PYSDL2_DLL_PATH"] = SDL2PATH

    #Importing SDL2

    import sdl2
    import sdl2.ext

    #Custom classes for game

    class Velocity(object):
        def __init__(self):
            super(Velocity, self).__init__()
            self.vx = 0
            self.vy = 0
    
    class MovementSystem(sdl2.ext.Applicator):
        def __init__(self, minx, miny, maxx, maxy):
            super(MovementSystem, self).__init__()
            self.componenttypes = Velocity, sdl2.ext.Sprite
            self.minx = minx
            self.miny = miny
            self.maxx = maxx
            self.maxy = maxy

        def process(self, world, componentsets):
            for velocity, sprite in componentsets:
                swidth, sheight = sprite.size
                sprite.x += velocity.vx
                sprite.y += velocity.vy

                sprite.x = max(self.minx, sprite.x)
                sprite.y = max(self.miny, sprite.y)

                pmaxx = sprite.x + swidth
                pmaxy = sprite.y + sheight

                if pmaxx > self.maxx:
                    sprite.x = self.maxx - swidth
                if pmaxy > self.maxy:
                    sprite.y = self.maxy - sheight

    class Renderer (sdl2.ext.SoftwareSpriteRenderSystem) : #Renderer class for sprites
        def __init__(self, window):
            super(Renderer, self).__init__(window)
    
        def render(self, components):
            sdl2.ext.fill(self.surface, sdl2.ext.Color(200, 200, 123)) #Background of renderer
            super(Renderer, self).render(components) #Call SoftwareSpriteRenderSystem.render() when using Render.render()
    

    class Player (sdl2.ext.Entity): #Player class
        def __init__(self, world, sprite, posx = 0, posy = 0):
            self.sprite = sprite #Given variable when making Player attribute to be associated with Player.sprite
            self.sprite.position = posx, posy
            self.velocity = Velocity()
            
    class Floor (sdl2.ext.Entity) : #Floor class
        def __init__(self, world, sprite, posx = 0, posy = 0):
            self.sprite = sprite 
            self.sprite.position = posx, posy
            self.velocity = Velocity()

    class Wall (sdl2.ext.Entity) : #Wall class
        def __init__(self, world, sprite, posx = 0, posy = 0):
            self.sprite = sprite 
            self.sprite.position = posx, posy
            self.velocity = Velocity()

    class WallSystem(sdl2.ext.Applicator):
        def __init__(self, minx, miny, maxx, maxy, touchedwall = False):
            super(WallSystem, self).__init__()
            self.componenttypes = Velocity, sdl2.ext.Sprite
            self.player = None
            self.itemhit = None
            self.wall = None
            self.side = None
            self.minx = minx
            self.miny = miny
            self.maxx = maxx
            self.maxy = maxy
            self.leftwall = False
            self.rightwall = False
            self.touchedwall = touchedwall
            self.floorsarray = None
            self.middle = None

        def _overlap(self, item):
            pos, sprite = item
            x = 0
            while x < len(self.floorsarray) :
                if self.floorsarray[x].velocity == item[0] :
                    return False
                x += 1

            if sprite == self.player.sprite:
                return False

            left, top, right, bottom = sprite.area
            pleft, ptop, pright, pbottom = self.player.sprite.area
            self.middle = (left + right) / 2

            if pleft > self.middle :
                self.leftwall = True
                self.rightwall = False

            if pright < self.middle :
                self.leftwall = False
                self.rightwall = True

            self.wall = item
            return (pright >= left and pleft <= right and pbottom <= bottom and ptop >= top)

        def process(self, world, componentsets):
            collitems = [comp for comp in componentsets if self._overlap(comp)]
            if collitems:
                self.itemhit = collitems[0]
                self.touchedwall = True
                
            elif collitems == [] :
                self.touchedwall = False
                self.leftwall = False
                self.rightwall = False

    class FloorSystem(sdl2.ext.Applicator):
        def __init__(self, minx, miny, maxx, maxy):
            super(FloorSystem, self).__init__()
            self.componenttypes = Velocity, sdl2.ext.Sprite
            self.player = None
            self.itemhit = None
            self.floor = None
            self.minx = minx
            self.miny = miny
            self.maxx = maxx
            self.maxy = maxy
            self.isonfloor = False
            self.wallsarray = None

        def _overlap(self, item):
            pos, sprite = item
            x = 0

            while x < len(self.wallsarray) :
                if self.wallsarray[x].velocity == item[0] :
                    return False
                x += 1

            if sprite == self.player.sprite :
                return False

            left, top, right, bottom = sprite.area
            pleft, ptop, pright, pbottom = self.player.sprite.area
            self.floor = item
            return (pbottom >= top and pright > left and pleft < right and ptop < bottom)

        def process(self, world, componentsets):
            collitems = [comp for comp in componentsets if self._overlap(comp)]
            if collitems:
                self.itemhit = collitems[0]
                self.isonfloor = True
                
            elif collitems == [] :
                self.isonfloor = False
            
                


#Main process for SDL2
    def run():
        print ("WOBLE LOG")


        #Constants and variables
        FPS = 8
        framecount = 0

        fallingspeed = 10

        lr = None

        jumpframe = 0
        jumping = False

        walkframe = 0
        walking = False

        landed = False
        reset = False

        resetx = False
        immobilized = True

        sdl2.ext.init() #Start SDL2
        window = sdl2.ext.Window("Woble [Alpha]", size=(800, 600))
        #window.maximize() #Remove first hashtag when ready for game development
        window.show() #Show window
        running = True

            #Add anything here
        movement = MovementSystem(0, 0, 800, 600)
        floorsystem = FloorSystem(0, 0, 800, 600)
        wallsystem = WallSystem(0, 0, 800, 600)
        renderer = Renderer(window)

        world = sdl2.ext.World()
        world.add_system(movement)
        world.add_system(floorsystem)
        world.add_system(wallsystem)
        world.add_system(renderer)

        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE) #Sprite maker

        playersprite = factory.from_color(sdl2.ext.Color(0, 0, 255), size=(20, 20))
        floorsprite = factory.from_color(sdl2.ext.Color(0, 0, 255), size=(500, 10))
        floor2sprite = factory.from_color(sdl2.ext.Color(0, 100, 255), size=(400, 10))
        wallsprite = factory.from_color(sdl2.ext.Color(0, 100, 255), size=(25, 400))

        floor = Floor(world, floorsprite, 5, 200)
        floor2 = Floor(world, floor2sprite, 200, 250)

        player = Player(world, playersprite, 20, 100)

        wall = Wall(world, wallsprite, 50, 100)

        floorsystem.player = player
        wallsystem.player = player

        floors = [o for o in gc.get_objects() if type(o).__name__ == "Floor"] #Gets all Floor objects from program and puts them in an array
        walls = [o for o in gc.get_objects() if type(o).__name__ == "Wall"] #Gets all Wall objects from program and puts them in an array
        floorsystem.wallsarray = walls #SDL2 bug fix purposes
        wallsystem.floorsarray = floors #SDL2 bug fix purposes


        while running:
            print("+++++ START of game loop +++++")


            """ *** Events *** """

            events = sdl2.ext.get_events() #Gets all external events
            for event in events : #Key press
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    break

                if event.type == sdl2.SDL_KEYDOWN: #On any key press

                    if event.key.keysym.sym == sdl2.SDLK_UP: #Up (jumping)    
                        jumping = True
                    
                    elif event.key.keysym.sym == sdl2.SDLK_DOWN: #Down
                        print ("down")

            keystatus = sdl2.SDL_GetKeyboardState(None) #Key holds
            if keystatus[sdl2.SDL_SCANCODE_LEFT]: #Left or right pressed
                walking = True
                lr = "left"
            elif keystatus[sdl2.SDL_SCANCODE_RIGHT] :
                walking = True
                lr = "right"
            elif keystatus[sdl2.SDL_SCANCODE_LEFT] == False and keystatus[sdl2.SDL_SCANCODE_RIGHT] == False :
                walking = False

            
            """ *** Walking logic *** """

            if (jumping == False and walking == True):
                if (lr == "left") :
                    player.velocity.vx = -10
                    print ("lllllllll")
                if lr == "right" :
                    player.velocity.vx = 10
                    print ("rrrrrrrrr")
            
            if jumping == False and walking == False :
                player.velocity.vx = 0

            """ *** Jumping logic *** """

            if (jumping) : #Jumping
                print ("Frame of jump is: " + str(jumpframe))
                player.velocity.vy = round((-2/3)* (((-1 * jumpframe) *jumpframe) + 9 * jumpframe))
                print (player.velocity.vy)
                jumpframe += 1

            elif (jumping and walking): #Jumping with walking speed
                print ("Frame of jump is: " + str(jumpframe))
                player.velocity.vy = round(-2/3* (((-1 * jumpframe) *jumpframe) + 9 * jumpframe))
                print (player.velocity.vy)
                jumpframe += 1

                if lr == "left":
                    player.velocity.vx = -10
                if lr == "right":
                    player.velocity.vx = 10

            if (jumpframe == 12):

                print("JUMP's done (" + str(jumpframe) + ")")

                if floorsystem.isonfloor == False :
                    player.velocity.vy = fallingspeed
                jumpframe = 0
                jumping = False
            
            """ *** Resetting and immobilizing logic for landing from fall or jump on floor *** """
            
            if landed and reset == False : #Immobilizing player after position reset
                player.velocity.vy = 0
                landed = False
                reset = True
                print("Immobilized")
            
            elif (floorsystem.isonfloor and landed == False and reset == False) : #Resetting player position to be on top of floor

                floor_ = None
                for x in floors :
                    if (x.velocity == floorsystem.itemhit[0]) : #If the velocity ID from a floor object in the
                        floor_ = x                              #floors array is equal to the velocity ID of the object hit
                                                                #then set floor_ to be that object (for resetting logic)
                left, top, right, bottom = floor_.sprite.area
                pleft, pbottom, pright, pbottom = player.sprite.area

                player.velocity.vy = (top - pbottom)
                print ("Reset frame velocity = " + str(player.velocity.vy))
                print("LANDED")
                jumpframe = 0
                jumping = False
                landed = True
                reset = False
                print("Reset")

            elif (floorsystem.isonfloor == False and jumping == False) : #If falling
                print ("IN THE AIR")
                player.velocity.vy = fallingspeed
                landed = False
                reset = False
            
            elif (floorsystem.isonfloor == False and jumping) : #If player is jumping and not on floor
                print ("IN THE AIR")
                landed = False

            ###############################################################
            if immobilized == False and resetx == True : #Immobilizing player after position reset
                player.velocity.vx = 0
                immobilized = True
                resetx = False
                print("Immobilized")

            if wallsystem.touchedwall :
                wall_ = None
                for x in walls :
                    if (x.velocity == wallsystem.itemhit[0]) : #If the velocity ID from a wall object in the
                        wall_ = x                              #walls array is equal to the velocity ID of the object hit
                                                               #then set wall_ to be that object (for resetting logic)
                wleft, wtop, wright, wbottom = wall_.sprite.area
                pleft, pbottom, pright, pbottom = player.sprite.area

                if wallsystem.leftwall :
                    player.velocity.vx = wright - pleft

                if wallsystem.rightwall :
                    player.velocity.vx = pright - wleft

            world.process() #Process objects in world

            framecount += 1 #Ongoing framecount for movement logic

            time.sleep(1/FPS) #Constant framerate

            print ("----- END of game loop -----")
            print (" ") #dont put anything after this

        return 0

    if __name__ == "__main__":
        sys.exit(run())
else : #Solely for development
    print("Use 'cd woble' in terminal to switch to the correct folder. (For VS Code)")