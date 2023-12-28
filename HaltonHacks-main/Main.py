import pygame, sys
import cv2
import time
import sys
import random
from pygame import mixer
mixer.init()

mixer.init()

pygame.init()

pygame.init()

HEIGHT = 720
WIDTH = 1280

WIN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("/Users/nirekshetty/Downloads/HaltonHacks-main/assets/Background.png")

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def processImage(cap, hand_cascade, palmCascade, start):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hand = hand_cascade.detectMultiScale(gray, 1.3, 5)
    palm = palmCascade.detectMultiScale(gray, 1.3, 5)
    if palm != (): 
        print("Detected")
        return "N"
    
    for (x, y, w, h) in hand:
        print( f"{x} , {y} , {h} ")
        center = [WIDTH/2 ,HEIGHT/2]
        print("center" , x - center[0] , y - center[1])
        
        DY = y - center[1]
        if time.time() - start >= 2:
            return "Timed Out"
        if DY > -90:
            print("D")
            return "D"
        if DY < -90:
            print("U")
            return "U"
        
        else: 
            return "N"

def play():
    while True:
        handCascade = cv2.CascadeClassifier('/Users/nirekshetty/Downloads/cv2/hand.xml')
        palmCascade = cv2.CascadeClassifier('/Users/nirekshetty/Downloads/palm.xml')
        smileCascade = cv2.CascadeClassifier('/Users/nirekshetty/Downloads/cv2/smile_cascade.xml')

        cap = cv2.VideoCapture(0)

        
        def handTrack(handCascade , LR=False ):
            start = time.time()
            WIDTH = 1080 
            HEIGHT = 720
            cap.set(3 ,WIDTH)
            cap.set(4 ,HEIGHT)
            hand_cascade = handCascade

            p_count=0
            frameMax = 60
            while True:
                # return processImage(cap, hand_cascade, palmCascade, start)
                if(p_count>=frameMax):
                    p_count = 0
                    return processImage(cap, hand_cascade, palmCascade, start)
                else:
                    p_count += 1
                    

        
        FPS = 30

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
        BALL_RADIUS = 7

        SCORE_FONT = pygame.font.SysFont("comicsans", 50)
        WINNING_SCORE = 10


        class Paddle:
            COLOR = WHITE
            VEL = 20

            def __init__(self, x, y, width, height):
                self.x = self.original_x = x
                self.y = self.original_y = y
                self.width = width
                self.height = height

            def draw(self, win):
                pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

            def move(self, up=True , N = False):
                if N == True:
                    self.y = self.y
                elif up:
                    self.y -= self.VEL
                else:
                    self.y += self.VEL

            def reset(self):
                self.x = self.original_x
                self.y = self.original_y

        def rightPaddleAlgorithm(right_paddle , ball):
                if ball.y > right_paddle.y + right_paddle.height/2:
                    right_paddle.move(up=False)
                if ball.y < right_paddle.y + right_paddle.height/2:
                    right_paddle.move(up=True)

        class Ball:
            MAX_VEL = 20
            COLOR = WHITE

            def __init__(self, x, y, radius):
                self.x = self.original_x = x
                self.y = self.original_y = y
                self.radius = radius
                self.x_vel = self.MAX_VEL
                self.y_vel = 0
                self.particles = []
                self.size = 12

            def draw(self, win):
                IMAGE = pygame.transform.scale(pygame.image.load('assets/cat.png').convert() , (50 , 50))  # or .convert_alpha()
                ball_rect = IMAGE.get_rect(center=(self.x, self.y))
                win.blit(IMAGE, ball_rect)
            def move(self):
                self.x += self.x_vel
                self.y += self.y_vel

            def reset(self):
                self.x = self.original_x
                self.y = self.original_y
                self.y_vel = 0
                self.x_vel *= -1
            def emit(self):
                if self.particles:
                    self.delete_particles()
                    for particle in self.particles:
                        particle[0].x -= 1
                        pygame.draw.rect(WIN,particle[1],particle[0])


            def add_particles(self,offset,color):
                pos_x = self.x
                pos_y = self.y
                particle_rect = pygame.Rect(int(pos_x - self.size/2),int(pos_y - self.size/2),self.size,self.size)
                self.particles.append((particle_rect,color))

            def delete_particles(self):
                particle_copy = [particle for particle in self.particles if particle[0].x > 0]
                self.particles = particle_copy


        def draw(win, paddles, ball, left_score, right_score):
            win.fill(BLACK)

            left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
            right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
            win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
            win.blit(right_score_text, (WIDTH * (3/4) -
            right_score_text.get_width()//2, 20))
            

            for paddle in paddles:
                paddle.draw(win)

            for i in range(10, HEIGHT, HEIGHT//20):
                if i % 2 == 1:
                    continue
                pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

            ball.draw(win)
            pygame.display.update()


        def handle_collision(ball, left_paddle, right_paddle):
            if ball.y + ball.radius >= HEIGHT:
                ball.y_vel *= -1
            elif ball.y - ball.radius <= 0:
                ball.y_vel *= -1

            if ball.x_vel < 0:
                if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
                    if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                        ball.x_vel *= -1

                        middle_y = left_paddle.y + left_paddle.height / 2
                        difference_in_y = middle_y - ball.y
                        reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                        y_vel = difference_in_y / reduction_factor
                        ball.y_vel = -1 * y_vel
                        mixer.music.load('sound.mp3')
                        mixer.music.play()

            else:
                if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
                    if ball.x + ball.radius >= right_paddle.x:
                        ball.x_vel *= -1

                        middle_y = right_paddle.y + right_paddle.height / 2
                        difference_in_y = middle_y - ball.y
                        reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                        y_vel = difference_in_y / reduction_factor
                        ball.y_vel = -1 * y_vel
                        mixer.music.load('sound.mp3')
                        mixer.music.play()


        def handle_paddle_movement(keys, left_paddle, right_paddle , ball):
            if handTrack(handCascade) == "U"and left_paddle.y - left_paddle.VEL >= 0:
                left_paddle.move(up=True)
            if handTrack(handCascade) == "D" and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
                left_paddle.move(up=False)
            else:
                left_paddle.move(N=True)   
            rightPaddleAlgorithm(right_paddle , ball)
            

        pygame.display.flip()

        def main():
            run = True
            clock = pygame.time.Clock()

            left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT //
                                2 + 200, PADDLE_WIDTH, PADDLE_HEIGHT)
            right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                                2 - PADDLE_HEIGHT//2 - 200, PADDLE_WIDTH, PADDLE_HEIGHT)
            ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

            left_score = 0
            right_score = 0

            while run:
                clock.tick(FPS)
                draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
                ball.add_particles(-30,pygame.Color("Red"))
                ball.add_particles(-18,pygame.Color("Orange"))
                ball.add_particles(-6,pygame.Color("Yellow"))
                ball.add_particles(6,pygame.Color("Green"))
                ball.add_particles(18,pygame.Color("Blue"))
                ball.add_particles(30,pygame.Color("Purple"))

                
                ball.emit()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        break

                keys = pygame.key.get_pressed()
                handle_paddle_movement(keys, left_paddle, right_paddle , ball)

                ball.move()
                handle_collision(ball, left_paddle, right_paddle)

                if ball.x < 0:
                    right_score += 1
                    ball.reset()
                elif ball.x > WIDTH:
                    left_score += 1
                    ball.reset()

                won = False
                if left_score >= WINNING_SCORE:
                    won = True
                    win_text = "Player Won!"
                elif right_score >= WINNING_SCORE:
                    won = True
                    win_text = "AI Won!"

                if won:
                    text = SCORE_FONT.render(win_text, 1, WHITE)
                    WIN.blit(text, (WIDTH//2 - text.get_width() //
                                    2, HEIGHT//2 - text.get_height()//2))
                    pygame.display.update()
                    pygame.time.delay(5000)
                    ball.reset()
                    left_paddle.reset()
                    right_paddle.reset()
                    left_score = 0
                    right_score = 0

            pygame.quit()


        if __name__ == '__main__':
            main()
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        WIN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        WIN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    
    mixer.music.load('/Users/nirekshetty/Downloads/HaltonHacks-main/assets/Soundtrack.mp3')
    mixer.music.play()
    while True:
        WIN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/Play.png"),(240,60)) , pos=(1000, 350) , 
                            text_input="PLAY", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/Options.png"),(400,60)), pos=(1000,450), 
                            text_input="OPTIONS", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/QUit.png"),(240,60)), pos=(1000 , 550), 
                            text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        WIN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
