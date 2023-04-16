import pygame
import random


import player
import asteroid

# Инициализация Pygame
pygame.init()

# Определение размеров экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 750

# Установка заголовка окна
pygame.display.set_caption("Астероиды")

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

star = pygame.image.load('pictures/bonus.png')
bg = pygame.image.load('pictures/bg.png')

shoot = pygame.mixer.Sound('sounds/shoot.wav')
bangLargeSound = pygame.mixer.Sound('sounds/bangLarge.wav')
bangSmallSound = pygame.mixer.Sound('sounds/bangSmall.wav')
shoot.set_volume(.25)
bangLargeSound.set_volume(.25)
bangSmallSound.set_volume(.25)

gameover = False
lives = 3
score = 0
rapidFire = False
rfStart = -1
isSoundOn = True
highScore = 0


class Bullet(object):
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = player.cosine
        self.s = player.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.w, self.h])

    def checkOffScreen(self):
        if self.x < -50 or self.x > SCREEN_WIDTH or self.y > SCREEN_HEIGHT or self.y < -50:
            return True

class Star(object):
    def __init__(self):
        self.img = star
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.ranPoint = random.choice([(random.randrange(0, SCREEN_WIDTH - self.w), random.choice([-1 * self.h - 5, SCREEN_HEIGHT + 5])),
                                       (random.choice([-1 * self.w - 5, SCREEN_WIDTH + 5]), random.randrange(0, SCREEN_HEIGHT - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < SCREEN_WIDTH//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < SCREEN_HEIGHT//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


def redrawGameWindow():
    win.blit(bg, (0,0))
    font = pygame.font.SysFont('arial',30)
    livesText = font.render('Жизни: ' + str(lives), 1, (255, 255, 255))
    playAgainText = font.render('Нажмите пробел, чтобы начать сначала', 1, (255,255,255))
    scoreText = font.render('Очки: ' + str(score), 1, (255,255,255))
    highScoreText = font.render('Максимальный результат: ' + str(highScore), 1, (255, 255, 255))

    player.draw(win)
    for a in asteroids:
        a.draw(win)
    for b in playerBullets:
        b.draw(win)
    for s in stars:
        s.draw(win)

    if rapidFire:
        pygame.draw.rect(win, (0, 0, 0), [SCREEN_WIDTH//2 - 51, 19, 102, 22])
        pygame.draw.rect(win, (255, 255, 255), [SCREEN_WIDTH//2 - 50, 20, 100 - 100*(count - rfStart)/500, 20])

    if gameover:
        win.blit(playAgainText, (SCREEN_WIDTH//2-playAgainText.get_width()//2, SCREEN_HEIGHT//2 - playAgainText.get_height()//2))
    win.blit(scoreText, (SCREEN_WIDTH- scoreText.get_width() - 25, 25))
    win.blit(livesText, (25, 25))
    win.blit(highScoreText, (SCREEN_WIDTH - highScoreText.get_width() -25, 35 + scoreText.get_height()))
    pygame.display.update()


# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Game Fonts
font = "Retro.ttf"


def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)

    return newText

# Main Menu
def main_menu():
    menu = True
    selected = "start"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        return
                    if selected == "quit":
                        pygame.quit()
                        quit()

        # Main Menu UI
        win.fill(blue)
        title = text_format("Asteroids", font, 90, yellow)
        if selected == "start":
            text_start = text_format("START", font, 75, white)
        else:
            text_start = text_format("START", font, 75, black)
        if selected == "quit":
            text_quit=text_format("QUIT", font, 75, white)
        else:
            text_quit = text_format("QUIT", font, 75, black)

        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()

        # Main Menu Text
        win.blit(title, (SCREEN_WIDTH/2 - (title_rect[2]/2), 80))
        win.blit(text_start, (SCREEN_WIDTH/2 - (start_rect[2]/2), 300))
        win.blit(text_quit, (SCREEN_WIDTH/2 - (quit_rect[2]/2), 360))
        pygame.display.update()
        pygame.display.set_caption("Python - Pygame Simple Main Menu Selection")
main_menu()
player = player.Player()
playerBullets = []
asteroids = []
count = 0
stars = []
run = True
while run:
    count += 1
    if not gameover:
        if count % 50 == 0:
            ran = 1
            asteroids.append(asteroid.Asteroid(ran))
        if count % 1000 == 0:
            stars.append(Star())


        player.updateLocation()
        for b in playerBullets:
            b.move()
            if b.checkOffScreen():
                playerBullets.pop(playerBullets.index(b))


        for a in asteroids:
            a.x += a.xv
            a.y += a.yv

            if (a.x >= player.x - player.w//2 and a.x <= player.x + player.w//2) or (a.x + a.w <= player.x + player.w//2 and a.x + a.w >= player.x - player.w//2):
                if(a.y >= player.y - player.h//2 and a.y <= player.y + player.h//2) or (a.y  +a.h >= player.y - player.h//2 and a.y + a.h <= player.y + player.h//2):
                    lives -= 1
                    asteroids.pop(asteroids.index(a))
                    if isSoundOn:
                        bangLargeSound.play()
                    break

            # bullet collision
            for b in playerBullets:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        if a.rank == 3:
                            if isSoundOn:
                                bangLargeSound.play()
                            score += 10
                            na1 = asteroid.Asteroid(2)
                            na2 = asteroid.Asteroid(2)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        elif a.rank == 2:
                            if isSoundOn:
                                bangSmallSound.play()
                            score += 20
                            na1 = asteroid.Asteroid(1)
                            na2 = asteroid.Asteroid(1)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        else:
                            score += 30
                            if isSoundOn:
                                bangSmallSound.play()
                        asteroids.pop(asteroids.index(a))
                        playerBullets.pop(playerBullets.index(b))
                        break

        for s in stars:
            s.x += s.xv
            s.y += s.yv
            if s.x < -100 - s.w or s.x > SCREEN_WIDTH + 100 or s.y > SCREEN_HEIGHT + 100 or s.y < -100 - s.h:
                stars.pop(stars.index(s))
                break
            for b in playerBullets:
                if (b.x >= s.x and b.x <= s.x + s.w) or b.x + b.w >= s.x and b.x + b.w <= s.x + s.w:
                    if (b.y >= s.y and b.y <= s.y + s.h) or b.y + b.h >= s.y and b.y + b.h <= s.y + s.h:
                        rapidFire = True
                        rfStart = count
                        stars.pop(stars.index(s))
                        playerBullets.pop(playerBullets.index(b))
                        break

        if lives <= 0:
            gameover = True

        if rfStart != -1:
            if count - rfStart > 500:
                rapidFire = False
                rfStart = -1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.turnLeft()
        if keys[pygame.K_RIGHT]:
            player.turnRight()
        if keys[pygame.K_UP]:
            player.moveForward()
        if keys[pygame.K_SPACE]:
            if rapidFire:
                playerBullets.append(Bullet())
                if isSoundOn:
                    shoot.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not gameover:
                    if not rapidFire:
                        playerBullets.append(Bullet())
                        if isSoundOn:
                            shoot.play()
            if event.key == pygame.K_m:
                isSoundOn = not isSoundOn

            if event.key == pygame.K_SPACE:
                if gameover:
                    gameover = False
                    lives = 3
                    asteroids.clear()
                    stars.clear()
                    if score > highScore:
                        highScore = score
                    score = 0

    redrawGameWindow()
# Закрытие Pygame
pygame.quit()
