import pygame
import random
import time

import player
import asteroid
import asteriodback

# Инициализация Pygame
pygame.init()

# Определение размеров экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 750

# Установка заголовка окна
pygame.display.set_caption("Астероиды")

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

star = pygame.image.load('pictures/bonus.png')  # Картинка для бонуса
bg = pygame.image.load('pictures/bg.png')  # Картинка для заднего фона

game_music = pygame.mixer.Sound('sounds/Rolle.wav')  # Фоновая музыка для иры
shoot = pygame.mixer.Sound('sounds/shoot.wav')  # Звук выстрела
bangLargeSound = pygame.mixer.Sound('sounds/explosion-01.mp3')  # Звук взрыва при соприкосновении с игроком
bangSmallSound = pygame.mixer.Sound('sounds/explosion-02.wav')  # Звук взрыва при соприкосновении выстрела с астероидом
shoot.set_volume(.25)  # Громкость
bangLargeSound.set_volume(.25)  # Громкость
bangSmallSound.set_volume(.25)  # Громкость
game_music.set_volume(.25)  # Громкость
gameover = False  # Переменная для проверки завершения игры
lives = 3  # Жизни
score = 0  # Очки
rapidFire = False  # Быстрый выстрел при уничтожении бонуса
rfStart = -1
isSoundOn = True
highScore = 0
clock = pygame.time.Clock()



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

global attack
attack = 0
def redrawGameWindow(x,y):
    win.blit(bg, (0,0))
    if x != 0 and y != 0:
        boom1 = pygame.image.load("pictures/2.png")
        win.blit(boom1, (x, y))
        boom2 = pygame.image.load("pictures/3.png")
        win.blit(boom2, (x, y))
        boom3 = pygame.image.load("pictures/4.png")
        win.blit(boom3, (x, y))
        boom4 = pygame.image.load("pictures/5.png")
        win.blit(boom4, (x, y))
        boom5 = pygame.image.load("pictures/6.png")
        win.blit(boom5, (x, y))
        boom6 = pygame.image.load("pictures/7.png")
        win.blit(boom6, (x, y))
    font = pygame.font.SysFont('arial',30)
    livesText = font.render('Жизни: ' + str(lives), 1, (255, 255, 255))
    playAgainText = font.render('Нажмите esc, чтобы начать сначала', 1, (255,255,255))
    scoreText = font.render('Очки: ' + str(score), 1, (255,255,255))
    highScoreText = font.render('Максимальный результат: ' + str(highScore), 1, (255, 255, 255))

    for d in asteroidsback:
        d.draw(win)
    player.draw(win,attack)
    for a in asteroids:
        a.draw(win)
    for b in playerBullets:
        b.draw(win)
    for s in stars:
        s.draw(win)

    if rapidFire:  # Быстрый выстрел при уничтожении бонуса
        pygame.draw.rect(win, (0, 0, 0), [SCREEN_WIDTH // 2 - 51, 19, 102, 22])
        pygame.draw.rect(win, (255, 255, 255), [SCREEN_WIDTH // 2 - 50, 20, 100 - 100 * (count - rfStart) / 500, 20])

    if gameover:
        win.blit(playAgainText, (SCREEN_WIDTH//2-playAgainText.get_width()//2, SCREEN_HEIGHT//2 - playAgainText.get_height()//2))
    win.blit(scoreText, (SCREEN_WIDTH- scoreText.get_width() - 25, 25))
    win.blit(livesText, (25, 25))
    win.blit(highScoreText, (SCREEN_WIDTH - highScoreText.get_width() -25, 35 + scoreText.get_height()))
    pygame.display.update()


class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        for i in range(7):
            img = pygame.image.load(f"pictures/{i + 1}.png")
            self.images.append(pygame.transform.scale(img, (100, 100)))

        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = (50, 50)

        self.animation_time = 0.05
        self.current_time = 0

    def update(self, dt):
        self.current_time += dt

        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.image_index += 1

            if self.image_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.image_index]
                self.rect = self.image.get_rect()
                self.rect.center = (self.rect.centerx, self.rect.centery)


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
                    shoot.play()
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    shoot.play()
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

main_menu()
game_music.play()
player = player.Player()
playerBullets = []
asteroids = []
asteroidsback = []
count = 0
stars = []
run = True
while run:
    count += 1
    if not gameover:
        for b in asteroidsback:
            b.x += b.xv
            b.y += b.yv
        if count % 25 == 0:
            asteroidsback.append(asteriodback.Asteroiback())
        if count % 50 == 0:
            asteroids.append(asteroid.Asteroid())
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

            # Столкновение с игроком
            if (a.x >= player.x - player.w//2 and a.x <= player.x + player.w//2) or (a.x + a.w <= player.x + player.w//2 and a.x + a.w >= player.x - player.w//2):
                if(a.y >= player.y - player.h//2 and a.y <= player.y + player.h//2) or (a.y + a.h >= player.y - player.h//2 and a.y + a.h <= player.y + player.h//2):
                    redrawGameWindow(a.x, a.y)
                    lives -= 1
                    attack += 1
                    bangLargeSound.play()
                    asteroids.pop(asteroids.index(a))
                    break

            # bullet collision
            for b in playerBullets:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        redrawGameWindow(a.x, a.y)
                        score += 1
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

            if event.key == pygame.K_ESCAPE:
                if gameover:
                    gameover = False
                    lives = 3
                    asteroids.clear()
                    stars.clear()
                    if score > highScore:
                        highScore = score
                    score = 0
                    attack = 0

    redrawGameWindow(0,0)
# Закрытие Pygame
pygame.quit()
