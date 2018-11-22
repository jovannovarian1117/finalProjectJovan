from pygame import *
import pygame.font
import random

window_x = 500
window_y = 550

# The main and the initial setting for the while True loop that display the screen
init()
window = display.set_mode((window_x, window_y))
bg = pygame.image.load('wallpaper.jpg').convert()
display.set_caption('Help Linux Jump!')
clock = time.Clock()

#class Play_Button:
    #def __init__(self,windows,theText):
        #self.windows = windows
        #self.windows_rect = self.windows.get_rect()
        #self.button_width = 100
        #self.button_height = 50
        #self.button_color = (255,255,0)
        #self.text_color = (0,0,0)
        #self.text_font = pygame.font.SysFont(None,36)

        #self.button_rect = pygame.Rect(0,0,self.button_width,self.button_height)
        #self.button_rect.center = self.windows_rect.center

        #self.prep_theText(theText)

    #def prep_theText(self,theText):
        #self.theText_img = self.text_font.render(theText,True,self.text_color,self.button_color)
       # self.theText_img_rect = self.theText_img.get_rect()
       # self.theText_img_rect.center = self.rect.center

    #def draw_button(self):
       ## self.windows.blit(self.theText_img,self.theText_img_rect)

class Stick_Man:
    # Class for the the Stick_man , so that it initiate the characters and also the the pictures when the
    # character wants to move in various movement.
    def __init__(self):
        self.crouch = image.load('dino.png')
        self.fall = image.load('dino.png')
        self.jumping_right = image.load('dino.png')
        self.jumping_left = transform.flip(self.jumping_right, True, False)
        self.stand = image.load('dino.png')

        self.reset()


    def reset(self):
        # this function is used for reset, so that if the characters dead, its reset into this condition.
        self.speed_x = 0
        self.speed_y = 0
        self.max_speed_x = 5
        self.max_speed_y = 15
        self.x_acceleration = 0.5
        self.img = self.jumping_right
        self.jump_speed = 15

        scale = 7
        self.width, self.height = 7 * scale, 12 * scale
        self.scale = scale

        self.x = (window_x - self.width) / 2
        self.y = window_y - self.height

    def update(self, p):
        # this function is for , after the reset/initial, it updates the movement when clicked ,in movement detection.
        # it contains function for side_controls of the wallpaper screen and also movement and show.
        self.side_control()
        self.physics(p)
        self.move()
        self.show()

        self.x += self.speed_x
        self.y -= self.speed_y

        return (self.img, (self.x, self.y, self.width, self.height))

    def physics(self, p):

        on = False

        for colour, rect in p:
            x, y, w, h = rect

            # X range
            if self.x + self.width / 2 > x and self.x - self.width / 2 < x + w:
                # Y range
                if self.y + self.height >= y and self.y + self.height <= y + h:

                    if self.speed_y < 0:
                        on =  True #sudden jump high

        if not on and not self.y >= window_y - self.height:
            # as it become slower , it jumps higher
            self.speed_y -= 0.5
        elif on:
            self.speed_y = self.jump_speed
        else:
            self.y = window_y - self.height
            self.speed_x = 0
            #set to 0 or not it jump in initiation
            self.speed_y = 0
            if self.x != (window_x - self.width) / 2:
                if self.x > (window_x - self.width) / 2:
                    self.x = max((window_x - self.width) / 2, self.x - 6)
                else:
                    self.x = min((window_x - self.width) / 2, self.x + 6)

            else:
                keys = key.get_pressed()
                if keys[K_SPACE]:
                    self.speed_y = self.jump_speed

    def side_control(self):
        if self.x + self.width < 0:
            self.x = window_x - self.scale
        if self.x > window_x:
            self.x = -self.width

    def show(self):
        if self.speed_y > 0:
            if self.speed_x > 0:
                self.img = self.jumping_right
            elif self.speed_x < 0:
                self.img = self.jumping_left
        else:
            self.img = self.fall

    def slow_character(self):
        if self.speed_x < 0: self.speed_x = min(0, self.speed_x + self.x_acceleration / 6)
        if self.speed_x > 0: self.speed_x = max(0, self.speed_x - self.x_acceleration / 6)

    def move(self):
        keys = key.get_pressed()

        if not self.y >= window_y - self.height:

            if keys[K_LEFT] and keys[K_RIGHT]:
                self.slow_character()
            elif keys[K_LEFT]:
                self.speed_x -= self.x_acceleration
            elif keys[K_RIGHT]:
                self.speed_x += self.x_acceleration
            else:
                self.slow_character()

            self.speed_x = max(-self.max_speed_x, min(self.max_speed_x, self.speed_x))
            self.speed_y = max(-self.max_speed_y, min(self.max_speed_y, self.speed_y))


