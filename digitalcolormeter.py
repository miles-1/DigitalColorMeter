from pyautogui import screenshot, position
from tkinter import Tk, Label, Button
from PIL import ImageDraw, ImageTk
from sys import platform

class Meter:
    def __init__(self, root):
        self.disp_scale = 2 if platform == "darwin" else 1
        self.root = root
        self.root.title("Digital Color Meter")
        self.pos, self.img, self.color = (None,) * 3
        self.view_rad, self.scale = 7, 15
        self.mag = self.scale * (2 * self.view_rad + 1)
        self.getScreen()
        self.updateImg(True)
        self.root.bind("<Motion>", lambda _: self.updateImg())

    def getScreen(self):
        self.screen = screenshot()

    def updateImg(self, initial=False):
        if self.updatePos():
            x, y = self.pos
            c, m, s = self.view_rad, self.mag, self.scale
            self.color = self.screen.getpixel((x, y))[:3]
            screen = self.screen.crop((x-c, y-c, x+(c+1), y+(c+1))) \
                                .resize((m,)*2, 0)
            draw = ImageDraw.Draw(screen)
            r_min = s * c - 2
            r_max = s * (c + 1) + 1
            draw.rectangle([(r_min,)*2,(r_max,)*2], outline=(255,)*3, width=2)
            draw.rectangle([(r_min-1,)*2,(r_max+1,)*2], outline=(90,)*3)
            self.img = ImageTk.PhotoImage(screen)
            if initial:
                self.img_label = Label(self.root, image=self.img, borderwidth=1, relief="solid")
                self.img_label.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
                self.text_label = Label(self.root, text=self.getLabelText(), justify="left")
                self.text_label.grid(row=0, column=1, padx=(0,20), sticky="w")
                Button(self.root, 
                       text="Update Screenshot", 
                       command=self.getScreen).grid(row=1, column=1, padx=(0,20))
            else:
                self.img_label.config(image=self.img)
                self.text_label.config(text=self.getLabelText())

    def updatePos(self):
        old_pos = self.pos
        self.pos = tuple(self.disp_scale * i for i in position())
        return self.pos != old_pos
    
    def getLabelText(self):
        return f"Position:\n   ({self.pos[0]}, {self.pos[1]})\n\n" + \
               f"R: {self.color[0]}\nG: {self.color[1]}\nB: {self.color[2]}\n\n" + \
               f"Hex:\n   #{'%02x%02x%02x' % self.color}"

if __name__ == '__main__':
    root = Tk()
    meter = Meter(root)
    root.mainloop()