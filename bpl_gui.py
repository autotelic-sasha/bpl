# Folder Icon made by Pixel perfect from www.flaticon.com
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from tkinter import filedialog
from tkinter import simpledialog
import tkinter.scrolledtext as scrolledtext
import subprocess
import os
import sys

executable_path = ""

this_directory = os.path.dirname(__file__)

def find_executable():
    if sys.platform == "win32":
        if os.path.exists(os.path.join(this_directory,"bpl.exe")):
            executable_path = str(os.path.join(this_directory,"bpl.exe"))
        elif os.path.exists(os.path.join(this_directory,"bpl_d.exe")):
            executable_path = str(os.path.join(this_directory,"bpl_d.exe"))
        elif os.path.exists(os.path.join(this_directory,"windows_build/bpl/packages/bpl/release/bpl.exe")):
            executable_path = str(os.path.join(this_directory,"windows_build/bpl/packages/bpl/release/bpl.exe"))
        elif os.path.exists(os.path.join(this_directory,"windows_build/bpl/packages/bpl/debug/bpl_d.exe")):
            executable_path = str(os.path.join(this_directory,"windows_build/bpl/packages/bpl/debug/bpl_d.exe"))
    else:
        if os.path.exists(os.path.join(this_directory,"bpl")):
            executable_path = str(os.path.join(this_directory,"bpl"))
        elif os.path.exists(os.path.join(this_directory,"bpl_d")):
            executable_path = str(os.path.join(this_directory,"bpl_d"))
        elif os.path.exists(os.path.join(this_directory,"linux_build/bpl/packages/bpl/release/bpl")):
            executable_path = str(os.path.join(this_directory,"linux_build/bpl/packages/bpl/release/bpl"))
        elif os.path.exists(os.path.join(this_directory,"linux_build/bpl/packages/bpl/debug/bpl_d")):
            executable_path = str(os.path.join(this_directory,"linux_build/bpl/packages/bpl/debug/bpl_d"))
    return executable_path

bg_color = "#32075e"
bg_color_light = "#52277e"
bg_color_mid="#5a258f"
fg_color = "white"
root = tk.Tk()
the_font = font.nametofont("TkDefaultFont")
the_font.configure(size=10, family="Helvetica")

root.option_add("*Font", the_font)
root.title("Autotelica bpl")
root.iconbitmap("logo.ico")
root.option_add("*Dialog.msg.background",bg_color)
padx = 6
pady = 4
folder_image = tk.PhotoImage(file="folder_16_wht.png", height=16, width=16)
frame = tk.Frame(root, padx=2*padx, pady=2*pady)
frame.configure(bg=bg_color)
frame.pack()

class output_box(tk.simpledialog.Dialog):
    def __init__(self, parent, title, message):
        self.message = message.replace("\r\n", "\n")
        # work out the size of the window
        lines = self.message.split("\n")
        lines = [l.strip() for l in lines]
        self.lines = len(lines)
        self.height = min(self.lines, 40)
        longest = 0
        for l in lines:
            if(len(l) > longest):
                longest = len(l)
        self.width = min(longest+2, 100)
        super().__init__(parent, title)
        

    def body(self, frame):
        # print(type(frame)) # tkinter.Frame
        self.iconbitmap("logo.ico")
        self.configure(bg=bg_color)
        self.resizable(False, False)

        if self.lines > self.height:
            text = scrolledtext.ScrolledText(frame, 
                    width=self.width, height=self.height, relief="flat",
                    bg=bg_color, fg=fg_color, font=the_font,
                    selectbackground = bg_color_light,
                    padx=padx, pady=pady)
            text.vbar.configure(bg=bg_color, troughcolor =fg_color)
        else:
            text = tk.Text(frame, 
                    width=self.width, height=self.height, relief="flat",
                    bg=bg_color, fg=fg_color, font=the_font,
                    selectbackground = bg_color_light,
                    padx=padx, pady=pady)
            
        text.insert(tk.INSERT, self.message)
        text.config(state=tk.DISABLED)
        text.pack(expand=True)
        return frame

    def ok_pressed(self):
        self.destroy()

    def buttonbox(self):
        self.bind("<Escape>", lambda event: self.ok_pressed())


