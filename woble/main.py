import os
import sys

contents = (os.listdir(os.getcwd()))
SDL2PATH = (os.getcwd() + "\\SDL2-2.0.10-win32-x64")
if "main.py" and "SDL2-2.0.10-win32-x64" in contents : #Solely for development
    os.environ["PYSDL2_DLL_PATH"] = SDL2PATH



    #Importing SDL2
    import sdl2
    import sdl2.ext
    #Custom classes for game
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


    #Main process for SDL2
    def run():
        sdl2.ext.init() #Start SDL2
        window = sdl2.ext.Window("Woble [Alpha]", size=(800, 600))
        #window.maximize() #Remove first hashtag when ready for game development
        window.show() #Show window
        running = True

        #Add anything here
        renderer = Renderer(window)
        world = sdl2.ext.World()
        world.add_system(renderer)
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE) #Sprite maker
        first = factory.from_color(sdl2.ext.Color(0, 0, 255), size=(20, 20))
        player = Player(world, first)

        renderer.render(first)




        while running:
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    break
                window.refresh()
        return 0

    if __name__ == "__main__":
        sys.exit(run())
else : #Solely for development
    print("Use 'cd woble' in terminal to switch to the correct folder. (For VS Code)")