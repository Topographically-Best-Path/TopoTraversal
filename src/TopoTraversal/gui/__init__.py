import tkinter as tk

def start():
    window=tk.Tk()
    window.geometry("620x780")
    window.title('TopoTraversal')

    name = tk.Label(text = "Name")
    name.grid(column=0,row=1)
    year = tk.Label(text = "Year")
    year.grid(column=0,row=2)
    month = tk.Label(text = "Month")
    month.grid(column=0,row=3)
    date = tk.Label(text = "Day")
    date.grid(column=0,row=4)

    nameEntry = tk.Entry()
    nameEntry.grid(column=1,row=1)
    yearEntry = tk.Entry()
    yearEntry.grid(column=1,row=2)
    monthEntry = tk.Entry()
    monthEntry.grid(column=1,row=3)
    dateEntry = tk.Entry()
    dateEntry.grid(column=1,row=4)

    #btn=tk.Button(window, text="This is Button widget", fg='blue')
    #btn.place(x=80, y=100)
    window.mainloop()

def getInput():
    name=nameEntry.get()
    monkey = Person(name,datetime.date(int(yearEntry.get()),int(monthEntry.get()),int(dateEntry.get())))

    textArea = tk.Text(master=window,height=10,width=25)
    textArea.grid(column=1,row=6)
    answer = " Heyy {monkey}!!!. You are {age} years old!!! ".format(monkey=name, age=monkey.age())
    textArea.insert(tk.END,answer)

def update():
    button=tk.Button(window,text="Calculate Age",command=getInput,bg="pink")
    button.grid(column=1,row=5)
