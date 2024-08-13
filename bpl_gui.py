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
import argparse 
import webbrowser
import configparser

executable_path = ""

this_directory = os.path.dirname(__file__)

def find_executable():
    executable_path = ""
    if sys.platform == "win32":
        if os.path.exists(os.path.join(this_directory,"bpl.exe")):
            executable_path = str(os.path.join(this_directory,"bpl.exe"))
        elif os.path.exists(os.path.join(this_directory,"bpl_d.exe")):
            executable_path = str(os.path.join(this_directory,"bpl_d.exe"))
        elif os.path.exists(os.path.join(this_directory,"windows_build/packages/bpl/release/bpl.exe")):
            executable_path = str(os.path.join(this_directory,"windows_build/packages/bpl/release/bpl.exe"))
        elif os.path.exists(os.path.join(this_directory,"windows_build/packages/bpl/debug/bpl_d.exe")):
            executable_path = str(os.path.join(this_directory,"windows_build/packages/bpl/debug/bpl_d.exe"))
    else:
        if os.path.exists(os.path.join(this_directory,"bpl")):
            executable_path = str(os.path.join(this_directory,"bpl"))
        elif os.path.exists(os.path.join(this_directory,"bpl_d")):
            executable_path = str(os.path.join(this_directory,"bpl_d"))
        elif os.path.exists(os.path.join(this_directory,"linux_build/packages/bpl/release/bpl")):
            executable_path = str(os.path.join(this_directory,"linux_build/packages/bpl/release/bpl"))
        elif os.path.exists(os.path.join(this_directory,"linux_build/packages/bpl/debug/bpl_d")):
            executable_path = str(os.path.join(this_directory,"linux_build/packages/bpl/debug/bpl_d"))
    return executable_path

# colours
color_scheme = "default"
bg_color = "#371B58"
bg_color_mid = "#4C3575"
bg_color_light = "#7858A6"
fg_color = "white"
fg_color_alert = "orange"

configs = None
if os.path.exists(os.path.join(this_directory,"bpl_gui.ini")):
    configs = configparser.ConfigParser()
    with open(os.path.join(this_directory,"bpl_gui.ini")) as f:
        configs.read_file(f)

def list_schemes():
    ret = []
    if configs:
        for s in configs.sections():
            if s != "settings":
                ret.append(s)
    else:
        ret = ["default"]
    return ret    

font_size = 10
def load_config(color_scheme_override = ""):
    global font_size
    global color_scheme
    global bg_color
    global bg_color_mid
    global bg_color_light
    global fg_color
    global fg_color_alert
    
    content = configs.sections()
    if "font_size" in configs.options("settings"):
        font_size = configs.get("settings","font_size")
    if not color_scheme_override and "settings" in content:
        if "color_scheme" in configs.options("settings"):
            color_scheme = configs.get("settings","color_scheme")
    elif color_scheme_override:
        color_scheme = color_scheme_override            

    if color_scheme in content:
        bg_color = configs.get(color_scheme, "bg_color")
        bg_color_mid = configs.get(color_scheme, "bg_color_mid")
        bg_color_light = configs.get(color_scheme, "bg_color_light")
        fg_color = configs.get(color_scheme, "fg_color")
        fg_color_alert = configs.get(color_scheme, "fg_color_alert")
        

# TK setup
root = tk.Tk()
# icons
logo_image = tk.PhotoImage(file=
                             os.path.join(this_directory,"icons", "logo_16.png"))
folder_image = tk.PhotoImage(file=
                             os.path.join(this_directory,"icons", "folder_16_wht.png"), 
                             height=16, width=16)
help_image = tk.PhotoImage(file=
                           os.path.join(this_directory,"icons", "help_16_wht.png"),
                           height=16, width=16)


root.title("Autotelica bpl")
root.iconphoto(True, logo_image)
root.option_add("*Dialog.msg.background",bg_color)
padx = 6
pady = 4


