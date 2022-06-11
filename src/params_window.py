# Shlomi Ben-Shushan 311408264


# File: param_window.py
# Content: An input window that allows a user to change hyper-parameters.


from src.style import fonts, colors
from src.analyze_window import invalid_input_message
from tkinter import Tk, Entry, Label, Button, Frame


WINDOW_H = 250
WINDOW_W = 150


def pop_params_window(parent):
    """
    This function pops a new Tkinter window.
    :param parent: the parent Tkinter window.
    :return: None.
    """

    # Window configuration.
    win = Tk()
    win.geometry(f'{WINDOW_H}x{WINDOW_W}')
    win.minsize(WINDOW_H, WINDOW_W)
    win.maxsize(WINDOW_H, WINDOW_W)
    win.config(bg=colors.app)

    # Create a frame for the parameter settings.
    win.params_frame = Frame(master=win, bg=colors.app)
    win.params_frame.pack(pady=10, padx=10)

    # Epoch Label and Entry.
    Label(
        master=win.params_frame,
        font=fonts.regular,
        bg=colors.app,
        fg=colors.white,
        text='Epochs: '
    ).grid(row=0, column=0, padx=5, pady=5, sticky='w')
    win.epochs = Entry(
        master=win.params_frame,
        font=fonts.regular,
        width=8,
        bg=colors.io_bg,
        fg=colors.io_text,
        justify='center'
    )
    win.epochs.insert(0, parent.epochs)
    win.epochs.grid(row=0, column=1, padx=2, pady=5, sticky='e')

    # Learning Rate Label and Entry.
    Label(
        master=win.params_frame,
        font=fonts.regular,
        bg=colors.app,
        fg=colors.white,
        text='Learning Rate:'
    ).grid(row=1, column=0, padx=5, pady=5, sticky='w')
    win.lr = Entry(
        master=win.params_frame,
        font=fonts.regular,
        width=8,
        bg=colors.io_bg,
        fg=colors.io_text,
        justify='center'
    )
    win.lr.insert(0, parent.lr)
    win.lr.grid(row=1, column=1, padx=2, pady=5, sticky='e')

    # 'Set' Button definition.
    def on_set():
        epochs = win.epochs.get().strip()
        lr = win.lr.get().strip()
        try:
            epochs = int(epochs)
            lr = float(lr)
            if lr < 0 or epochs < 1:
                raise ValueError
            parent.epochs = epochs
            parent.lr = lr
            win.destroy()
        except ValueError:
            invalid_input_message()

    set_btn = Button(
        master=win.params_frame,
        width=8,
        bg=colors.button_prime,
        fg=colors.white,
        relief='groove',
        font=fonts.regular,
        text='Set',
        command=on_set
    )
    set_btn.grid(row=2, column=1, padx=2, pady=17, sticky='w')

    # 'Cancel' Button definition.
    cancel_btn = Button(
        master=win.params_frame,
        width=8,
        bg=colors.button,
        fg=colors.white,
        relief='groove',
        font=fonts.regular,
        text='Cancel',
        command=lambda: win.destroy()
    )
    cancel_btn.grid(row=2, column=0, padx=2, pady=17, sticky='w')