entry_style=ttk.Style(frame)
entry_style.element_create("plain.field", "from", "clam")
entry_style.layout("EntryStyle.TEntry",
                   [('Entry.plain.field', {'children': [(
                       'Entry.background', {'children': [(
                           'Entry.padding', {'children': [(
                               'Entry.textarea', {'sticky': 'we'})],
                      'sticky': 'we'})], 'sticky': 'we'})],
                      'border':1, 'sticky': 'we'})])
entry_style.configure('EntryStyle.TEntry', 
                      padding=(5,2,2,2),  
                      background=bg_color_light,
                      foreground=fg_color,
                      fieldbackground=bg_color_light,
                      insertcolor=fg_color,
                      selectbackground = bg_color
                      )
def create_label(text):
    return tk.Label( frame, text=text, bg=bg_color, fg=fg_color)

def create_entry(var, width):
    return ttk.Entry(frame, textvariable=var, width=width, style="EntryStyle.TEntry")

def create_small_btn(command):
    return tk.Button(frame, image=folder_image, command = command, 
                      bd=0, highlightthickness=0, relief="flat",
                      activebackground = bg_color, bg=bg_color, fg=fg_color)

def create_big_btn(text, command):
    return tk.Button(frame, text = text, command = command, 
                      width = 20,
                      bd=0, highlightthickness=1, relief="solid", 
                      default="active",
                      highlightcolor=fg_color,
                      activebackground = bg_color, activeforeground = fg_color, 
                      bg=bg_color, fg=fg_color)

def create_separator():
    return tk.Frame(frame, bg=fg_color, height=1, bd=0)

def ask_directory(title, var):
    root.update_idletasks()
    dir = filedialog.askdirectory(initialdir=var.get(),mustexist=True, title=title)
    if(dir):
        var.set(dir)
    root.update_idletasks()

def ask_filename(title, var):
    root.update_idletasks()
    f = filedialog.askopenfilename(initialdir=var.get(),title=title, 
                                   filetypes=[("JSON file","*.json *.jsn"), ("Ini file","*.ini")])
    if(f):
        var.set(f)
    root.update_idletasks()

# source path
sp_label = create_label("Source Template Path")
sp_var = tk.StringVar()
sp_entry = create_entry(sp_var, 60)

def sp_folder():
    ask_directory("Source Template Path", sp_var)

sp_button = create_small_btn(sp_folder)
sp_label.grid(row=0, column=0, sticky=tk.W, padx=padx, pady=pady)
sp_entry.grid(row=0, column=1, columnspan=2, sticky=tk.W, padx=padx, pady=pady)
sp_button.grid(row=0, column=3, sticky=tk.E, padx=padx, pady=pady)
# target path
tp_label = create_label("Target Project Path")
tp_var = tk.StringVar()
tp_entry = create_entry(tp_var, 60)
def tp_folder():
    ask_directory("Source Template Path", tp_var)
tp_button = create_small_btn(tp_folder)
tp_label.grid(row=1, column=0, sticky=tk.W, padx=padx, pady=pady)
tp_entry.grid(row=1, column=1, columnspan=2, sticky=tk.E, padx=padx, pady=pady)
tp_button.grid(row=1, column=3, sticky=tk.E, padx=padx, pady=pady)
# config file path
cp_label = create_label("Configuration File Path")
cp_var = tk.StringVar()
cp_entry = create_entry(cp_var, 60)
def cp_file():
    ask_filename("Configuration File Path", cp_var)

cp_button = create_small_btn(cp_file)
cp_label.grid(row=2, column=0, sticky=tk.W, padx=padx, pady=pady)
cp_entry.grid(row=2, column=1, columnspan=2, sticky=tk.E, padx=padx, pady=pady)
cp_button.grid(row=2, column=3, sticky=tk.E, padx=padx, pady=pady)