#menu for edit boxes
class edit_menu:
    def __init__(self, widget,
                 include_paste, selection_exists_f):
        self.include_paste = include_paste
        self.selection_exists_f = selection_exists_f
        self.widget = widget
        self.menu = tk.Menu(widget, tearoff=False, 
                            background=bg_color_light,foreground=fg_color, 
                            activebackground = bg_color, disabledforeground = bg_color_mid, 
                            relief="flat")
        self.menu.add_command(label="Select All", command=self.popup_select_all)
        self.menu.add_separator()
        self.menu.add_command(label="Copy", command=self.popup_copy)
        if include_paste:
            self.menu.add_command(label="Cut", command=self.popup_cut)
            self.menu.add_separator()
            self.menu.add_command(label="Paste", command=self.popup_paste)
        self.widget.bind("<Button-3>", self.display_popup)

    def display_popup(self, event):
        s = self.selection_exists_f()
        if s:
            self.menu.entryconfigure("Copy", state=tk.NORMAL)
            if self.include_paste:
                self.menu.entryconfigure("Cut", state=tk.NORMAL)
        else:
            self.menu.entryconfigure("Copy", state=tk.DISABLED)
            if self.include_paste:
                self.menu.entryconfigure("Cut", state=tk.DISABLED)
        self.menu.post(event.x_root, event.y_root)

    def popup_select_all(self):
        self.widget.event_generate("<Control-a>")

    def popup_copy(self):
        self.widget.event_generate("<Control-c>")

    def popup_cut(self):
        self.widget.event_generate("<Control-x>")

    def popup_paste(self):
        self.widget.event_generate("<Control-v>")

# a nice box for showing outputs
class output_box(tk.simpledialog.Dialog):
    def __init__(self, parent, title, message, the_font):
        self.message = message.replace("\r\n", "\n")
        # work out the size of the window
        lines = self.message.split("\n")
        lines = [l.strip() for l in lines]
        self.lines = len(lines)
        self.height = min(self.lines, 40)
        self.the_font = the_font
        longest = 0
        for l in lines:
            if(len(l) > longest):
                longest = len(l)
        self.width = min(longest+2, 100)
        super().__init__(parent, title)
        

    def body(self, frame):
        # print(type(frame)) # tkinter.Frame
        self.iconphoto(True, logo_image)
        self.configure(bg=bg_color)
        self.resizable(False, False)

        if self.lines > self.height:
            text = scrolledtext.ScrolledText(frame, 
                    width=self.width, height=self.height, relief="flat",
                    bg=bg_color, fg=fg_color, font=self.the_font,
                    selectbackground = bg_color_light,
                    padx=padx, pady=pady)
            text.vbar.configure(bg=bg_color, troughcolor =fg_color)
        else:
            text = tk.Text(frame, 
                    width=self.width, height=self.height, relief="flat",
                    bg=bg_color, fg=fg_color, font=self.the_font,
                    selectbackground = bg_color_light,
                    padx=padx, pady=pady)
        menu = edit_menu(text, False, lambda : "sel" in text.tag_names(tk.INSERT))
            
        text.insert(tk.INSERT, self.message)
        text.config(state=tk.DISABLED)
        text.pack(expand=True)
        return frame

    def ok_pressed(self):
        self.destroy()

    def buttonbox(self):
        self.bind("<Escape>", lambda event: self.ok_pressed())

# widgets creation
def create_label(frame, text):
    return tk.Label( frame, text=text, bg=bg_color, fg=fg_color)

def create_entry_style(frame):
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
                        border = 1,
                        padding=(5,2,2,2),  
                        background=bg_color_mid,
                        foreground=fg_color,
                        fieldbackground=bg_color_light,
                        insertcolor=fg_color,
                        selectbackground = bg_color
                        )
    entry_style.map('EntryStyle.TEntry', 
                        fieldbackground=[("focus", bg_color_light), ("!focus", bg_color_mid)],
                        selectbackground=[("focus", bg_color), ("!focus", bg_color)],
                        selectforeground=[("focus", fg_color), ("!focus", fg_color)]
                    )    

def create_entry_style_alert(frame):
    entry_style=ttk.Style(frame)
    entry_style.element_create("alerted.field", "from", "clam")
    entry_style.layout("EntryStyle.TEntryAlert",
                    [('Entry.alerted.field', {'children': [(
                        'Entry.background', {'children': [(
                            'Entry.padding', {'children': [(
                                'Entry.textarea', {'sticky': 'we'})],
                        'sticky': 'we'})], 'sticky': 'we'})],
                        'border':1, 'sticky': 'we'})])
    entry_style.configure('EntryStyle.TEntryAlert', 
                        border = 1,
                        padding=(5,2,2,2),  
                        background=bg_color_mid,
                        foreground=fg_color_alert,
                        fieldbackground=bg_color_mid,
                        insertcolor=fg_color,
                        selectbackground = bg_color
                        )
    entry_style.map('EntryStyle.TEntry', 
                        fieldbackground=[("focus", bg_color_light), ("!focus", bg_color_mid)],
                        selectbackground=[("focus", bg_color), ("!focus", bg_color)],
                        selectforeground=[("focus", fg_color), ("!focus", fg_color)]
                    )  

