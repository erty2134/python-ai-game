import sys
import pygame
import math

pygame.init()
pygame.font.init()

def main(argc:"int", argv:list[str]) -> None:
    FPS = 60
    frame = 0

    SCREEN_COLUR = "#CCCCCC"
    SCREEN_W, SCREEN_H = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
    screen.fill(SCREEN_COLUR)
    pygame.display.set_caption("AI, Game")
    ICON: pygame.surface = pygame.image.load("car.png")
    pygame.display.set_icon(ICON)

    clock = pygame.time.Clock()
    
    mouse: bool = False
    arrowKeys: dict = {
        "up": False,
        "down": False,
        "left": False,
        "right": False
    }
    
    class car:
        def __init__(self, frame="car.png", terminal_velocity:"int"=10, control:"str"="arrow") -> None:
            """
            control, arrowkeys or WASD (for movement CONST)
            terminal_velocity, max speed (half of it is max speed backwards)
            frame, the image being rendered
            """
            self.acceleration: float = 0.0
            self.velocity: float = 0.0
            self.x: int = SCREEN_W / 2
            self.y: int = SCREEN_H / 2
            self.angle: float = 0
            self.CONTROL = control
            self.TERMINAL_VELOCITY: "float" = terminal_velocity

            self.frame: pygame.Surface = pygame.image.load(frame)
            self.frame = pygame.transform.scale(self.frame, (SCREEN_W/16, SCREEN_H/16))
            self.frame = pygame.transform.rotate(self.frame, self.angle)
            self.frame.set_colorkey(SCREEN_COLUR)
            self.frame_copy = None
        def update(self) -> None:   
            pressed = pygame.key.get_pressed()

            radians = math.radians(self.angle)
            vertical = math.cos(radians) * self.velocity
            horizontal = math.sin(radians) * self.velocity

            self.x += horizontal
            self.y += vertical

            controlKeys: dict = {"forward":pygame.K_UP, "rotate-":pygame.K_LEFT, "reverse":pygame.K_DOWN, "rotate+":pygame.K_RIGHT}
            if self.CONTROL.lower() == "arrow":
                controlKeys = {
                    "forward":pygame.K_UP,
                    "rotate-":pygame.K_LEFT,
                    "reverse":pygame.K_DOWN,
                    "rotate+":pygame.K_RIGHT
                    
                }
            elif self.CONTROL.upper() == "WASD":
                controlKeys = {
                    "forward":pygame.K_w,
                    "rotate+":pygame.K_a,
                    "reverse":pygame.K_s,
                    "rotate-":pygame.K_d
                    
                }
            else: controlKeys = {"forward":pygame.K_UP, "rotate-":pygame.K_LEFT, "reverse":pygame.K_DOWN, "rotate+":pygame.K_RIGHT}

            if pressed[controlKeys["forward"]]:
                self.velocity += SCREEN_W/2000
            elif pressed[controlKeys["reverse"]]:
                self.velocity -= SCREEN_W/2000
            else: 
                if self.velocity > 0: self.velocity -= SCREEN_W/20000
                elif self.velocity < 0: self.velocity += SCREEN_W/20000

            #if self.velocity < 0 : self.velocity = 0

            if pressed[controlKeys["rotate+"]]:
                self.angle += self.velocity/2         

            if pressed[controlKeys["rotate-"]]:
                self.angle -= self.velocity/2

            self.frame_copy = pygame.transform.rotate(self.frame, self.angle-90)
            screen.blit(self.frame_copy, (self.x - int(self.frame_copy.get_width()/2), self.y - int(self.frame_copy.get_height()/2)))
            if self.velocity > self.TERMINAL_VELOCITY:
                self.velocity = self.TERMINAL_VELOCITY
            elif self.velocity < -(self.TERMINAL_VELOCITY/2):
                self.velocity = -(self.TERMINAL_VELOCITY/2)

    greencar = car()
    redCar = car(frame="car red.png", control="wasd")
    running = True
    while running:
        frame+=1
        screen.fill("#CCCCCC")
        text = pygame.font.SysFont('Arial', 30).render(f"angle: {greencar.angle}", False, (0,0,0))
        pressed = pygame.key.get_pressed()
        
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = False

            if event.type == pygame.KEYDOWN: pass                

            if event.type == pygame.QUIT:
                running = False
            

        redCar.update()        
        greencar.update()
        screen.blit(text, (SCREEN_W+(SCREEN_W/16), SCREEN_H+(SCREEN_H/16)))
        
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__" : main(len(sys.argv[0:]), sys.argv[0:])