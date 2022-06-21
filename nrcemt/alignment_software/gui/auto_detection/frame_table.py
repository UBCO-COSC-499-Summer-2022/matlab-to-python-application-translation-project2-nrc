import tkinter as tk

ROW_PADDING = 5
CELL_HEIGHT = 2
CELL_WIDTH = 3


class TableFrame(tk.Frame):

    def __init__(self, master, rows, columns, table_data):
        super().__init__(master)
        self.label_table = []
        for i in range(rows):
            for j in range(columns):
                if j == 0:
                    self.label_table.append([])

                self.label_table[i].append(
                    tk.Label(
                        self, bd=1, relief="solid",
                        text=str(table_data[i][j]),
                        width=CELL_WIDTH,
                        height=CELL_HEIGHT
                    )
                )
                self.label_table[i][j].grid(
                    row=i, column=j, sticky="nwse"
                )
