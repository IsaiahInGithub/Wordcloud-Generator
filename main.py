import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
import platform

stopwords = set(STOPWORDS)
all_stopwords = []

background_colour = None
max_words = 50
file_location = None
file_selected = None
font_path = None
transparent_file_location = None
width = 390
ent_width_one = 30
ent_width_two = 35

if platform.system() == "Linux":
    width = 1250
    ent_width_one = 28
    ent_width_two = 30
else:
    width = 1200
    ent_width_one = 30
    ent_width_two = 35


def spacer(window):
    spacing = tkinter.Label(window, text="", background="#ddd")
    spacing.pack()


app = tkinter.Tk()
app.geometry("650x625")
app.title("Wordcloud Generator")
app.configure(background="#ddd")
frame = tkinter.Frame(app, background=None)
frame.pack()
frame.configure(background="#ddd")
box = tkinter.Frame(app)
box.pack()


def open_command():
    global fileplace
    fileplace = askopenfilename(
        filetypes=[
            ("CSV Files", "*.csv"), ("All Files", "*.*")
        ]
    )
    if not fileplace:
        return
    global data
    data = pd.read_csv(fileplace, encoding='latin1')
    global file_location
    file_location = fileplace
    global box
    box.destroy()
    global file_selected
    box = tkinter.Frame(app, background=None)
    box.pack()
    file_selected = tkinter.Label(box, text="File Selected: " + str(file_location), font="Calibri, 11", background="#ddd")
    file_selected.pack()

text = tkinter.Label(frame, text="Hello User!", font="Calibri, 25", background="#ddd", foreground="black")
text.pack(pady=40)

def get_settings():
    settings = tkinter.Tk()
    settings.title("Wordcloud Settings")
    settings.geometry("500x400")
    spacing_six = tkinter.Label(settings, text="")
    spacing_six.pack()
    heading_one = tkinter.Label(settings, text="Background Colour", font="Calibri, 15")
    heading_one.pack()
    spacing_two = tkinter.Label(settings, text="")
    spacing_two.pack()
    clicked = tkinter.StringVar(settings)
    clicked.set("Transparent (Default)")
    dropdown = tkinter.OptionMenu(settings, clicked, "Transparent (Default)", "White", "Black", "Silver", "Red", "Green", "Blue")
    dropdown.pack()

    def save_bg():
        global background_colour
        if str(clicked.get()) == "Transparent (Default)":
            background_colour = None
        elif str(clicked.get()) == "Blue":
            background_colour = "#0000aa"
        else:
            background_colour = str(clicked.get())

    bg_btn = tkinter.Button(settings, text="Save", command=save_bg, width=20)
    bg_btn.pack()
    spacing_three = tkinter.Label(settings, text="")
    spacing_three.pack()
    max_words_heading = tkinter.Label(settings, text="Max Words (Default = 50)", font="Calibri, 15")
    max_words_heading.pack()
    spacing_four = tkinter.Label(settings, text="")
    spacing_four.pack()
    max_words_ent = tkinter.Entry(settings, width=22)
    max_words_ent.pack()

    def save_max_words():
        global max_words
        max_words = int(max_words_ent.get())
        max_words_ent.delete(0, tkinter.END)

    max_words_btn = tkinter.Button(settings, text="Save", width=20, command=save_max_words)
    max_words_btn.pack()
    spacing_five = tkinter.Label(settings, text="")
    spacing_five.pack()
    font_heading = tkinter.Label(settings, text="Font", font="Calibri, 15")
    font_heading.pack()
    spacing_six = tkinter.Label(settings, text="")
    spacing_six.pack()

    def save_font():
        fileplace = askopenfilename(
             parent=settings,
             filetypes=[
                ("TTF File", "*.ttf"), ("All Files", "*.*")
             ]
         )
        if not fileplace:
            return
        global font_path

        font_path = fileplace

    font_btn = tkinter.Button(settings, text="Select Font", width=20, command=save_font)
    font_btn.pack()

def generate():
    global wordCloud_one
    wordCloud_one = WordCloud(stopwords=stopwords, background_color=background_colour, mode='RGBA', max_words=max_words, font_path=font_path, collocations=True).generate(data.to_string())
    plt.imshow(wordCloud_one)
    plt.axis("off")
    plt.show()

def save_with_transparent_background():

        fileplace = asksaveasfilename(
             filetypes=[
                ("PNG File", "*.png"), ("All Files", "*.*")
             ]
         )
        if not fileplace:
            return

        global transparent_file_location

        if platform.system() == "Linux":
            transparent_file_location = fileplace
        elif platform.system() != "Linux":
            transparent_file_location = fileplace + ".png"
            
        WordCloud(stopwords=stopwords, background_color=background_colour, mode='RGBA', max_words=max_words, font_path=font_path, collocations=True, width=800, height=600).generate(data.to_string()).to_file(transparent_file_location)

open_btn = tkinter.Button(
    frame, text="Select CSV File", command=open_command, width=25, height=2, borderwidth=0, background="white", activebackground="white", fg=None, activeforeground=None, font="Bold, 11")
open_btn.pack(side=tkinter.TOP, pady=15)


def add_stopword():
    all_stopwords = ent.get().split(', ')
    stopwords.update(all_stopwords)
    ent.delete(0, tkinter.END)

spacer(frame)
ent = tkinter.Entry(frame, width=ent_width_two)
ent.pack()    
ent_btn = tkinter.Button(frame, text="Add Stopword(s)",
                        command=add_stopword, width=ent_width_one)
ent_btn.pack()
spacer(frame)
settings_btn = tkinter.Button(
    frame, text="Advanced Settings", command=get_settings, width=25, height=2, borderwidth=0, background="white", activebackground="white", fg=None, activeforeground=None, font="Bold, 11")
settings_btn.pack(side=tkinter.TOP, pady=15)
gen_btn = tkinter.Button(
    frame, text="Preview Wordcloud", command=generate, width=25, height=2, borderwidth=0, background="white", activebackground="white", fg=None, activeforeground=None, font="Bold, 11")
gen_btn.pack(side=tkinter.TOP, pady=15)
download_btn = tkinter.Button(
    frame, text="Download Wordcloud", command=save_with_transparent_background, width=25, height=2, borderwidth=0, background="white", activebackground="white", fg=None, activeforeground=None, font="Bold, 11")
download_btn.pack(side=tkinter.TOP, pady=15)

spacer(frame)
spacer(frame)

app.mainloop()