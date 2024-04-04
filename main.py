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

    clock = pygame.time.Clock()
    
    mouse: bool = False
    arrowKeys: dict = {
        "up": False,
        "down": False,
        "left": False,
        "right": False
    }
    
    class car:
        def __init__(self, frame="car.png") -> None:
            self.acceleration: float = 0.0
            self.velocity: float = 0.0
            self.x: int = SCREEN_W / 2
            self.y: int = SCREEN_H / 2
            self.angle: float = 0
            self.frame: pygame.Surface = pygame.image.load("car.png")
            self.frame = pygame.transform.scale(self.frame, (SCREEN_W/16, SCREEN_H/16))
            self.frame = pygame.transform.rotate(self.frame, self.angle)
            self.frame.set_colorkey(SCREEN_COLUR)
            self.frame_copy = None
        def update(self) -> None:
            self.frame_copy = pygame.transform.rotate(self.frame, self.angle-90)
            screen.blit(self.frame_copy, (self.x - int(self.frame_copy.get_width()/2), self.y - int(self.frame_copy.get_height()/2)))
        def move(self, direction:"float", velocity:"float") -> None:
            radians = math.radians(self.angle)
            vertical = math.cos(radians) * self.velocity
            horizontal = math.sin(radians) * self.velocity

            self.x += horizontal
            self.y += vertical

    greencar = car()
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
            
        
        if mouse or pressed[pygame.K_UP]:
            greencar.velocity += SCREEN_W/20000
        elif mouse or pressed[pygame.K_DOWN]:
            greencar.velocity -= SCREEN_W/20000
        else: 
            if greencar.velocity > 0: greencar.velocity -= SCREEN_W/20000
            elif greencar.velocity < 0: greencar.velocity += SCREEN_W/20000

        #if greencar.velocity < 0 : greencar.velocity = 0

        greencar.move(greencar.angle, greencar.velocity)

        if pressed[pygame.K_LEFT]:
            greencar.angle += greencar.velocity/6

        if pressed[pygame.K_RIGHT]:
            greencar.angle -= greencar.velocity/6

                
        greencar.update()
        screen.blit(text, (SCREEN_W+(SCREEN_W/16), SCREEN_H+(SCREEN_H/16)))
        
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__" : main(len(sys.argv[0:]), sys.argv[0:])