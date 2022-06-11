# Shlomi Ben-Shushan 311408264


# File: app.py
# Content: All the definitions and settings regard to the application.


from ntpath import basename
from tkinter import Tk, Text, Button, Frame, Canvas, filedialog, messagebox
from prettytable import PrettyTable
from src.parser import parse
from src.som import train, analyze
from src.evaluation import plot_errors_per_epoch
from src.style import fonts, colors, scale
from src.analyze_window import pop_analyze_window
from src.params_window import pop_params_window


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
    """
    This function creates a context note when the mouse hovers above a hexagon.
    :param pos: the position of the hovered hexagon.
    :param x: the x-coordinate of the mouse pointer.
    :param y: the y-coordinate of the mouse pointer.
    :return:
    """
    global POPUP_TEXT, POPUP_RECT, CELLS
    (i, j) = pos

    # Clear previous note.
    if POPUP_TEXT or POPUP_RECT:
        CANVAS.delete(POPUP_TEXT)
        CANVAS.delete(POPUP_RECT)

    # If the cell represents any voting vector, show a note adjacent to the
    # mouse pointer.
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
        POPUP_TEXT = CANVAS.create_text(xx + 4, yy + 4, text=msg, anchor='nw')


def motion(event):
    """
    This function catches the event of mouse moves and checks if the pointer is
    hovering above a hexagon.
    :param event: and event from the main event loop.
    :return: None.
    """
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
    """
    This function get the town-to-cell mapper and the global CELLS, which is a
    cell-to-towns mapper, and creates information structures. It creates a table
    for the app's console, and prints additional information to the terminal.
    :param towns: a dictionary that maps a town-name to cells.
    :return: a PrettyTable of the mapping.
    """
    t_towns = PrettyTable()
    t_towns.align = 'l'
    t_towns.field_names = ['Town', 'Cluster', 'Cell']
    for town, (cluster, cell) in towns.items():
        t_towns.add_row([town, cluster, cell.pos])
    print('Printing representative cell => represented towns (and cluster)')
    for pos, (vrs, _) in CELLS.items():
        if len(vrs) > 0:
            towns_str = ''
            for vr in vrs:
                towns_str += f'{vr.town} ({vr.cluster}), '
            towns_str = towns_str[:-2]
            print(pos, '=>', towns_str)
    return t_towns


def no_input_message():
    """
    This function pops a "no input" info message.
    :return:
    """
    title = 'Hint'
    msg = 'Make sure you have selected an input file first.'
    messagebox.showinfo(title, msg)


