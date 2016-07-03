import Tkinter as tk
import random

root = tk.Tk()
root.title("__M_O_O_N___E_X_P_R_E_S_S__")

PHOTO_TITL = tk.PhotoImage(file="moonsur.gif")
PHOTO_GO = tk.PhotoImage(file="go.gif")
PHOTO_WIN = tk.PhotoImage(file="win.gif")
PHOTO_START = tk.PhotoImage(file="moonsurtitle.gif")
PHOTO_BUT1 = tk.PhotoImage(file="Quit.gif")
PHOTO_BUT2 = tk.PhotoImage(file="newgame.gif")
PHOTO_H3 = tk.PhotoImage(file="hearts3.gif")
PHOTO_H2 = tk.PhotoImage(file="hearts2.gif")
PHOTO_H1 = tk.PhotoImage(file="hearts.gif")
PHOTO_H0 = tk.PhotoImage(file="hearts0.gif")
PHOTO_LP = tk.PhotoImage(file="padleft.gif")
PHOTO_LP = tk.PhotoImage(file="padright.gif")
WIDTH = 700  # Width of the canvas
HEIGHT = 500  # Height of the canvas
RAD = 20  # Ball's radius
CIRCLE = [WIDTH / 2 - RAD, HEIGHT / 2 - RAD,
         WIDTH / 2 + RAD, HEIGHT / 2 + RAD]
         # The position of the circle on the canvas.


PADS_H = 120  # The height of the pad
PADS_W = 20  # The width of the pad
PAD_VEL = 15  # Paddle velocity

#Global values
SPEEDS = [-1, 1, -1, 1]
count = 0
level = 0
respawncounter = 0
accel = 0
x1 = 1*SPEEDS[1]  # Direction|speed of the ball on the canvas (x axis)
y2 = 1*SPEEDS[0]  # Direction|speed of the ball on the canvas (y axis)
levellab = tk.StringVar()

# Describes canvas's parameters and objects on the canvas
Surface = tk.Canvas(master=root, width=WIDTH, height=HEIGHT, borderwidth=0)
Surface.pack(fill=tk.BOTH, expand = tk.YES) # the pack geometry is used
Surface.create_image(350, 250, image=PHOTO_START, tag = "photostart")


def quits():
    root.quit()


def new_game():
    global level, count, x1, y2, itemlp, itemrp, respawncounter, accel
    global timerevent, padcl, padcr, ballco
    Surface.delete("ball", "game_over", "photostart", "win", "phototitl",
                  "itemrp", "itemlp", "padleft", "padright")
    accel = 1
    count = 0
    level = 0
    respawncounter = 0
    random.shuffle(SPEEDS)
    x1 = 1*SPEEDS[1]*accel
    y2 = 1*SPEEDS[0]*accel

    Surface.create_image(350, 250, image=PHOTO_TITL, tag= "phototitl")
    Surface.create_oval(CIRCLE, tag = "ball", fill = "White", outline= "White")
    Surface.create_rectangle([2, 2, PADS_W, PADS_H], tag = "padleft")
    Surface.create_rectangle([WIDTH-PADS_W+2, 2, WIDTH, PADS_H],
                            tag = "padright")
    itemlp = Surface.create_image(10, 60, image = PHOTO_LP, tag = "itempl")
    itemrp = Surface.create_image(692, 60, image = PHOTO_LP, tag = "itemrp")
    labelh = tk.Label(master=root, image=PHOTO_H3, bg="black").place(x=485, y = 7)
    padcl = Surface.coords("padleft")
    padcr = Surface.coords("padright")
    ballco = Surface.coords("ball")

    root.after_cancel(timerevent)
    drawcirc()


def respawn():
    '''Respawn the ball in the middle'''
    global respawncounter
    Surface.delete("ball")
    Surface.create_oval(CIRCLE, tag = "ball", fill = "White", outline= "White")

    if respawncounter == 1:
        labelh = tk.Label(master=root, image=PHOTO_H2, bg="black")
        labelh.place(x=485, y = 7)
    elif respawncounter == 2:
        labelh = tk.Label(master=root, image=PHOTO_H1, bg="black")
        labelh.place(x=485, y = 7)
    elif respawncounter == 3:
        Surface.delete("ball")
        labelh = tk.Label(master=root, image=PHOTO_H0, bg="black")
        labelh.place(x=485, y = 7)
        Surface.create_image(350, 250, image=PHOTO_GO, tag = "game_over")
    else:
        new_game()


