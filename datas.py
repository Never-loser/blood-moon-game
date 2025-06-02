import random
import pygame
lives = 0
counter = 0
Persian_language = False
Theme = 1
Volume_percentage = 100
timer_stop = False
global_total_seconds = 0
count__ = 40
count2 = 0
started = False
move = 1
s_width = 400
s_height = 400
snake = [(20, 20), (20, 30), (20, 40)]
s_direction = 'Down'
s_food_position = (random.randint(0, 39) * 10, random.randint(0, 39) * 10)
s_game_over = False
s_score = 0
s_time_left = 30
color = False
chess = False
riddle1 = False
riddle2 = False
riddle3 = False

math_physics1 = False
math_physics2 = False
math_physics3 = False

chemistry1 = False
chemistry2 = False
chemistry3 = False

biology1 = False
biology2 = False
biology3 = False

math_game = False
a = ""
b = ""
snake_game = False
maze = False
score = 0
time_left = 60

pygame.mixer.init()
save_file = "saving.txt"
musics = ["music2.mp3", "music3.mp3", "music4.mp3", "music1.mp3", "music5.mp3", "music6.mp3", "music7.mp3"]

music = 'SoundEffects/startup.mp3'
