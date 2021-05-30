import constants
import algo
import data
import tkinter as tk

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # Enter Radius
        r = tk.Entry(self, width=40)
        r.pack(side="bottom", fill="both")
        label = tk.Label(self, text="Enter Size")
        label.pack(side="bottom", fill="both")

        # Enter Y coordinate
        y = tk.Entry(self, width=40)
        y.pack(side="bottom", fill="both")
        label = tk.Label(self, text="Enter Latitude")
        label.pack(side="bottom", fill="both")

        # Enter X coordinate
        x = tk.Entry(self, width=40)
        x.pack(side="bottom", fill="both")
        label = tk.Label(self, text="Enter Longitude")
        label.pack(side="bottom", fill="both")

        # Generate Image
        generate = tk.Button(self, text='Generate', command=lambda: get_etopo_data(int(x.get()),int(y.get()),int(r.get())))
        generate.pack(side="bottom", fill="both")

        label = tk.Label(self, text="This is Page 1")
        label.pack(side="top", fill="both", expand=True)

        def get_etopo_data(lon, lat, size):
            value = lon+lat+size
            label.configure(text="sum is: " + str(value))



class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="This is page 2")
        label.pack(side="top", fill="both", expand=True)

class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="This is page 3")
        label.pack(side="top", fill="both", expand=True)

class Quit(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.destroy()

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = Page(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Page 1", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Page 2", command=p2.lift)
        b3 = tk.Button(buttonframe, text="Page 3", command=p3.lift)
        b4 = tk.Button(buttonframe, text='Quit', command=root.destroy)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="right")

        p1.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x800")
    root.mainloop()
