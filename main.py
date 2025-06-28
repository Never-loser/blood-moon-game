from tkinter import *
import pygame
import random
from PIL import Image, ImageTk
# from tkvideo import tkvideo
import os
# import pyttsx3
import cv2

# import time
ckh = 0
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


def start():
    root = Tk()
    root.title('Game Name')
    root.attributes('-fullscreen', True)
    root.config(bg='black')
    video_path = "Videos/VID_20250519_105544.mp4"
    cap = cv2.VideoCapture(video_path)

    def Exit_game():
        messagebox = Toplevel(root)
        messagebox.title("Exit Confirmation")
        messagebox.configure(bg="black")  # Set background color

        # Prevent focus stealing
        messagebox.transient(root)
        messagebox.grab_set()
        if Theme == 1:
            if not Persian_language:
                label = Label(messagebox, text="Are you sure you want to leave?", fg="red", bg="black",
                              font=("Arial", 14))
                label.pack(pady=10)

                btn_yes = Button(messagebox, text="Yes", fg="red", bg="black", font=("Arial", 12),
                                 command=lambda: Confirmation_Exit())
                btn_yes.pack(side="left", padx=20, pady=10)

                btn_no = Button(messagebox, text="No", fg="red", bg="black", font=("Arial", 12),
                                command=messagebox.destroy)
                btn_no.pack(side="right", padx=20, pady=10)
            else:
                label = Label(messagebox, text="آیا مطمعنی که می خوای خارج شی؟", fg="red", bg="black",
                              font=("B Titr", 14))
                label.pack(pady=10)

                btn_yes = Button(messagebox, text="بله", fg="red", bg="black", font=("B Titr", 12),
                                 command=lambda: Confirmation_Exit())
                btn_yes.pack(side="left", padx=20, pady=10)

                btn_no = Button(messagebox, text="خیر", fg="red", bg="black", font=("B Titr", 12),
                                command=messagebox.destroy)
                btn_no.pack(side="right", padx=20, pady=10)
        else:
            if not Persian_language:
                label = Label(messagebox, text="Are you sure you want to leave?", fg="lightblue", bg="black",
                              font=("Arial", 14))
                label.pack(pady=10)

                btn_yes = Button(messagebox, text="Yes", fg="lightblue", bg="black", font=("Arial", 12),
                                 command=lambda: Confirmation_Exit())
                btn_yes.pack(side="left", padx=20, pady=10)

                btn_no = Button(messagebox, text="No", fg="lightblue", bg="black", font=("Arial", 12),
                                command=messagebox.destroy)
                btn_no.pack(side="right", padx=20, pady=10)

    def Confirmation_Exit():
        root.destroy()  # Close main window

    # Get video dimensions
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create a label for video background
    video_label = Label(root)
    video_label.place(x=0, y=0, relwidth=1, relheight=1)

    def update_video():
        ret, frame = cap.read()
        if ret:
            # Convert OpenCV BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert to PIL Image
            img = Image.fromarray(frame)
            # Resize to fit the window (optional)
            img = img.resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS)
            # Convert to Tkinter PhotoImage
            imgtk = ImageTk.PhotoImage(image=img)
            # Update the label
            video_label.imgtk = imgtk
            video_label.config(image=imgtk)
        else:
            # Loop the video
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        # Schedule the next update (~30 FPS)
        root.after(33, update_video)  # ~30 فریم در ثانیه

    # Start updating the video
    update_video()

    def music():
        global music
        pygame.mixer.music.load(music)
        pygame.mixer.music.play()

    music()

    lives = 0

    # Settings Page

    class Settings:

        # Defining root and widgets

        def __init__(self):
            self.root = Tk()
            self.root.title('Settings')
            self.root.attributes('-fullscreen', True)
            self.root.config(bg='black')
            self.Background_image = Image.open('Pictures/settings.jpg')

            def resize_image(event):
                global Fixed_bg_image
                new_width, new_height = event.width, event.height
                resized = self.Background_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                Fixed_bg_image = ImageTk.PhotoImage(resized)
                background_label.configure(image=Fixed_bg_image)

            # Create label and bind resize event
            Fixed_bg_image = ImageTk.PhotoImage(self.Background_image)
            background_label = Label(self.root, image=Fixed_bg_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Ensure it covers the entire window

            self.root.bind("<Configure>", resize_image)

            if Theme == 1:
                if not Persian_language:
                    self.root.label = Label(self.root, text='Settings', font=('Roman', 30, 'bold'), bg='black',
                                            fg='red')
                    self.change_audio_label = Label(self.root, text='Audio', font=('Roman', 20, 'bold'),
                                                    bg='black'
                                                    , fg='red', width=30, highlightthickness=1.5,
                                                    highlightcolor='white')

                    self.scale = Scale(self.root, from_=0, to=100, orient=HORIZONTAL, width=20, bg='black', fg='red',
                                       cursor="hand2",
                                       sliderlength=30, label='                  Volume'
                                       , length=387, font=('Roman', 15, 'bold'))
                    self.apply = Button(self.root, text='Change\nVolume', bg='black', fg='red', cursor="hand2",
                                        relief="flat",
                                        font=('Roman', 20, 'bold'),
                                        command=self.change_vol)
                    self.apply.bind('<Enter>', lambda e: self.apply.config(bg='red', fg='black'))
                    self.apply.bind('<Leave>', lambda e: self.apply.config(bg='black', fg='red'))

                    self.persian_lang_button = Radiobutton(self.root, text='Persian', font=('Roman', 20, 'bold'),
                                                           bg='black',
                                                           fg='red', width=20, command=self.persian_lang_change)

                    self.persian_lang_button.bind('<Enter>',
                                                  lambda e: self.persian_lang_button.config(bg='red', fg='black'))
                    self.persian_lang_button.bind('<Leave>',
                                                  lambda e: self.persian_lang_button.config(bg='black', fg='red'))

                    self.english_lang_button = Radiobutton(self.root, text='English', font=('Roman', 20, 'bold'),
                                                           bg='black',
                                                           fg='red', width=20, command=self.english_lang_change)

                    self.english_lang_button.bind('<Enter>',
                                                  lambda e: self.english_lang_button.config(bg='red', fg='black'))
                    self.english_lang_button.bind('<Leave>',
                                                  lambda e: self.english_lang_button.config(bg='black', fg='red'))

                    self.change_lang_label = Label(self.root, text='Language', font=('Roman', 20, 'bold'),
                                                   bg='black'
                                                   , fg='red', width=30, highlightthickness=1.5, highlightcolor='white')

                    self.theme_change_label = Label(self.root, text='Theme', bg='black', fg='red', width=30,
                                                    font=('Roman', 20, 'bold'), highlightthickness=1.5,
                                                    highlightbackground='white')
                    self.first_theme_button = Radiobutton(self.root, text='Theme 1', bg='black', fg='red',
                                                          font=('Roman', 20, 'bold'), width=10,
                                                          command=self.Theme_1_change)

                    self.first_theme_button.bind('<Enter>',
                                                 lambda e: self.first_theme_button.config(bg='red', fg='black'))
                    self.first_theme_button.bind('<Leave>',
                                                 lambda e: self.first_theme_button.config(bg='black', fg='red'))

                    self.second_theme_button = Radiobutton(self.root, text='Theme 2', bg='black', fg='red',
                                                           font=('Roman', 20, 'bold'), width=10,
                                                           command=self.Theme_2_change)

                    self.second_theme_button.bind('<Enter>',
                                                  lambda e: self.second_theme_button.config(bg='red', fg='black'))
                    self.second_theme_button.bind('<Leave>',
                                                  lambda e: self.second_theme_button.config(bg='black', fg='red'))

                    self.change_audio = Button(self.root, text='Change Audio', font=('Roman', 20, 'bold'), bg='black',
                                               cursor="hand2", relief='groove',
                                               fg='red', width=30, highlightthickness=1.5, highlightcolor='white',
                                               command=self.change_music)
                    self.change_audio.bind('<Enter>',
                                           lambda e: self.change_audio.config(bg='red', fg='black'))
                    self.change_audio.bind('<Leave>',
                                           lambda e: self.change_audio.config(bg='black', fg='red'))
                    self.back = Button(self.root, text='Main Menu', bg='black', fg='red', font=('Roman', 20, 'bold'),
                                       command=self.Back)

                    self.back.bind('<Enter>', lambda e: self.back.config(bg='red', fg='black'))
                    self.back.bind('<Leave>', lambda e: self.back.config(bg='black', fg='red'))


                else:
                    self.root.label = Label(self.root, text='تنظیمات ', font=('Mj_Kaman', 25), bg='black',
                                            fg='red')
                    self.change_audio_label = Label(self.root, text='موسیقی', font=('Mj_Kaman', 20),
                                                    bg='black'
                                                    , fg='red', width=20, highlightthickness=1.5,
                                                    highlightcolor='white')

                    self.scale = Scale(self.root, from_=0, to=100, orient=HORIZONTAL, width=20, bg='black', fg='red',
                                       cursor="hand2",
                                       sliderlength=30, label='                  صدا'
                                       , length=387, font=('Mj_Kaman', 15))
                    self.apply = Button(self.root, text='تغییر صدا', bg='black', fg='red', cursor="hand2",

                                        relief="flat",
                                        font=('Mj_Kaman', 15),
                                        command=self.change_vol)
                    self.apply.bind('<Enter>', lambda e: self.apply.config(bg='red', fg='black'))
                    self.apply.bind('<Leave>', lambda e: self.apply.config(bg='black', fg='red'))

                    self.persian_lang_button = Radiobutton(self.root, text='فارسی',
                                                           font=('Mj_Kaman', 20, 'bold'),
                                                           bg='black', cursor="hand2",
                                                           fg='red', width=10, command=self.persian_lang_change)

                    self.persian_lang_button.bind('<Enter>',
                                                  lambda e: self.persian_lang_button.config(bg='red', fg='black'))
                    self.persian_lang_button.bind('<Leave>',
                                                  lambda e: self.persian_lang_button.config(bg='black', fg='red'))

                    self.english_lang_button = Radiobutton(self.root, text='انگلیسی',
                                                           font=('Mj_Kaman', 20, 'bold'), cursor="hand2",
                                                           bg='black',
                                                           fg='red', width=10, command=self.english_lang_change)

                    self.english_lang_button.bind('<Enter>',
                                                  lambda e: self.english_lang_button.config(bg='red', fg='black'))
                    self.english_lang_button.bind('<Leave>',
                                                  lambda e: self.english_lang_button.config(bg='black', fg='red'))

                    self.change_lang_label = Label(self.root, text='زبان', font=('Mj_Kaman', 20, 'bold'),
                                                   bg='black'
                                                   , fg='red', width=20, highlightthickness=1.5, highlightcolor='white')

                    self.theme_change_label = Label(self.root, text='تم', bg='black', fg='red', width=20,
                                                    font=('Mj_Kaman', 20, 'bold'), highlightthickness=1.5,
                                                    highlightbackground='white')
                    self.first_theme_button = Radiobutton(self.root, text='تم1', bg='black', fg='red',
                                                          font=('Mj_Kaman', 20, 'bold'), width=10, cursor="hand2",
                                                          command=self.Theme_1_change)

                    self.first_theme_button.bind('<Enter>',
                                                 lambda e: self.first_theme_button.config(bg='red', fg='black'))
                    self.first_theme_button.bind('<Leave>',
                                                 lambda e: self.first_theme_button.config(bg='black', fg='red'))

                    self.second_theme_button = Radiobutton(self.root, text='تم2', bg='black', fg='red',
                                                           font=('Mj_Kaman', 20, 'bold'), width=10, cursor="hand2",
                                                           command=self.Theme_2_change)

                    self.second_theme_button.bind('<Enter>',
                                                  lambda e: self.second_theme_button.config(bg='red', fg='black'))
                    self.second_theme_button.bind('<Leave>',
                                                  lambda e: self.second_theme_button.config(bg='black', fg='red'))

                    self.change_audio = Button(self.root, text='تغییر موسیقی ', font=('Mj_Kaman', 20, 'bold'),
                                               bg='black',
                                               cursor="hand2", relief='groove',
                                               fg='red', width=20, highlightthickness=1.5, highlightcolor='white',
                                               command=self.change_music)
                    self.change_audio.bind('<Enter>',
                                           lambda e: self.change_audio.config(bg='red', fg='black'))
                    self.change_audio.bind('<Leave>',
                                           lambda e: self.change_audio.config(bg='black', fg='red'))
                    self.back = Button(self.root, text=' منو اصلی', bg='black', fg='red',
                                       font=('Mj_Kaman', 20, 'bold'),
                                       command=self.Back, cursor="hand2")

                    self.back.bind('<Enter>', lambda e: self.back.config(bg='red', fg='black'))
                    self.back.bind('<Leave>', lambda e: self.back.config(bg='black', fg='red'))

            else:
                if not Persian_language:
                    self.root.label = Label(self.root, text='Settings', font=('Roman', 30, 'bold'), bg='black',
                                            fg='lightblue')
                    self.change_audio_label = Label(self.root, text='Audio', font=('Roman', 20, 'bold'),
                                                    bg='black'
                                                    , fg='lightblue', width=30, highlightthickness=1.5,
                                                    highlightcolor='white')

                    self.scale = Scale(self.root, from_=0, to=100, orient=HORIZONTAL, width=20, bg='black',
                                       fg='lightblue',
                                       cursor="hand2",
                                       sliderlength=30, label='                  Volume'
                                       , length=387, font=('Roman', 15, 'bold'))
                    self.apply = Button(self.root, text='Change\nVolume', bg='black', fg='lightblue', cursor="hand2",
                                        relief="flat",
                                        font=('Roman', 20, 'bold'),
                                        command=self.change_vol)
                    self.apply.bind('<Enter>', lambda e: self.apply.config(bg='lightblue', fg='black'))
                    self.apply.bind('<Leave>', lambda e: self.apply.config(bg='black', fg='red'))

                    self.persian_lang_button = Radiobutton(self.root, text='Persian', font=('Roman', 20, 'bold'),
                                                           bg='black',
                                                           fg='lightblue', width=20, command=self.persian_lang_change)

                    self.persian_lang_button.bind('<Enter>',
                                                  lambda e: self.persian_lang_button.config(bg='lightblue', fg='black'))
                    self.persian_lang_button.bind('<Leave>',
                                                  lambda e: self.persian_lang_button.config(bg='black', fg='lightblue'))

                    self.english_lang_button = Radiobutton(self.root, text='English', font=('Roman', 20, 'bold'),
                                                           bg='black',
                                                           fg='lightblue', width=20, command=self.english_lang_change)

                    self.english_lang_button.bind('<Enter>',
                                                  lambda e: self.english_lang_button.config(bg='lightblue', fg='black'))
                    self.english_lang_button.bind('<Leave>',
                                                  lambda e: self.english_lang_button.config(bg='black', fg='lightblue'))

                    self.change_lang_label = Label(self.root, text='Language', font=('Roman', 20, 'bold'),
                                                   bg='black'
                                                   , fg='lightblue', width=30, highlightthickness=1.5,
                                                   highlightcolor='white')

                    self.theme_change_label = Label(self.root, text='Theme', bg='black', fg='lightblue', width=30,
                                                    font=('Roman', 20, 'bold'), highlightthickness=1.5,
                                                    highlightbackground='white')
                    self.first_theme_button = Radiobutton(self.root, text='Theme 1', bg='black', fg='lightblue',
                                                          font=('Roman', 20, 'bold'), width=10,
                                                          command=self.Theme_1_change)

                    self.first_theme_button.bind('<Enter>',
                                                 lambda e: self.first_theme_button.config(bg='lightblue', fg='black'))
                    self.first_theme_button.bind('<Leave>',
                                                 lambda e: self.first_theme_button.config(bg='black', fg='lightblue'))

                    self.second_theme_button = Radiobutton(self.root, text='Theme 2', bg='black', fg='lightblue',
                                                           font=('Roman', 20, 'bold'), width=10,
                                                           command=self.Theme_2_change)

                    self.second_theme_button.bind('<Enter>',
                                                  lambda e: self.second_theme_button.config(bg='lightblue', fg='black'))
                    self.second_theme_button.bind('<Leave>',
                                                  lambda e: self.second_theme_button.config(bg='black', fg='lightblue'))

                    self.change_audio = Button(self.root, text='Change Audio', font=('Roman', 20, 'bold'), bg='black',
                                               cursor="hand2", relief='groove',
                                               fg='lightblue', width=30, highlightthickness=1.5, highlightcolor='white',
                                               command=self.change_music)
                    self.change_audio.bind('<Enter>',
                                           lambda e: self.change_audio.config(bg='lightblue', fg='black'))
                    self.change_audio.bind('<Leave>',
                                           lambda e: self.change_audio.config(bg='black', fg='lightblue'))
                    self.back = Button(self.root, text='Main Menu', bg='black', fg='lightblue',
                                       font=('Roman', 20, 'bold'),
                                       command=self.Back)

                    self.back.bind('<Enter>', lambda e: self.back.config(bg='lightblue', fg='black'))
                    self.back.bind('<Leave>', lambda e: self.back.config(bg='black', fg='lightblue'))

                else:
                    self.root.label = Label(self.root, text='تنظیمات ', font=('Mj_Kaman', 25), bg='black',

                                            fg='lightblue')

                    self.change_audio_label = Label(self.root, text='موسیقی', font=('Mj_Kaman', 20),

                                                    bg='black'

                                                    , fg='lightblue', width=20, highlightthickness=1.5,

                                                    highlightcolor='white')

                    self.scale = Scale(self.root, from_=0, to=100, orient=HORIZONTAL, width=20, bg='black',
                                       fg='lightblue',

                                       cursor="hand2",

                                       sliderlength=30, label='                  صدا'

                                       , length=387, font=('Mj_Kaman', 15))

                    self.apply = Button(self.root, text='تغییر صدا', bg='black', fg='lightblue', cursor="hand2",

                                        relief="flat",

                                        font=('Mj_Kaman', 15),

                                        command=self.change_vol)

                    self.apply.bind('<Enter>', lambda e: self.apply.config(bg='lightblue', fg='black'))

                    self.apply.bind('<Leave>', lambda e: self.apply.config(bg='black', fg='lightblue'))

                    self.persian_lang_button = Radiobutton(self.root, text='فارسی',

                                                           font=('Mj_Kaman', 20, 'bold'),

                                                           bg='black', cursor="hand2",

                                                           fg='lightblue', width=10, command=self.persian_lang_change)

                    self.persian_lang_button.bind('<Enter>',

                                                  lambda e: self.persian_lang_button.config(bg='lightblue', fg='black'))

                    self.persian_lang_button.bind('<Leave>',

                                                  lambda e: self.persian_lang_button.config(bg='black', fg='lightblue'))

                    self.english_lang_button = Radiobutton(self.root, text='انگلیسی',

                                                           font=('Mj_Kaman', 20, 'bold'), cursor="hand2",

                                                           bg='black',

                                                           fg='lightblue', width=10, command=self.english_lang_change)

                    self.english_lang_button.bind('<Enter>',

                                                  lambda e: self.english_lang_button.config(bg='lightblue', fg='black'))

                    self.english_lang_button.bind('<Leave>',

                                                  lambda e: self.english_lang_button.config(bg='black', fg='lightblue'))

                    self.change_lang_label = Label(self.root, text='زبان', font=('Mj_Kaman', 20, 'bold'),

                                                   bg='black'

                                                   , fg='lightblue', width=20, highlightthickness=1.5,
                                                   highlightcolor='white')

                    self.theme_change_label = Label(self.root, text='تم', bg='black', fg='lightblue', width=20,

                                                    font=('Mj_Kaman', 20, 'bold'), highlightthickness=1.5,

                                                    highlightbackground='white')

                    self.first_theme_button = Radiobutton(self.root, text='تم1', bg='black', fg='lightblue',

                                                          font=('Mj_Kaman', 20, 'bold'), width=10, cursor="hand2",

                                                          command=self.Theme_1_change)

                    self.first_theme_button.bind('<Enter>',

                                                 lambda e: self.first_theme_button.config(bg='lightblue', fg='black'))

                    self.first_theme_button.bind('<Leave>',

                                                 lambda e: self.first_theme_button.config(bg='black', fg='lightblue'))

                    self.second_theme_button = Radiobutton(self.root, text='تم2', bg='black', fg='lightblue',

                                                           font=('Mj_Kaman', 20, 'bold'), width=10, cursor="hand2",

                                                           command=self.Theme_2_change)

                    self.second_theme_button.bind('<Enter>',

                                                  lambda e: self.second_theme_button.config(bg='lightblue', fg='black'))

                    self.second_theme_button.bind('<Leave>',

                                                  lambda e: self.second_theme_button.config(bg='black', fg='lightblue'))

                    self.change_audio = Button(self.root, text='تغییر موسیقی ', font=('Mj_Kaman', 20, 'bold'),

                                               bg='black',

                                               cursor="hand2", relief='groove',

                                               fg='lightblue', width=20, highlightthickness=1.5, highlightcolor='white',

                                               command=self.change_music)

                    self.change_audio.bind('<Enter>',

                                           lambda e: self.change_audio.config(bg='lightblue', fg='black'))

                    self.change_audio.bind('<Leave>',

                                           lambda e: self.change_audio.config(bg='black', fg='lightblue'))

                    self.back = Button(self.root, text=' منو اصلی', bg='black', fg='lightblue',

                                       font=('Mj_Kaman', 20, 'bold'),

                                       command=self.Back, cursor="hand2")

                    self.back.bind('<Enter>', lambda e: self.back.config(bg='lightblue', fg='black'))

                    self.back.bind('<Leave>', lambda e: self.back.config(bg='black', fg='lightblue'))
                    self.root.label.pack()
            self.scale.place(x=1050, y=300)
            self.scale.set(Volume_percentage)
            self.apply.place(x=1200, y=400)
            self.change_lang_label.place(x=90, y=100)
            self.english_lang_button.place(x=120, y=200)
            self.persian_lang_button.place(x=120, y=280)
            self.theme_change_label.place(x=570, y=100)
            self.change_audio_label.place(x=1050, y=100)
            self.first_theme_button.place(x=690, y=200)
            self.second_theme_button.place(x=690, y=280)
            self.change_audio.place(x=1050, y=550)
            self.back.place(x=690, y=780)
            # Functions

        def change_music(self):
            global musics, music
            music = f'SoundEffects/{random.choice(musics)}'

        def Back(self, event=None):
            self.root.destroy()
            start()

        def start(self):
            self.root.mainloop()

        def change_vol(self):
            global Volume_percentage
            Volume_percentage = self.scale.get()
            percentage = self.scale.get() / 100
            pygame.mixer.music.set_volume(percentage)

        def persian_lang_change(self):
            global Persian_language

            if not Persian_language:
                Persian_language = True

                self.restart_settings()

        def english_lang_change(self):
            global Persian_language

            if Persian_language:
                Persian_language = False

                self.restart_settings()

        def Theme_1_change(self):
            global Theme

            if Theme == 2:
                Theme = 1

                self.restart_settings()

        def Theme_2_change(self):
            global Theme

            if Theme == 1:
                Theme = 2

                self.restart_settings()

        def restart_settings(self):
            self.root.destroy()
            Settings()

    # level 1 page

    class Level1:

        def __init__(self):
            self.root = Tk()
            self.root.title('Level 1')
            self.root.attributes('-fullscreen', True)
            self.root.config(bg='black')
            pygame.mixer.music.load('SoundEffects/Enter Hallownest.mp3')
            pygame.mixer.music.play()

            with open(save_file, 'r') as file:
                lines = file.readlines()

            lines[0] = 'Level1'

            with open(save_file, 'w') as file:
                file.writelines(lines)

            def on_click(event):
                x, y = event.x, event.y
                if 370 >= x >= 245 and 200 >= y >= 114:
                    self.color_game()
                    # self.canvas.config(cursor="hand2")
                elif 1040 >= x >= 200 and 490 >= y >= 375:
                    self.chess_game()
                elif 837 >= event.x >= 710 and 275 >= y >= 160:
                    self.riddle_game()

            def on_motion(event):
                x, y = event.x, event.y
                if 370 >= x >= 245 and 200 >= y >= 114:
                    self.canvas.config(cursor="hand2")
                elif 1040 >= x >= 200 and 490 >= y >= 375:
                    self.canvas.config(cursor="hand2")
                elif 837 >= event.x >= 710 and 275 >= y >= 160:
                    self.canvas.config(cursor="hand2")

                else:
                    self.canvas.config(cursor="")

            if Theme == 1:
                if not Persian_language:
                    room = Label(self.root, text='room 1', relief="raised")
                    room.place(x=10, y=10)
                    position = Label(self.root, text="your position:30%", bg='black', fg='red', font=("arial", 20),
                                     width=72,
                                     highlightthickness=0.75, highlightcolor='white')
                    position.place(x=10, y=700)
                    items = Label(self.root,
                                  text="score 10 \nin colorgame \n\n\n\n\n\n\n\n answer the riddles\n with one word \n\n\n\n\n\n\n\n do the chess puzzle",
                                  height=20, width=22, relief="flat", fg="red", bg="black", anchor="n",
                                  font=("roman", 20))
                    items.place(x=1200, y=50)

                    option = Button(self.root, text='Option', bg='black', fg='red', font=('Roman', 11, 'bold'),
                                    height=2, width=6, justify='center', command=self.option_page, relief='flat')
                    option.place(x=1480, y=0)
                    option.bind('<Enter>', lambda e: option.config(bg='red', fg='black'))
                    option.bind('<Leave>', lambda e: option.config(bg='black', fg='red'))

                    self.timer = Label(self.root, bg="black", fg='red', text="", font=("nothing", 20, 'bold'),
                                       relief="raised")
                    self.timer.place(x=550, y=750)
                    self.canvas = Canvas(self.root, width=1180, height=680, bg="white")
                    self.canvas.place(x=0, y=10)
                    image = Image.open("Pictures/image1.jpg")
                    image = image.resize((1180, 680))
                    photo = ImageTk.PhotoImage(image)

                    self.image = self.canvas.create_image(0, 0, anchor=NW, image=photo, tag="gg")
                    self.canvas.bind("<Button-1>", on_click)
                    self.canvas.bind("<Motion>", on_motion)
                    next_room = Button(self.root, text='Next\nroom', bg='black', fg='red', font=('Roman', 11, 'bold'),
                                       height=2, width=6, justify='center', command=self.check_next_room, relief="flat")
                    next_room.place(x=1480, y=60)
                    next_room.bind('<Enter>', lambda e: next_room.config(bg='red', fg='black'))
                    next_room.bind('<Leave>', lambda e: next_room.config(bg='black', fg='red'))
                    self.story_voice = Button(self.root, text="voice of\nstory", bg="black", fg='red',
                                              font=('Roman', 11, 'bold'), height=2, width=6, justify='center',
                                              relief="flat",
                                              command=self.story)
                    self.story_voice.place(x=1480, y=120)
                    self.story_voice.bind('<Enter>', lambda e: self.story_voice.config(bg='red', fg='black'))
                    self.story_voice.bind('<Leave>', lambda e: self.story_voice.config(bg='black', fg='red'))
                    self.timer_label()
                else:
                    # room = Label(self.root, text='1 اتاق', font=('Mj_Kaman', 15), bg="red", width=165, height=45,
                    #              relief="raised")
                    # room.place(x=10, y=10)
                    position = Label(self.root, text="30%:موقعیت شما", bg='black', fg='red', font=("Mj_Kaman", 20),
                                     width=62,
                                     highlightthickness=0.75, highlightcolor='white')
                    position.place(x=10, y=700)
                    # health = Label(self.root, text="%100", border=10, width=38, bg="green")
                    # health.place(x=1200, y=0)

                    items = Label(self.root,
                                  text="ده امتیاز در بازی\nرنگ ها بدست بیاور\n\n\n\n\n\n\n\nپازل شطرنج را حل کن\n\n\n\n\n\n\n\nجواب معما هارو \n در یک کلمه بده ",
                                  height=20, width=22, relief="flat", fg="red", bg="black", anchor="n",
                                  font=("Mj_Kaman", 15))
                    items.place(x=1200, y=50)

                    option = Button(self.root, text='تنظیمات', bg='black', fg='red', font=('Mj_kaman', 11, 'bold'),
                                    height=2, width=6, anchor='center', cursor='hand2', command=self.option_page,
                                    relief='flat')
                    option.place(x=1465, y=0)
                    option.bind("<Enter>", lambda e: option.config(bg='red', fg="black"))
                    option.bind("<Leave>", lambda e: option.config(bg='black', fg="red"))

                    self.timer = Label(self.root, bg="black", fg='red', text="", font=("nothing", 20), relief="raised")
                    self.timer.place(x=550, y=750)
                    self.canvas = Canvas(self.root, width=1180, height=680, bg="white")
                    self.canvas.place(x=0, y=10)
                    image = Image.open("Pictures/image1.jpg")
                    image = image.resize((1180, 680))
                    photo = ImageTk.PhotoImage(image)

                    self.canvas.create_image(0, 0, anchor=NW, image=photo)
                    self.canvas.bind("<Button-1>", on_click)
                    self.canvas.bind("<Motion>", on_motion)
                    next_room = Button(self.root, text='اتاق\nبعدی', bg='black', fg='red',
                                       font=('Mj_kaman', 11, 'bold'), cursor='hand2',
                                       height=2, width=6, relief='flat', justify='center', command=self.check_next_room)
                    next_room.place(x=1465, y=80)
                    next_room.bind("<Enter>", lambda e: next_room.config(bg='red', fg="black"))
                    next_room.bind("<Leave>", lambda e: next_room.config(bg='black', fg="red"))

                    self.story_voice = Button(self.root, text="صوت\n داستان", bg="black", fg='red',
                                              font=('Mj_Kaman', 11, 'bold'), relief='flat', cursor='hand2', height=2,
                                              width=6, justify='center',
                                              command=self.story)
                    self.story_voice.place(x=1465, y=160)
                    self.story_voice.bind("<Enter>", lambda e: self.story_voice.config(bg='red', fg="black"))
                    self.story_voice.bind("<Leave>", lambda e: self.story_voice.config(bg='black', fg="red"))

                    self.timer_label()
            else:
                if not Persian_language:
                    room = Label(self.root, text='room 1', bg="red", width=165, height=45, relief="raised")
                    room.place(x=10, y=10)
                    position = Label(self.root, text="your position:30%", bg='black', fg='lightblue',
                                     font=("arial", 20),
                                     width=72, highlightthickness=0.75, highlightcolor='white')
                    position.place(x=10, y=700)
                    health = Label(self.root, text="%100", border=10, width=38, bg="green")
                    health.place(x=1200, y=0)

                    items = Label(self.root,
                                  text="score 10 in\n colorgame \n\n\n\n\n\n\n\n answer the riddles\n with one word \n\n\n\n\n\n\n\n do the chess puzzle",
                                  height=20, width=22, relief="raised", fg="lightblue", bg="black", anchor="n",
                                  font=("roman", 20))
                    items.place(x=1200, y=50)
                    self.timer = Label(self.root, bg="black", fg='lightblue', text="", font=("nothing", 20),
                                       relief="raised")

                    option = Button(self.root, text='option', bg='lightblue', fg='black', font=('Roman', 11, 'bold'),
                                    height=2, width=6, anchor='center', command=self.option_page)
                    option.place(x=1490, y=0)

                    self.timer.place(x=550, y=750)
                    self.canvas = Canvas(self.root, width=1180, height=680, bg="white")
                    self.canvas.place(x=0, y=10)
                    image = Image.open("Pictures/image1.jpg")
                    image = image.resize((1180, 680))
                    photo = ImageTk.PhotoImage(image)

                    self.canvas.create_image(0, 0, anchor=NW, image=photo)
                    self.canvas.bind("<Button-1>", on_click)
                    self.canvas.bind("<Motion>", on_motion)
                    next_room = Button(self.root, text='Next\nroom', bg='light blue', fg='black',
                                       font=('Roman', 11, 'bold'),
                                       height=2, width=6, justify='center', command=self.check_next_room)

                    next_room.place(x=1490, y=47)
                    self.story_voice = Button(self.root, text="voice of\n story", bg="lightblue", fg='black',
                                              font=('Roman', 11, 'bold'), height=2, width=6, justify='center',
                                              command=self.story)
                    self.story_voice.place(x=1490, y=94)
                    self.timer_label()
                else:
                    # room = Label(self.root, text='1 اتاق', bg="red", width=165, height=45, relief="raised")
                    # room.place(x=10, y=10)
                    position = Label(self.root, text="30%:موقعیت شما", bg='black', fg='lightblue',
                                     font=("Mj_Kaman", 20),
                                     width=62,
                                     highlightthickness=0.75, highlightcolor='white')
                    position.place(x=10, y=700)
                    # health = Label(self.root, text="%100", border=10, width=38, bg="green")
                    # health.place(x=1200, y=0)

                    items = Label(self.root,
                                  text="ده امتیاز در بازی\nرنگ ها بدست بیاور\n\n\n\n\n\n\n\nپازل شطرنج را حل کن\n\n\n\n\n\n\n\nجواب معما هارو \n در یک کلمه بده ",
                                  height=20, width=22, relief="flat", fg="lightblue", bg="black", anchor="n",
                                  font=("Mj_Kaman", 15))
                    items.place(x=1200, y=50)

                    option = Button(self.root, text='تنظیمات', bg='black', fg='lightblue',
                                    font=('Mj_kaman', 11, 'bold'),
                                    height=2, width=6, anchor='center', cursor='hand2', command=self.option_page,
                                    relief='flat')
                    option.place(x=1465, y=0)
                    option.bind("<Enter>", lambda e: option.config(bg='lightblue', fg="black"))
                    option.bind("<Leave>", lambda e: option.config(bg='black', fg="lightblue"))

                    self.timer = Label(self.root, bg="black", fg='lightblue', text="", font=("nothing", 20),
                                       relief="raised")
                    self.timer.place(x=550, y=750)
                    self.canvas = Canvas(self.root, width=1180, height=680, bg="white")
                    self.canvas.place(x=0, y=10)
                    image = Image.open("Pictures/image1.jpg")
                    image = image.resize((1180, 680))
                    photo = ImageTk.PhotoImage(image)

                    self.canvas.create_image(0, 0, anchor=NW, image=photo)
                    self.canvas.bind("<Button-1>", on_click)
                    self.canvas.bind("<Motion>", on_motion)
                    next_room = Button(self.root, text='اتاق\nبعدی', bg='black', fg='lightblue',
                                       font=('Mj_kaman', 11, 'bold'), cursor='hand2',
                                       height=2, width=6, relief='flat', justify='center', command=self.check_next_room)
                    next_room.place(x=1465, y=80)
                    next_room.bind("<Enter>", lambda e: next_room.config(bg='lightblue', fg="black"))
                    next_room.bind("<Leave>", lambda e: next_room.config(bg='black', fg="lightblue"))

                    self.story_voice = Button(self.root, text="صوت\n داستان", bg="black", fg='lightblue',
                                              font=('Mj_Kaman', 11, 'bold'), relief='flat', cursor='hand2', height=2,
                                              width=6, justify='center',
                                              command=self.story)
                    self.story_voice.place(x=1465, y=160)
                    self.story_voice.bind("<Enter>", lambda e: self.story_voice.config(bg='lightblue', fg="black"))
                    self.story_voice.bind("<Leave>", lambda e: self.story_voice.config(bg='black', fg="lightblue"))

                    self.timer_label()

        def chess_game(self):
            from tkinter import messagebox

            new_window = Toplevel(self.root)
            new_window.config(height=528, width=525, bg="#FDF6DA")
            new_window.resizable(False, False)
            image_1 = Image.open("Pictures/Screenshot (21).png")
            image_1 = image_1.resize((525, 528))
            photo_1 = ImageTk.PhotoImage(image_1)

            image_2 = Image.open("Pictures/Screenshot (17).png")
            image_2 = image_2.resize((525, 528))
            photo_2 = ImageTk.PhotoImage(image_2)

            image_3 = Image.open("Pictures/Screenshot (18).png")
            image_3 = image_3.resize((525, 528))
            photo_3 = ImageTk.PhotoImage(image_3)

            image_4 = Image.open("Pictures/Screenshot (19).png")
            image_4 = image_4.resize((525, 528))
            photo_4 = ImageTk.PhotoImage(image_4)

            image_5 = Image.open("Pictures/Screenshot (20).png")
            image_5 = image_5.resize((525, 528))
            photo_5 = ImageTk.PhotoImage(image_5)

            move = 1
            time = 0

            def start():
                board.config(image=photo_1)
                sub.destroy()

            def next_board(event):
                global move, chess, ckh

                x, y = event.x, event.y

                if 396 > x > 330 and 267 < y < 333 and ckh == 0:
                    ckh = 1
                elif 396 < x < 461 and 135 < y < 201 and ckh == 1:
                    board.config(image=photo_2)
                elif 396 < x < 461 and 135 < y < 201 and ckh == 1:
                    ckh = 2
                elif 395 > x > 330 and 3 < y < 68:
                    board.config(image=photo_3)
                elif 201 < x < 265 and 399 < y < 464:
                    ckh = 3
                elif 462 < x < 526 and 137 < y < 201 and ckh == 3:
                    board.config(image=photo_4)
                elif 332 < x < 397 and 71 < y < 137:
                    ckh = 4
                elif 464 < x < 527 and 71 < y < 135:
                    board.config(image=photo_5)

                else:
                    messagebox.showerror(
                        title="wrong move",
                        message="your move is not True try more!"

                    )
                    new_window.destroy()

            board = Label(new_window, image=photo_1)
            board.place(x=0, y=0)
            new_window.bind("<Button-1>", next_board)
            # start = Entry(new_window, bg="#75AB3F", font=("roman", 25))
            # start.place(x=605, y=30)

            # label = Label(new_window, text="TO", font=("roman", 20), bg="#666666", relief="raised", width=6)
            # label.place(x=730, y=150)

            # end = Entry(new_window, bg="#75AB3F", font=("roman", 25))
            # end.place(x=605, y=270)

            sub = Button(new_window, text="start", bg="#FFFFCC", font=("Roman", 20), width=6, command=start)

        def color_game(self):
            root = Toplevel(self.root)
            root.config(width=400, height=500, bg="black")
            root.resizable(False, False)

            def time():
                global count__, started
                start.config(state=DISABLED)
                sabt.config(state=NORMAL)
                started = True
                root.after(1000, time)
                count__ -= 1
                second = count__ % 60
                minute = count__ // 60
                time_table.config(text=f"{minute}:{second}")
                if time_table.cget("text") == "0:0":
                    started = False
                    count__ = 40
                    root.destroy()
                    root2 = Tk()
                    label = Label(root2, text="game over", bg="black", fg="red", font=("roman", 20))
                    label.pack()
                    root2.mainloop()

            nothing = StringVar()

            def check():
                global count2, started, color
                label_bg = str(label.cget("fg"))
                if answer.get() == label_bg and started == True:
                    count2 += 1
                    score.config(text=f"score:{count2}")
                    label.config(fg=random.choice(colors), text=random.choice(colors))
                    nothing.set("")
                if count2 == 10:
                    color = True
                    print(6)
                    root.destroy()
                    root2 = Tk()
                    label2 = Label(root2, text="you won!", bg="black", fg="red", font=("roman", 20))
                    label2.pack()
                    root2.mainloop()

            colors = ["purple", "red", "blue", "yellow", "white", "orange"]
            label = Label(root, text=f"{random.choice(colors)}", fg=f"{random.choice(colors)}", font=("roman", 25),
                          justify="center", bg="black", relief="groove")
            label.place(x=163, y=50)

            answer = Entry(root, textvariable=nothing, font=("Arial", 15), )
            answer.place(x=65, y=230)

            sabt = Button(root, text="enter", bg="#FFC400", state=DISABLED, command=check)
            sabt.place(x=300, y=230)
            root.bind("<Return>", lambda event: check())
            time_table = Label(root, text="", bg="red")
            time_table.place(x=200, y=300)

            score = Label(root, text="score:0", font=("roman", 20), fg="red", relief="groove", bg="black")
            score.place(x=163, y=0)

            start = Button(root, text="start", font=("roman", 10), command=time)
            start.place(x=0, y=0)
            root.mainloop()

        def riddle_game(self):
            root = Tk()
            root.config(width=510, height=400)
            root.resizable(False, False)

            def check_a_1():
                global riddle1
                if answer_of_first_riddle.get() == "match":
                    riddle1 = True
                    print(1)

            def check_a_2():
                global riddle2
                if answer_of_second_riddle.get() == "hiccup" or "hiccough":
                    riddle2 = True
                    print(2)

            def check_a_3():
                global riddle3
                if answer_of_third_riddle.get() == "breath":
                    riddle3 = True
                    print(3)

            title_first_riddle = Label(root, text="first riddle", bg="gray", font=("roman", 15), width=56)
            title_first_riddle.place(x=0, y=0)
            first_riddle = Label(root,
                                 text="In a dark room, there is a candle, a heater, and a lantern.\nYou only have one match.\n Which one do you light first?",
                                 justify="center", font=("roman", 15), bg="black", fg="orange")
            first_riddle.place(x=0, y=29)

            label_answer_of_first_riddle = Label(root, text='answer:', bg="orange", font=("roman", 15))
            label_answer_of_first_riddle.place(x=0, y=104)

            answer_of_first_riddle = Entry(root, font=("roman", 15), width=36)
            answer_of_first_riddle.place(x=67, y=104)

            submit_answer_of_first_riddle = Button(root, text='submit', font=("roman", 10), bg='gray', width=11,
                                                   command=check_a_1)
            submit_answer_of_first_riddle.place(x=432, y=104)

            title_second_riddle = Label(root, text="second riddle", bg="gray", font=("roman", 15), width=56)
            title_second_riddle.place(x=0, y=133)
            second_riddle = Label(root,
                                  text="John enters a bar and asks for a glass of water.\n The bartender suddenly shoots the ceiling with a gun. \nJohn says thank you and leaves. \nWhy did John want water?",
                                  justify="center", font=("roman", 15), bg="black", fg="orange", width=56)
            second_riddle.place(x=0, y=162)

            label_answer_of_second_riddle = Label(root, text='answer:', bg="orange", font=("roman", 15))
            label_answer_of_second_riddle.place(x=0, y=261)

            answer_of_second_riddle = Entry(root, font=("roman", 15), width=36)
            answer_of_second_riddle.place(x=67, y=261)

            submit_answer_of_second_riddle = Button(root, text='submit', font=("roman", 10), bg='gray', width=11,
                                                    command=check_a_2)
            submit_answer_of_second_riddle.place(x=433, y=261)

            title_second_riddle = Label(root, text="third riddle", bg="gray", font=("roman", 15), width=56)
            title_second_riddle.place(x=0, y=290)
            third_riddle = Label(root,
                                 text="I'm light as a feather, yet the strongest \nperson can't hold me for long. What am I?",
                                 justify="center", font=("roman", 15), bg="black", fg="orange", width=56)
            third_riddle.place(x=0, y=319)

            label_answer_of_third_riddle = Label(root, text='answer:', bg="orange", font=("roman", 15))
            label_answer_of_third_riddle.place(x=0, y=371)

            answer_of_third_riddle = Entry(root, font=("roman", 15), width=36)
            answer_of_third_riddle.place(x=67, y=371)

            submit_answer_of_third_riddle = Button(root, text='submit', font=("roman", 10), bg='gray', width=11,
                                                   command=check_a_3)
            submit_answer_of_third_riddle.place(x=433, y=371)

            root.mainloop()

        def check_next_room(self):
            global riddle3, riddle1, riddle2, chess, color, global_total_seconds
            if riddle2 == True and riddle3 == True and riddle1 == True and chess == True and color == True:
                self.root.destroy()
                self.root.quit()
                global_total_seconds = 600
                Level2()

        def option_page(self):
            global timer_stop
            timer_stop = True
            option_root = Tk()
            option_root.config(bg='black')
            option_root.attributes('-fullscreen', True)

            pygame.mixer.music.stop()

            def start_timer():
                option_root.destroy()

                global timer_stop
                timer_stop = False
                pygame.mixer.music.play()
                self.update_timer(global_total_seconds)

            def quit_option():
                option_root.destroy()
                quit_game()

            def quit_game():
                return_to_menu()

            def return_to_menu():
                self.root.destroy()
                os.system("python main.py")

            if Theme == 1:
                if not Persian_language:
                    Button(option_root, text='Back To Game', command=start_timer, bg='black', fg='red',
                           font=('Roman', 20, 'bold')).place(x=180, y=300)
                else:
                    Button(option_root, text='بازی به برگشت', command=start_timer, bg='black', fg='red',
                           font=('Roman', 20, 'bold')).place(x=180, y=300)
            else:
                if not Persian_language:
                    Button(option_root, text='Back To Game', command=start_timer, bg='black', fg='lightblue',
                           font=('Roman', 20, 'bold')).place(x=180, y=300)

                else:
                    Button(option_root, text='بازی به برگشت', command=start_timer, bg='black', fg='lightblue',
                           font=('Roman', 20, 'bold')).place(x=180, y=300)

            if Theme == 1:
                if not Persian_language:
                    Button(option_root, text='Save And Quit', command=quit_option, bg='black', fg='red',
                           font=('Roman', 20, 'bold')).place(x=180, y=500)
                else:
                    Button(option_root, text='بازی از خروج و ذخیره', command=quit_option, bg='black', fg='red',
                           font=('Roman', 20, 'bold')).place(x=180, y=500)
            else:
                if not Persian_language:
                    Button(option_root, text='Save And Quit', command=quit_option, bg='black', fg='lightblue',
                           font=('Roman', 20, 'bold')).place(x=180, y=500)

                else:
                    Button(option_root, text='بازی از خروج و ذخیره', command=quit_option, bg='black', fg='lightblue',
                           font=('Roman', 20, 'bold')).place(x=180, y=500)

            if Theme == 1:
                if not Persian_language:
                    Label(option_root, text='GAME PAUSED', font=('Roman', 20, 'bold'), bg='black', fg='red').pack()
                else:
                    Label(option_root, text='شده متوقفق بازی', font=('Roman', 20, 'bold'), bg='black', fg='red').pack()
            else:
                if not Persian_language:
                    Label(option_root, text='GAME PAUSED', font=('Roman', 20, 'bold'), bg='black',
                          fg='lightblue').pack()
                else:
                    Label(option_root, text='شده متوقف بازی', font=('Roman', 20, 'bold'), bg='black', fg='red').pack()

            option_root.mainloop()

        def gameover(self):
            pygame.mixer.music.stop()
            self.root.destroy()
            self.jumpscare()

        def jumpscare(self):
            global Persian_language

            root = Tk()
            root.title('GAME OVER')
            root.attributes('-fullscreen', True)
            root.config(bg='black')

            def return_to_menu():
                root.destroy()
                os.system("python main.py")

            if Theme == 1:
                if not Persian_language:
                    Label(root, text='Game Over', font=('Roman', 70, 'bold'), bg='black', fg='red').place(x=550, y=360)
                else:
                    Label(root, text='شد تمام بازی', font=('Roman', 70, 'bold'), bg='black', fg='red').place(x=550,
                                                                                                             y=360)
            else:
                if not Persian_language:
                    Label(root, text='Game Over', font=('Roman', 70, 'bold'), bg='black', fg='lightblue').place(x=550,
                                                                                                                y=360)
                else:
                    Label(root, text='شد تمام بازی', font=('Roman', 70, 'bold'), bg='black', fg='lightblue').place(
                        x=550,
                        y=360)

            root.after(5000, return_to_menu)

        def timer_label(self):
            global lives
            if lives == 3:
                self.update_timer(300)
            elif lives == 4:
                self.update_timer(600)
            elif lives == 5:
                self.update_timer(900)

        def update_timer(self, total_seconds):
            global lives, mode, timer_stop, global_total_seconds

            if not timer_stop:
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                global_total_seconds = total_seconds
                self.timer.config(text=f"{minutes}:{seconds}")

                if total_seconds > 0:
                    self.root.after(1000, lambda: self.update_timer(total_seconds - 1))
                else:
                    self.gameover()

                self.root.mainloop()

        def story(self):
            global Persian_language
            if self.story_voice.cget("text") == "صوت\n داستان" or self.story_voice.cget("text") == "voice of\n story":
                pygame.mixer.music.load('SoundEffects/room1.wav')
                pygame.mixer.music.play()
                if not Persian_language:
                    self.story_voice.config(text="play\nmusic")
                else:
                    self.story_voice.config(text="پخش\nموسیقی")
            elif self.story_voice.cget("text") == "play\nmusic" or "موسیقی\nپخش":
                if not Persian_language:
                    self.story_voice.config(text="voice of\n story")
                else:
                    self.story_voice.config(text="صوت\n داستان")

                pygame.mixer.music.load('SoundEffects/Enter Hallownest.mp3')
                pygame.mixer.music.play()

    # level 2 page

    class Level2:
        # Defining root and widgets

        def __init__(self):
            self.level2 = Tk()
            self.level2.title('Level 1')
            self.level2.attributes('-fullscreen', True)
            self.level2.config(bg='black')
            pygame.mixer.music.load('SoundEffects/Hans-Zimmer-Day-One (1).mp3')
            pygame.mixer.music.play()
            with open(save_file, 'r') as file:
                lines = file.readlines()

            lines[0] = 'Level2'

            with open(save_file, 'w') as file:
                file.writelines(lines)

            def on_motion(event):
                x, y = event.x, event.y
                if 480 <= event.x <= 714 and 436 <= event.y <= 457:
                    self.canvas.config(cursor="hand2")
                if 825 <= event.x <= 1113 and 422 <= event.y <= 457:
                    self.canvas.config(cursor="hand2")

                if 85 <= event.x <= 367 and 432 <= event.y <= 457:
                    self.canvas.config(cursor="hand2")
                else:
                    self.canvas.config(cursor="")

            def on_click(event):
                print("Clicked at:", event.x, event.y)
                if 480 <= event.x <= 714 and 436 <= event.y <= 457:
                    self.bio_q()

                if 825 <= event.x <= 1113 and 422 <= event.y <= 457:
                    self.math_q()
                if 85 <= event.x <= 367 and 432 <= event.y <= 457:
                    self.chemistry_q()

            if Theme == 1:
                if not Persian_language:
                    position = Label(self.level2, text="your position", bg='black', fg='red', font=("arial", 20),
                                     width=72,
                                     highlightthickness=0.75, highlightcolor='white')
                    position.place(x=10, y=700)
                    items = Label(self.level2,
                                  text="\n\n\n\n\n\n\njust choose \n\n\nthe right answer",
                                  height=20, width=22, relief="flat", fg="red", bg="black", anchor="n",
                                  font=("roman", 22))
                    items.place(x=1200, y=50)
                    option = Button(self.level2, text='Option', bg='black', cursor='hand2', fg='red',
                                    font=('Roman', 11, 'bold'),
                                    height=2, width=6, justify='center', command=self.option_page, relief='flat')
                    option.place(x=1480, y=0)
                    option.bind('<Enter>', lambda e: option.config(bg='red', fg='black'))
                    option.bind('<Leave>', lambda e: option.config(bg='black', fg='red'))

                    self.timer = Label(self.level2, bg="black", fg='red', text="", font=("nothing", 20, 'bold'),
                                       relief="raised")
                    self.timer.place(x=550, y=750)
                    self.canvas = Canvas(self.level2, width=1180, height=680, bg="white")
                    self.canvas.place(x=0, y=10)
                    image = Image.open("Pictures/level2.jpg")
                    image = image.resize((1180, 680))
                    photo = ImageTk.PhotoImage(image)

                    self.canvas.create_image(0, 0, anchor=NW, image=photo)
                    self.canvas.bind("<Button-1>", on_click)
                    self.canvas.bind("<Motion>", on_motion)
                    next_room = Button(self.level2, text='Next\nroom', bg='black', fg='red', font=('Roman', 11, 'bold'),
                                       height=2, width=6, justify='center', command=self.check_next_room, relief="flat",
                                       cursor='hand2')
                    next_room.place(x=1480, y=60)
                    next_room.bind('<Enter>', lambda e: next_room.config(bg='red', fg='black'))
                    next_room.bind('<Leave>', lambda e: next_room.config(bg='black', fg='red'))
                    self.story_voice = Button(self.level2, text="voice of\nstory", bg="black", fg='red',
                                              font=('Roman', 11, 'bold'), height=2, width=6, justify='center',
                                              relief="flat",
                                              command=self.story, cursor='hand2')
                    self.story_voice.place(x=1480, y=120)
                    self.story_voice.bind('<Enter>', lambda e: self.story_voice.config(bg='red', fg='black'))
                    self.story_voice.bind('<Leave>', lambda e: self.story_voice.config(bg='black', fg='red'))
                    self.timer_label()
                else:
                    room = Label(self.level2, text='1 اتاق', bg="red", width=165, height=45, relief="raised")
                    room.place(x=10, y=10)
                    position = Label(self.level2, text="موقعیت شما", bg='black', fg='red', font=("arial", 20), width=72,
                                     highlightthickness=0.75, highlightcolor='white')
                    position.place(x=10, y=700)

                    items = Label(self.level2, text='فقط جواب درست رو انتخاب کن ', height=46, width=40, bg='black',
                                  fg='red', relief="flat", font=('Mj_kaman', 22))
                    items.place(x=1200, y=50)

                    option = Button(self.level2, text='تنظیمات', bg='black', fg='red', font=('Mj_kaman', 11, 'bold'),
                                    height=2, width=6, anchor='center', cursor='hand2', command=self.option_page,
                                    relief='flat')
                    option.place(x=1465, y=0)
                    option.bind("<Enter>", lambda e: option.config(bg='red', fg="black"))
                    option.bind("<Leave>", lambda e: option.config(bg='black', fg="red"))

                    self.timer = Label(self.level2, bg="black", fg='red', text="", font=("nothing", 20),
                                       relief="raised")
                    self.timer.place(x=550, y=750)
                    self.canvas = Canvas(self.level2, width=1180, height=680, bg="white")
                    self.canvas.place(x=0, y=10)
                    image = Image.open("Pictures/level2.jpg")
                    image = image.resize((1180, 680))
                    photo = ImageTk.PhotoImage(image)

                    self.canvas.create_image(0, 0, anchor=NW, image=photo)
                    self.canvas.bind("<Button-1>", on_click)
                    self.canvas.bind("<Motion>", on_motion)
                    next_room = Button(self.level2, text='اتاق\nبعدی', bg='black', fg='red',
                                       font=('Mj_kaman', 11, 'bold'), cursor='hand2',
                                       height=2, width=6, relief='flat', justify='center', command=self.check_next_room)
                    next_room.place(x=1465, y=80)
                    next_room.bind("<Enter>", lambda e: next_room.config(bg='red', fg="black"))
                    next_room.bind("<Leave>", lambda e: next_room.config(bg='black', fg="red"))

                    self.story_voice = Button(self.level2, text="صوت\n داستان", bg="black", fg='red',
                                              font=('Mj_Kaman', 11, 'bold'), relief='flat', cursor='hand2', height=2,
                                              width=6, justify='center',
                                              command=self.story)
                    self.story_voice.place(x=1465, y=160)
                    self.story_voice.bind("<Enter>", lambda e: self.story_voice.config(bg='red', fg="black"))
                    self.story_voice.bind("<Leave>", lambda e: self.story_voice.config(bg='black', fg="red"))

                self.timer_label()
            else:
                if not Persian_language:
                    room = Label(self.level2, text='room 1', bg="red", width=165, height=45, relief="raised")
                    room.place(x=10, y=10)
                    position = Label(self.level2, text="your position", bg='black', fg='lightblue', font=("arial", 20),
                                     width=72, highlightthickness=0.75, highlightcolor='white')
                    position.place(x=10, y=700)
                    health = Label(self.level2, text="%100", border=10, width=38, bg="green")
                    health.place(x=1200, y=0)

                    items = Label(self.level2, height=46, width=40, relief="raised")
                    items.place(x=1200, y=50)
                    self.timer = Label(self.level2, bg="black", fg='lightblue', text="", font=("nothing", 20),
                                       relief="raised")

                    option = Button(self.level2, text='option', bg='lightblue', fg='black', font=('Roman', 11, 'bold'),
                                    height=2, width=6, anchor='center', command=self.option_page)
                    option.place(x=1490, y=0)

                    self.timer.place(x=550, y=750)
                    self.canvas = Canvas(self.level2, width=1180, height=680, bg="white")
                    self.canvas.place(x=0, y=10)
                    image = Image.open("Pictures/level2.jpg")
                    image = image.resize((1180, 680))
                    photo = ImageTk.PhotoImage(image)

                    self.canvas.create_image(0, 0, anchor=NW, image=photo)
                    self.canvas.bind("<Button-1>", on_click)
                    self.canvas.bind("<Motion>", on_motion)
                    next_room = Button(self.level2, text='Next\nroom', bg='light blue', fg='black',
                                       font=('Roman', 11, 'bold'),
                                       height=2, width=6, justify='center', command=self.check_next_room)
                    next_room.place(x=1490, y=47)
                    self.story_voice = Button(self.level2, text="voice of\n story", bg="lightblue", fg='black',
                                              font=('Roman', 11, 'bold'), height=2, width=6, justify='center',
                                              command=self.story)
                    self.story_voice.place(x=1490, y=94)
                    self.timer_label()
                else:
                    room = Label(self.level2, text='1 اتاق', bg="red", width=165, height=45, relief="raised")
                    room.place(x=10, y=10)
                    position = Label(self.level2, text="موقعیت شما", bg='black', fg='lightblue', font=("arial", 20),
                                     width=72, highlightthickness=0.75, highlightcolor='white')
                    position.place(x=10, y=700)
                    health = Label(self.level2, text="%100", border=10, width=38, bg="green")
                    health.place(x=1200, y=0)

                    items = Label(self.level2, height=46, width=40, relief="raised")
                    items.place(x=1200, y=50)

                    option = Button(self.level2, text='تنظیمات', bg='lightblue', fg='black', font=('Roman', 11, 'bold'),
                                    height=2, width=6, anchor='center', command=self.option_page)
                    option.place(x=1490, y=0)

                    self.timer = Label(self.level2, bg="black", fg='lightblue', text="", font=("nothing", 20),
                                       relief="raised")
                    self.timer.place(x=550, y=750)
                    self.canvas = Canvas(self.level2, width=1180, height=680, bg="white")
                    self.canvas.place(x=0, y=10)

                    image = Image.open("Pictures/level2.jpg")
                    image = image.resize((1180, 680))
                    photo = ImageTk.PhotoImage(image)

                    self.canvas.create_image(0, 0, anchor=NW, image=photo)
                    self.canvas.bind("<Button-1>", on_click)
                    self.canvas.bind("<Motion>", on_motion)
                    next_room = Button(self.level2, text='اتاق\nبعدی', bg='lightblue', fg='black',
                                       font=('Roman', 11, 'bold'),
                                       height=2, width=6, justify='center', command=self.check_next_room)
                    next_room.place(x=1490, y=47)
                    self.story_voice = Button(self.level2, text="صوت\n داستان", bg="lightblue", fg='black',
                                              font=('Roman', 11, 'bold'), height=2, width=6, justify='center',
                                              command=self.story)
                    self.story_voice.place(x=1490, y=94)
                    self.timer_label()

        def story(self):
            global Persian_language
            if self.story_voice.cget("text") == "صوت\n داستان" or self.story_voice.cget("text") == "voice of\n story":
                pygame.mixer.music.load('SoundEffects/room2.wav')
                pygame.mixer.music.play()
                if not Persian_language:
                    self.story_voice.config(text="play\nmusic")
                else:
                    self.story_voice.config(text="پخش\nموسیقی")
            elif self.story_voice.cget("text") == "play\nmusic" or "موسیقی\nپخش":
                if not Persian_language:
                    self.story_voice.config(text="voice of\n story")
                else:
                    self.story_voice.config(text="صوت\n داستان")

                pygame.mixer.music.load('SoundEffects/Hans-Zimmer-Day-One (1).mp3')
                pygame.mixer.music.play()

        def math_q(self):
            root = Toplevel(self.level2)
            root.title("")
            root.configure(bg="#ffffff")
            root.attributes("-fullscreen", True)

            def check_Q_1():
                global math_physics1
                selected_value = var_1.get()
                if selected_value == "Option 1":
                    math_physics1 = True
                    print(math_physics1)

            def check_Q_2():
                global math_physics2
                if answer_box.get() == "776/777":
                    math_physics2 = True
                    print(math_physics2)

            def check_Q_3():
                global math_physics3
                if answer_box2.get() == "3":
                    math_physics3 = True
                    print(math_physics3)

            image = Image.open("Pictures/q1.png")
            photo = ImageTk.PhotoImage(image)

            image_2 = Image.open("Pictures/q3.png")
            image_2 = image_2.resize((238, 84))
            photo_2 = ImageTk.PhotoImage(image_2)

            title_label = Label(root, text="برگ امتحانی", font=("IranNastaliq", 43), relief="solid", borderwidth=1,
                                width=35,
                                fg="#158db0", bg="#beeffd")
            title_label.place(x=10, y=10)

            s_1_mf_matn = Label(root,
                                text="درحدود 500 سال قبل____برای توصیف حرکت یک متحرک کمیت____را معرفی کرد",
                                font=("IranNastaliq", 20),
                                bg="white")
            s_1_mf_matn.place(x=1100, y=140)
            var_1 = StringVar(value=" ")

            Q_1_1 = Radiobutton(root, text="گالیله - تندی متوسط", variable=var_1, bg="white",
                                font=("Arial", 15),
                                value="Option 1", command=check_Q_1)
            Q_1_1.place(x=1250, y=260)

            Q_1_2 = Radiobutton(root, text="نیوتون-تندی لحظه ای", variable=var_1, bg="white",
                                font=("Arial", 15),
                                value="Option 2", command=check_Q_1)
            Q_1_2.place(x=1250, y=340)

            Q_1_3 = Radiobutton(root, text="نیوتون-تندی موسط", font=("Arial", 15), bg="white",
                                variable=var_1,
                                value="Option 3", command=check_Q_1)
            Q_1_3.place(x=1250, y=420)

            Q_1_4 = Radiobutton(root, text="گالیله-تندی لحظه ای", font=("Arial", 15), bg="white", variable=var_1,
                                value="Option 4", command=check_Q_1)
            Q_1_4.place(x=1250, y=500)

            s_2_mf_matn = Label(root,
                                text="را بیابید x در عبارت های زیر",
                                font=("IranNastaliq", 29), bg="white")
            s_2_mf_matn.place(x=60, y=130)

            q1 = Label(root, image=photo, bg="white")
            q1.place(x=60, y=230)

            answer = Label(root, text="پاسخ:", bg="lightblue", relief="raised", height=4)  # noqa
            answer.place(x=400, y=249)

            answer_box = Entry(root, font=("Irannastaliq", 23), width=15, bg="#158db0")
            answer_box.place(x=433, y=250)
            submit_anr = Button(root, text="تائید  پاسخ", font=("irannastaliq", 14), bg="lightblue", height=1,
                                command=check_Q_2)
            submit_anr.place(x=752, y=250)
            q2 = Label(root, image=photo_2, bg="white")
            q2.place(x=60, y=470)
            answer2 = Label(root, text="پاسخ:", bg="lightblue", relief="raised", height=4)  # noqa
            answer2.place(x=400, y=489)
            answer_box2 = Entry(root, font=("Irannastaliq", 23), width=15, bg="#158db0")
            answer_box2.place(x=433, y=490)
            submit_anr2 = Button(root, text="تائید  پاسخ", font=("irannastaliq", 14), bg="lightblue", height=1,
                                 command=check_Q_3)
            submit_anr2.place(x=752, y=490)
            submit = Button(root, text="ثبت آزمون", font=("IranNastaliq", 20), bg="#beeffd", fg="#158db0", height=1,
                            command=lambda: root.destroy())
            submit.place(x=740, y=630)
            root.mainloop()

        def bio_q(self):
            root = Toplevel(self.level2)
            root.title("")
            root.configure(bg="#ffffff")
            root.attributes("-fullscreen", True)

            def check_Q_1():
                global biology1
                selected_value = var_1.get()
                if selected_value == "Option 1":
                    biology1 = True
                    print(biology1)

            def check_Q_2():
                global biology2
                selected_value = var_2.get()
                if selected_value == "Option 3":
                    biology2 = True
                    print(biology2)

            def check_Q_3():
                global biology3
                selected_value = var_3.get()
                if selected_value == "Option 3":
                    biology3 = True
                    print(biology3)

            title_label = Label(root, text="برگ امتحانی", font=("IranNastaliq", 43), relief="solid", borderwidth=1,
                                width=35,
                                fg="#158db0", bg="#beeffd")
            title_label.place(x=10, y=10)

            s_1_bio_matn = Label(root, text="نام علمی قمری خانگی کدام است؟", font=("IranNastaliq", 29),
                                 bg="white")
            s_1_bio_matn.place(x=1250, y=140)
            var_1 = StringVar(value=" ")

            Q_1_1 = Radiobutton(root, text="Sterptoelia   sengalensis", variable=var_1, bg="white",
                                font=("Arial", 15),
                                value="Option 1", command=check_Q_1)
            Q_1_1.place(x=1250, y=260)

            Q_1_2 = Radiobutton(root, text="Sterptoelia   Sengalensis", variable=var_1, bg="white",
                                font=("Arial", 15),
                                value="Option 2", command=check_Q_1)
            Q_1_2.place(x=1250, y=340)

            Q_1_3 = Radiobutton(root, text="Streptoeila   sengalensis", font=("Arial", 15), bg="white",
                                variable=var_1,
                                value="Option 3", command=check_Q_1)
            Q_1_3.place(x=1250, y=420)

            Q_1_4 = Radiobutton(root, text="terptoelia   sengalensis", font=("Arial", 15), bg="white", variable=var_1,
                                value="Option 4", command=check_Q_1)
            Q_1_4.place(x=1250, y=500)

            s_2_bio_matn = Label(root,
                                 text="یوکاریوت بودن و پر سلولی بودن و داشتن ویتامین زیاد از ویژگی های جانداری",
                                 font=("IranNastaliq", 29), bg="white")
            s_2_bio_matn.place(x=560, y=140)

            var_2 = StringVar(value=" ")

            Q_2_1 = Radiobutton(root, text="در کنسرو سم تولید میکند", variable=var_2, bg="white", font=("Arial", 15),
                                value="Option 1", command=check_Q_2)
            Q_2_1.place(x=780, y=260)

            Q_2_2 = Radiobutton(root, text="بیماری کویید 19 ایجاد می کند", variable=var_2, bg="white",
                                font=("Arial", 15),
                                value="Option 2", command=check_Q_2)
            Q_2_2.place(x=780, y=340)

            Q_2_3 = Radiobutton(root, text="از آن آگار تهیه می شود", font=("Arial", 15), bg="white", variable=var_2,
                                value="Option 3", command=check_Q_2)
            Q_2_3.place(x=780, y=420)

            Q_2_4 = Radiobutton(root, text="باعث زنگ گندم میشود", font=("Arial", 15), bg="white", variable=var_2,
                                value="Option 4", command=check_Q_2)
            Q_2_4.place(x=780, y=500)

            s_3_bio_matn = Label(root, text="عامل کدام بیماری ساختمان سلولی ندارد؟", font=("IranNastaliq", 29),
                                 bg="white")
            s_3_bio_matn.place(x=60, y=140)

            var_3 = StringVar(value=" ")

            Q_3_1 = Radiobutton(root, text="سل", variable=var_3, bg="white", font=("IranNastaliq", 30),
                                value="Option 1", command=check_Q_3)
            Q_3_1.place(x=210, y=230)

            Q_3_2 = Radiobutton(root, text="دیفتری", variable=var_3, bg="white", font=("IranNastaliq", 30),
                                value="Option 2", command=check_Q_3)
            Q_3_2.place(x=210, y=310)

            Q_3_3 = Radiobutton(root, text="ایدز", font=("IranNastaliq", 30), bg="white", variable=var_3,
                                value="Option 3", command=check_Q_3)
            Q_3_3.place(x=210, y=390)

            Q_3_4 = Radiobutton(root, text="مالاریا", font=("IranNastaliq", 30), bg="white", variable=var_3,
                                value="Option 4", command=check_Q_3)
            Q_3_4.place(x=210, y=470)

            submit = Button(root, text="ثبت آزمون", font=("IranNastaliq", 20), bg="#beeffd", fg="#158db0", height=1,
                            command=lambda: root.destroy())
            submit.place(x=12, y=760)
            root.mainloop()

        def chemistry_q(self):
            root = Toplevel(self.level2)
            root.title("")
            root.configure(bg="#ffffff")
            root.attributes("-fullscreen", True)

            def check_Q_1():
                global chemistry1
                selected_value = var_1.get()
                if selected_value == "Option 2":
                    chemistry1 = True
                    print(7)

            def check_Q_2():
                global chemistry2
                selected_value = var_2.get()
                if selected_value == "Option 4":
                    chemistry2 = True
                    print(8)

            def check_Q_3():
                global chemistry3
                selected_value = var_3.get()
                if selected_value == "Option 3":
                    chemistry3 = True
                    print(9)

            title_label = Label(root, text="برگ امتحانی", font=("IranNastaliq", 43), relief="solid", borderwidth=1,
                                width=35,
                                fg="#158db0", bg="#beeffd")
            title_label.place(x=10, y=10)

            s_1_bio_matn = Label(root,
                                 text="با قرار دادن تیغه ای از فلز ----- در محلول ------ هیچ واکنشی رخ نمی دهد",
                                 font=("IranNastaliq", 29),
                                 bg="white")
            s_1_bio_matn.place(x=1010, y=140)
            var_1 = StringVar(value=" ")

            Q_1_1 = Radiobutton(root, text="آهن -مس سلوفات", variable=var_1, bg="white",
                                font=("Arial", 15),
                                value="Option 1", command=check_Q_1)
            Q_1_1.place(x=1250, y=260)

            Q_1_2 = Radiobutton(root, text="روی - منیزیم سلوفات", variable=var_1, bg="white",
                                font=("Arial", 15),
                                value="Option 2", command=check_Q_1)
            Q_1_2.place(x=1250, y=340)

            Q_1_3 = Radiobutton(root, text="منیزیم -روی سولفات", font=("Arial", 15), bg="white",
                                variable=var_1,
                                value="Option 3", command=check_Q_1)
            Q_1_3.place(x=1250, y=420)

            Q_1_4 = Radiobutton(root, text="منیزیم-آهننسلوفات", font=("Arial", 15), bg="white", variable=var_1,
                                value="Option 4", command=check_Q_1)
            Q_1_4.place(x=1250, y=500)

            s_2_bio_matn = Label(root,
                                 text="نشانه شیمیایی کدام یون به درستی نشان داده شده است ؟",
                                 font=("IranNastaliq", 29), bg="white")
            s_2_bio_matn.place(x=560, y=140)

            var_2 = StringVar(value=" ")

            Q_2_1 = Radiobutton(root, text="+ Na", variable=var_2, bg="white", font=("Arial", 15),
                                value="Option 1", command=check_Q_2)
            Q_2_1.place(x=750, y=260)

            Q_2_2 = Radiobutton(root, text="Mg +2", variable=var_2, bg="white",
                                font=("Arial", 15),
                                value="Option 2", command=check_Q_2)
            Q_2_2.place(x=750, y=340)

            Q_2_3 = Radiobutton(root, text="2+ Fe", font=("Arial", 15), bg="white", variable=var_2,
                                value="Option 3", command=check_Q_2)
            Q_2_3.place(x=750, y=420)

            Q_2_4 = Radiobutton(root, text="O 2-", font=("Arial", 15), bg="white", variable=var_2,
                                value="Option 4", command=check_Q_2)
            Q_2_4.place(x=750, y=500)

            s_3_bio_matn = Label(root, text="نفطه جوش کدام یک از هیدروکربن های زیر از سایرین بالاتر است؟",
                                 font=("IranNastaliq", 29),
                                 bg="white")
            s_3_bio_matn.place(x=60, y=140)

            var_3 = StringVar(value=" ")
            # C4h10   c2h6   c8h18   ch4
            Q_3_1 = Radiobutton(root, text="بوتان", variable=var_3, bg="white", font=("IranNastaliq", 30),
                                value="Option 1", command=check_Q_3)
            Q_3_1.place(x=220, y=230)

            Q_3_2 = Radiobutton(root, text="اتان", variable=var_3, bg="white", font=("IranNastaliq", 30),
                                value="Option 2", command=check_Q_3)
            Q_3_2.place(x=220, y=310)

            Q_3_3 = Radiobutton(root, text="اکتان", font=("IranNastaliq", 30), bg="white", variable=var_3,
                                value="Option 3", command=check_Q_3)
            Q_3_3.place(x=220, y=390)

            Q_3_4 = Radiobutton(root, text="متان", font=("IranNastaliq", 30), bg="white", variable=var_3,
                                value="Option 4", command=check_Q_3)
            Q_3_4.place(x=220, y=470)

            submit = Button(root, text="ثبت آزمون", font=("IranNastaliq", 20), bg="#beeffd", fg="#158db0", height=1,
                            command=lambda: root.destroy())
            submit.place(x=12, y=760)
            root.mainloop()

        def check_next_room(self):
            global chemistry3, chemistry2, chemistry1, biology, biology2, biology3, math_physics3, math_physics2, math_physics1
            if chemistry3 == True and chemistry2 == True and chemistry1 == True and biology3 == True and biology2 == True and biology1 == True and math_physics1 == True and math_physics2 == True and math_physics3 == True:
                self.level2.destroy()
                Level3()

        def option_page(self):
            global timer_stop
            timer_stop = True
            option_root = Tk()
            option_root.config(bg='black')
            option_root.attributes('-fullscreen', True)

            pygame.mixer.music.stop()

            def start_timer():
                option_root.destroy()

                global timer_stop
                timer_stop = False
                pygame.mixer.music.play()
                self.update_timer(global_total_seconds)

            def quit_option():
                option_root.destroy()
                quit_game()

            def quit_game():
                return_to_menu()

            def return_to_menu():
                global timer_stop
                timer_stop = True
                self.level2.destroy()
                os.system("python main.py")

            if Theme == 1:
                if not Persian_language:
                    Button(option_root, text='Back To Game', command=start_timer, bg='black', fg='red',
                           font=('Roman', 20, 'bold')).place(x=180, y=300)
                else:
                    Button(option_root, text='بازی به برگشت', command=start_timer, bg='black', fg='red',
                           font=('Roman', 20, 'bold')).place(x=180, y=300)
            else:
                if not Persian_language:
                    Button(option_root, text='Back To Game', command=start_timer, bg='black', fg='lightblue',
                           font=('Roman', 20, 'bold')).place(x=180, y=300)

                else:
                    Button(option_root, text='بازی به برگشت', command=start_timer, bg='black', fg='lightblue',
                           font=('Roman', 20, 'bold')).place(x=180, y=300)

            if Theme == 1:
                if not Persian_language:
                    Button(option_root, text='Save And Quit', command=quit_option, bg='black', fg='red',
                           font=('Roman', 20, 'bold')).place(x=180, y=500)
                else:
                    Button(option_root, text='بازی از خروج و ذخیره', command=quit_option, bg='black', fg='red',
                           font=('Roman', 20, 'bold')).place(x=180, y=500)
            else:
                if not Persian_language:
                    Button(option_root, text='Save And Quit', command=quit_option, bg='black', fg='lightblue',
                           font=('Roman', 20, 'bold')).place(x=180, y=500)

                else:
                    Button(option_root, text='بازی از خروج و ذخیره', command=quit_option, bg='black', fg='lightblue',
                           font=('Roman', 20, 'bold')).place(x=180, y=500)

            if Theme == 1:
                if not Persian_language:
                    Label(option_root, text='GAME PAUSED', font=('Roman', 20, 'bold'), bg='black', fg='red').pack()
                else:
                    Label(option_root, text='شده متوقفق بازی', font=('Roman', 20, 'bold'), bg='black', fg='red').pack()
            else:
                if not Persian_language:
                    Label(option_root, text='GAME PAUSED', font=('Roman', 20, 'bold'), bg='black',
                          fg='lightblue').pack()
                else:
                    Label(option_root, text='شده متوقف بازی', font=('Roman', 20, 'bold'), bg='black', fg='red').pack()

            option_root.mainloop()

        def gameover(self):
            pygame.mixer.music.stop()
            self.level2.destroy()
            self.jumpscare()

        def jumpscare(self):
            global Persian_language

            root = Tk()
            root.title('GAME OVER')
            root.attributes('-fullscreen', True)
            root.config(bg='black')

            if Theme == 1:
                if not Persian_language:
                    Label(root, text='Game Over', font=('Roman', 70, 'bold'), bg='black', fg='red').place(x=550, y=360)
                else:
                    Label(root, text='شد تمام بازی', font=('Roman', 70, 'bold'), bg='black', fg='red').place(x=550,
                                                                                                             y=360)
            else:
                if not Persian_language:
                    Label(root, text='Game Over', font=('Roman', 70, 'bold'), bg='black', fg='lightblue').place(x=550,
                                                                                                                y=360)
                else:
                    Label(root, text='شد تمام بازی', font=('Roman', 70, 'bold'), bg='black', fg='lightblue').place(
                        x=550,
                        y=360)

            root.after(5000, start)

        def timer_label(self):
            global lives, global_total_seconds
            if lives == 3:
                self.update_timer(300)
            elif lives == 4:
                self.update_timer(600)
            elif lives == 5:
                self.update_timer(900)

        def update_timer(self, total_seconds):
            global lives, mode, timer_stop, global_total_seconds

            if not timer_stop:
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                global_total_seconds = total_seconds
                self.timer.config(text=f"{minutes}:{seconds}")

                if total_seconds > 0:
                    self.level2.after(1000, lambda: self.update_timer(total_seconds - 1))
                else:
                    self.gameover()

                self.level2.mainloop()

    # level 3 page

    class Level3:
        # Defining root and widgets

        def __init__(self):
            self.level3 = Tk()
            self.level3.title('Level 1')
            self.level3.attributes('-fullscreen', True)
            self.level3.config(bg='black')
            pygame.mixer.music.load('SoundEffects/music4.mp3')
            pygame.mixer.music.play()
            with open(save_file, 'r') as file:
                lines = file.readlines()

            lines[0] = 'Level3'

            with open(save_file, 'w') as file:
                file.writelines(lines)

            def on_click(event):
                print("Clicked at:", event.x, event.y)
                if 53 <= event.x <= 214 and 263 <= event.y <= 377:
                    self.math_game()

                if 422 <= event.x <= 735 and 204 <= event.y <= 480:
                    self.maze_game()
                if 774 <= event.x <= 1148 and 227 <= event.y <= 640:
                    self.snake_game()

            if Theme == 1:
                if not Persian_language:
                    room = Label(self.level3, text='room 1', relief="raised")
                    room.place(x=10, y=10)
                    position = Label(self.level3, text="your position:90%", bg='black', fg='red', font=("arial", 20),
                                     width=72,
                                     highlightthickness=0.75, highlightcolor='white')
                    position.place(x=10, y=700)
                    health = Label(self.level3, text="%100", border=10, width=38, bg="green")
                    health.place(x=1200, y=0)
                    option = Button(self.level3, text='Option', bg='red', fg='black', font=('Roman', 11, 'bold'),
                                    height=2, width=6, justify='center', command=self.option_page)
                    option.place(x=1490, y=0)
                    items = Label(self.level3,
                                  text="score 10 in mathgame \n\n\n\n\n\n\n\n score 70 in snake \n\n\n\n\n\n\n\n reach to red \nsquare in maze",
                                  height=20, width=22, relief="raised", fg="red", bg="black", anchor="n",
                                  font=("roman", 20))
                    items.place(x=1200, y=50)

                    self.timer = Label(self.level3, bg="black", fg='red', text="", font=("nothing", 20, 'bold'),
                                       relief="raised")
                    self.timer.place(x=550, y=750)
                    self.canvas = Canvas(self.level3, width=1180, height=680, bg="white")
                    self.canvas.place(x=0, y=10)
                    image = Image.open("Pictures/level3.jpg")
                    image = image.resize((1180, 680))
                    photo = ImageTk.PhotoImage(image)

                    self.canvas.create_image(0, 0, anchor=NW, image=photo)
                    self.canvas.bind("<Button-1>", on_click)
                    next_room = Button(self.level3, text='Next\nroom', bg='red', fg='black', font=('Roman', 11, 'bold'),
                                       height=2, width=6, justify='center', command=self.check_next_room)
                    next_room.place(x=1490, y=47)
                    self.story_voice = Button(self.level3, text='voice of\n story', bg="red", fg='black',
                                              font=('Roman', 11, 'bold'), height=2, width=6, justify='center',
                                              command=self.story)
                    self.story_voice.place(x=1490, y=94)
                    self.timer_label()
                else:
                    room = Label(self.level3, text='3 اتاق', bg="red", width=165, height=45, relief="raised")
                    room.place(x=10, y=10)
                    position = Label(self.level3, text="90%:موقعیت شما", bg='black', fg='red', font=("arial", 20),
                                     width=72,
                                     highlightthickness=0.75, highlightcolor='white')
                    position.place(x=10, y=700)
                    health = Label(self.level3, text="%100", border=10, width=38, bg="green")
                    health.place(x=1200, y=0)

                    items = Label(self.level3,
                                  text="بازی در امتیاز ده\nبیاور بدست ریاضی  \n\n\n\n\n\n\n\nبازی در امتیاز هفتاد  \nبیاور بدست مار\n\n\n\n\n\n\n\nبرس قرمز مربع به ماز در ",
                                  height=20, width=22, relief="raised", fg="red", bg="black", anchor="n",
                                  font=("roman", 20))
                    items.place(x=1200, y=50)

                    option = Button(self.level3, text='تنظیمات', bg='red', fg='black', font=('Roman', 11, 'bold'),
                                    height=2, width=6, anchor='center', command=self.option_page)
                    option.place(x=1490, y=0)

                    self.timer = Label(self.level3, bg="black", fg='red', text="", font=("nothing", 20),
                                       relief="raised")
                    self.timer.place(x=550, y=750)
                    self.canvas = Canvas(self.level3, width=1180, height=680, bg="white")
                    self.canvas.place(x=0, y=10)
                    image = Image.open("Pictures/level3.jpg")
                    image = image.resize((1180, 680))
                    photo = ImageTk.PhotoImage(image)

                    self.canvas.create_image(0, 0, anchor=NW, image=photo)
                    self.canvas.bind("<Button-1>", on_click)
                    next_room = Button(self.level3, text='اتاق\nبعدی', bg='red', fg='black', font=('Roman', 11, 'bold'),
                                       height=2, width=6, justify='center', command=self.check_next_room)
                    next_room.place(x=1490, y=47)
                    self.story_voice = Button(self.level3, text="صوت\n داستان", bg="red", fg='black',
                                              font=('Roman', 11, 'bold'), height=2, width=6, justify='center',
                                              command=self.story)
                    self.story_voice.place(x=1490, y=94)
                    self.timer_label()
            else:
                if not Persian_language:
                    room = Label(self.level3, text='room 1', bg="red", width=165, height=45, relief="raised")
                    room.place(x=10, y=10)
                    position = Label(self.level3, text="your position:90%", bg='black', fg='lightblue',
                                     font=("arial", 20),
                                     width=72, highlightthickness=0.75, highlightcolor='white')
                    position.place(x=10, y=700)
                    health = Label(self.level3, text="%100", border=10, width=38, bg="green")
                    health.place(x=1200, y=0)
                    items = Label(self.level3,
                                  text="score 10 in mathgame \n\n\n\n\n\n\n\n score 70 in snake \n\n\n\n\n\n\n\n reach to red \nsquare in maze",
                                  height=20, width=22, relief="raised", fg="lightblue", bg="black", anchor="n",
                                  font=("roman", 20))
                    items.place(x=1200, y=50)
                    self.timer = Label(self.level3, bg="black", fg='lightblue', text="", font=("nothing", 20),
                                       relief="raised")

                    option = Button(self.level3, text='option', bg='lightblue', fg='black', font=('Roman', 11, 'bold'),
                                    height=2, width=6, anchor='center', command=self.option_page)
                    option.place(x=1490, y=0)

                    self.timer.place(x=550, y=750)
                    self.canvas = Canvas(self.level3, width=1180, height=680, bg="white")
                    self.canvas.place(x=0, y=10)
                    image = Image.open("Pictures/level3.jpg")
                    image = image.resize((1180, 680))
                    photo = ImageTk.PhotoImage(image)

                    self.canvas.create_image(0, 0, anchor=NW, image=photo)
                    self.canvas.bind("<Button-1>", on_click)
                    next_room = Button(self.level3, text='Next\nroom', bg='light blue', fg='black',
                                       font=('Roman', 11, 'bold'),
                                       height=2, width=6, justify='center', command=self.check_next_room)
                    next_room.place(x=1490, y=47)
                    self.story_voice = Button(self.level3, text="voice of\n story", bg="light blue", fg='black',
                                              font=('Roman', 11, 'bold'), height=2, width=6, justify='center',
                                              command=self.story)
                    self.story_voice.place(x=1490, y=94)
                    self.timer_label()
                else:
                    room = Label(self.level3, text='1 اتاق', bg="red", width=165, height=45, relief="raised")
                    room.place(x=10, y=10)
                    position = Label(self.level3, text="موقعیت شما:%90", bg='black', fg='lightblue', font=("arial", 20),
                                     width=72, highlightthickness=0.75, highlightcolor='white')
                    position.place(x=10, y=700)
                    health = Label(self.level3, text="%100", border=10, width=38, bg="green")
                    health.place(x=1200, y=0)
                    items = Label(self.level3,
                                  text="بازی در امتیاز ده\nبیاور بدست ریاضی  \n\n\n\n\n\n\n\nبازی در امتیاز هفتاد  \nبیاور بدست مار\n\n\n\n\n\n\n\nبرس قرمز مربع به ماز در ",
                                  height=20, width=22, relief="raised", fg="lightblue", bg="black", anchor="n",
                                  font=("roman", 20))
                    items.place(x=1200, y=50)

                    option = Button(self.level3, text='تنظیمات', bg='lightblue', fg='black', font=('Roman', 11, 'bold'),
                                    height=2, width=6, anchor='center', command=self.option_page)
                    option.place(x=1490, y=0)

                    self.timer = Label(self.level3, bg="black", fg='lightblue', text="", font=("nothing", 20),
                                       relief="raised")
                    self.timer.place(x=550, y=750)
                    self.canvas = Canvas(self.level3, width=1180, height=680, bg="white")
                    self.canvas.place(x=0, y=10)

                    image = Image.open("Pictures/level3.jpg")
                    image = image.resize((1180, 680))
                    photo = ImageTk.PhotoImage(image)

                    self.canvas.create_image(0, 0, anchor=NW, image=photo)
                    self.canvas.bind("<Button-1>", on_click)
                    next_room = Button(self.level3, text='اتاق\nبعدی', bg='lightblue', fg='black',
                                       font=('Roman', 11, 'bold'),
                                       height=2, width=6, justify='center', command=self.check_next_room)
                    next_room.place(x=1490, y=47)
                    self.story_voice = Button(self.level3, text="صوت\n داستان", bg="lightblue", fg='black',
                                              font=('Roman', 11, 'bold'), height=2, width=6, justify='center',
                                              command=self.story)
                    self.story_voice.place(x=1490, y=94)
                    self.timer_label()

        def story(self):
            global Persian_language
            if self.story_voice.cget("text") == "صوت\n داستان" or self.story_voice.cget(
                    "text") == "voice of\n story":
                pygame.mixer.music.load('SoundEffects/room3.wav')
                pygame.mixer.music.play()
                if not Persian_language:
                    self.story_voice.config(text="play\nmusic")
                else:
                    self.story_voice.config(text="پخش\nموسیقی")
            elif self.story_voice.cget("text") == "play\nmusic" or "موسیقی\nپخش":
                if not Persian_language:
                    self.story_voice.config(text="voice of\n story")
                else:
                    self.story_voice.config(text="صوت\n داستان")

                pygame.mixer.music.load('SoundEffects/music4.mp3')
                pygame.mixer.music.play()

        def check_next_room(self):
            global snake_game, math_game, maze
            if snake_game == True and math_game == True and maze == True:

                self.level3.destroy()

                root = Tk()
                root.attributes('-fullscreen', True)
                root.config(bg="black")
                with open(save_file, 'r') as file:
                    lines = file.readlines()

                lines[0] = 'Level1'

                with open(save_file, 'w') as file:
                    file.writelines(lines)

                def option_page():
                    global timer_stop
                    timer_stop = True
                    option_root = Tk()
                    option_root.config(bg='black')
                    option_root.attributes('-fullscreen', True)

                    pygame.mixer.music.stop()

                    def start_timer():
                        option_root.destroy()

                        global timer_stop
                        timer_stop = False
                        pygame.mixer.music.play()
                        self.update_timer(global_total_seconds)

                    def quit_option():
                        option_root.destroy()
                        quit_game()

                    def quit_game():
                        return_to_menu()

                    def return_to_menu():
                        global timer_stop
                        timer_stop = True
                        root.destroy()
                        os.system("python main.py")

                    if Theme == 1:
                        if not Persian_language:
                            Button(option_root, text='Back To Game', command=start_timer, bg='black', fg='red',
                                   font=('Roman', 20, 'bold')).place(x=180, y=300)
                        else:
                            Button(option_root, text='بازی به برگشت', command=start_timer, bg='black', fg='red',
                                   font=('Roman', 20, 'bold')).place(x=180, y=300)
                    else:
                        if not Persian_language:
                            Button(option_root, text='Back To Game', command=start_timer, bg='black', fg='lightblue',
                                   font=('Roman', 20, 'bold')).place(x=180, y=300)

                        else:
                            Button(option_root, text='بازی به برگشت', command=start_timer, bg='black', fg='lightblue',
                                   font=('Roman', 20, 'bold')).place(x=180, y=300)

                    if Theme == 1:
                        if not Persian_language:
                            Button(option_root, text='Save And Quit', command=quit_option, bg='black', fg='red',
                                   font=('Roman', 20, 'bold')).place(x=180, y=500)
                        else:
                            Button(option_root, text='بازی از خروج و ذخیره', command=quit_option, bg='black', fg='red',
                                   font=('Roman', 20, 'bold')).place(x=180, y=500)
                    else:
                        if not Persian_language:
                            Button(option_root, text='Save And Quit', command=quit_option, bg='black', fg='lightblue',
                                   font=('Roman', 20, 'bold')).place(x=180, y=500)

                        else:
                            Button(option_root, text='بازی از خروج و ذخیره', command=quit_option, bg='black',
                                   fg='lightblue',
                                   font=('Roman', 20, 'bold')).place(x=180, y=500)

                    if Theme == 1:
                        if not Persian_language:
                            Label(option_root, text='GAME PAUSED', font=('Roman', 20, 'bold'), bg='black',
                                  fg='red').pack()
                        else:
                            Label(option_root, text='شده متوقفق بازی', font=('Roman', 20, 'bold'), bg='black',
                                  fg='red').pack()
                    else:
                        if not Persian_language:
                            Label(option_root, text='GAME PAUSED', font=('Roman', 20, 'bold'), bg='black',
                                  fg='lightblue').pack()
                        else:
                            Label(option_root, text='شده متوقف بازی', font=('Roman', 20, 'bold'), bg='black',
                                  fg='red').pack()

                    option_root.mainloop()

                def story():
                    pygame.mixer.music.load('SoundEffects/the end.wav')
                    pygame.mixer.music.play()

                endgame = Button(root, text="you finished this game but...", bg="red", fg="black", font=('roman', 20),
                                 command=story)
                endgame.place(x=600, y=400)
                option = Button(root, text='option', bg='lightblue', fg='black', font=('Roman', 11, 'bold'),
                                height=2, width=6, anchor='center', command=option_page)
                option.place(x=1490, y=0)
                root.mainloop()

        def math_game(self):

            def start_game():
                global score, time_left

                answer_entry.config(state=NORMAL)
                start_button.config(state=DISABLED)
                time_left = 60
                score = 0
                update_score()
                update_timer()
                next_question()

            def next_question():
                global math_game, a, b
                if time_left > 0:
                    a = random.randint(10, 100)
                    b = random.randint(10, 100)
                    question_label.config(text=f"{a} + {b} = ?")
                    answer_entry.delete(0, END)
                if score == 10:
                    math_game = True
                    print("finished")

            def check_answer(event):
                global score, time_left
                answer = answer_entry.get()
                if answer.isdigit():
                    if int(answer) == a + b:
                        score += 1
                        update_score()

                next_question()

            def update_score():
                score_label.config(text=f"score: {score}")

            def update_timer():
                global time_left
                if time_left > 0:
                    time_left -= 1
                    time_label.config(text=f"time: {time_left} second ")
                    root.after(1000, update_timer)
                else:
                    question_label.config(text="game over!")
                    answer_entry.config(state=DISABLED)
                    start_button.config(state=NORMAL)

            root = Toplevel(self.level3)
            root.config(bg="black")

            question_label = Label(root, text="", font=("Arial", 24), bg="black", fg="red")
            question_label.pack()

            answer_entry = Entry(root, font=("roman", 24), bg="red")
            answer_entry.pack()
            answer_entry.bind("<Return>", check_answer)

            score_label = Label(root, text="score:0", font=("roman", 16), fg="red", bg="black", relief="ridge")
            score_label.pack()

            time_label = Label(root, text="time:30 second", font=("roman", 16), fg="red", bg="black", relief="ridge")
            time_label.pack()

            start_button = Button(root, text="start game", command=lambda: start_game(), font=("roman", 16), fg="red",
                                  bg="black",
                                  relief="ridge")
            start_button.pack()

            root.mainloop()

        def maze_game(self):
            WIDTH, HEIGHT = 800, 600
            CELL_SIZE = 40
            maze_map = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
                [1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
                [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
                [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1],
                [1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
                [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2]
            ]

            obstacles = [(4, 3), (5, 5), (6, 10), (8, 8), (10, 2)]
            obstacle_speed = 1
            player_pos = [1, 1]

            def draw_maze(canvas):

                for row in range(len(maze_map)):
                    for col in range(len(maze_map[row])):
                        x0 = col * CELL_SIZE
                        y0 = row * CELL_SIZE
                        x1 = x0 + CELL_SIZE
                        y1 = y0 + CELL_SIZE
                        if maze_map[row][col] == 1:
                            canvas.create_rectangle(x0, y0, x1, y1, fill='black')
                        elif maze_map[row][col] == 2:
                            canvas.create_rectangle(x0, y0, x1, y1, fill='red')

            def draw_player(canvas):

                x0 = player_pos[1] * CELL_SIZE + 5
                y0 = player_pos[0] * CELL_SIZE + 5
                return canvas.create_oval(x0, y0, x0 + (CELL_SIZE - 10), y0 + (CELL_SIZE - 10), fill='green')

            def draw_obstacles(canvas):

                obstacle_rects = []
                for (row, col) in obstacles:
                    x0 = col * CELL_SIZE
                    y0 = row * CELL_SIZE
                    x1 = x0 + CELL_SIZE
                    y1 = y0 + CELL_SIZE
                    rect = canvas.create_rectangle(x0, y0, x1, y1, fill='yellow')
                    obstacle_rects.append((rect, (row, col)))
                return obstacle_rects

            def move_player(event, canvas, player):
                global maze
                direction = {'Left': (0, -1), 'Right': (0, 1), 'Up': (-1, 0), 'Down': (1, 0)}
                move = direction.get(event.keysym)
                if move:
                    new_row = player_pos[0] + move[0]
                    new_col = player_pos[1] + move[1]
                    if maze_map[new_row][new_col] != 1:
                        player_pos[0], player_pos[1] = new_row, new_col
                        canvas.delete(player)
                        player = draw_player(canvas)
                        if maze_map[new_row][new_col] == 2:
                            root.destroy()
                            root2 = Toplevel(self.level3)
                            root2.config(bg="black")
                            won = Label(root2, text="you won this!", fg="red", font=("Roman", 20), bg="black")
                            maze = True
                            print(maze)
                            won.pack()
                            root2.mainloop()

            root = Toplevel(self.level3)
            canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
            canvas.pack()
            draw_maze(canvas)
            player = draw_player(canvas)
            obstacle_rects = draw_obstacles(canvas)

            root.bind('<KeyPress>', lambda event: move_player(event, canvas, player))

            root.mainloop()

        def snake_game(self):
            global s_score, snake_game
            if not snake_game:
                def change_direction(event):
                    global s_direction
                    if event.keysym in ['Up', 'Down', 'Left', 'Right']:
                        s_direction = event.keysym

                def move_snake():
                    global s_score, s_food_position
                    head_x, head_y = snake[-1]
                    if s_direction == 'Up':
                        head_y -= 10
                    elif s_direction == 'Down':
                        head_y += 10
                    elif s_direction == 'Left':
                        head_x -= 10
                    elif s_direction == 'Right':
                        head_x += 10
                    snake.append((head_x, head_y))

                    if (head_x, head_y) == s_food_position:
                        s_score += 10
                        s_food_position = (random.randint(0, 39) * 10, random.randint(0, 39) * 10)

                    else:
                        snake.pop(0)

                def check_collisions():
                    global s_game_over
                    head_x, head_y = snake[-1]
                    if head_x < 0 or head_x >= s_width or head_y < 0 or head_y >= s_height or s_time_left == 0:
                        s_game_over = True

                def update_timer():
                    global s_time_left, s_game_over
                    if s_time_left > 0 and not s_game_over:
                        s_time_left -= 1
                        timer_label.config(text=f"Time Left: {s_time_left} seconds")
                        snake_room.after(1000, update_timer)
                    elif s_time_left == 0:
                        s_game_over = True

                def draw_elements():
                    global snake_game
                    canvas.delete(ALL)
                    for (x, y) in snake:
                        canvas.create_rectangle(x, y, x + 10, y + 10, fill='green')
                    food_x, food_y = s_food_position
                    canvas.create_oval(food_x, food_y, food_x + 10, food_y + 10, fill='red')
                    score_label.config(text=f"Score: {s_score}")

                    if s_game_over:
                        canvas.create_text(200, 200, text="Game Over!", fill="white", font=('Arial', 24))
                        if s_score >= 60:
                            canvas.create_text(200, 230, text="You Win!", fill="yellow", font=('Arial', 20))
                            snake_game = True
                            print(True)
                        restart_button.pack()

                def update_game():
                    if not s_game_over:
                        move_snake()
                        check_collisions()
                        draw_elements()
                        snake_room.after(50, update_game)

                def restart_game():
                    global snake, s_direction, s_food_position, s_game_over, s_score, s_time_left
                    snake = [(20, 20), (20, 30), (20, 40)]
                    s_direction = 'Down'
                    s_food_position = (random.randint(0, 39) * 10, random.randint(0, 39) * 10)
                    s_game_over = False
                    s_score = 0
                    s_time_left = 30
                    score_label.config(text=f"Score: {score}")
                    timer_label.config(text=f"Time Left: {time_left} seconds")
                    restart_button.pack_forget()
                    update_game()
                    update_timer()

                snake_room = Toplevel(self.level3)
                canvas = Canvas(snake_room, width=s_width, height=s_height, bg='black')
                canvas.pack()
                if Theme == 1:
                    score_label = Label(snake_room, text=f"Score: {s_score}", font=('Arial', 16))
                    score_label.pack()
                    timer_label = Label(snake_room, text=f"Time Left: {time_left} seconds", font=('Arial', 16))
                    timer_label.pack()
                    restart_button = Button(snake_room, text="Restart", command=restart_game)

                    snake_room.bind("<Key>", change_direction)
                update_game()
                update_timer()
                snake_room.mainloop()
            else:
                snake_room = Toplevel(self.level3)
                canvas = Canvas(snake_room, width=s_width, height=s_height, bg='black')

                canvas.pack()

                canvas.create_text(200, 230, text="You've already finished this game!", fill="yellow",
                                   font=('Arial', 20))
                snake_room.mainloop()

        def option_page(self):
            global timer_stop
            timer_stop = True
            option_root = Tk()
            option_root.config(bg='black')
            option_root.attributes('-fullscreen', True)

            pygame.mixer.music.stop()

            def start_timer():
                option_root.destroy()

                global timer_stop
                timer_stop = False
                pygame.mixer.music.play()
                self.update_timer(global_total_seconds)

            def quit_option():
                option_root.destroy()
                quit_game()

            def quit_game():
                return_to_menu()

            def return_to_menu():
                global timer_stop
                timer_stop = True
                self.level3.destroy()
                os.system("python main.py")

            if Theme == 1:
                if not Persian_language:
                    Button(option_root, text='Back To Game', command=start_timer, bg='black', fg='red',
                           font=('Roman', 20, 'bold')).place(x=180, y=300)
                else:
                    Button(option_root, text='بازی به برگشت', command=start_timer, bg='black', fg='red',
                           font=('Roman', 20, 'bold')).place(x=180, y=300)
            else:
                if not Persian_language:
                    Button(option_root, text='Back To Game', command=start_timer, bg='black', fg='lightblue',
                           font=('Roman', 20, 'bold')).place(x=180, y=300)

                else:
                    Button(option_root, text='بازی به برگشت', command=start_timer, bg='black', fg='lightblue',
                           font=('Roman', 20, 'bold')).place(x=180, y=300)

            if Theme == 1:
                if not Persian_language:
                    Button(option_root, text='Save And Quit', command=quit_option, bg='black', fg='red',
                           font=('Roman', 20, 'bold')).place(x=180, y=500)
                else:
                    Button(option_root, text='بازی از خروج و ذخیره', command=quit_option, bg='black', fg='red',
                           font=('Roman', 20, 'bold')).place(x=180, y=500)
            else:
                if not Persian_language:
                    Button(option_root, text='Save And Quit', command=quit_option, bg='black', fg='lightblue',
                           font=('Roman', 20, 'bold')).place(x=180, y=500)

                else:
                    Button(option_root, text='بازی از خروج و ذخیره', command=quit_option, bg='black', fg='lightblue',
                           font=('Roman', 20, 'bold')).place(x=180, y=500)

            if Theme == 1:
                if not Persian_language:
                    Label(option_root, text='GAME PAUSED', font=('Roman', 20, 'bold'), bg='black', fg='red').pack()
                else:
                    Label(option_root, text='شده متوقفق بازی', font=('Roman', 20, 'bold'), bg='black', fg='red').pack()
            else:
                if not Persian_language:
                    Label(option_root, text='GAME PAUSED', font=('Roman', 20, 'bold'), bg='black',
                          fg='lightblue').pack()
                else:
                    Label(option_root, text='شده متوقف بازی', font=('Roman', 20, 'bold'), bg='black', fg='red').pack()

            option_root.mainloop()

        def gameover(self):
            pygame.mixer.music.stop()
            self.level3.destroy()
            self.jumpscare()

        def jumpscare(self):
            global Persian_language

            root = Tk()
            root.title('GAME OVER')
            root.attributes('-fullscreen', True)
            root.config(bg='black')

            if Theme == 1:
                if not Persian_language:
                    Label(root, text='Game Over', font=('Roman', 70, 'bold'), bg='black', fg='red').place(x=550, y=360)
                else:
                    Label(root, text='شد تمام بازی', font=('Roman', 70, 'bold'), bg='black', fg='red').place(x=550,
                                                                                                             y=360)
            else:
                if not Persian_language:
                    Label(root, text='Game Over', font=('Roman', 70, 'bold'), bg='black', fg='lightblue').place(x=550,
                                                                                                                y=360)
                else:
                    Label(root, text='شد تمام بازی', font=('Roman', 70, 'bold'), bg='black', fg='lightblue').place(
                        x=550,
                        y=360)

            root.after(5000, start)

        def timer_label(self):
            global lives
            if lives == 3:
                self.update_timer(300)
            elif lives == 4:
                self.update_timer(600)
            elif lives == 5:
                self.update_timer(900)

        def update_timer(self, total_seconds):
            global lives, mode, timer_stop, global_total_seconds

            if not timer_stop:
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                global_total_seconds = total_seconds
                self.timer.config(text=f"{minutes}:{seconds}")

                if total_seconds > 0:
                    self.level3.after(1000, lambda: self.update_timer(total_seconds - 1))
                else:
                    self.gameover()

                self.level3.mainloop()

    # Functions of main menu

    def easy():
        global lives
        lives = 5

        with open(save_file, 'r') as file:
            lines = file.readlines()
        if "Level2" in f'{lines[0]}':
            Level2()

        if "Level1" in f'{lines[0]}':
            Level1()

        if "Level3" in f'{lines[0]}':
            Level3()

    def medium():
        global lives
        lives = 4
        with open(save_file, 'r') as file:
            lines = file.readlines()
        if "Level2" in f'{lines[0]}':
            Level2()

        if "Level1" in f'{lines[0]}':
            Level1()

        if "Level3" in f'{lines[0]}':
            Level3()

    def hard():
        global lives
        lives = 3

        with open(save_file, 'r') as file:
            lines = file.readlines()
        if "Level2" in f'{lines[0]}':
            Level2()
        if "Level1" in f'{lines[0]}':
            Level1()
        if "Level3" in f'{lines[0]}':
            Level3()

    def difficulties():
        root = Tk()
        root.title('Choose Difficulty')
        root.attributes('-fullscreen', True)
        root.config(bg='black')

        def back():
            root.destroy()
            start()

        Background_image = Image.open('Pictures/difficulties.jpg')

        def resize_image(event):
            global Fixed_bg_image
            new_width, new_height = event.width, event.height
            resized = Background_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            Fixed_bg_image = ImageTk.PhotoImage(resized)
            background_label.configure(image=Fixed_bg_image)

        # Create label and bind resize event
        Fixed_bg_image = ImageTk.PhotoImage(Background_image)
        background_label = Label(root, image=Fixed_bg_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Ensure it covers the entire window

        root.bind("<Configure>", resize_image)

        if Theme == 1:
            if not Persian_language:
                B_btn = Button(root, text='Back', font=('Roman', 30), bg='black', fg='red', command=back, width=20)
                B_btn.place(x=580, y=700)
                B_btn.bind('<Enter>', lambda e: B_btn.config(bg='red', fg='black'))
                B_btn.bind('<Leave>', lambda e: B_btn.config(bg='black', fg='red'))

            else:
                B_btn = Button(root, text='برگشت', font=('Roman', 30), bg='black', fg='red', command=back, width=20)
                B_btn.place(x=580, y=700)
                B_btn.bind('<Enter>', lambda e: B_btn.config(bg='red', fg='black'))
                B_btn.bind('<Leave>', lambda e: B_btn.config(bg='black', fg='red'))

        else:
            if not Persian_language:
                B_btn = Button(root, text='Back', font=('Roman', 30), bg='black', fg='lightblue', command=back,
                               width=20)
                B_btn.place(x=580, y=700)
                B_btn.bind('<Enter>', lambda e: B_btn.config(bg='lightblue', fg='black'))
                B_btn.bind('<Leave>', lambda e: B_btn.config(bg='black', fg='lightblue'))

            else:
                B_btn = Button(root, text='برگشت', font=('Roman', 30), bg='black', fg='lightblue', command=back,
                               width=20)
                B_btn.place(x=580, y=700)
                B_btn.bind('<Enter>', lambda e: B_btn.config(bg='lightblue', fg='black'))
                B_btn.bind('<Leave>', lambda e: B_btn.config(bg='black', fg='lightblue'))

        def start1():
            root.destroy()
            easy()

        def start2():
            root.destroy()
            medium()

        def start3():
            root.destroy()
            hard()

        if Theme == 1:
            if not Persian_language:
                easy1 = Button(root, text='Easy\nTimePerLevel: 15min', font=('Roman', 20, 'bold'), bg='black',
                               fg='red',
                               command=start1, width=70, justify='center', cursor='hand2', relief='flat')
                easy1.bind("<Enter>", lambda e: easy1.config(bg='red', fg='black'))
                easy1.bind('<Leave>', lambda e: easy1.config(bg='black', fg='red'))

                medium1 = Button(root, text='Medium\nTimePerLevel: 10min', font=('Roman', 20, 'bold'),
                                 bg='black',
                                 fg='red', command=start2, width=70, cursor='hand2', justify='center', relief='flat')

                medium1.bind("<Enter>", lambda e: medium1.config(bg='red', fg='black'))
                medium1.bind('<Leave>', lambda e: medium1.config(bg='black', fg='red'))

                hard1 = Button(root, text='Hard\nTimePerLevel: 5min', font=('Roman', 20, 'bold'), bg='black',
                               fg='red',
                               command=start3, width=70, justify='center', cursor='hand2', relief='flat')

                hard1.bind("<Enter>", lambda e: hard1.config(bg='red', fg='black'))
                hard1.bind('<Leave>', lambda e: hard1.config(bg='black', fg='red'))

            else:
                easy1 = Button(root, text='آسان\n دقیقه 30 : مرحله هر زمان', font=('Roman', 20, 'bold'),
                               bg='black',
                               fg='red',
                               command=start1, width=70, cursor='hand2', justify='center')

                easy1.bind("<Enter>", lambda e: easy1.config(bg='red', fg='black'))
                easy1.bind('<Leave>', lambda e: easy1.config(bg='black', fg='red'))

                medium1 = Button(root, text='متوسط\n دقیقه 15 : مرحله هر زمان',
                                 font=('Roman', 20, 'bold'),
                                 bg='black',
                                 fg='red', command=start2, width=70, justify='center', cursor='hand2', relief='flat')

                medium1.bind("<Enter>", lambda e: medium1.config(bg='red', fg='black'))
                medium1.bind('<Leave>', lambda e: medium1.config(bg='black', fg='red'))

                hard1 = Button(root, text='سخت\n دقیقه 5 : مرحله هر زمان', font=('Roman', 20, 'bold'),
                               bg='black',
                               fg='red',
                               command=start3, width=70, justify='center', cursor='hand2', relief='flat')

                hard1.bind("<Enter>", lambda e: hard1.config(bg='red', fg='black'))
                hard1.bind('<Leave>', lambda e: hard1.config(bg='black', fg='red'))

        else:
            if not Persian_language:
                easy1 = Button(root, text='Easy\nTimePerLevel: 15min', font=('Roman', 20, 'bold'), bg='black',
                               fg='lightblue', cursor='hand2', relief='flat',
                               command=start1, width=70, justify='center')
                easy1.bind("<Enter>", lambda e: easy1.config(bg='lightblue', fg='black'))
                easy1.bind('<Leave>', lambda e: easy1.config(bg='black', fg='lightblue'))

                medium1 = Button(root, text='Medium\nTimePerLevel: 10min', font=('Roman', 20, 'bold'),
                                 bg='black',
                                 fg='lightblue', command=start2, width=70, justify='center', cursor='hand2',
                                 relief='flat')

                medium1.bind("<Enter>", lambda e: medium1.config(bg='lightblue', fg='black'))
                medium1.bind('<Leave>', lambda e: medium1.config(bg='black', fg='lightblue'))

                hard1 = Button(root, text='Hard\nTimePerLevel: 5min', font=('Roman', 20, 'bold'), bg='black',
                               fg='lightblue',
                               command=start3, width=70, justify='center', relief='flat', cursor='hand2')

                hard1.bind("<Enter>", lambda e: hard1.config(bg='lightblue', fg='black'))
                hard1.bind('<Leave>', lambda e: hard1.config(bg='black', fg='lightblue'))

            else:
                easy1 = Button(root, text='آسان\n دقیقه 30 : مرحله هر زمان', font=('Roman', 20, 'bold'),
                               bg='black',
                               fg='lightblue',
                               command=start1, width=70, justify='center', cursor='hand2', relief='flat')

                easy1.bind("<Enter>", lambda e: easy1.config(bg='lightblue', fg='black'))
                easy1.bind('<Leave>', lambda e: easy1.config(bg='black', fg='lightblue'))

                medium1 = Button(root, text='متوسط\n دقیقه 15 : مرحله هر زمان',
                                 font=('Roman', 20, 'bold'),
                                 bg='black',
                                 fg='lightblue', command=start2, width=70, justify='center', relief='flat',
                                 cursor='hand2')

                medium1.bind("<Enter>", lambda e: medium1.config(bg='lightblue', fg='black'))
                medium1.bind('<Leave>', lambda e: medium1.config(bg='black', fg='lightblue'))

                hard1 = Button(root, text='سخت \n دقیقه 5 : مرحله هر زمان', font=('Roman', 20, 'bold'),
                               bg='black',
                               fg='lightblue', cursor='hand2', relief='flat',
                               command=start3, width=70, justify='center')

                hard1.bind("<Enter>", lambda e: hard1.config(bg='lightblue', fg='black'))
                hard1.bind('<Leave>', lambda e: hard1.config(bg='black', fg='lightblue'))

        easy1.place(x=305, y=185)
        medium1.place(x=305, y=400)
        hard1.place(x=305, y=600)
        root.mainloop()

    def gamemodes():
        root.destroy()
        difficulties()

    def settings():
        root.destroy()
        Settings()

    if Theme == 1:
        if not Persian_language:
            title = Label(root, text="the blood moon", bg='black', fg="red", relief="raised",
                          font=('roman', 40, 'bold'))
            title.place(x=595, y=200)
            S_g = Button(root, text='Start Game', cursor="hand2", bg='black', fg='red', font=('Roman', 20, 'bold'),
                         width=45,
                         relief='flat',
                         command=gamemodes)
            S_g.place(x=470, y=450)
            S_g.bind('<Enter>', lambda e: S_g.config(bg='red', fg='black'))
            S_g.bind('<Leave>', lambda e: S_g.config(bg='black', fg='red'))

            Sett = Button(root, text='Settings', cursor="hand2", bg='black', fg='red', font=('Roman', 20, 'bold'),
                          width=45,
                          relief='flat',
                          command=settings)
            Sett.bind('<Enter>', lambda e: Sett.config(bg='red', fg='black'))
            Sett.bind('<Leave>', lambda e: Sett.config(bg='black', fg='red'))
            Sett.place(x=470, y=575)
            E_g = Button(root, text='Exit Game', cursor="hand2", bg='black', fg='red', font=('Roman', 20, 'bold'),
                         width=45,
                         relief="flat",
                         command=Exit_game)
            E_g.bind('<Enter>', lambda e: E_g.config(bg='red', fg='black'))
            E_g.bind('<Leave>', lambda e: E_g.config(bg='black', fg='red'))
            E_g.place(
                x=470, y=700)

        else:
            title = Label(root, text="   ماه خونین   ", bg='black', fg="red", relief="raised",
                          font=('Mj_Kaman', 30, 'bold'), highlightcolor="red", highlightthickness=2)
            title.place(x=650, y=200)
            S_g = Button(root, text='شروع بازی', bg='black', fg='red', cursor="hand2", relief="flat",
                         font=('Mj_Kaman', 15,), width=45,
                         command=gamemodes)
            S_g.bind('<Enter>', lambda e: S_g.config(bg='red', fg='black'))
            S_g.bind('<Leave>', lambda e: S_g.config(bg='black', fg='red'))
            S_g.place(x=440, y=450)
            Sett = Button(root, text='تنظیمات', bg='black', fg='red', cursor="hand2", relief="flat",
                          font=('Mj_Kaman', 15), width=45,
                          command=settings)
            Sett.bind('<Enter>', lambda e: Sett.config(bg='red', fg='black'))
            Sett.bind('<Leave>', lambda e: Sett.config(bg='black', fg='red'))
            Sett.place(x=440, y=575)
            E_g = Button(root, text='خروج از بازی', bg='black', cursor="hand2", fg='red', font=('Mj_Kaman', 15),
                         width=45,
                         relief="flat",
                         command=Exit_game)
            E_g.bind('<Enter>', lambda e: E_g.config(bg='red', fg='black'))
            E_g.bind('<Leave>', lambda e: E_g.config(bg='black', fg='red'))
            E_g.place(x=440, y=700)
    else:
        if not Persian_language:
            title = Label(root, text="the blood moon", bg='black', fg="lightblue", relief="raised",
                          font=('roman', 40, 'bold'))
            title.place(x=595, y=200)
            S_g = Button(root, text='Start Game', bg='black', fg='lightblue', cursor="hand2", relief="flat",
                         font=('Roman', 20, 'bold'), width=45,
                         command=gamemodes)
            S_g.bind('<Enter>', lambda e: S_g.config(bg='lightblue', fg='black'))
            S_g.bind('<Leave>', lambda e: S_g.config(bg='black', fg='lightblue'))
            S_g.place(x=470, y=450)
            Sett = Button(root, text='Settings', bg='black', fg='lightblue', cursor="hand2", relief="flat",
                          font=('Roman', 20, 'bold'), width=45,
                          command=settings)
            Sett.bind('<Enter>', lambda e: Sett.config(bg='lightblue', fg='black'))
            Sett.bind('<Leave>', lambda e: Sett.config(bg='black', fg='lightblue'))
            Sett.place(x=470, y=575)
            E_g = Button(root, text='Exit Game', bg='black', fg='lightblue', cursor="hand2", relief="flat",
                         font=('Roman', 20, 'bold'), width=45,
                         command=Exit_game)
            E_g.bind('<Enter>', lambda e: E_g.config(bg='lightblue', fg='black'))
            E_g.bind('<Leave>', lambda e: E_g.config(bg='black', fg='lightblue'))
            E_g.place(
                x=470, y=700)

        else:
            title = Label(root, text="   ماه خونین   ", bg='black', fg="lightblue", relief="raised",
                          font=('Mj_Kaman', 30, 'bold'))
            title.place(x=650, y=200)
            S_g = Button(root, text='شروع بازی', bg='black', fg='lightblue', cursor="hand2", relief="flat",
                         font=('Mj_Kaman', 15, 'bold'),
                         width=45,
                         command=gamemodes)
            S_g.bind('<Enter>', lambda e: S_g.config(bg='lightblue', fg='black'))
            S_g.bind('<Leave>', lambda e: S_g.config(bg='black', fg='lightblue'))
            S_g.place(x=440, y=450)
            Sett = Button(root, text='تنظیمات', bg='black', fg='lightblue', cursor="hand2", relief="flat",
                          font=('Mj_Kaman', 15, 'bold'),
                          width=45,
                          command=settings)
            Sett.bind('<Enter>', lambda e: Sett.config(bg='lightblue', fg='black'))
            Sett.bind('<Leave>', lambda e: Sett.config(bg='black', fg='lightblue'))
            Sett.place(x=440, y=575)
            E_g = Button(root, text='خروج از بازی', bg='black', cursor="hand2", relief="flat", fg='lightblue',
                         font=('Mj_Kaman', 15, 'bold'),
                         width=45,
                         command=Exit_game)
            E_g.bind('<Enter>', lambda e: E_g.config(bg='lightblue', fg='black'))
            E_g.bind('<Leave>', lambda e: E_g.config(bg='black', fg='lightblue'))
            E_g.place(x=440, y=700)
    root.mainloop()


start()