class App(Tk):
    """
    This class inherits the Tk (-inter) class that creates a basic app with
    mainloop useful graphic tools (basic) and functions.
    """

    def __init__(self):

        # Initialize parent and window.
        super().__init__()
        self.geometry(f'{WINDOW_W}x{WINDOW_H}')
        self.minsize(WINDOW_W, WINDOW_H)
        self.maxsize(WINDOW_W, WINDOW_H)
        self.configure(background=colors.app, highlightcolor=colors.highlight)
        self.title('Self Organizing Map')

        # Closing message.
        def on_closing():
            if messagebox.askokcancel('Quit', 'Do you want to quit?'):
                self.destroy()
                exit(0)
        self.protocol("WM_DELETE_WINDOW", on_closing)

        # Create a canvas.
        self.canvas = Canvas(
            bg=colors.white,
            highlightbackground=colors.outlines,
            width=CANVAS_W,
            height=CANVAS_H
        )
        self.canvas.place(relx=0.38, rely=0.01)
        global CANVAS
        CANVAS = self.canvas
        self.canvas.bind('<Motion>', motion)

        # Create a console
        self.console = Text(
            master=self,
            height=37,
            width=50,
            bg=colors.io_bg,
            fg=colors.io_text
        )
        self.console.place(relx=0.01, rely=0.01)
        welcome = 'Hi,\n\nThis program created by Shlomi Ben-Shushan.' \
                  '\nPlease select a valid CSV input file.\nThen click "Run".\n'
        self.console.insert('end', welcome)
        self.console.tag_configure('center', justify='center')

        # Create a configuration frame
        self.config = Frame(
            master=self,
            bg=colors.app,
        )
        self.config.place(relx=0.01, rely=0.861)

        # Create a browse frame.
        self.browse_frame = Frame(
            master=self.config,
            bg=colors.app,
        )

        # Browse label and button.
        self.browse_frame.pack()
        self.file = ''
        self.browse_btn = Button(
            master=self.browse_frame,
            width=14,
            bg=colors.button,
            fg=colors.white,
            relief='raised',
            font=fonts.bold,
            text='Select File',
            command=self.__browse
        )
        self.browse_btn.grid(row=0, column=0, sticky='w')
        self.file_name_area = Text(
            master=self.browse_frame,
            height=1,
            width=19,
            bg=colors.io_bg,
            fg=colors.io_text,
            font=fonts.io
        )
        self.file_name_area.bind('<Key>', lambda e: 'break')
        self.file_name_area.grid(row=0, column=2, padx=15, sticky='w')

        # Create another frame for analyze, set parameters and run buttons.
        self.buttons_frame = Frame(
            master=self.config,
            bg=colors.app,
        )
        self.buttons_frame.pack(side='left')

        # Analyze button.
        self.start_lr = 0.01
        self.end_lr = 1.0
        self.step_lr = 0.05
        self.analyze_btn = Button(
            master=self.buttons_frame,
            width=14,
            bg=colors.button,
            fg=colors.white,
            relief='raised',
            font=fonts.bold,
            text='Analyze LR',
            command=self.__analyze
        )
        self.analyze_btn.grid(row=0, column=0, pady=12, sticky='w')

        # Set parameters button.
        self.epochs = 10
        self.lr = 0.1
        self.params_btn = Button(
            master=self.buttons_frame,
            width=14,
            bg=colors.button,
            fg=colors.white,
            relief='raised',
            font=fonts.bold,
            text='Set Params',
            command=self.__set_params
        )
        self.params_btn.grid(row=0, column=1, padx=15, pady=12, sticky='s')

        # Run button.
        self.run_btn = Button(
            master=self.buttons_frame,
            width=10,
            bg=colors.button_prime,
            fg=colors.white,
            relief='groove',
            font=fonts.bold,
            text='Run \u23f5',
            command=self.__run
        )
        self.run_btn.grid(row=0, column=2, padx=0, pady=12, sticky='e')

    def __browse(self):
        """
        This method shows the user a new window that allows her to browse files
        and select a valid CSV input file.
        :return: None.
        """
        types = (('Text files', "*.csv*"), ('all files', '*.*'))
        self.file = filedialog.askopenfilename(initialdir=".",
                                               title='Select a File',
                                               filetypes=types)
        file_name = basename(self.file)
        self.file_name_area.insert('end', file_name)

    def __analyze(self):
        """
        This method shows the user a new window that allows him to analyze a
        range of learning rates and display assisting plots.
        :return: None.
        """
        if self.file:
            pop_analyze_window(self)
        else:
            no_input_message()

    def __set_params(self):
        """
        This method shows the user a new window that allows her to change the
        learning-rate and epochs parameters.
        :return: None.
        """
        pop_params_window(self)

    def __run(self):
        """
        This method allows the user to run the SOM algorithm, if the input file
        is set.
        :return: None.
        """
        if self.file:

            # Parse.
            data = parse(self.file)

            # Train.
            results = train(data, epochs=self.epochs, learning_rate=self.lr)
            solutions, model, q_errors, t_errors = results

            # Analyze.
            town_to_cell, cell_to_vectors = analyze(results=solutions[-1],
                                                    positions=model.positions)

            # Output.
            global CELLS
            CELLS = cell_to_vectors
            t_towns = info(town_to_cell)
            self.console.delete('1.0', 'end')
            self.console.insert('end', str(t_towns))
            self.console.tag_add('center', '1.0', 'end')
            self.__draw_scale()
            self.__draw_hexagonal_grid(size=5)

            # Evaluate.
            plot_errors_per_epoch(q_errors, t_errors)

        else:
            no_input_message()

    def __draw_scale(self):
        """
        This method draw an economic cluster scale on the canvas.
        :return: None.
        """
        x0 = 70
        y0 = 100
        y1 = 140
        self.canvas.create_text(x0 + 100, y0 - 15,
                                text='Economic Clusters', font=fonts.big)
        for i, m in scale.items():
            xi = x0 + 50 * i
            xj = xi + 50
            ii = i if i > 0 else 'n/a'
            self.canvas.create_rectangle(xi, y0, xj, y1, fill=m)
            self.canvas.create_text(xi + 25, y0 + 20, text=ii,
                                    font=fonts.regular)

    def __draw_hexagon(self, top_x, top_y, color, label):
        """
        This method is responsible for drawing ONE hexagon on the canvas.
        :param top_x: the x coordinate to the top vertex.
        :param top_y: the y coordinate to the top vertex.
        :param color: the color of the hexagon.
        :param label: the text to write inside it.
        :return:
        """
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
        self.canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5,
                                   y5, fill=color, outline=colors.black)
        self.canvas.create_text(x0, y0 + SIZE_M_PAD, text=label)
        return x4, x1, y1, y2

    def __draw_hexagonal_grid(self, size):
        """
        This method draw the resulted hexagonal grid using __draw_hexagon()
        :param size: the size of the hexagon (the edge of it).
        :return: None.
        """
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
