import pygame
import os, sys
import ctypes
import json
import tkinter
import threading
import shutil

from pygame import mixer
from tkinter.filedialog import askopenfilename

from pygame.constants import MOUSEBUTTONUP

# intit()
pygame.init()
mixer.init()

clock = pygame.time.Clock()

# ctypes message boxW
def message(description, title):
    ctypes.windll.user32.MessageBoxW(0, description, title, 0)

# configuration
with open('configuration.json') as readfile:
    config = json.load(readfile)


screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption('Simple Music Player')
pygame.display.set_icon(pygame.image.load('icon.png'))


def background():
    try:
        image = pygame.image.load(config['background'])
        image = pygame.transform.scale(image, (600, 300))
        screen.blit(image, (0, 0))
    except:
        message('Please select a background image', 'Error')
        backgroundSelect()

def backgroundSelect():
    window = tkinter.Tk()
    window.withdraw()
    filename = askopenfilename(
        initialdir='Backgrounds',
        title='Select a background',
        filetypes=([('Supported Files', '*.png *.jpg')])
    )
    if filename != '':
        with open('configuration.json', 'w') as writefile:
            config['background'] = filename
            json.dump(config, writefile)
    window.destroy()

# maximum 1
play_count = 0
def play():
    # some variables
    global play_count
    play_count += 1
    def playThread():
        # make sure only one thread is running
        global play_count
        if play_count > 1:
            message('Music is already playing', 'Got a pair of eyes?')
            sys.exit()

        global musicList
        musicList = []
        for (dirpath, dirnames, filenames) in os.walk('Music'):
            musicList.extend(filenames)

        global scroll, scrollLimit
        scroll = 0
        scrollLimit = len(musicList) - 1

        while True:
            mixer.music.load(f'Music\{musicList[scroll]}')
            mixer.music.play()
            scroll += 1
            # wait until song is finished before moving on
            while mixer.music.get_busy():
                pass
            if scroll > scrollLimit:
                scroll = 0
    threading.Thread(target=(playThread)).start()

# It just works some how
def skip():
    global scroll, scrollLimit, musicList
    try:
        if scroll > scrollLimit:
            scroll = 0

        # skip any songs that are not found to prevent errors
        try:
            mixer.music.load(f'Music\{musicList[scroll]}')
        except:
            scroll += 1
        mixer.music.play()
    except:
        message('You can\'t skip music if you haven\'t played any yet', 'Bruh')

def add():
    window = tkinter.Tk()
    window.withdraw()
    filename = askopenfilename(
        title='Select a song to import',
        filetypes=([('Supported Files', '*.mp3 *.wav')])
    )
    if filename != '':
        shutil.copy(filename, 'Music')
    window.destroy()

def remove():
    window = tkinter.Tk()
    window.withdraw()
    filename = askopenfilename(
        initialdir='Music',
        title='Select a song to delete',
        filetypes=([('Supported Files', '*.mp3 *.wav')])
    )
    if filename != '':
        os.remove(filename)
    window.destroy()


class Button():
    def __init__(
        self, x, y, width, height, text,
        font, fontsize, colour, forecolour,
        outlineBool, function, outlineLength=2,
        outlineColour=(0, 0, 0),
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.colour = colour
        self.forecolour = forecolour
        self.fontsize = fontsize
        self.font = font
        self.outlineBool = outlineBool
        self.outlineLength = outlineLength
        self.outlineColour = outlineColour
        self.function = function

    def draw(self):
        if self.outlineBool == True:
            pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, self.outlineColour, (self.x, self.y, self.width, self.height), self.outlineLength)
        else:
            pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont(self.font, self.fontsize)
        text = font.render(self.text, True, self.forecolour)
        text_rect = text.get_rect()
        text_rect.center = (self.x + (self.width / 2), self.y + (self.height / 2))
        screen.blit(text, text_rect)

    def is_hover(self):
        if pygame.mouse.get_pos()[0] > self.x and pygame.mouse.get_pos()[0] < self.x + self.width:
            if pygame.mouse.get_pos()[1] > self.y and pygame.mouse.get_pos()[1] < self.y + self.height:
                # show hover state
                overlay_button = Button(
                    self.x, self.y, self.width, self.height, self.text, self.font, self.fontsize,
                    (150, 225, 225), (255, 255, 255), True, self.function, 2, 'white'
                )
                overlay_button.draw()
                # call function when button clicked
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.function()


# ---- class variables ----
# Button(self, x, y, width, height, text, font, fontsize, colour, forecolour, outlineBool, function, outlineLength=2, outlineColour=(0, 0, 0))
backgroundSelect_button = Button(440, 10, 150, 25, 'Select Background', 'arial', 20,(255, 255, 255), (0, 0, 0), True, backgroundSelect)
play_button = Button(250, 245, 100, 50, 'Play', 'cosmic sans ms', 50, (255, 255, 255), (0, 0, 0), True, play)
skip_button = Button(250, 220, 100, 25, 'Skip', 'cosmic sans ms', 25, (255, 255, 255), (0, 0, 0), True, skip)
add_button = Button(10, 10, 50, 25, 'Add', 'cosmic sans ms', 25, (255, 255, 255), (0, 0, 0), True, add)
del_button = Button(10, 37, 50, 25, 'Del', 'cosmic sans ms', 25, (255, 255, 255), (0, 0, 0), True, remove)

# event handler variables
run = True


while run:
    clock.tick(60)
    background()


    backgroundSelect_button.draw()
    backgroundSelect_button.is_hover()
    play_button.draw()
    play_button.is_hover()
    skip_button.draw()
    skip_button.is_hover()
    add_button.draw()
    add_button.is_hover()
    del_button.draw()
    del_button.is_hover()


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()

pygame.quit()
sys.exit()