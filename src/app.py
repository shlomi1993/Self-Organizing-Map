# Shlomi Ben-Shushan 311408264


import src.parser as parser
import src.som as som
from src.style import fonts, colors, scale
from tkinter import Tk, Text, Button, Canvas, filedialog, messagebox, NW, END
from prettytable import PrettyTable
from ntpath import basename


WINDOW_H = 720
WINDOW_W = 1150
CANVAS_H = 690
CANVAS_W = 690

SIZE_S = 12
SIZE_M = round(1.5 * SIZE_S)
SIZE_M_PAD = SIZE_M + 2  # padding

CANVAS: Canvas
CELLS: dict
POLYGONS = {}
POPUP_RECT = -1
POPUP_TEXT = -1


def pop(pos, x, y):
    global POPUP_TEXT, POPUP_RECT, CELLS
    (i, j) = pos
    if POPUP_TEXT or POPUP_RECT:
        CANVAS.delete(POPUP_TEXT)
        CANVAS.delete(POPUP_RECT)
    if pos in CELLS.keys():
        cell_list, cell_class = CELLS[pos]
        if cell_class > 0:
            msg = f'Cell ({i}, {j}):\n'
            longest = 0
            for vr in cell_list:
                line = f' - {vr.town} ({vr.cluster})\n'
                if longest < len(line):
                    longest = len(line)
                msg += line
            offset_x = longest * 6 + 10
            offset_y = (len(cell_list) + 1) * 15 + 8
            xx = x - offset_x
            yy = y - offset_y
            POPUP_RECT = CANVAS.create_rectangle(xx, yy, x, y, fill=colors.notes)
            POPUP_TEXT = CANVAS.create_text(xx + 4, yy + 4, text=msg, anchor=NW)


def motion(event):
    x, y = event.x, event.y
    for k in POLYGONS.keys():
        x1, x2, y1, y2 = k
        if x1 <= x <= x2 and y1 <= y <= y2:
            pop(POLYGONS[k], x, y)
            break
        else:
            global POPUP_TEXT, POPUP_RECT
            CANVAS.delete(POPUP_TEXT)
            CANVAS.delete(POPUP_RECT)


def info(towns):
    t_towns = PrettyTable()
    t_towns.align = 'l'
    t_towns.field_names = ['Town', 'Cluster', 'Cell']
    for town, (cluster, cell) in towns.items():
        t_towns.add_row([town, cluster, cell.pos])
    t_rep = PrettyTable()
    t_rep.border = False
    t_rep.align = 'l'
    t_rep.field_names = ['Representative', 'Towns (cluster)']
    for pos, (vrs, _) in CELLS.items():
        if len(vrs) > 0:
            towns_str = ''
            for vr in vrs:
                towns_str += f'{vr.town} ({vr.cluster}), '
            towns_str = towns_str[:-2]
            t_rep.add_row([str(pos), towns_str])
    print(t_rep)
    return t_towns


