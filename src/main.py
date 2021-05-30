import constants
import algo
import data
import tkinter as tk
from tkinter import filedialog

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

# About Page
class Page0(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        img = tk.PhotoImage(file="Image1.png")
        img = img.subsample(7)
        label = tk.Label(self, image=img)
        label.image = img
        label.pack(side="top", fill="both", expand=True)

        T = tk.Text(self, height=10, width=75, font=("Helvetica", 16))
        T.pack()

        quote = """Our project will be a research project based on finding the optimal route between two points on a
topographic elevation map. We will find the most reasonable route by taking into account factors
such as traversal time, safety, distance, steepness, and physical features of the area including
rivers and prebuilt paths. Our end goal is to make something like Google Maps’ fastest route
calculator, but for a place without as many man-built roads like a mountain or a valley,
hence the use of a topographic map. We hope to gain knowledge of a variety of graph algorithms
such as BFS, DFS, Dijikstra’s Algorithm and develop our own algorithm which could be helpful
with planning and creating paths in the wilderness."""
        T.insert(tk.END, quote)

# World Data Page
class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)


        def openInputField():
            newWindow = tk.Toplevel(root)
            newWindow.title("Endpoint Input")

            plot = tk.Button(newWindow, text='Plot', command=lambda: sum2(int(x1.get()),int(y1.get()),int(x2.get())))
            plot.pack(side="bottom", fill="both")

            bottomframe = tk.Frame(newWindow)
            bottomframe.pack( side ="bottom")

            topframe = tk.Frame(newWindow)
            topframe.pack( side = "top")

            label = tk.Label(topframe, text="Enter x1")
            label.pack(side="left")
            x1 = tk.Entry(topframe, width=10)
            x1.pack(side="left")

            y1 = tk.Entry(topframe, width=10)
            y1.pack(side="right")
            label = tk.Label(topframe, text="Enter y1")
            label.pack(side="right")

            label = tk.Label(bottomframe, text="Enter x2")
            label.pack(side="left")
            x2 = tk.Entry(bottomframe, width=10)
            x2.pack(side="left")

            y2 = tk.Entry(bottomframe, width=10)
            y2.pack(side="right")
            label = tk.Label(bottomframe, text="Enter y2")
            label.pack(side="right")

        #This function runs getetopodata and create image then displays the image
        def sum(lon, lat, size):
            value = lon+lat+size
            img1 = tk.PhotoImage(file="Image1.png")
            img1 = img1.subsample(7)
            label.image = img1
            label.configure(image=img1)

        def sum2(lon, lat, size):
            value = lon+lat+size
            img2 = tk.PhotoImage(file="Image2.png")
            img2 = img2.subsample(7)
            label.image = img2
            label.configure(image=img2)

        # Enter Radius
        r = tk.Entry(self, width=40)
        r.pack(side="bottom", fill="both")
        label = tk.Label(self, text="Enter Size (suggested 0.1 <= size <= 10)")
        label.pack(side="bottom", fill="both")

        # Enter Y coordinate
        y = tk.Entry(self, width=40)
        y.pack(side="bottom", fill="both")
        label = tk.Label(self, text="Enter Latitude (suggested -85 <= lat <= 85)")
        label.pack(side="bottom", fill="both")

        # Enter X coordinate
        x = tk.Entry(self, width=40)
        x.pack(side="bottom", fill="both")
        label = tk.Label(self, text="Enter Longitude (suggested -175 <= lon <= 175)")
        label.pack(side="bottom", fill="both")

        # Best Path
        showpath = tk.Button(self, text='Display Best Path', command=lambda: sum(int(x.get()),int(y.get()),int(r.get())))
        showpath.pack(side="bottom", fill="both")

        # New Line
        label = tk.Label(self, text="")
        label.pack(side="bottom", fill="both")

        # Plot Endpoints
        generate = tk.Button(self, text='Plot Endpoints', command=openInputField)
        generate.pack(side="bottom", fill="both")

        # Generate Image
        generate = tk.Button(self, text='Generate Image', command=lambda: sum(int(x.get()),int(y.get()),int(r.get())))
        generate.pack(side="bottom", fill="both")

        img = tk.PhotoImage(file="Image1.png")
        img = img.subsample(7)
        label = tk.Label(self, image=img)
        label.image = img
        label.pack(side="top", fill="both", expand=True)

