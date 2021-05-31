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

        T = tk.Text(self, height=10, width=75, font=("Helvetica", 16))
        T.pack()

        quote = """Our project will be a research project based on finding the optimal route between two points on a
topographic elevation map. We will find the most reasonable route by taking into account factors
such as traversal time, safety, distance, steepness, and physical features of the area including
rivers and lakes. Our end goal is to make something like Google Maps’ fastest route
calculator, but for a place without as many man-built roads like a mountain or a valley,
hence the use of a topographic map. We hope to gain knowledge of a variety of graph algorithms
such as BFS, DFS, Dijikstra’s Algorithm and develop our own algorithm which could be helpful
with planning and creating paths in the wilderness."""
        T.insert(tk.END, quote)

# World Data Page
class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # Image1 Creation
        def image1(lon, lat, size):
            if (lon < -180 or lon > 180): return
            if (lat < -89 or lat > 89): return
            if (size < 0.05 or size > 180): return
            data.get_etopo_data(lon, lat, size)
            data.create_image()
            img1 = tk.PhotoImage(file=constants.TEMPDIR/"Image1.png")
            img1 = img1.subsample(7)
            imglabel.image = img1
            imglabel.configure(image=img1)

        # Image2 Creation
        def image2(x1, y1, x2, y2):
            bounds = data.get_bounds();
            if (x1 < bounds[0] or x2 < bounds[0]): return
            if (x1 > bounds[1] or x2 > bounds[1]): return
            if (y1 < bounds[2] or y2 < bounds[2]): return
            if (y1 > bounds[3] or y2 > bounds[3]): return
            constants.LON1 = x1
            constants.LAT1 = y1
            constants.LON2 = x2
            constants.LAT2 = y2
            data.plot_endpoints([x1,y1],[x2,y2])
            img2 = tk.PhotoImage(file=constants.TEMPDIR/"Image2.png")
            img2 = img2.subsample(7)
            imglabel.image = img2
            imglabel.configure(image=img2)

        # Image3 Creation
        def image3():
            if (constants.LON1 == constants.LON2 and constants.LAT1 == constants.LAT2): return
            path = algo.get_path(
                (constants.LON1,constants.LAT1),
                (constants.LON2,constants.LAT2),
                data.get_scale()[0],
                0.25
            )
            data.plot_points(path)
            img3 = tk.PhotoImage(file=constants.TEMPDIR/"Image3.png")
            img3 = img3.subsample(7)
            imglabel.image = img3
            imglabel.configure(image=img3)

        # Creating Frames
        bottomframe = tk.Frame(self)
        bottomframe.pack(side = "bottom")
        topframe = tk.Frame(self)
        topframe.pack(side = "top")

        # Best Path
        showpath = tk.Button(
            bottomframe,
            text='Display Best Path',
            command=lambda: image3()
        )
        showpath.pack(side="bottom", fill="both")

        # Plot Endpoints
        generate = tk.Button(bottomframe, text='Plot Endpoints', command=lambda: image2(float(x1.get()),float(y1.get()),float(x2.get()),float(y2.get())))
        generate.pack(side="bottom", fill="both")

        # Enter Start Point
        label = tk.Label(bottomframe, text="Enter long 1")
        label.pack(side="left")
        x1 = tk.Entry(bottomframe, width=20)
        x1.pack(side="left")

        label = tk.Label(bottomframe, text="Enter lat 1")
        label.pack(side="left")
        y1 = tk.Entry(bottomframe, width=20)
        y1.pack(side="left")

        # Enter End Point
        y2 = tk.Entry(bottomframe, width=20)
        y2.pack(side="right")
        label = tk.Label(bottomframe, text="Enter long 2")
        label.pack(side="right")

        x2 = tk.Entry(bottomframe, width=20)
        x2.pack(side="right")
        label = tk.Label(bottomframe, text="Enter lat 2")
        label.pack(side="right")

        # Initial Image
        img = tk.PhotoImage(file="White.png")
        img = img.subsample(2)
        imglabel = tk.Label(topframe, image=img, height=600, width=109)
        imglabel.image = img
        imglabel.pack(side="top", fill="both", expand=False)

        # Generate Image
        generate = tk.Button(topframe, text='Generate Image', command=lambda: image1(float(x.get()),float(y.get()),float(r.get())))
        generate.pack(side="bottom", fill="both")

        # Enter Radius
        r = tk.Entry(topframe, width=109)
        r.pack(side="bottom", fill="both")
        label = tk.Label(topframe, text="Enter Size (limit: 0.05 <= size <= 180, suggested: 0.1 <= size <= 10)")
        label.pack(side="bottom", fill="both")

        # Enter Y coordinate
        y = tk.Entry(topframe, width=109)
        y.pack(side="bottom", fill="both")
        label = tk.Label(topframe, text="Enter Latitude (limit: -89 <= lat <= 89, suggested: -85 <= lat <= 85)")
        label.pack(side="bottom", fill="both")

        # Enter X coordinate
        x = tk.Entry(topframe, width=109)
        x.pack(side="bottom", fill="both")
        label = tk.Label(topframe, text="Enter Longitude (limit: -180 <= lon <= 180, suggested: -175 <= lon <= 175)")
        label.pack(side="bottom", fill="both")

