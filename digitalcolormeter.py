from pyautogui import screenshot, position
from tkinter import Tk, Label, Button, Text
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
        self.color_msg = f"{'Saved Colors (S):':^60}\n" + "-"*60 + "\n"
        self.color_lst = []
        self.getScreen(initial=True)
        self.root.bind("u", self.getScreen)
        self.root.bind("s", self.saveColor)
        self.updateImg(initial=True)

    def getScreen(self, event=None, initial=False):
        self.screen = screenshot()
        if not initial:
            self.updateImg(repeat=False)
    
    def saveColor(self, event=None, max_len=5):
        notes = f"Pos: {str(self.pos):<12}\tRGB: {str(self.color):<17}\tHex: #{'%02x%02x%02x' % self.color}"
        self.color_lst = [notes] + self.color_lst[:max_len-1]
        self.save_text.delete(1.0, "end")
        self.save_text.insert(1.0, self.color_msg + "\n".join(self.color_lst))

    def updateImg(self, initial=False, repeat=True):
        if self.updatePos() or not repeat:
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
                       text="Update Screenshot (U)", 
                       command=self.getScreen).grid(row=1, column=1, padx=(0,20))
                self.save_text = Text(self.root, height=7, width=60, borderwidth=0)
                self.save_text.insert(1.0, self.color_msg)
                self.save_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
            else:
                self.img_label.config(image=self.img)
                self.text_label.config(text=self.getLabelText())
        if repeat:
            self.root.after(10, self.updateImg)

    def updatePos(self):
        old_pos = self.pos
        self.pos = tuple(self.disp_scale * i for i in position())
        return self.pos != old_pos
    
    def getLabelText(self):
        return f"Position:\n   {self.pos}\n\n" + \
               "".join(f"{comp}: {self.color[num]}\n" for num, comp in enumerate(("R", "G", "B"))) + \
               f"\nHex:\n   #{'%02x%02x%02x' % self.color}"

if __name__ == '__main__':
    root = Tk()
    meter = Meter(root)
    root.mainloop()