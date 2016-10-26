#!/usr/bin/python3

import requests
import webbrowser
import pyautogui
import time
import random
import tkinter as tk
import tkinter.messagebox

def request_words():
    """ Request dictionary of words for the world wide web.
    """
    url = 'http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain'
    response = requests.get(url)
    words = response.content.splitlines()
    words = [ word.decode('ascii') for word in words ]
    return words

def open_browser():
    """ Launch google-chrome browser.
    """
    browser = webbrowser.get('google-chrome')
    browser.open(r'')

def highlight_ominbar():
    """ Click on omnibar in chrome browser.
    """
    pyautogui.keyDown('ctrlleft') 
    pyautogui.press('l') 
    pyautogui.keyUp('ctrlleft') 

def word_sampler(number):
    """ Randomly sample a word from the dictionary.
    """
    words = request_words()
    while True:
        yield random.sample(words, number)  

def search_google(terms):
    """ Type search terms into chrome omnibar.
    """
    term = ' '.join(terms)
    pyautogui.typewrite(term, 0.1)
    pyautogui.typewrite(['enter'])

def confoogle(repeats=1, wait=2, terms=2):
    """ Stand alone Confoogle program.

    This may be called from the command line with a fixed number of 
    repeats. For indeterminate repeats use the tkinter version.  
    """
    words = word_sampler(number=terms)
    open_browser()
    for _ in range(repeats):
        terms = next(words)
        highlight_ominbar()
        search_google(terms)
        time.sleep(wait)

class StartWindow(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        root.bind('<Key>', lambda e: root.destroy())

        button = tk.Button(root, text="Confoogle!", command=lambda: self.open_browser() & self.confoogle())
        button.pack()

        label = tk.Label(root, text="")

    def confoogle(self):
        terms = next(self.words)
        root.attributes('-topmost', 0)
        highlight_ominbar()
        search_google(terms)
        self.after(1000, self.confoogle)
        root.attributes('-topmost', 1)
        return 1

    def open_browser(self):
        open_browser()
        self.words = word_sampler(2)
        return 1

    def quit(self):
        self.destroy()
        tk.sys.exit()

if __name__ == '__main__':
    root = tk.Tk()
    StartWindow(root).pack()
    root.mainloop()
