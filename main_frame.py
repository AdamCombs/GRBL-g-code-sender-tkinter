try:
    import Tkinter as tk
except:
    import tkinter as tk
from tkinter import filedialog as fd
import tkinter.messagebox
import tkinter.ttk as ttk
import serial
import time
import serial.tools.list_ports

class main_frame(tk.Frame):
    def __init__(self, master):
        master.title('Main Window')
        w, h = master.winfo_screenwidth(), master.winfo_screenheight()
        tk.Frame.__init__(self, master)

        # String object that holds the value of the currently selected filename.
        current_selected_file = tk.StringVar()
        current_selected_file.set("")

        # Displays code line being sent and confirmation of send.
        code_send_view = tk.Frame(self)
        tk.Label(code_send_view, 
                 text="Code being sent: ", 
                 font=('Arial', 16))\
            .grid(row=0, column=0, sticky=tk.W)

        # Shows the lines of code being sent.
        code_line = tk.StringVar()
        code_line.set('Sending line will display here.')
        line_label = tk.Label(code_send_view, textvariable=code_line)
        line_label.grid(row=0, column=1, sticky=tk.W)

        # Shows confirmation of the sent code.
        confirmation = tk.StringVar()
        confirmation.set('Confirmation will display here.')
        confirmation_label = tk.Label(code_send_view, textvariable=confirmation)
        confirmation_label.grid(row=1, column=1, sticky=tk.W)


        # Displays currently selected code file.
        code_display = tk.Frame(self)
        # Title for code display.
        tk.Label(code_display, 
                 text="Current File:", 
                 font=('Arial', 16))\
            .pack(anchor=tk.W)

        # Label displays title of loaded text file. Binds to uploaded file.
        code_name = tk.Label(code_display, 
                             textvariable=current_selected_file, 
                             font=('Arial', 14))

        # Canvas to display code.
        display_canvas = tk.Canvas(code_display, 
                                   bg='#FFFFFF', 
                                   width=w/3, 
                                   height=h/2)

        code_text = display_canvas.create_text( 10, 10, font=('Arial', 12), anchor=tk.NW)

        # Default text on canvas.
        display_canvas.itemconfigure(code_text, text='Your code displays here.')

        # Scrollbar for canvas
        scrollbar = tk.Scrollbar(code_display, orient="vertical", command=display_canvas.yview)
        display_canvas.configure(yscrollcommand=scrollbar.set)

        # Add labels, canvas, and scroll bar to frame.
        code_name.pack(anchor=tk.W)
        scrollbar.pack(side="right", fill="y")
        display_canvas.pack()

        # Control Functions
        # Opens file for display window
        def open_current_file():
            file = fd.askopenfilename()
            if file.endswith('.txt'):
                text_for_display = ''
                for line in open(file):
                    text_for_display = text_for_display + str(line)
                display_canvas.itemconfigure(code_text, text=text_for_display)
                display_canvas.configure(scrollregion=display_canvas.bbox("all"))
                current_selected_file.set(str(file))
                code_name.configure(text=current_selected_file.get())
            elif file == '':
                pass
            else:
                tk.messagebox.showerror('Invalid File Type', 'File must be of .txt extension.')

        # Sends G-Code to GRBL
        def send_to_GRBL(com, current):
            try:
                # Open grbl serial port
                s = serial.Serial(com, 9600)
                f = open(current, 'r');

                # Wake up grbl
                s.write("\r\n\r\n".encode())
                time.sleep(2)
                s.flushInput()

                # Stream g-code to grbl
                for line in f:
                    l = line.strip()  # Strip all EOL characters for streaming

                    current_line = l + '\n'

                    s.write(current_line.encode())  # Send g-code block to grbl
                    grbl_out = s.readline()

                    code_line.set(str(l))
                    confirmation.set(str(grbl_out.strip()))
                    self.update_idletasks()

                code_line.set("Transmission completed")
                confirmation.set("Transmission completed")

                f.close()
                s.close()
            except:
                tk.messagebox.showerror('Send Failure', 'No device detected on given port.')
        
        # Frame for holding button controls
        controls = tk.Frame(self)

        # Label for Com port select.
        tk.Label(controls,
                 text='Send to Port: ')\
            .pack(padx=5, pady=2, anchor=tk.W)

        # Combobox to allow the user to choose a comport.
        com_port_box = ttk.Combobox(controls,
                                    width=int(round(w/100, 0)),
                                    values=['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6'])
        com_port_box.pack(padx=5, pady=2)
        com_port_box.current(4)

        # Send code button
        tk.Button(controls,
                  text='Send Code',
                  width=int(round(w/130, 0)),
                  height=int(round(h/170, 0)),
                  font = ('Arial', 12),
                  command= lambda: send_to_GRBL(com_port_box.get(), current_selected_file.get()))\
            .pack(padx=5, pady=5)

        # Open File Button
        tk.Button(controls,
                  text='Open File',
                  width=int(round(w/130, 0)),
                  height=int(round(h/170, 0)),
                  font = ('Arial', 12),
                  command=open_current_file)\
            .pack(padx=5, pady=5)

        # Organize the frames inside the main frame.
        code_display.grid(row=0, column=0 ,padx=10, pady=10)
        controls.grid(row=0, column=1 ,padx=10, pady=10)
        code_send_view.grid(row=1, column=0, columnspan=2 ,padx=10, pady=10)


