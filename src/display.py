# Shlomi Ben-Shushan 311408264


from tkinter import Tk, LabelFrame, Label, Canvas, Button, messagebox


res = 400
factor1 = 12
factor2 = round(1.5 * factor1)
factor3 = factor2 + 2  # padding


mapper = {
    0: '#ffffff',
    1: '#9e0142',
    2: '#d53e4f',
    3: '#f46d43',
    4: '#fdae61',
    5: '#fee08b',
    6: '#e6f598',
    7: '#abdda4',
    8: '#66c2a5',
    9: '#3288bd',
    10: '#5e4fa2',
}


class HexagonalDisplay(Tk):

    def __init__(self, clusters, size):
        super().__init__()
        self.geometry(f'{res}x{res}')
        self.minsize(res, res)
        self.maxsize(res, res)
        self.title('Self Organizing Map')
        self.frame = Canvas(bg='white', bd=0, width=res, height=res)
        self.frame.pack()
        self.__draw_hexagonal_grid(clusters, size)

    def __draw_hexagon(self, top_x, top_y, color):
        x0 = top_x
        y0 = top_y
        x1 = x0 + factor2
        y1 = y0 + factor1
        x2 = x1
        y2 = y1 + factor2
        x3 = x0
        y3 = y2 + factor1
        x4 = x0 - factor2
        y4 = y2
        x5 = x4
        y5 = y1
        self.frame.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3,
                                  x4, y4, x5, y5, fill=color, outline='black')

    def __draw_hexagonal_grid(self, cells_clusters, size):
        start_x = round(res / 3) - factor1
        start_y = 40
        for (i, j), c in cells_clusters.items():
            if i < size:
                x = start_x + j * 2 * factor3 - i * factor3
            else:
                x = start_x + j * 2 * factor3 + (i - size - 3) * factor3
            y = start_y + i * 2 * (factor2 - 1)
            self.__draw_hexagon(x, y, mapper[c])

    def display(self):
        self.mainloop()
