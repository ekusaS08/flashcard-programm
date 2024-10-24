from tkinter import *
import pandas as pd
import random

from pandas.core.interchange.dataframe_protocol import DataFrame

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Ariel",40,"italic")
WORD_FONT = ("Ariel",60,"bold")


#----------------------- FLASHCARD GENERATION -------------------------------------
#import and convert data
all_words = pd.read_csv("data/french_words.csv")
try:
    words_to_learn = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    all_words.to_csv("data/words_to_learn.csv", index=False)
    words_to_learn = pd.read_csv("data/words_to_learn.csv")


all_words = all_words.to_dict(orient="records")
words_to_learn = words_to_learn.to_dict(orient="records")
print(type(words_to_learn))

current_word = {}
#pick random entry
def pick_word(is_correct: bool):
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    current_word = random.choice(words_to_learn)
    card_canvas.itemconfig(shown_side, image=card_front_img)
    card_canvas.itemconfig(word_text,text=f"{current_word['French']}")
    card_canvas.itemconfig(title_text, text="French")
    flip_timer = window.after(3000,flip_card)
    if is_correct:
        words_to_learn.remove(current_word)


def flip_card():

    card_canvas.itemconfig(shown_side, image = card_back_img)
    card_canvas.itemconfig(word_text, text=f"{current_word['English']}")
    card_canvas.itemconfig(title_text, text= "English")
#----------------------- SAVING --------------------------------------
def _on_close():
    pd.DataFrame(words_to_learn).to_csv("data/words_to_learn.csv", index=False)
    window.destroy()

#----------------------- UI SETUP -------------------------------------
window = Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
### CARD
card_canvas = Canvas(width=800,height=526,bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file= "images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
shown_side = card_canvas.create_image(400, 263, image=card_front_img)
card_canvas.grid(row=0,column=0, columnspan=2)

title_text = card_canvas.create_text(400,150,text="Title",font=TITLE_FONT)
word_text = card_canvas.create_text(400,263, text="Card",font=WORD_FONT)

###TIMER
flip_timer = window.after(3000,flip_card)

###BUTTONS
wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=lambda:pick_word(False))
wrong_button.grid(row=1,column =0)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command= lambda:pick_word(True) )
right_button.grid(row=1,column =1)

pick_word(False)


window.protocol("WM_DELETE_WINDOW", _on_close)
window.mainloop()