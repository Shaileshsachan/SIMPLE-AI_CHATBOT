import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from keras.models import load_model
import json
import random

lemm = WordNetLemmatizer()
model = load_model('bot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

def pre_process(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemm.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = pre_process(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("FOUND IN BAG: %s" % w)
    return(np.array(bag))

def predict_Class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def response(ints, intents_json):
    tag = ints[0]['intent']
    intents_list = intents_json['intents']
    for i in intents_list:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_Class(msg, model)
    res = response(ints, intents)
    return res

import tkinter
from tkinter import *

root = Tk()
root.title("SHAILESH RESUME")
root.geometry("500x500")
root.resizable(width=FALSE, height=FALSE)

def send(msg):
    msg = box.get("1.0", 'end-1c').strip()
    box.delete("0.0", END)

    if msg != '':
        chat.config(state=NORMAL)
        chat.insert(END, "You: " + msg + '\n\n')
        chat.config(foreground="#ffffff", font=("Verdana", 12))

        res = chatbot_response(msg)

        chat.insert(END, "Bot: " + res + '\n\n')
        chat.config(state=DISABLED)
        chat.yview(END)


chat = Text(root, bd=0, bg="black", height='10', width='50', font="Arial", fg='white')
chat.config(state=DISABLED)

scrollBar = Scrollbar(root, command=chat.yview, cursor="heart")
chat['yscrollcommand'] = scrollBar.set

sendButton = Button(root, font=("Verdana",10,'bold'), text='Send', width="10", height=5, bd=4, bg="green", fg="black", command= send, padx='0.6', pady='0.6')

box = Text(root, bd=4, bg="white", width='29', height='5', font='Arial', padx='0.6', pady='0.6')
box.bind("<Return>", send)

scrollBar.place(x=476, y=6, height=386)
chat.place(x=6, y=6, height=386, width=470)
box.place(x=128, y=401, height=90, width=365)
sendButton.place(x=6, y=401, height=90)

root.mainloop()




















