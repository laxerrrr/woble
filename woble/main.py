import os
import sys
contents = (os.listdir(os.getcwd()))
SDL2PATH = (os.getcwd() + "\\SDL2-2.0.10-win32-x64")
if "main.py" and "SDL2-2.0.10-win32-x64" in contents :
    os.environ["PYSDL2_DLL_PATH"] = SDL2PATH
    #Importing SDL2
    import sdl2
    import sdl2.ext
    #Main process for SDL2
    def run():
        sdl2.ext.init() #Start SDL2
        window = sdl2.ext.Window("Woble [Alpha]", size=(800, 600))
        window.show() #Show window
        running = True
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
else :
    print("Use 'cd woble' in terminal to switch to the correct folder. (For VS Code)")