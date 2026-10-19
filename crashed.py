import tkinter as tk
def crash_window(parent, errors: list):
    msg = ''
    for error in errors:
        print(errors)
        msg = msg + error + '\n'
    msg = msg.strip()

    error_window = tk.Toplevel(parent)
    error_window.title("An error occured")
    error_window.grab_set()
    error_window.transient(parent)
    
    error_box = tk.Text(error_window, height=10, width=60)
    error_box.pack()

    error_box.insert("1.0", msg)

    tk.Label(error_window, text="(The player will close once this dialogue is closed)").pack()

    error_window.protocol("WM_DELETE_WINDOW", parent.destroy) 
    error_box.mainloop()