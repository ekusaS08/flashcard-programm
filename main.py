from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")

# ----------------------- FLASHCARD GENERATION -------------------------------------
# import and convert data
all_words = pd.read_csv("data/french_words.csv")
try:
    words_to_learn = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    all_words.to_csv("data/words_to_learn.csv", index=False)
    words_to_learn = pd.read_csv("data/words_to_learn.csv")

words_to_learn = words_to_learn.to_dict(orient="records")

# pick random "Card" to show next
current_word = {}


def pick_word(is_correct: bool):
    '''Randomly picks a word from "words_to_learn" and displays it.
    Starts a timer, when it runs out, it calls flip_card().
    Removes the word, if guessed correctly.'''
    global current_word, flip_timer
    window.after_cancel(flip_timer)  # resetting the flip_timer
    current_word = random.choice(words_to_learn)
    # changing the card_layout to "front"
    card_canvas.itemconfig(shown_side, image=card_front_img)
    card_canvas.itemconfig(word_text, text=f"{current_word['French']}")
    card_canvas.itemconfig(title_text, text="French")
    flip_timer = window.after(3000, flip_card)

    if is_correct:
        words_to_learn.remove(current_word)  # remove the card from the list


def flip_card():
    '''Flips a card to the backside (english).'''
    card_canvas.itemconfig(shown_side, image=card_back_img)
    card_canvas.itemconfig(word_text, text=f"{current_word['English']}")
    card_canvas.itemconfig(title_text, text="English")


# ----------------------- SAVING --------------------------------------
def _on_close():
    '''Saves the current progress (called when window is closed). '''
    pd.DataFrame(words_to_learn).to_csv("data/words_to_learn.csv", index=False)
    window.destroy() # close the window


# ----------------------- UI SETUP -------------------------------------
window = Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

### CARDS (CANVAS)
card_canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")

shown_side = card_canvas.create_image(400, 263, image=card_front_img)
card_canvas.grid(row=0, column=0, columnspan=2)


title_text = card_canvas.create_text(400, 150, text="Title", font=TITLE_FONT)
word_text = card_canvas.create_text(400, 263, text="Card", font=WORD_FONT)

###TIMER / FIRST CARD
flip_timer = window.after(3000, flip_card) #starts the flip_timer

pick_word(False) # display the first card

###BUTTONS
wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=lambda: pick_word(False))
wrong_button.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=lambda: pick_word(True))
right_button.grid(row=1, column=1)



window.protocol("WM_DELETE_WINDOW", _on_close) # overrides what happens on window close
window.mainloop()