# File Input Page
class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # Image1 Creation
        def image1():
            input = filedialog.askopenfilename(initialdir="/")
            if (input[-3:] == "csv"):
                data.get_csvfile(input)
            elif (input[-2:] == "nv"):
                data.get_ncfile(input)
            else: return
            data.create_image()
            img1 = tk.PhotoImage(file=constants.TEMPDIR/"Image1.png")
            img1 = img1.subsample(7)
            imglabel.image = img1
            imglabel.configure(image=img1)

        # Image2 Creation
        def image2(x1, y1, x2, y2):
            bounds = data.get_bounds();
            if (x1 < bounds[0] or x2 < bounds[0]): return
            if (x1 > bounds[1] or x2 > bounds[1]): return
            if (y1 < bounds[2] or y2 < bounds[2]): return
            if (y1 > bounds[3] or y2 > bounds[3]): return
            constants.LON1 = x1
            constants.LAT1 = y1
            constants.LON2 = x2
            constants.LAT2 = y2
            data.plot_endpoints([x1,y1],[x2,y2])
            img2 = tk.PhotoImage(file=constants.TEMPDIR/"Image2.png")
            img2 = img2.subsample(7)
            imglabel.image = img2
            imglabel.configure(image=img2)

        # Image3 Creation
        def image3():
            if (constants.LON1 == constants.LON2 and constants.LAT1 == constants.LAT2): return
            path = algo.get_path(
                (constants.LON1,constants.LAT1),
                (constants.LON2,constants.LAT2),
                data.get_scale()[0],
                0.25
            )
            data.plot_points(path)
            img3 = tk.PhotoImage(file=constants.TEMPDIR/"Image3.png")
            img3 = img3.subsample(7)
            imglabel.image = img3
            imglabel.configure(image=img3)

        # Creating Frames
        bottomframe = tk.Frame(self)
        bottomframe.pack(side = "bottom")
        topframe = tk.Frame(self)
        topframe.pack(side = "top")

        # Initial Image
        img = tk.PhotoImage(file="White.png")
        img = img.subsample(2)
        imglabel = tk.Label(topframe, image=img, height=750, width=107)
        imglabel.image = img
        imglabel.pack(side="top", fill="both", expand=False)

        # File Selecter
        select = tk.Button(topframe, text='Select a .nc/.csv file', command=image1, width=107)
        select.pack(side="bottom", fill="both")

        # Best Path
        showpath = tk.Button(
            bottomframe,
            text='Display Best Path',
            command=lambda: image3()
        )
        showpath.pack(side="bottom", fill="both")

        # Plot Endpoints
        generate = tk.Button(bottomframe, text='Plot Endpoints', command=lambda: image2(float(x1.get()),float(y1.get()),float(x2.get()),float(y2.get())))
        generate.pack(side="bottom", fill="both")

        # Enter Start Point
        label = tk.Label(bottomframe, text="Enter x1")
        label.pack(side="left")
        x1 = tk.Entry(bottomframe, width=20)
        x1.pack(side="left")

        label = tk.Label(bottomframe, text="Enter y1")
        label.pack(side="left")
        y1 = tk.Entry(bottomframe, width=20)
        y1.pack(side="left")

        # Enter End Point
        y2 = tk.Entry(bottomframe, width=20)
        y2.pack(side="right")
        label = tk.Label(bottomframe, text="Enter y2")
        label.pack(side="right")

        x2 = tk.Entry(bottomframe, width=20)
        x2.pack(side="right")
        label = tk.Label(bottomframe, text="Enter x2")
        label.pack(side="right")