platform_spacing = 125


class Platform_Manager:
    # This class is for the management of the platforms
    def __init__(self):
        self.platforms = []
        self.spawns = 0
        self.start_spawn = window_y

    # the distance of each platforms movement heights
        scale = 3
        self.width, self.height = 24 * scale, 6 * scale

    def update(self):
        self.spawner()
        return self.manage()

    def spawner(self):
        if window_y - info['screen_y'] > self.spawns * platform_spacing:
            self.spawn()

# This function is for appending the platforms as the character jump over the screen(self.spawns += 1)
    # random movement and also added
    def spawn(self):
        y = self.start_spawn - self.spawns * platform_spacing
        x = random.randint(-self.width, window_x)

        self.platforms.append(Platform(x, y, random.choice([1, -1])))
        self.spawns += 1

    def manage(self):
        u = []
        b = []
        for i in self.platforms:
            i.move()
            i.change_direction()
            b.append(i.show())

            if i.on_screen():
                u.append(i)

        self.platforms = u
        return b


class Platform:
    # This class is for making the platform exist, generate the one platform so that it can be implemented
    # in the platform manager as it arrange alr from the class above
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 2
        self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        scale = 3
        self.width, self.height = 24 * scale, 6 * scale

    def move(self):
        self.x += self.speed * self.direction
        self.change_direction()

    def change_direction(self):
        if self.x <= 0:
            self.direction = 1
        if self.x + self.width >= window_x:
            self.direction = -1

    def on_screen(self):
        # if window_y changed to window_x , the platform that has been jump will dissapear
        if self.y > info['screen_y'] + window_y:
            return False
        return True

    def show(self):
        return ((25, 25, 112), (self.x, self.y, self.width, self.height))


def random_colour(l, h):
    return (random.randint(l, h), random.randint(l, h), random.randint(l, h))


def blit_images(x):
    for i in x:
        window.blit(transform.scale(i[0], (i[1][2], i[1][3])), (i[1][0], i[1][1] - info['screen_y']))

def event_loop():
    for loop in event.get():
        if loop.type == KEYDOWN:
            if loop.key == K_ESCAPE:
                quit()
        if loop.type == QUIT:
            quit()


f = font.SysFont('', 60)


def show_score(score, pos):
    # This function is for showing the score , in str with color code as following , initiate as True
    # on the screen. contains mathematical formula
    message = f.render(str(round(score)), True, (255, 255, 0))
    rect = message.get_rect()

    if pos == 0:
        x = window_x - rect.width - 10
    else:
        x = 10
    y = rect.height + 10

    # for showing the messege use the blit syntax

    window.blit(message, (x, y))


info = {
    'screen_y': 0,
    'score': 0,
    'high_score': 0
}

# call out the function from the c
stick_man = Stick_Man()
platform_manager = Platform_Manager()

while True:
    # Place the score for the screen

    event_loop()

    platform_blit = platform_manager.update()
    stick_blit = stick_man.update(platform_blit)
    info['screen_y'] = min(min(0, stick_blit[1][1] - window_y * 0.4), info['screen_y'])
    info['score'] = (-stick_blit[1][1] + 470) / 50

    print(stick_blit[1][1], info['screen_y'])
    if stick_blit[1][1] - 470 > info['screen_y']:
        info['score'] = 0
        info['screen_y'] = 0
        stick_man = Stick_Man()
        platform_manager = Platform_Manager()

    clock.tick(60)

    # Displaying the
    window.blit(bg,[0,0])

    blit_images([stick_blit])

    for x in platform_blit:
        i = list(x)
        i[1] = list(i[1])
        i[1][1] -= info['screen_y']
        draw.rect(window, i[0], i[1])

    info['high_score'] = max(info['high_score'], info['score'])

    show_score(info['score'], 1)
    show_score(info['high_score'], 0)

    display.update()