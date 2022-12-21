"""
Py Image Editor
Developed By : Abhishek Mishra
Contact : mishrababhishek.2899@gmail.com
Description : A Simple Python Gui Application Using Tkinter For Apply Different Filters on Image
"""


import tkinter
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk
import editor


class App(tkinter.Tk, editor.EditorCallbacks):
    cActiveFrame: tkinter.Widget = None
    my: int
    mx: int
    s: ttk.Style

    def on_error(self, msg):
        messagebox.showerror("Failed", msg)

    def image_update(self, img: ImageTk):
        self.imageLabel.config(image=img)
        self.imageLabel.image = img

    # noinspection PyUnusedLocal
    def open_file(self, event: tkinter.Event):
        file_types = [
            ("Image", "*.jpeg *.jpg *.png"),
        ]
        path = filedialog.askopenfilename(
            title="Open Image File",
            initialdir="/",
            filetypes=file_types,
        )
        if len(path) > 0:
            self.editor.set_image(path)

    # noinspection PyUnusedLocal
    def save_file(self, event: tkinter.Event):
        if not self.editor.can_save():
            self.on_error("No Image Loaded To Save")
            return

        print(self.editor.extension)
        path = filedialog.asksaveasfilename(
            title="Save Image File",
            initialdir="/",
            initialfile="PyEditorImage",
            defaultextension=self.editor.extension,
        )
        if len(path) > 0:
            self.editor.save_image(path)

    # noinspection PyUnusedLocal
    @staticmethod
    def show_about(event: tkinter.Event):
        messagebox.showinfo("About",
                            '''
Py Image Editor
Developed By : Abhishek Mishra
Contact : mishrababhishek.2899@gmail.com
Description : A Simple Python Gui Application Using Tkinter For Apply Different Filters on Image
                            ''')

    def style(self):
        self.s = ttk.Style(self)
        self.s.theme_use("default")
        self.s.configure("f1.TFrame", background="#2B2B2B")
        self.s.configure("f2.TFrame", background="#423F3E")
        self.s.configure("l1.TLabel", background="#2B2B2B", foreground="white", padding=[5, 3, 5, 3])
        self.s.configure("l2.TLabel", background="#423F3E", foreground="white", padding=[5, 3, 5, 3])
        self.s.configure("TSeparator", background="#171010")
        self.s.theme_settings("default", {
            "TCombobox": {
                "configure": {"padding": 5},
                "map": {
                    "background": [("active", "#2B2B2B"),
                                   ("!disabled", "#2B2B2B")],
                    "fieldbackground": [("!disabled", "#2B2B2B")],
                    "foreground": [("focus", "white"),
                                   ("!disabled", "white")],
                    "selectbackground": [
                        ("active", "#2B2B2B"),
                        ("!disabled", "#2B2B2B")
                    ],
                }
            }
        })

    @staticmethod
    def change_color(e: tkinter.Event, color: str):
        e.widget.config(background=color)

    def start_move(self, e: tkinter.Event):
        self.mx = e.x
        self.my = e.y

    # noinspection PyUnusedLocal
    def stop_move(self, e: tkinter.Event):
        self.mx = 0
        self.my = 0

    def move(self, e: tkinter.Event):
        deltax = e.x - self.mx
        deltay = e.y - self.my
        self.geometry(f"+{self.winfo_x()+deltax}+{self.winfo_y()+deltay}")

    # noinspection PyUnusedLocal
    def on_filter_change(self, e: tkinter.Event = None):
        if self.cActiveFrame is not None:
            self.cActiveFrame.destroy()

        match self.filterVar.get():
            case "BLUR":
                self.blur_frame()
            case "CONTOUR":
                self.contour_frame()
            case "DETAIL":
                self.detail_frame()
            case "EDGE_ENHANCE":
                self.edge_enhance_frame()
            case "EMBOSS":
                self.emboss_frame()
            case "SHARPEN":
                self.sharpen_frame()
            case "SMOOTH":
                self.smooth_frame()

    def blur_frame(self):
        def apply():
            self.editor.apply_blur(
                True if blur.get() != "0" else False,
                float(bblur.get()),
                float(gblur.get())
            )
        self.cActiveFrame = ttk.Frame(self.controlFrame, style="f2.TFrame")
        self.cActiveFrame.pack_propagate(False)
        self.cActiveFrame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        ttk.Label(self.cActiveFrame, text="Blur", style="l2.TLabel").grid(row=0, column=0, padx=5, pady=5)
        blur = tkinter.StringVar(value="0")
        ttk.Entry(self.cActiveFrame, textvariable=blur).grid(row=0, column=1)
        ttk.Label(self.cActiveFrame, text="Box Blur", style="l2.TLabel").grid(row=1, column=0, padx=5, pady=5)
        bblur = tkinter.StringVar(value="0")
        ttk.Entry(self.cActiveFrame, textvariable=bblur).grid(row=1, column=1)
        ttk.Label(self.cActiveFrame, text="Gaussian Blur", style="l2.TLabel").grid(row=2, column=0, padx=5, pady=5)
        gblur = tkinter.StringVar(value="0")
        ttk.Entry(self.cActiveFrame, textvariable=gblur).grid(row=2, column=1)
        ttk.Button(self.cActiveFrame, text="Apply", command=apply).grid(row=3, column=1)

    def contour_frame(self):
        def apply():
            self.editor.apply_contour(
                True if contour.get() != "0" else False
            )
        self.cActiveFrame = ttk.Frame(self.controlFrame, style="f2.TFrame")
        self.cActiveFrame.pack_propagate(False)
        self.cActiveFrame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        ttk.Label(self.cActiveFrame, text="Contour", style="l2.TLabel").grid(row=0, column=0, padx=5, pady=5)
        contour = tkinter.StringVar(value="0")
        ttk.Entry(self.cActiveFrame, textvariable=contour).grid(row=0, column=1)
        ttk.Button(self.cActiveFrame, text="Apply", command=apply).grid(row=1, column=1)

    def detail_frame(self):
        def apply():
            self.editor.apply_detail(
                True if detail.get() != "0" else False
            )
        self.cActiveFrame = ttk.Frame(self.controlFrame, style="f2.TFrame")
        self.cActiveFrame.pack_propagate(False)
        self.cActiveFrame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        ttk.Label(self.cActiveFrame, text="Detail", style="l2.TLabel").grid(row=0, column=0, padx=5, pady=5)
        detail = tkinter.StringVar(value="0")
        ttk.Entry(self.cActiveFrame, textvariable=detail).grid(row=0, column=1)
        ttk.Button(self.cActiveFrame, text="Apply", command=apply).grid(row=1, column=1)

    def edge_enhance_frame(self):
        def apply():
            self.editor.apply_edge_enhance(
                True if enhance.get() != "0" else False
            )
        self.cActiveFrame = ttk.Frame(self.controlFrame, style="f2.TFrame")
        self.cActiveFrame.pack_propagate(False)
        self.cActiveFrame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        ttk.Label(self.cActiveFrame, text="Edge Enhance", style="l2.TLabel").grid(row=0, column=0, padx=5, pady=5)
        enhance = tkinter.StringVar(value="0")
        ttk.Entry(self.cActiveFrame, textvariable=enhance).grid(row=0, column=1)
        ttk.Button(self.cActiveFrame, text="Apply", command=apply).grid(row=1, column=1)

    def emboss_frame(self):
        def apply():
            self.editor.apply_emboss(
                True if emboss.get() != "0" else False
            )
        self.cActiveFrame = ttk.Frame(self.controlFrame, style="f2.TFrame")
        self.cActiveFrame.pack_propagate(False)
        self.cActiveFrame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        ttk.Label(self.cActiveFrame, text="Emboss", style="l2.TLabel").grid(row=0, column=0, padx=5, pady=5)
        emboss = tkinter.StringVar(value="0")
        ttk.Entry(self.cActiveFrame, textvariable=emboss).grid(row=0, column=1)
        ttk.Button(self.cActiveFrame, text="Apply", command=apply).grid(row=1, column=1)

    def sharpen_frame(self):
        def apply():
            self.editor.apply_sharpen(
                True if sharpen.get() != "0" else False
            )
        self.cActiveFrame = ttk.Frame(self.controlFrame, style="f2.TFrame")
        self.cActiveFrame.pack_propagate(False)
        self.cActiveFrame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        ttk.Label(self.cActiveFrame, text="Sharpen", style="l2.TLabel").grid(row=0, column=0, padx=5, pady=5)
        sharpen = tkinter.StringVar(value="0")
        ttk.Entry(self.cActiveFrame, textvariable=sharpen).grid(row=0, column=1)
        ttk.Button(self.cActiveFrame, text="Apply", command=apply).grid(row=1, column=1)

    def smooth_frame(self):
        def apply():
            self.editor.apply_smooth(
                True if smooth.get() != "0" else False
            )
        self.cActiveFrame = ttk.Frame(self.controlFrame, style="f2.TFrame")
        self.cActiveFrame.pack_propagate(False)
        self.cActiveFrame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        ttk.Label(self.cActiveFrame, text="smooth", style="l2.TLabel").grid(row=0, column=0, padx=5, pady=5)
        smooth = tkinter.StringVar(value="0")
        ttk.Entry(self.cActiveFrame, textvariable=smooth).grid(row=0, column=1)
        ttk.Button(self.cActiveFrame, text="Apply", command=apply).grid(row=1, column=1)

    def __init__(self, debug: bool = False):
        super().__init__()
        self.debug = debug
        self.style()
        self.editor = editor.Editor(self)

        # window
        self.title("Image Editor")
        self.geometry(f"{850}x{550}+{150}+{100}")
        self.iconphoto(False, tkinter.PhotoImage(file="logo.png"))
        self.config(bg="#2B2B2B")

        # menu bar
        self.menuBar = ttk.Frame(self, height=25, style="f1.TFrame")
        self.menuBar.pack(side="top", fill="x")
        self.openFileLabel = ttk.Label(self.menuBar, text="Open File", style="l1.TLabel")
        self.saveFileLabel = ttk.Label(self.menuBar, text="Save File", style="l1.TLabel")
        self.aboutLabel = ttk.Label(self.menuBar, text="About", style="l1.TLabel")
        self.openFileLabel.bind("<Button-1>", self.open_file)
        self.saveFileLabel.bind("<Button-1>", self.save_file)
        self.aboutLabel.bind("<Button-1>", self.show_about)
        self.openFileLabel.bind("<Enter>", lambda x: self.change_color(x, "#423F3E"))
        self.openFileLabel.bind("<Leave>", lambda x: self.change_color(x, "#2B2B2B"))
        self.saveFileLabel.bind("<Enter>", lambda x: self.change_color(x, "#423F3E"))
        self.saveFileLabel.bind("<Leave>", lambda x: self.change_color(x, "#2B2B2B"))
        self.aboutLabel.bind("<Enter>", lambda x: self.change_color(x, "#423F3E"))
        self.aboutLabel.bind("<Leave>", lambda x: self.change_color(x, "#2B2B2B"))
        self.openFileLabel.pack(side="left")
        self.saveFileLabel.pack(side="left")
        self.aboutLabel.pack(side="left")
        ttk.Separator(self, orient="horizontal").pack(side="top", fill="x")

        # main frame
        self.mainFrame = ttk.Frame(self, style="f2.TFrame")
        self.mainFrame.pack(side="bottom", fill="both", expand=True, padx=5, pady=5, ipadx=5, ipady=5)

        # image frame
        # 476 525
        self.imageFrame = ttk.Frame(self.mainFrame, style="f1.TFrame")
        self.imageFrame.pack(side="left", padx=5, pady=5, fill="both", expand=True)
        self.imageLabel = ttk.Label(self.imageFrame, text="Please Open Image", style="l1.TLabel")
        self.imageLabel.pack(fill="y", expand=True)

        # control frame
        self.controlFrame = ttk.Frame(self.mainFrame, style="f1.TFrame", width=300)
        self.controlFrame.pack_propagate(False)
        self.controlFrame.pack(side="left", padx=(0, 5), pady=5, fill="y")

        filters = [
            "BLUR",
            "CONTOUR",
            "DETAIL",
            "EDGE_ENHANCE",
            "EMBOSS",
            "SHARPEN",
            "SMOOTH"
        ]
        self.filterVar = tkinter.StringVar(value="BLUR")
        ttk.Label(self.controlFrame, text="Please Choose Filter", style="l1.TLabel").pack(side="top", pady=2)
        self.filterChooser = ttk.Combobox(
            self.controlFrame,
            textvariable=self.filterVar,
            values=filters,
            state="readonly"
        )
        self.filterChooser.bind("<<ComboboxSelected>>", self.on_filter_change)
        self.filterChooser.pack(side="top")
        self.on_filter_change()

        self.resetButton = ttk.Button(self.controlFrame, text="Reset", command=self.editor.reset_image)
        self.resetButton.pack(side="bottom", fill="x", pady=(2, 5), padx=5)

        self.update()
