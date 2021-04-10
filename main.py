try:
    import Tkinter as tk
except:
    import tkinter as tk
import main_frame

# Creates a window and a frame object that can be changed out depending what view the user accesses.
# There's only one view in this application.
# The main_frame.

class UIApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(main_frame.main_frame)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

# Destroys the window when the app is closed
def on_closing():
    app.destroy()

# Starts off the main app.
if __name__ == "__main__":
    app = UIApp()
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()