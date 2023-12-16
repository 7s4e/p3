# Bryant Smith
# 4 November 2022
# CSE 110
# Word Guessing Game

from random import randrange
from textwrap import fill
from tkinter import Tk, Label

border = '-' * 70
count = 1
credit = fill('Credit: The Secret Word is randomly selected from a text file of the scriptures obtained from https://scriptures.nephi.org/ on 11 October 2022.', subsequent_indent='    ')
game_words = []
hints = fill('Hints: If a letter appears, it\'s in the Secret Word. If the letter is capitalized, it\'s in the right spot.', subsequent_indent='    ')
instructions = fill('Instructions: Guess the Secret Word in as few tries as possible! Guesses with an incorrect number of letters will clear all hints.', subsequent_indent='    ')
prompt = 'What is the Secret Word? {}\n             Your guess: '
punctuation = ['!','(',')','--','[',']',':',';','"',"'",',','.','?']
title = 'WoRdLe'
verses = []
window = Tk()
window.title('Word Guessing Game')
window.geometry('400x1000+50+20')

with open('lds-scriptures.txt') as file:
    for line in file:
        line = line.strip()
        values = line.split('     ')
        verses.append(values)

random_verse = randrange(len(verses))
citation = (verses[random_verse])[0]
text = (verses[random_verse])[1]
words = text.split(' ')
verse = fill(f'"{text}"', initial_indent='    ')

for word in words:
    letters = ''
    for character in word:
        if character not in punctuation:
            letters += character
    if len(letters) > 4:
            game_words.append(letters)

secret_word = game_words[randrange(len(game_words))].lower()

def congratulations(count):
    if count == 1:
        tries = 'in one try!'
    else:
        tries = f'in {count} tries.'
    message = fill(f'Congratulations! You guessed the secret word in {citation} {tries}',subsequent_indent='    ')
    print(f'\n{message}\n\n{verse}\n')

def error(correct_length):
    if correct_length:
        suggestion = 'Try again.'
        populated = True
    else:
        suggestion = 'Check the number of letters.'
        populated = False
    print(f'\nYour guess was not correct. {suggestion}')
    hint(populated)

def hint(populated):
    global guess
    hint = ''
    if populated:
        for i, guessed_letter in enumerate(guess):
            for j, secret_letter in enumerate(secret_word):
                if i == j:
                    if guessed_letter.lower() == secret_letter.lower():
                        hint += guessed_letter.upper()
                    elif guessed_letter.lower() in secret_word.lower():
                        hint += guessed_letter.lower()
                    else:
                        hint += '_'
    else:
        k = 0
        while k != len(secret_word):
            hint += '_'
            k += 1
    guess = input(prompt.format(hint)).lower()

heading = Label(window,text=f'\n{title :-^70}\n{instructions}\n\n{hints}\n\n{credit}\n{border}\n',justify='left')
heading.grid(row=1,column=1,padx=15,pady=0,columnspan=2,rowspan=3)

cue = Label(window,text=hint(False))
cue.grid(row=4,column=1,padx=15,pady=0,columnspan=2)

window.mainloop()

# hint(False)
# if guess is secret_word:
#     congratulations(count)
# else:
#     while guess != secret_word:
#         count += 1
#         if len(guess) == len(secret_word):
#             error(True)
#         else:
#             error(False)
#     congratulations(count)