import os
import sys
import struct
import time
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
    

    class Player (sdl2.ext.Entity) : #Player class
        def __init__(self, world, sprite, posx = 0, posy = 0):
            self.sprite = sprite #Given variable when making Player attribute to be associated with Player.sprite
            self.sprite.position = posx, posy #Set posx posy to player sprite position
            self.velocity = Velocity()

#Main process for SDL2
    def run():
        
        #Constants
        FPS = 30
        framecount = 0
        jumpending = 0
        jumping = False
        jumpframe = 0

        sdl2.ext.init() #Start SDL2
        window = sdl2.ext.Window("Woble [Alpha]", size=(800, 600))
        #window.maximize() #Remove first hashtag when ready for game development
        window.show() #Show window
        running = True

            #Add anything here
        movement = MovementSystem(0, 0, 800, 600)
        renderer = Renderer(window)

        world = sdl2.ext.World()
        world.add_system(movement)
        world.add_system(renderer)

        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE) #Sprite maker
        first = factory.from_color(sdl2.ext.Color(0, 0, 255), size=(20, 20))
        player = Player(world, first, 20, 460)

        while running:
            #print (framecount)
            time.sleep(1/30)
            events = sdl2.ext.get_events()

            #Events 
            for event in events :
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    break

                if event.type == sdl2.SDL_KEYDOWN: #On any key press

                    if event.key.keysym.sym == sdl2.SDLK_UP: #Up (jumping)    
                        jumping = True
                        jumpending = framecount + 20
                    elif event.key.keysym.sym == sdl2.SDLK_DOWN: #Down
                        player.velocity.vy = 0
                    
                    elif event.type == sdl2.SDL_KEYUP: #On any key release
                        if event.key.keysym.sym in (sdl2.SDLK_UP, sdl2.SDLK_DOWN):
                            player.velocity.vy = 0
           
            #Jumping logic
            if (jumping == True):
                print ("Frame of jump is: " + str(jumpframe))
                player.velocity.vy = jumpframe * -jumpframe + (10*jumpframe)
                player.velocity.vx = jumpframe
                jumpframe += 1

            if (jumpframe == 22):
                print("WERE IN CAPTAIN")
                jumpframe =- 1
                player.velocity.vx = 0
                player.velocity.vy = 0
                jumping = False

            world.process()
            framecount = framecount + 1
            print (framecount)
        return 0

    if __name__ == "__main__":
        sys.exit(run())
else : #Solely for development
    print("Use 'cd woble' in terminal to switch to the correct folder. (For VS Code)")