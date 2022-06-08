import tkinter as tk
from tkinter import ttk
from nrcemt.qeels.engine import qeels_engine_greeting


def main():
    ui()


def ui():
    # Configure panel
    # create window
    root = tk.Tk()
    # set title
    root.title("qEEls peak detection")
    # setting size of window(will change later)
    root.geometry("1500x700+10+0")
    selectedButton = tk.StringVar()

    # placment variables
    initHeight = 20
    initWidth = 50
    textWidth = 20
    textSeperation = 80
    secondWidth = 225

    ####################Bulk plasmon 1(bp1)####################
    bp1x = tk.IntVar()
    bp1y = tk.IntVar()
    bpWidth = tk.IntVar()

    # Creates radio buttons for bp1
    bulkPlasmon1_button = ttk.Radiobutton(
        root, text="Bulk Plasmon 1", value="bp1", variable=selectedButton)
    bulkPlasmon1_button.place(x=initWidth, y=initHeight)

    # Creates Text boxes for bp1
    # x input
    ttk.Label(root, text="X: ").place(x=initWidth, y=initHeight*2)
    bp1x_entry = ttk.Entry(root, textvariable=bp1x, width=7)
    bp1x_entry.place(x=initWidth+textWidth, y=initHeight*2)

    # y input
    ttk.Label(root, text="Y: ").place(
        x=initWidth+textSeperation, y=initHeight*2)
    bp1y_entry = ttk.Entry(root, textvariable=bp1y, width=7)
    bp1y_entry.place(x=initWidth+textSeperation+textWidth, y=initHeight*2)

    ####################Bulk plasmon 2####################
    bp2x = tk.IntVar()
    bp2y = tk.IntVar()
    # Creates radio buttons for bulk plasmon 2
    bulkPlasmon2_button = ttk.Radiobutton(
        root, text="Bulk Plasmon 2", value="bp2", variable=selectedButton)
    bulkPlasmon2_button.place(x=secondWidth, y=initHeight)

    # Creates Text boxes for bp12
    # x input
    ttk.Label(root, text="X: ").place(x=secondWidth, y=initHeight*2)
    bp2x_entry = ttk.Entry(root, textvariable=bp2x, width=7)
    bp2x_entry.place(x=secondWidth+textWidth, y=initHeight*2)

    # y input
    ttk.Label(root, text="Y: ").place(
        x=secondWidth+textSeperation, y=initHeight*2)
    bp2y_entry = ttk.Entry(root, textvariable=bp2y, width=7)
    bp2y_entry.place(x=secondWidth+textSeperation+textWidth, y=initHeight*2)

    # width
    ttk.Label(root, text="Width: ").place(x=secondWidth +
                                          2*textSeperation+textWidth, y=initHeight*2)
    bpWidth_entry = ttk.Entry(root, textvariable=bpWidth, width=7)
    bpWidth_entry.place(x=secondWidth+2*textSeperation +
                        3*textWidth+5, y=initHeight*2)
    # detect

    ####################Surface plasmon Upper 1 (spu1)####################
    spu1x = tk.IntVar()
    spu1y = tk.IntVar()
    spuWidth = tk.IntVar()

    # Creates radio buttons for spu1
    surfacePlasmonUpper1_button = ttk.Radiobutton(
        root, text="Surface Plasmon Upper 1", value="spu1", variable=selectedButton)
    surfacePlasmonUpper1_button.place(x=initWidth, y=initHeight*4)

    # Creates Text boxes for spu1
    # x input
    ttk.Label(root, text="X: ").place(x=initWidth, y=initHeight*5)
    spu1x_entry = ttk.Entry(root, textvariable=spu1x, width=7)
    spu1x_entry.place(x=initWidth+textWidth, y=initHeight*5)

    # y input
    ttk.Label(root, text="Y: ").place(
        x=initWidth+textSeperation, y=initHeight*5)
    spu1y_entry = ttk.Entry(root, textvariable=spu1y, width=7)
    spu1y_entry.place(x=initWidth+textSeperation+textWidth, y=initHeight*5)

    ####################Surface Plasmon upper 2(spu2)####################
    spu2x = tk.IntVar()
    spu2y = tk.IntVar()

    # Creates radio buttons for spu2
    surfacePlasmonUpper2_button = ttk.Radiobutton(
        root, text="Surface Plasmon Upper 2", value="spu2", variable=selectedButton)
    surfacePlasmonUpper2_button.place(x=secondWidth, y=initHeight*4)

    # Creates Text boxes for spu2
    # x input
    ttk.Label(root, text="X: ").place(x=secondWidth, y=initHeight*5)
    spu2x_entry = ttk.Entry(root, textvariable=spu2x, width=7)
    spu2x_entry.place(x=secondWidth+textWidth, y=initHeight*5)

    # y input
    ttk.Label(root, text="Y: ").place(
        x=secondWidth+textSeperation, y=initHeight*5)
    spu2y_entry = ttk.Entry(root, textvariable=spu2y, width=7)
    spu2y_entry.place(x=secondWidth+textSeperation+textWidth, y=initHeight*5)

    # width
    ttk.Label(root, text="Width: ").place(x=secondWidth +
                                          2*textSeperation+textWidth, y=initHeight*5)
    spuWidth_entry = ttk.Entry(root, textvariable=spuWidth, width=7)
    spuWidth_entry.place(x=secondWidth+2*textSeperation +
                         3*textWidth+5, y=initHeight*5)
    # detect
    ####################Surface plasmon lower 1 (spl1)####################
    spl1x = tk.IntVar()
    spl1y = tk.IntVar()
    splWidth = tk.IntVar()

    # Creates radio buttons for spl1
    surfacePlasmonLower1_button = ttk.Radiobutton(
        root, text="Surface Plasmon Lower 1", value="spl1", variable=selectedButton)
    surfacePlasmonLower1_button.place(x=initWidth, y=initHeight*7)

    # Creates Text boxes for spl1
    # x input
    ttk.Label(root, text="X: ").place(x=initWidth, y=initHeight*8)
    spl1x_entry = ttk.Entry(root, textvariable=spl1x, width=7)
    spl1x_entry.place(x=initWidth+textWidth, y=initHeight*8)

    # y input
    ttk.Label(root, text="Y: ").place(
        x=initWidth+textSeperation, y=initHeight*8)
    spl1y_entry = ttk.Entry(root, textvariable=spl1y, width=7)
    spl1y_entry.place(x=initWidth+textSeperation+textWidth, y=initHeight*8)

    ####################Surface Plasmon lower 2(spl2)####################
    spl2x = tk.IntVar()
    spl2y = tk.IntVar()

    # Creates radio buttons for Surface plasmon lower 2
    surfacePlasmonLower2_button = ttk.Radiobutton(
        root, text="Surface Plasmon Lower 2", value="spl2", variable=selectedButton)
    surfacePlasmonLower2_button.place(x=secondWidth, y=initHeight*7)

    # Creates Text boxes for spl2
    # x input
    ttk.Label(root, text="X: ").place(x=secondWidth, y=initHeight*8)
    spl2x_entry = ttk.Entry(root, textvariable=spl2x, width=7)
    spl2x_entry.place(x=secondWidth+textWidth, y=initHeight*8)

    # y input
    ttk.Label(root, text="Y: ").place(
        x=secondWidth+textSeperation, y=initHeight*8)
    spl2y_entry = ttk.Entry(root, textvariable=spl2y, width=7)
    spl2y_entry.place(x=secondWidth+textSeperation+textWidth, y=initHeight*8)

    # width
    ttk.Label(root, text="Width: ").place(x=secondWidth +
                                          2*textSeperation+textWidth, y=initHeight*8)
    splWidth_entry = ttk.Entry(root, textvariable=splWidth, width=7)
    splWidth_entry.place(x=secondWidth+2*textSeperation +
                         3*textWidth+5, y=initHeight*8)
    # detect

    message = tk.Label(root, text=qeels_engine_greeting())
    message.place(x=500, y=500)
    root.mainloop()


if __name__ == "__main__":
    main()
