import tkinter as tk
import tkinter.font as tkFont


class App:
    def __init__(self, root):
        # setting title
        root.title("undefined")
        # setting window size
        width = 1167
        height = 681
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_388 = tk.Label(root)
        ft = tkFont.Font(family="Times", size=10)
        GLabel_388["font"] = ft
        GLabel_388["fg"] = "#333333"
        GLabel_388["justify"] = "center"
        GLabel_388["text"] = "label"
        GLabel_388.place(x=70, y=50, width=1016, height=530)

        GButton_26 = tk.Button(root)
        GButton_26["bg"] = "#f7f7f7"
        ft = tkFont.Font(family="Times", size=10)
        GButton_26["font"] = ft
        GButton_26["fg"] = "#273134"
        GButton_26["justify"] = "center"
        GButton_26["text"] = "Button"
        GButton_26.place(x=60, y=630, width=70, height=25)
        GButton_26["command"] = self.GButton_26_command

        GButton_542 = tk.Button(root)
        GButton_542["bg"] = "#f7f7f7"
        ft = tkFont.Font(family="Times", size=10)
        GButton_542["font"] = ft
        GButton_542["fg"] = "#273134"
        GButton_542["justify"] = "center"
        GButton_542["text"] = "Button"
        GButton_542.place(x=210, y=630, width=70, height=25)
        GButton_542["command"] = self.GButton_542_command

        GButton_505 = tk.Button(root)
        GButton_505["bg"] = "#f7f7f7"
        ft = tkFont.Font(family="Times", size=10)
        GButton_505["font"] = ft
        GButton_505["fg"] = "#273134"
        GButton_505["justify"] = "center"
        GButton_505["text"] = "Button"
        GButton_505.place(x=340, y=630, width=70, height=25)
        GButton_505["command"] = self.GButton_505_command

        GButton_341 = tk.Button(root)
        GButton_341["bg"] = "#f7f7f7"
        ft = tkFont.Font(family="Times", size=10)
        GButton_341["font"] = ft
        GButton_341["fg"] = "#273134"
        GButton_341["justify"] = "center"
        GButton_341["text"] = "Button"
        GButton_341.place(x=460, y=630, width=70, height=25)
        GButton_341["command"] = self.GButton_341_command

        GButton_526 = tk.Button(root)
        GButton_526["bg"] = "#f7f7f7"
        ft = tkFont.Font(family="Times", size=10)
        GButton_526["font"] = ft
        GButton_526["fg"] = "#273134"
        GButton_526["justify"] = "center"
        GButton_526["text"] = "Button"
        GButton_526.place(x=580, y=630, width=70, height=25)
        GButton_526["command"] = self.GButton_526_command

        GButton_815 = tk.Button(root)
        GButton_815["bg"] = "#f7f7f7"
        ft = tkFont.Font(family="Times", size=10)
        GButton_815["font"] = ft
        GButton_815["fg"] = "#273134"
        GButton_815["justify"] = "center"
        GButton_815["text"] = "Button"
        GButton_815.place(x=700, y=630, width=70, height=25)
        GButton_815["command"] = self.GButton_815_command

        GButton_863 = tk.Button(root)
        GButton_863["bg"] = "#f7f7f7"
        ft = tkFont.Font(family="Times", size=10)
        GButton_863["font"] = ft
        GButton_863["fg"] = "#273134"
        GButton_863["justify"] = "center"
        GButton_863["text"] = "Button"
        GButton_863.place(x=820, y=630, width=70, height=25)
        GButton_863["command"] = self.GButton_863_command

        GButton_217 = tk.Button(root)
        GButton_217["bg"] = "#f7f7f7"
        ft = tkFont.Font(family="Times", size=10)
        GButton_217["font"] = ft
        GButton_217["fg"] = "#273134"
        GButton_217["justify"] = "center"
        GButton_217["text"] = "Button"
        GButton_217.place(x=930, y=630, width=70, height=25)
        GButton_217["command"] = self.GButton_217_command

    def GButton_26_command(self):
        print("command")

    def GButton_542_command(self):
        print("command")

    def GButton_505_command(self):
        print("command")

    def GButton_341_command(self):
        print("command")

    def GButton_526_command(self):
        print("command")

    def GButton_815_command(self):
        print("command")

    def GButton_863_command(self):
        print("command")

    def GButton_217_command(self):
        print("command")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