class App(Tk):

    def __init__(self):

        # Initialize parent and window.
        super().__init__()
        self.geometry(f'{WINDOW_W}x{WINDOW_H}')
        self.minsize(WINDOW_W, WINDOW_H)
        self.maxsize(WINDOW_W, WINDOW_H)
        self.configure(background=colors.app, highlightcolor=colors.highlight)
        self.title('Self Organizing Map')

        # Closing message
        def on_closing():
            if messagebox.askokcancel('Quit', 'Do you want to quit?'):
                self.destroy()
                exit(0)
        self.protocol("WM_DELETE_WINDOW", on_closing)

        # Canvas
        self.canvas = Canvas(bg=colors.white, highlightbackground=colors.outlines, width=CANVAS_W, height=CANVAS_H)
        self.canvas.place(relx=0.38, rely=0.01)
        global CANVAS
        CANVAS = self.canvas
        self.canvas.bind('<Motion>', motion)

        # Console
        self.console = Text(master=self, height=40, width=50, bg=colors.console_bg, fg=colors.console_text)
        self.console.place(relx=0.01, rely=0.01)
        welcome = 'Hi,\n\nThis program created by Shlomi Ben-Shushan.' \
                  '\nPlease select a valid csv input file.\nThen click "Run".\n'
        self.console.insert(END, welcome)
        self.console.tag_configure('center', justify='center')

        # Browse button
        self.file = ''
        self.browse_btn = Button(
            master=self,
            width=14,
            bg=colors.console_bg,
            fg=colors.white,
            relief='groove',
            font=fonts.bold,
            text='Select File',
            command=self.__browse
        )
        self.browse_btn.place(relx=0.01, rely=0.93)
        self.file_name_area = Text(master=self, height=1, width=21, bg=colors.app, fg=colors.black, borderwidth=0)
        self.file_name_area.place(relx=0.14, rely=0.94)

        # Run button
        self.run_btn = Button(
            master=self,
            width=8,
            bg=colors.console_bg,
            fg=colors.white,
            relief='groove',
            font=fonts.bold,
            text='Run \u23f5',
            command=self.__run
        )
        self.run_btn.place(relx=0.29, rely=0.93)

    def __browse(self):
        types = (('Text files', "*.csv*"), ('all files', '*.*'))
        self.file = filedialog.askopenfilename(initialdir=".", title='Select a File', filetypes=types)
        file_name = basename(self.file)
        self.file_name_area.insert(END, file_name)

    def __run(self):
        if self.file:
            data = parser.parse(self.file)
            solutions, positions = som.train(data, epochs=10, learning_rate=0.1)
            town_to_cell, cell_to_vectors = som.analyze(solutions[-1], positions)
            global CELLS
            CELLS = cell_to_vectors
            t_towns = info(town_to_cell)
            self.console.delete('1.0', END)
            self.console.insert(END, str(t_towns))
            self.console.tag_add('center', '1.0', 'end')
            self.__draw_scale()
            self.__draw_hexagonal_grid(size=5)
        else:
            title = 'Hint'
            msg = 'Make sure you have selected an input file first.'
            messagebox.showinfo(title, msg)

    def __draw_scale(self):
        x0 = 70
        y0 = 100
        y1 = 140
        self.canvas.create_text(x0 + 100, y0 - 15, text='Economic Clusters', font=fonts.big)
        for i, m in scale.items():
            xi = x0 + 50 * i
            xj = xi + 50
            ii = i if i > 0 else 'n/a'
            self.canvas.create_rectangle(xi, y0, xj, y1, fill=m)
            self.canvas.create_text(xi + 25, y0 + 20, text=ii, font=fonts.regular)

    def __draw_hexagon(self, top_x, top_y, color, label):
        x0 = top_x
        y0 = top_y
        x1 = x0 + SIZE_M
        y1 = y0 + SIZE_S
        x2 = x1
        y2 = y1 + SIZE_M
        x3 = x0
        y3 = y2 + SIZE_S
        x4 = x0 - SIZE_M
        y4 = y2
        x5 = x4
        y5 = y1
        self.canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, fill=color, outline=colors.black)
        self.canvas.create_text(x0, y0 + SIZE_M_PAD, text=label)
        return x4, x1, y1, y2

    def __draw_hexagonal_grid(self, size):
        start_x = round(CANVAS_W / 2) - SIZE_M * 4.5
        start_y = round(CANVAS_H / 2) - SIZE_M * 4.5
        for (i, j), (vrs, c) in CELLS.items():
            if i < size:
                x = start_x + j * 2 * SIZE_M_PAD - i * SIZE_M_PAD
            else:
                x = start_x + j * 2 * SIZE_M_PAD + (i - size - 3) * SIZE_M_PAD
            y = start_y + i * 2 * (SIZE_M - 1)
            key = self.__draw_hexagon(x, y, scale[c], len(vrs))
            POLYGONS[key] = (i, j)
        hint = 'Hint: Move your mouse over the hexagons.'
        self.canvas.create_text(CANVAS_W // 2, CANVAS_H - 15, text=hint, font=fonts.small)
