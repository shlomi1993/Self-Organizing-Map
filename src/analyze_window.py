# Shlomi Ben-Shushan 311408264


# File: analyze_window.py
# Content: Implementation of a window for LR analysis.


from src.parser import parse
from src.evaluation import eval_errors
from src.style import fonts, colors
from tkinter import Tk, Entry, Label, Button, Frame, messagebox


WINDOW_H = 220
WINDOW_W = 215


def invalid_input_message():
    """
    This functions pops an "invalid input" error message.
    :return: None
    """
    title = 'Invalid Input'
    msg = 'Values should be positive integers and End LR should be greater ' \
          'then Start LR.'
    messagebox.showerror(title, msg)


def pop_analyze_window(parent):
    """
    This function pops a new Tkinter window.
    :param parent: the parent Tkinter window.
    :return: None.
    """

    # Window configurations.
    win = Tk()
    win.geometry(f'{WINDOW_H}x{WINDOW_W}')
    win.minsize(WINDOW_H, WINDOW_W)
    win.maxsize(WINDOW_H, WINDOW_W)
    win.config(bg=colors.app)
    win.analyze_frame = Frame(master=win, bg=colors.app)
    win.analyze_frame.pack(pady=10, padx=10)

    # 'LR Start' Label and Entry.
    Label(
        master=win.analyze_frame,
        font=fonts.regular,
        bg=colors.app,
        fg=colors.white,
        text='LR Start: '
    ).grid(row=0, column=0, padx=5, pady=5, sticky='w')
    win.start_lr = Entry(
        master=win.analyze_frame,
        font=fonts.regular,
        width=7,
        bg=colors.io_bg,
        fg=colors.io_text,
        justify='center'
    )
    win.start_lr.insert(0, parent.start_lr)
    win.start_lr.grid(row=0, column=1, padx=2, pady=5, sticky='e')

    # 'LR End' Label and Entry.
    Label(
        master=win.analyze_frame,
        font=fonts.regular,
        bg=colors.app,
        fg=colors.white,
        text='LR End:'
    ).grid(row=1, column=0, padx=5, pady=5, sticky='w')
    win.end_lr = Entry(
        master=win.analyze_frame,
        font=fonts.regular,
        width=7,
        bg=colors.io_bg,
        fg=colors.io_text,
        justify='center'
    )
    win.end_lr.insert(0, parent.end_lr)
    win.end_lr.grid(row=1, column=1, padx=2, pady=5, sticky='e')

    # 'LR Step' Label and Entry.
    Label(
        master=win.analyze_frame,
        font=fonts.regular,
        bg=colors.app,
        fg=colors.white,
        text='LR Step:'
    ).grid(row=2, column=0, padx=5, pady=5, sticky='w')
    win.step_lr = Entry(
        master=win.analyze_frame,
        font=fonts.regular,
        width=7,
        bg=colors.io_bg,
        fg=colors.io_text,
        justify='center'
    )
    win.step_lr.insert(0, parent.step_lr)
    win.step_lr.grid(row=2, column=1, padx=2, pady=5, sticky='e')

    # 'Epochs' Label and Entry.
    Label(
        master=win.analyze_frame,
        font=fonts.regular,
        bg=colors.app,
        fg=colors.white,
        text='Epochs:'
    ).grid(row=3, column=0, padx=5, pady=5, sticky='w')
    win.epochs = Entry(
        master=win.analyze_frame,
        font=fonts.regular,
        width=7,
        bg=colors.io_bg,
        fg=colors.io_text,
        justify='center'
    )
    win.epochs.insert(0, parent.epochs)
    win.epochs.grid(row=3, column=1, padx=2, pady=5, sticky='e')

    # 'Analyze' Button definition and functionality.
    def on_set():
        slr = win.start_lr.get().strip()
        elr = win.end_lr.get().strip()
        step = win.step_lr.get().strip()
        epochs = win.epochs.get().strip()
        try:
            slr = float(slr)
            elr = float(elr)
            step = float(step)
            epochs = int(epochs)
            if elr < slr or slr < 0 or elr < 0 or step < 0 or epochs < 1:
                raise ValueError
            parent.start_lr = slr
            parent.end_lr = elr
            parent.step_lr = step
            parent.epochs = epochs
            win.destroy()
            parsed = parse(parent.file)
            eval_errors(parsed, parent.start_lr, parent.end_lr, parent.step_lr, parent.epochs, parent.console)
        except ValueError:
            invalid_input_message()
    analyze_btn = Button(
        master=win.analyze_frame,
        width=8,
        bg=colors.button_prime,
        fg=colors.white,
        relief='groove',
        font=fonts.regular,
        text='Analyze',
        command=on_set
    )
    analyze_btn.grid(row=4, column=1, padx=2, pady=13, sticky='w')

    # 'Cancel' Button definition and functionality.
    cancel_btn = Button(
        master=win.analyze_frame,
        width=8,
        bg=colors.button,
        fg=colors.white,
        relief='groove',
        font=fonts.regular,
        text='Cancel',
        command=lambda: win.destroy()
    )
    cancel_btn.grid(row=4, column=0, padx=2, pady=13, sticky='w')