def create_entry(frame, var, width):
    edit_box = ttk.Entry(frame, textvariable=var, width=width, style="EntryStyle.TEntry")
    menu = edit_menu(edit_box, True, edit_box.select_present)
    def on_focus_in(e):
        e.widget.configure(style="EntryStyle.TEntry")
    edit_box.bind("<FocusIn>", on_focus_in)
    return edit_box

def create_small_btn(frame, command, help = False):
    image = help_image if help else folder_image
    return tk.Button(frame, image=image, command = command, 
                      bd=0, highlightthickness=0, relief="flat",
                      activebackground = bg_color, bg=bg_color, fg=fg_color)

def create_big_btn(frame, text, command):
    return tk.Button(frame, text = text, command = command, 
                      width = 20,
                      bd=0, highlightthickness=1, relief="flat", 
                      default="active",
                      highlightcolor=fg_color,
                      activebackground = bg_color, activeforeground = fg_color, 
                      bg=bg_color, fg=fg_color)

def create_separator(frame):
    return tk.Frame(frame, bg=fg_color, height=1, bd=0)

def create_check_button(frame, text, var_):
    return tk.Checkbutton(frame, text = text, variable=var_, 
                        onvalue=1, offvalue = 0, 
                        offrelief = tk.FLAT,relief = tk.FLAT,
                        highlightthickness=0,bd=0,
                        selectcolor = bg_color, activebackground = bg_color, 
                        activeforeground = fg_color,
                        bg=bg_color, fg=fg_color)


# helpers
def ask_directory(title, var):
    root.update_idletasks()
    dir = filedialog.askdirectory(initialdir=var.get(),mustexist=True, title=title)
    if(dir):
        var.set(os.path.normpath(dir))
    root.update_idletasks()

def ask_filename(title, var):
    root.update_idletasks()
    f = filedialog.askopenfilename(initialdir=var.get(),title=title, 
                                   filetypes=[("JSON file","*.json *.jsn"), ("Ini file","*.ini")])
    if(f):
        var.set(os.path.normpath(f))
    root.update_idletasks()

