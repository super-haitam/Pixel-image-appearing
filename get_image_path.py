from tkinter import *

window = Tk()
window.geometry("500x100")
window.title("Get path of image")


def get_path():
    global path, end
    end = True
    path = path_entry.get()


Label(window, text="Paste the absolute path of the image").pack()
path_entry = Entry(window, width=50)
path_entry.pack()
Button(window, text="Enter", command=get_path).pack()

end = False
while not end:
    window.update()
window.destroy()


def get_img_path():
    return path