# separator
sep_1 = create_separator()
sep_1.grid(row=4,column=0, columnspan=4, ipadx=300, pady=1.5*pady)

# named values
nv_label = create_label("Named Values")
nv_var = tk.StringVar()
nv_entry = create_entry(nv_var, 60)
nv_label.grid(row=5, column=0, sticky=tk.W, padx=padx, pady=pady)
nv_entry.grid(row=5, column=1, columnspan=2, sticky=tk.E, padx=padx, pady=pady)

# extensions to ignore
ei_label = create_label("Extensions To Ignore")
ei_var = tk.StringVar()
ei_var.set("*.xl*, *.exe, *.dll")
ei_entry = create_entry(ei_var, 40)
ei_label.grid(row=6, column=0, sticky=tk.W, padx=padx, pady=pady)
ei_entry.grid(row=6, column=1, columnspan=2, sticky=tk.W, padx=padx, pady=pady)

# files to ignore
fi_label = create_label("Files To Ignore")
fi_var = tk.StringVar()
fi_entry = create_entry(fi_var, 40)
fi_label.grid(row=7, column=0, sticky=tk.W, padx=padx, pady=pady)
fi_entry.grid(row=7, column=1, columnspan=2, sticky=tk.W, padx=padx, pady=pady)

# strict
strict = tk.IntVar()
strict_btn = tk.Checkbutton(frame, text = "Strict", variable=strict, 
                            onvalue=1, offvalue = 0, 
                            offrelief = tk.FLAT,relief = tk.FLAT,
                            highlightthickness=1,bd=1,
                            selectcolor = bg_color, activebackground = bg_color, 
                            activeforeground = fg_color,
                            bg=bg_color, fg=fg_color)

strict_btn.grid(row=8, column=2, sticky=tk.E, padx=padx, pady=pady)

# separator
sep_2 = create_separator()
sep_2.grid(row=9,column=0, columnspan=4, ipadx=300, pady=1.5*pady)

# dealing with execution
def build_command_line():
    root.update_idletasks()
    ret = [executable_path]
    def add_string_var(arg, var_):
        s = var_.get().strip()
        if s:
            ret.append(arg)
            ret.append(s)

    add_string_var("-s", sp_var)
    add_string_var("-t", tp_var)
    add_string_var("-c", cp_var)
    add_string_var("-e", ei_var)
    add_string_var("-f", fi_var)
    add_string_var("-named_values", nv_var)
    
    if strict.get() == 1:
        ret.append("-strict")
    
    return ret

def show_command_output(cmd_line, title):
    b = os.path.exists(cmd_line[0])
    result = subprocess.run(cmd_line, stdout=subprocess.PIPE)
    text = result.stdout.decode("utf-8")
    output_box(root, title, text)

# generate configuration file
def generate_configuration():
    cmd_line = build_command_line()
    cmd_line.append("-generate_configuration")
    show_command_output(cmd_line, "Configuration Generation")

generate_conf_btn = create_big_btn(text="Generate Configuration", 
                              command=generate_configuration)    
generate_conf_btn.grid(row=10,column=0, padx=padx, pady=pady)  

# describe
def describe():
    cmd_line = build_command_line()
    cmd_line.append("-describe")
    show_command_output(cmd_line, "Description")

describe_btn = create_big_btn(text="Describe Template", 
                         command=describe)    
describe_btn.grid(row=10,column=1, padx=padx, pady=pady)  

# generate code
def generate():
    cmd_line = build_command_line()
    cmd_line.append("-generate")
    show_command_output(cmd_line, "Project Generation")

generate_btn = create_big_btn(text="Generate Project", 
                         command=generate)
generate_btn.grid(row=10,column=2, padx=padx, pady=pady, sticky="e")  

if not executable_path:
    executable_path = find_executable()

if not executable_path:
    print("[ERROR] Could not find blp executable.")

root.mainloop()