# File Input Page
class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        def file_opener():
            # Get file path
            input = filedialog.askopenfilename(initialdir="/")

            # Check for csv or nv
            if (input[-3:] == "csv"):
                data.get_csvfile(input)
            if (input[-2:] == "nv"):
                data.get_ncfile(input)

            # Create image
            data.create_image()

            # Display image
            img2 = tk.PhotoImage(file="Image2.png")
            img2 = img2.subsample(7)
            label.image = img2
            label.configure(image=img2)


        select = tk.Button(self, text ='Select a .nc/.csv file', command = file_opener)
        select.pack(side="bottom", fill="both")

        img = tk.PhotoImage(file="Image1.png")
        img = img.subsample(7)
        label = tk.Label(self, image=img)
        label.image = img
        label.pack(side="top", fill="both", expand=True)

# Random Data Page
class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        def openInputField():
            newWindow = tk.Toplevel(root)
            newWindow.title("Endpoint Input")

            plot = tk.Button(newWindow, text='Plot', command=lambda: sum2(int(x1.get()),int(y1.get()),int(x2.get())))
            plot.pack(side="bottom", fill="both")

            bottomframe = tk.Frame(newWindow)
            bottomframe.pack( side ="bottom")

            topframe = tk.Frame(newWindow)
            topframe.pack( side = "top")

            label = tk.Label(topframe, text="Enter x1")
            label.pack(side="left")
            x1 = tk.Entry(topframe, width=10)
            x1.pack(side="left")

            y1 = tk.Entry(topframe, width=10)
            y1.pack(side="right")
            label = tk.Label(topframe, text="Enter y1")
            label.pack(side="right")

            label = tk.Label(bottomframe, text="Enter x2")
            label.pack(side="left")
            x2 = tk.Entry(bottomframe, width=10)
            x2.pack(side="left")

            y2 = tk.Entry(bottomframe, width=10)
            y2.pack(side="right")
            label = tk.Label(bottomframe, text="Enter y2")
            label.pack(side="right")

        # Enter Water
        w = tk.Entry(self, width=40)
        w.pack(side="bottom", fill="both")
        label = tk.Label(self, text="water, 0 <= water <= 100, percentage of the map that is water")
        label.pack(side="bottom", fill="both")

        # Enter Height
        h = tk.Entry(self, width=40)
        h.pack(side="bottom", fill="both")
        label = tk.Label(self, text="height, 100 <= height <= 8000, controls max altitude difference")
        label.pack(side="bottom", fill="both")

        # Enter Frequency
        f = tk.Entry(self, width=40)
        f.pack(side="bottom", fill="both")
        label = tk.Label(self, text="frequency, 1 <= frequency <= 25, controls how mountainous the data will be")
        label.pack(side="bottom", fill="both")

        # New Line
        label = tk.Label(self, text="")
        label.pack(side="bottom", fill="both")

        # Best Path
        showpath = tk.Button(self, text='Display Best Path', command=lambda: sum(int(x.get()),int(y.get()),int(r.get())))
        showpath.pack(side="bottom", fill="both")

        # Plot Endpoints
        generate = tk.Button(self, text='Plot Endpoints', command=openInputField)
        generate.pack(side="bottom", fill="both")

        # Generate Image
        generate = tk.Button(self, text='Generate Image', command=lambda: sum(int(x.get()),int(y.get()),int(r.get())))
        generate.pack(side="bottom", fill="both")

        img = tk.PhotoImage(file="Image1.png")
        img = img.subsample(7)
        label = tk.Label(self, image=img)
        label.image = img
        label.pack(side="top", fill="both", expand=True)

# Quit
class Quit(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.destroy()

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p0 = Page0(self)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = Page(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p0.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b0 = tk.Button(buttonframe, text="About", command=p0.lift)
        b1 = tk.Button(buttonframe, text="World Data", command=p1.lift)
        b2 = tk.Button(buttonframe, text="File Input", command=p2.lift)
        b3 = tk.Button(buttonframe, text="Random Data Page", command=p3.lift)
        b4 = tk.Button(buttonframe, text='Quit', command=root.destroy)

        b0.pack(side="left")
        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="right")

        p0.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x800")
    root.mainloop()
