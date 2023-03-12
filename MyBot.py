from tkinter import *
import requests

def codeGenerator(version, question):
    try:
        answer =requests.post('https://www.useblackbox.io/autocomplete'+version, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Content-Type': 'application/json'
            }, json={"userId":"","textInput":question}, timeout=15).json()
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError): return
    return answer


def setAnswer(views, version, question):
    window, send, answerv =views
    send.configure(text='Wait')
    window.update_idletasks()
    answer =codeGenerator(version, question)
    if answer and answer.get('status')=='success':
        answerv.delete('1.0', 'end')
        response =answer.get('response')
        if type(response) is list:
            for lines in response:
                for line in lines: answerv.insert('end', line+'\n')
        elif type(response) is str: answerv.insert('1.0', response)
    send.configure(text='Send')

def main():
    window =Tk()
    window.title('MyBot')
    window.config(padx=5, pady=10)
    frame =Frame(window)
    label1 =Label(window, text='Ask Questions')
    question =Text(window, wrap='none', height=3, padx=5, pady=10, undo=True)
    label1.pack()
    question.pack()
    version =StringVar()
    radio1 =Radiobutton(frame, variable=version, value='v2', text='V2 (Code Mode)')
    radio2 =Radiobutton(frame, variable=version, value='v3', text='V3 (Code With References)')
    send =Button(frame, text='Send', padx=20, pady=5, command=lambda:setAnswer((window, send, answerv), version.get(), question.get('1.0', 'end')))
    version.set('v2')
    radio1.grid(row=1, column=1)
    radio2.grid(row=1, column=2, padx=(0,10))
    send.grid(row=1, column=3)
    frame.pack()
    answerv =Text(window, wrap='none', padx=5, pady=10)
    xscrollbar = Scrollbar(window, orient=HORIZONTAL, command=answerv.xview)
    xscrollbar.pack(side=BOTTOM, fill='x')
    yscrollbar = Scrollbar(window, orient=VERTICAL, command=answerv.yview)
    yscrollbar.pack(side=RIGHT, fill='y')
    answerv.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
    answerv.pack()
    window.mainloop()

if __name__ == '__main__':
    main()