def drawcirc():
    '''Ball mobility'''
    global x1, y2, count, respawncounter, padcl, padcr, ballco
    global accel, level, timerevent
    if 0 <= count <= 1:
        accel = 2
        level = 0
        Surface.move ("ball", x1*accel, y2*accel)
    if 2 <= count <= 4:
        accel = 2.5
        level = 1
        Surface.move ("ball", x1*accel, y2*accel)
    if 5 <= count <= 8:
        accel = 3
        level = 2
        Surface.move ("ball", x1*accel, y2*accel)
    if 8<= count <= 12:
        accel = 4
        level = 3
        Surface.move ("ball", x1*accel, y2*accel)
    if count >= 13:
        Surface.create_image(350, 250, image=PHOTO_WIN, tag="win")

    if Surface.find_overlapping(0, HEIGHT, WIDTH, HEIGHT):
        y2 = -y2
    if Surface.find_overlapping(0, 0, WIDTH, 0):
        y2 = -y2

    padcl = Surface.coords("padleft")
    padcr = Surface.coords("padright")
    ballco = Surface.coords("ball")
    if ballco[0] < padcl[2]:
        if padcl[3] + RAD >= ballco[3] and padcl[1] - RAD <= ballco[1]:
            x1 = -x1
            count += 1
    if ballco[0] <= 0:
            respawncounter += 1
            respawn()
    if ballco[2] > padcr[0]:
        if padcr[3] + RAD >= ballco[3] and padcr[1] - RAD <= ballco[1]:
            x1 = -x1
            count +=1
    if ballco[2] >= 700:
            respawncounter += 1
            respawn()

    levellab.set(str(level))
    timerevent = root.after(1, drawcirc)
timerevent = root.after(1, drawcirc)


# Describes the logic of the pads mobility.

# The mobility of the left pad
def keypress(a):
    global itemlp, itemrp
    Surface.move("padleft", 0, -PAD_VEL)
    Surface.move(itemlp, 0, -PAD_VEL)
    if Surface.find_overlapping(0, 0, WIDTH, 0):  # Stop's pad on the border
        Surface.move("padleft", 0, PAD_VEL)
        Surface.move(itemlp, 0, PAD_VEL)
    Surface.update()
def keypress2(d):
    global itemlp, itemrp
    Surface.move("padleft", 0, PAD_VEL)
    Surface.move(itemlp, 0, PAD_VEL)
    if Surface.find_overlapping(0, 500, 700, 500):  # Stop's pad on the border
        Surface.move("padleft", 0, -PAD_VEL)
        Surface.move(itemlp, 0, -PAD_VEL)
    Surface.update()
# The mobility of the right pad
def keypress3(Left):
    global itemlp, itemrp
    Surface.move("padright", 0, -PAD_VEL)
    Surface.move(itemrp, 0, -PAD_VEL)
    if Surface.find_overlapping(0, 0, WIDTH, 0):  # Stop's pad on the border
        Surface.move("padright", 0, PAD_VEL)
        Surface.move(itemrp, 0, PAD_VEL)
    Surface.update()
def keypress4(Right):
    global itemlp, itemrp
    Surface.move("padright", 0, PAD_VEL)
    Surface.move(itemrp, 0, PAD_VEL)
    if Surface.find_overlapping(0, 502, 700, 502):  # Stop's pad on the border
        Surface.move("padright", 0, -PAD_VEL)
        Surface.move(itemrp, 0, -PAD_VEL)
    Surface.update()


label_level = tk.Label(master=root, textvariable=levellab, bg="black",
font=("Helvetica", 15), fg = "#EC3572")
label_level.place(x=262, y = 7)
label_level2 = tk.Label(master=root, text="Level is",bg="black",
font=("Helvetica", 15), fg = "#EC3572")
label_level2.place(x=190, y = 7)
button_1 = tk.Button(master = root, image=PHOTO_BUT2, command=new_game)
button_1.place(x=268, y=500)
button_2 = tk.Button(master = root, image=PHOTO_BUT1, command=quits)
button_2.place(x=613, y=517)

frame = tk.Frame(master = root, width=0, height=61)
frame.bind("<KeyPress-a>", keypress)
frame.bind("<KeyPress-d>", keypress2)
frame.bind("<KeyPress-Left>", keypress3)
frame.bind("<KeyPress-Right>", keypress4)
frame.pack()
frame.focus_set()

root.mainloop()