# configuring the window layout
def configure():
    the_font = font.nametofont("TkDefaultFont")
    the_font.configure(size=font_size, family="Helvetica")
    root.option_add("*Font", the_font)

    # frame in the root
    frame = tk.Frame(root, padx=2*padx, pady=2*pady)
    frame.configure(bg=bg_color)
    frame.pack()

    # styling for entry boxes
    create_entry_style(frame)
    create_entry_style_alert(frame)
    
    # source path
    sp_label = create_label(frame, "Source Template Path")
    sp_var = tk.StringVar()
    sp_entry = create_entry(frame, sp_var, 60)

    def sp_folder():
        ask_directory("Source Template Path", sp_var)

    sp_button = create_small_btn(frame, sp_folder)
    
    sp_label.grid(row=0, column=0, sticky=tk.W, padx=padx, pady=pady)
    sp_entry.grid(row=0, column=1, columnspan=2, sticky=tk.W, padx=padx, pady=pady)
    sp_button.grid(row=0, column=3, sticky=tk.E, padx=padx, pady=pady)

    # target path
    tp_label = create_label(frame, "Target Project Path")
    tp_var = tk.StringVar()
    tp_entry = create_entry(frame, tp_var, 60)
    
    def tp_folder():
        ask_directory("Source Template Path", tp_var)
    
    tp_button = create_small_btn(frame, tp_folder)
    
    tp_label.grid(row=1, column=0, sticky=tk.W, padx=padx, pady=pady)
    tp_entry.grid(row=1, column=1, columnspan=2, sticky=tk.E, padx=padx, pady=pady)
    tp_button.grid(row=1, column=3, sticky=tk.E, padx=padx, pady=pady)
    
    # config file path
    cp_label = create_label(frame, "Configuration File Path")
    cp_var = tk.StringVar()
    cp_entry = create_entry(frame, cp_var, 60)
    
    def cp_file():
        ask_filename("Configuration File Path", cp_var)

    cp_button = create_small_btn(frame, cp_file)
    
    cp_label.grid(row=2, column=0, sticky=tk.W, padx=padx, pady=pady)
    cp_entry.grid(row=2, column=1, columnspan=2, sticky=tk.E, padx=padx, pady=pady)
    cp_button.grid(row=2, column=3, sticky=tk.E, padx=padx, pady=pady)

    # separator
    sep_1 = create_separator(frame)
    sep_1.grid(row=4,column=0, columnspan=4, ipadx=300, pady=1.5*pady)

    # named values
    nv_label = create_label(frame, "Named Values")
    nv_var = tk.StringVar()
    nv_entry = create_entry(frame, nv_var, 60)
    
    nv_label.grid(row=5, column=0, sticky=tk.W, padx=padx, pady=pady)
    nv_entry.grid(row=5, column=1, columnspan=2, sticky=tk.E, padx=padx, pady=pady)

    # extensions to ignore
    ei_label = create_label(frame, "Extensions To Ignore")
    ei_var = tk.StringVar()
    ei_var.set("*.xl*, *.exe, *.dll")
    ei_entry = create_entry(frame, ei_var, 40)
    
    ei_label.grid(row=6, column=0, sticky=tk.W, padx=padx, pady=pady)
    ei_entry.grid(row=6, column=1, columnspan=2, sticky=tk.W, padx=padx, pady=pady)

    # files to ignore
    fi_label = create_label(frame, "Files To Ignore")
    fi_var = tk.StringVar()
    fi_entry = create_entry(frame, fi_var, 40)
    
    fi_label.grid(row=7, column=0, sticky=tk.W, padx=padx, pady=pady)
    fi_entry.grid(row=7, column=1, columnspan=2, sticky=tk.W, padx=padx, pady=pady)

    # strict
    strict = tk.IntVar()
    strict_btn = create_check_button(frame,"Strict", strict)

    strict_btn.grid(row=8, column=2, sticky=tk.E, padx=padx, pady=pady)

    # separator
    sep_2 = create_separator(frame)
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
    def parse_command_output(output):
        if "Command line hints" in output:
            tail = output.split("Command line hints", 1)[1]
            lines = tail.split("\n")
            for line in lines:
                if "-named_values" in line:
                    v = line.split("-named_values",1)[1].strip()
                    nv_entry.configure(style = "EntryStyle.TEntryAlert")
                    nv_var.set(v)
                elif "-extensions_to_ignore" in line:
                    v = line.split("-extensions_to_ignore",1)[1].strip()
                    ei_entry.configure(style = "EntryStyle.TEntryAlert")
                    ei_var.set(v)
                elif "-files_to_ignore" in line:
                    v = line.split("-files_to_ignore",1)[1].strip()
                    fi_entry.configure(style = "EntryStyle.TEntryAlert")
                    fi_var.set(v)
        root.update_idletasks()
                    
    def show_command_output(cmd_line, title):
        b = os.path.exists(cmd_line[0])
        result = subprocess.run(cmd_line, stdout=subprocess.PIPE)
        text = result.stdout.decode("utf-8")
        output_box(root, title, text, the_font)
        parse_command_output(text)

    # generate configuration file
    def generate_configuration():
        cmd_line = build_command_line()
        cmd_line.append("-generate_config")
        show_command_output(cmd_line, "Configuration Generation")

    generate_conf_btn = create_big_btn(frame, text="Generate Configuration", 
                                command=generate_configuration)    
    generate_conf_btn.grid(row=10,column=0, padx=padx, pady=pady)  

    # describe
    def describe():
        cmd_line = build_command_line()
        cmd_line.append("-describe")
        show_command_output(cmd_line, "Description")

    describe_btn = create_big_btn(frame, text="Describe Template", 
                            command=describe)    
    describe_btn.grid(row=10,column=1, padx=padx, pady=pady)  

    # generate code
    def generate():
        cmd_line = build_command_line()
        cmd_line.append("-generate")
        show_command_output(cmd_line, "Project Generation")

    generate_btn = create_big_btn(frame, text="Generate Project", 
                            command=generate)
    generate_btn.grid(row=10,column=2, padx=padx, pady=pady, sticky=tk.E)  

    # help
    def help():
        webbrowser.open("https://github.com/autotelic-sasha/bpl/blob/main/README.md")

    help_btn = create_small_btn(frame, help, True)
    help_btn.grid(row=10,column=3, padx=padx, pady=pady, sticky=tk.E)  



args = argparse.ArgumentParser(description="bpl templated code generator")
args.add_argument("--executable", type=str, required=False, default="", help="Path to bpl executable.")
args.add_argument("--theme", type=str, required=False, choices=list_schemes(), help="Colour scheme to use, defined in bpl_gui.ini file.")

arguments = args.parse_args()

if arguments.executable:
    executable_path = arguments.executable

color_scheme_override = ""
if arguments.theme:
    color_scheme_override = arguments.theme

load_config(color_scheme_override)    
if not executable_path:
    executable_path = find_executable()

if not executable_path:
    print("[ERROR] Could not find bpl executable.")

configure()
root.mainloop()

