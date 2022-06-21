import tkinter as tk


class TableFrame(tk.Frame):

    def __init__(self, master, rows, columns, table_data):
        super().__init__(master)
        self.label_table = []
        for i in range(rows):
            for j in range(columns):
                if i == 0:
                    self.columnconfigure(j, weight=1)
                if j == 0:
                    self.rowconfigure(i, weight=1)
                    self.label_table.append([])

                self.label_table[i].append(
                    tk.Label(
                        self, bd=1, relief="solid",
                        text=str(table_data[i][j]),
                    )
                )
                self.label_table[i][j].grid(
                    row=i, column=j, sticky="nwse"
                )
