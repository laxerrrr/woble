import os
import sys
import struct
import time
import ctypes



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
            
    class GluedObject (sdl2.ext.Entity) : #GluedObject class
        def __init__(self, world, sprite, posx = 0, posy = 0):
            self.sprite = sprite 
            self.sprite.position = posx, posy
            self.velocity = Velocity()

    class FloorSystem(sdl2.ext.Applicator):
        def __init__(self, minx, miny, maxx, maxy, isonfloor = False):
            super(FloorSystem, self).__init__()
            self.componenttypes = Velocity, sdl2.ext.Sprite
            self.player = None
            self.minx = minx
            self.miny = miny
            self.maxx = maxx
            self.maxy = maxy
            self.isonfloor = isonfloor

        def _overlap(self, item):
            pos, sprite = item
            
            if sprite == self.player.sprite:
                return False

            left, top, right, bottom = sprite.area
            gleft, gtop, gright, gbottom = self.player.sprite.area
            #print (str(gright))

            return (gbottom >= top and gright > left and gleft < right and gtop < bottom)

        def process(self, world, componentsets):
            collitems = [comp for comp in componentsets if self._overlap(comp)]
            if collitems:
                self.isonfloor = True
            elif collitems == [] :
                self.isonfloor = False
            
                


#Main process for SDL2
    def run():
        print ("WOBLE LOG")


        #Constants
        FPS = 8
        framecount = 0

        fallingspeed = 2

        lr = None

        jumpframe = 0
        jumping = False

        walkframe = 0
        walking = False

        landed = False

        sdl2.ext.init() #Start SDL2
        window = sdl2.ext.Window("Woble [Alpha]", size=(800, 600))
        #window.maximize() #Remove first hashtag when ready for game development
        window.show() #Show window
        running = True

            #Add anything here
        movement = MovementSystem(0, 0, 800, 600)
        floorsystem = FloorSystem(0, 0, 800, 600)
        renderer = Renderer(window)

        world = sdl2.ext.World()
        world.add_system(movement)
        world.add_system(floorsystem)
        world.add_system(renderer)

        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE) #Sprite maker

        playersprite = factory.from_color(sdl2.ext.Color(0, 0, 255), size=(20, 20))
        floorsprite = factory.from_color(sdl2.ext.Color(0, 0, 255), size=(500, 10))
        floor2sprite = factory.from_color(sdl2.ext.Color(0, 100, 255), size=(400, 10))

        floor = GluedObject(world, floorsprite, 5, 400)
        floor2 = GluedObject(world, floor2sprite, 200, 380)
        player = Player(world, playersprite, 20, 100)

        floorsystem.player = player
        

        while running:
            print("+++++ START of game loop +++++")
            if (floorsystem.isonfloor and landed == False) :
                player.velocity.vy = 0
                print("it beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                jumpframe = 0
                jumping = False
                landed = True

            elif (floorsystem.isonfloor == False) :
                print ("IT IS NOT")
                player.velocity.vy = fallingspeed
                landed = False
            
            events = sdl2.ext.get_events()

            keystatus = sdl2.SDL_GetKeyboardState(None) #Key holds
            if keystatus[sdl2.SDL_SCANCODE_LEFT]: #Left or right pressed
                walking = True
                lr = "left"
            elif keystatus[sdl2.SDL_SCANCODE_RIGHT] :
                walking = True
                lr = "right"
            elif keystatus[sdl2.SDL_SCANCODE_LEFT] == False and keystatus[sdl2.SDL_SCANCODE_RIGHT] == False :
                walking = False


            #Jumping logic
            if (jumping) :
                print ("Frame of jump is: " + str(jumpframe))
                player.velocity.vy = -2* (((-1 * jumpframe) *jumpframe) + jumpframe + 10)
                """print (player.velocity.vy)"""
                jumpframe += 1

            elif (jumping and walking): #Jumping with walking speed
                print ("Frame of jump is: " + str(jumpframe))
                player.velocity.vy = -2* (((-1 * jumpframe) *jumpframe) + jumpframe + 10)
                #print (player.velocity.vy)
                jumpframe += 1

                if lr == "left":
                    player.velocity.vx = -10
                if lr == "right":
                    player.velocity.vx = 10

            if (jumpframe == 9):

                print("JUMP's done (" + str(jumpframe) + ")")

                if floorsystem.isonfloor == False :
                    player.velocity.vy = fallingspeed
                jumpframe = 0
                jumping = False
            
            #Walking logic
            if (jumping == False and walking == True):
                if lr == "left":
                    player.velocity.vx = -10
                if lr == "right":
                    player.velocity.vx = 10

                print ("VX = " + str(player.velocity.vx))

            if walking == False and jumping == False:
                player.velocity.vx = 0


            for event in events : #Key press
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    break

                if event.type == sdl2.SDL_KEYDOWN: #On any key press

                    if event.key.keysym.sym == sdl2.SDLK_UP: #Up (jumping)    
                        jumping = True
                    
                    elif event.key.keysym.sym == sdl2.SDLK_DOWN: #Down
                        print ("down")
                    

            world.process()
            framecount += 1
            #print (framecount)
            time.sleep(1/FPS)
            #events = sdl2.ext.get_events()
            print ("----- END of game loop -----")
            print (" ") #dont put anything after this

        return 0

    if __name__ == "__main__":
        sys.exit(run())
else : #Solely for development
    print("Use 'cd woble' in terminal to switch to the correct folder. (For VS Code)")