# Random Data Page
class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # Image1 Creation
        def image1(freq, height, water):
            data.create_random_terrain(freq, height, water)
            data.create_image()
            img1 = tk.PhotoImage(file=constants.TEMPDIR/"Image1.png")
            img1 = img1.subsample(7)
            imglabel.image = img1
            imglabel.configure(image=img1)

        # Image2 Creation
        def image2(x1, y1, x2, y2):
            bounds = data.get_bounds();
            if (x1 < bounds[0] or x2 < bounds[0]): return
            if (x1 > bounds[1] or x2 > bounds[1]): return
            if (y1 < bounds[2] or y2 < bounds[2]): return
            if (y1 > bounds[3] or y2 > bounds[3]): return
            constants.LON1 = x1
            constants.LAT1 = y1
            constants.LON2 = x2
            constants.LAT2 = y2
            data.plot_endpoints([x1,y1],[x2,y2])
            img2 = tk.PhotoImage(file=constants.TEMPDIR/"Image2.png")
            img2 = img2.subsample(7)
            imglabel.image = img2
            imglabel.configure(image=img2)

        # Image3 Creation
        def image3():
            if (constants.LON1 == constants.LON2 and constants.LAT1 == constants.LAT2): return
            path = algo.get_path(
                (constants.LON1,constants.LAT1),
                (constants.LON2,constants.LAT2),
                data.get_scale()[0],
                0.25
            )
            data.plot_points(path)
            img3 = tk.PhotoImage(file=constants.TEMPDIR/"Image3.png")
            img3 = img3.subsample(7)
            imglabel.image = img3
            imglabel.configure(image=img3)

        # Creating Frames
        bottomframe = tk.Frame(self)
        bottomframe.pack(side = "bottom")
        topframe = tk.Frame(self)
        topframe.pack(side = "top")

        # Best Path
        showpath = tk.Button(
            bottomframe,
            text='Display Best Path',
            command=lambda: image3()
        )
        showpath.pack(side="bottom", fill="both")

        # Plot Endpoints
        generate = tk.Button(bottomframe, text='Plot Endpoints', command=lambda: image2(float(x1.get()),float(y1.get()),float(x2.get()),float(y2.get())))
        generate.pack(side="bottom", fill="both")

        # Enter Start Point
        label = tk.Label(bottomframe, text="Enter x1")
        label.pack(side="left")
        x1 = tk.Entry(bottomframe, width=20)
        x1.pack(side="left")

        label = tk.Label(bottomframe, text="Enter y1")
        label.pack(side="left")
        y1 = tk.Entry(bottomframe, width=20)
        y1.pack(side="left")

        # Enter End Point
        y2 = tk.Entry(bottomframe, width=20)
        y2.pack(side="right")
        label = tk.Label(bottomframe, text="Enter y2")
        label.pack(side="right")

        x2 = tk.Entry(bottomframe, width=20)
        x2.pack(side="right")
        label = tk.Label(bottomframe, text="Enter x2")
        label.pack(side="right")

        # Initial Image
        img = tk.PhotoImage(file="White.png")
        img = img.subsample(2)
        imglabel = tk.Label(topframe, image=img, height=600, width=109)
        imglabel.image = img
        imglabel.pack(side="top", fill="both", expand=False)

        # Generate Image
        generate = tk.Button(topframe, text='Generate Image', command=lambda: image1(float(freq.get()),float(height.get()),float(water.get())))
        generate.pack(side="bottom", fill="both")

        # Enter Radius
        water = tk.Entry(topframe, width=109)
        water.pack(side="bottom", fill="both")
        label = tk.Label(topframe, text="Enter Water (suggested: 0 <= water <= 100), percentage of map that is water")
        label.pack(side="bottom", fill="both")

        # Enter Y coordinate
        height = tk.Entry(topframe, width=109)
        height.pack(side="bottom", fill="both")
        label = tk.Label(topframe, text="Enter Height (suggested: 100 <= height <= 8000), controls max altitude difference")
        label.pack(side="bottom", fill="both")

        # Enter X coordinate
        freq = tk.Entry(topframe, width=109)
        freq.pack(side="bottom", fill="both")
        label = tk.Label(topframe, text="Enter Frequency (suggested: 1 <= freq <= 100), controls how mountainous data will be")
        label.pack(side="bottom", fill="both")

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
    root.wm_geometry("960x960")
    root.mainloop()
