# import tkinter as tk
# from tkinter import ttk, messagebox
# from PIL import Image, ImageTk, ImageOps, ImageDraw
# import urllib.request
# import io
# import re
# import sys
# import os

# # Style Consts
# DARK_BG = "#1e1e1e"
# CARD_BG = "#2a2a2a"
# ACCENT = "#33ccff"
# TEXT_COLOR = "#ffffff"
# HIGHLIGHT = "#444"
# SELECT_COLOR = "#3c84f4"

# class YouTubeThumbnailApp(tk.Tk):
#     def __init__(self):
#         super(YouTubeThumbnailApp, self).__init__()
#         self.title("YouTube Thumbnail Downloader")
#         self.geometry("800x480")
#         self.configure(bg=DARK_BG)
#         self.resizable(False, False)
        
#         # Configuración del ícono
#         try:
#             if getattr(sys, 'frozen', False):
#                 icon_path = os.path.join(sys._MEIPASS, 'yt_thumb.ico')
#             else:
#                 icon_path = 'yt_thumb.ico'
                
#             self.iconbitmap(icon_path)
#         except Exception as e:
#             print("Error loading icon: {}".format(str(e)))

#         # Center Window
#         self.update_idletasks()
#         width = 800
#         height = 480
#         x = (self.winfo_screenwidth() // 2) - (width // 2)
#         y = (self.winfo_screenheight() // 2) - (height // 2)
#         self.geometry("{}x{}+{}+{}".format(width, height, x, y))

#         style = ttk.Style(self)
#         self.configure_style(style)

#         self.container = tk.Frame(self, bg=DARK_BG)
#         self.container.pack(fill="both", expand=True)

#         self.frames = {}
#         for F in (StartPage, ThumbnailPage):
#             frame = F(self.container, self)
#             self.frames[F] = frame
#             frame.place(x=0, y=0, relwidth=1, relheight=1)

#         self.show_frame(StartPage)

#     def configure_style(self, style):
#         style.theme_use("clam")
#         style.configure("Rounded.TButton",
#                         font=("Segoe UI", 12),
#                         padding=8,
#                         relief="flat",
#                         background=ACCENT,
#                         foreground=TEXT_COLOR,
#                         borderwidth=0,
#                         focusthickness=0)
#         style.map("Rounded.TButton",
#                 background=[("active", "#29b6f6")],
#                 lightcolor=[("active", ACCENT)],
#                 darkcolor=[("active", ACCENT)])

#     def show_frame(self, cont):
#         frame = self.frames[cont]
#         frame.tkraise()

# class StartPage(tk.Frame):
#     def __init__(self, parent, controller):
#         super(StartPage, self).__init__(parent, bg=DARK_BG)
#         self.controller = controller

#         ttk.Label(self, text="Download YouTube Thumbnails", 
#                 font=("Segoe UI", 24, "bold"),
#                 background=DARK_BG, foreground=TEXT_COLOR).pack(pady=40)

#         self.entry_frame = tk.Frame(self, bg=ACCENT)
#         self.entry_frame.pack(pady=10)
#         self.url_entry = tk.Entry(
#             self.entry_frame, font=("Segoe UI", 12), width=50,
#             bg=CARD_BG, fg=TEXT_COLOR, bd=0, relief="flat",
#             insertbackground=TEXT_COLOR
#         )
#         self.url_entry.pack(padx=3, pady=3, ipady=6)

#         self.menu = tk.Menu(self, tearoff=0, bg=CARD_BG, fg=TEXT_COLOR)
#         self.menu.add_command(label="Paste", command=lambda: self.url_entry.event_generate("<<Paste>>"))
#         self.url_entry.bind("<Button-3>", self.show_context_menu)

#         self.search_button = ttk.Button(self, text="Search", style="Rounded.TButton", command=self.on_search)
#         self.search_button.pack(pady=20)

#     def show_context_menu(self, event):
#         self.menu.tk_popup(event.x_root, event.y_root)

#     def extract_video_id(self, url):
#         patterns = [r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})"]
#         for pattern in patterns:
#             match = re.search(pattern, url)
#             if match:
#                 return match.group(1)
#         return None

#     def on_search(self):
#         url = self.url_entry.get().strip()
#         if not url:
#             messagebox.showwarning("Empty Field", "Please enter a valid URL.")
#             return

#         video_id = self.extract_video_id(url)
#         if not video_id:
#             messagebox.showerror("Invalid URL", "Video ID could not be extracted.")
#             return

#         self.controller.frames[ThumbnailPage].load_thumbnails(video_id)
#         self.controller.show_frame(ThumbnailPage)

# class ThumbnailPage(tk.Frame):
#     def __init__(self, parent, controller):
#         super(ThumbnailPage, self).__init__(parent, bg=DARK_BG)
#         self.controller = controller
#         self.selected_indices = []
#         self.thumbnails = []
#         self.video_id = ""
#         self.resolutions = {
#             "maxresdefault": "1280x720",
#             "sddefault": "640x480",
#             "hqdefault": "480x360",
#             "mqdefault": "320x180",
#             "default": "120x90"
#         }

#         top_frame = tk.Frame(self, bg=DARK_BG)
#         top_frame.pack(side="top", fill="x")
        
#         ttk.Button(top_frame, text="Back", style="Rounded.TButton",
#                 command=lambda: controller.show_frame(StartPage)).pack(side="left", padx=10, pady=10)

#         self.main_container = tk.Frame(self, bg=DARK_BG)
#         self.main_container.pack(expand=True, fill="both")
        
#         self.grid_frame = tk.Frame(self.main_container, bg=DARK_BG)
#         self.grid_frame.pack(expand=True)

#         for i in range(3):
#             self.grid_frame.columnconfigure(i, weight=1)

#         self.bottom_frame = tk.Frame(self, bg=DARK_BG)
#         self.bottom_frame.pack(side="bottom", fill="x", pady=10)
#         self.download_button = ttk.Button(self.bottom_frame, text="Download All", style="Rounded.TButton",
#                                         command=self.download_thumbnails, state="normal")
#         self.download_button.pack()

#     def create_rounded_thumbnail(self, im, radius=10):
#         mask = Image.new("L", im.size, 0)
#         draw = ImageDraw.Draw(mask)
        
#         draw.rectangle([(0, radius), (im.size[0], im.size[1]-radius)], fill=255)
#         draw.rectangle([(radius, 0), (im.size[0]-radius, im.size[1])], fill=255)
#         draw.pieslice([(0, 0), (radius*2, radius*2)], 180, 270, fill=255)
#         draw.pieslice([(im.size[0]-radius*2, 0), (im.size[0], radius*2)], 270, 360, fill=255)
#         draw.pieslice([(0, im.size[1]-radius*2), (radius*2, im.size[1])], 90, 180, fill=255)
#         draw.pieslice([(im.size[0]-radius*2, im.size[1]-radius*2), (im.size[0], im.size[1])], 0, 90, fill=255)
        
#         im.putalpha(mask)
#         return im

#     def load_thumbnails(self, video_id):
#         self.video_id = video_id
#         for widget in self.grid_frame.winfo_children():
#             widget.destroy()

#         self.thumbnails = []
#         self.selected_indices = []
#         self.download_button.config(state="normal", text="Download All")

#         qualities = ["maxresdefault", "sddefault", "hqdefault", "mqdefault", "default"]
#         thumbnail_size = (160, 90)
#         border_size = 3

#         for index, quality in enumerate(qualities):
#             url = "https://img.youtube.com/vi/{0}/{1}.jpg".format(video_id, quality)
#             try:
#                 with urllib.request.urlopen(url) as u:
#                     raw_data = u.read()
#                 im = Image.open(io.BytesIO(raw_data)).convert("RGB")
#                 im = im.resize(thumbnail_size)
#                 im = ImageOps.expand(im, border=border_size, fill=DARK_BG)
#                 im = self.create_rounded_thumbnail(im, 8)
#                 photo = ImageTk.PhotoImage(im)

#                 resolution = self.resolutions[quality]
#                 self.thumbnails.append((url, photo, resolution))

#                 main_frame = tk.Frame(self.grid_frame, bg=DARK_BG)
#                 main_frame.grid(row=index // 3, column=index % 3, padx=10, pady=10, sticky="nsew")

#                 selection_frame = tk.Frame(main_frame, bg=DARK_BG, 
#                                         highlightthickness=2, 
#                                         highlightbackground=DARK_BG)
#                 selection_frame.pack()

#                 lbl = tk.Label(selection_frame, image=photo, bg=DARK_BG, cursor="hand2")
#                 lbl.image = photo
#                 lbl.pack()

#                 ttk.Label(main_frame, text=resolution,
#                         background=DARK_BG, foreground=TEXT_COLOR).pack()

#                 lbl.bind("<Button-1>", lambda e, idx=index, sf=selection_frame: self.on_select(idx, sf))

#             except Exception as e:
#                 print("Error loading Image: {}".format(str(e)))

#     def on_select(self, index, selection_frame):
#         if index in self.selected_indices:
#             self.selected_indices.remove(index)
#             selection_frame.config(highlightbackground=DARK_BG)
#         else:
#             self.selected_indices.append(index)
#             selection_frame.config(highlightbackground=SELECT_COLOR)

#         self.download_button.config(
#             text="Download Selected" if self.selected_indices else "Download All"
#         )

#     def download_thumbnails(self):
#         # Base Path
#         if getattr(sys, 'frozen', False):
#             base_dir = os.path.dirname(sys.executable)
#         else:
#             base_dir = os.path.dirname(os.path.abspath(__file__))
        
#         thumb_dir = os.path.join(base_dir, "thumb")
#         try:
#             os.makedirs(thumb_dir, exist_ok=True)
#         except Exception as e:
#             messagebox.showerror("Error", "Could not create directory: {}".format(e))
#             return

#         indices = self.selected_indices if self.selected_indices else range(len(self.thumbnails))

#         download_errors = []
#         for idx in indices:
#             url, _, resolution = self.thumbnails[idx]
#             try:
#                 filename = "thumbnail_{}_{}.jpg".format(self.video_id, resolution)
#                 filepath = os.path.join(thumb_dir, filename)
#                 urllib.request.urlretrieve(url, filepath)
#             except Exception as e:
#                 download_errors.append(str(e))

#         if download_errors:
#             error_msg = "Errors occurred:\n\n" + "\n".join(download_errors)
#             messagebox.showerror("Error", error_msg)
#         else:
#             messagebox.showinfo("Success", "Thumbnails successfully saved in:\n{}".format(thumb_dir))
        
#         self.selected_indices.clear()
#         self.download_button.config(text="Download All")
#         for child in self.grid_frame.winfo_children():
#             for widget in child.winfo_children():
#                 if isinstance(widget, tk.Frame):
#                     widget.config(highlightbackground=DARK_BG)

# if __name__ == "__main__":
#     app = YouTubeThumbnailApp()
#     app.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageOps, ImageDraw
import urllib.request
import io
import re
import sys
import os
import webbrowser

# Style Consts
DARK_BG = "#1e1e1e"
CARD_BG = "#2a2a2a"
ACCENT = "#33ccff"
TEXT_COLOR = "#ffffff"
HIGHLIGHT = "#444"
SELECT_COLOR = "#3c84f4"

class YouTubeThumbnailApp(tk.Tk):
    def __init__(self):
        super(YouTubeThumbnailApp, self).__init__()
        self.title("YouTube Thumbnail Downloader")
        self.geometry("800x480")
        self.configure(bg=DARK_BG)
        self.resizable(False, False)
        
        # Configuración del ícono
        try:
            if getattr(sys, 'frozen', False):
                icon_path = os.path.join(sys._MEIPASS, 'yt_thumb.ico')
            else:
                icon_path = 'yt_thumb.ico'
                
            self.iconbitmap(icon_path)
        except Exception as e:
            print("Error loading icon: {}".format(str(e)))

        # Center Window
        self.update_idletasks()
        width = 800
        height = 480
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry("{}x{}+{}+{}".format(width, height, x, y))

        style = ttk.Style(self)
        self.configure_style(style)

        self.container = tk.Frame(self, bg=DARK_BG)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (StartPage, ThumbnailPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame(StartPage)

    def configure_style(self, style):
        style.theme_use("clam")
        style.configure("Rounded.TButton",
                        font=("Segoe UI", 12),
                        padding=8,
                        relief="flat",
                        background=ACCENT,
                        foreground=TEXT_COLOR,
                        borderwidth=0,
                        focusthickness=0)
        style.map("Rounded.TButton",
                background=[("active", "#29b6f6")],
                lightcolor=[("active", ACCENT)],
                darkcolor=[("active", ACCENT)])

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super(StartPage, self).__init__(parent, bg=DARK_BG)
        self.controller = controller

        ttk.Label(self, text="Download YouTube Thumbnails", 
                font=("Segoe UI", 24, "bold"),
                background=DARK_BG, foreground=TEXT_COLOR).pack(pady=40)

        self.entry_frame = tk.Frame(self, bg=ACCENT)
        self.entry_frame.pack(pady=10)
        self.url_entry = tk.Entry(
            self.entry_frame, font=("Segoe UI", 12), width=50,
            bg=CARD_BG, fg=TEXT_COLOR, bd=0, relief="flat",
            insertbackground=TEXT_COLOR
        )
        self.url_entry.pack(padx=3, pady=3, ipady=6)
        self.url_entry.bind("<Return>", lambda event: self.on_search())  # Enter key binding

        self.menu = tk.Menu(self, tearoff=0, bg=CARD_BG, fg=TEXT_COLOR)
        self.menu.add_command(label="Paste", command=lambda: self.url_entry.event_generate("<<Paste>>"))
        self.url_entry.bind("<Button-3>", self.show_context_menu)

        self.search_button = ttk.Button(self, text="Search", style="Rounded.TButton", command=self.on_search)
        self.search_button.pack(pady=20)

        # Credits label with link
        credit_label = tk.Label(self, 
                             text="Credits to MichaelX17", 
                             fg=ACCENT, 
                             bg=DARK_BG,
                             font=("Segoe UI", 10, 'bold'),
                             cursor="hand2")
        credit_label.pack(side="bottom", pady=20)
        credit_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/MichaelX17"))

    def show_context_menu(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)

    def extract_video_id(self, url):
        patterns = [r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})"]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def on_search(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Empty Field", "Please enter a valid URL.")
            return

        video_id = self.extract_video_id(url)
        if not video_id:
            messagebox.showerror("Invalid URL", "Video ID could not be extracted.")
            return

        self.controller.frames[ThumbnailPage].load_thumbnails(video_id)
        self.controller.show_frame(ThumbnailPage)

class ThumbnailPage(tk.Frame):
    def __init__(self, parent, controller):
        super(ThumbnailPage, self).__init__(parent, bg=DARK_BG)
        self.controller = controller
        self.selected_indices = []
        self.thumbnails = []
        self.video_id = ""
        self.resolutions = {
            "maxresdefault": "1280x720",
            "sddefault": "640x480",
            "hqdefault": "480x360",
            "mqdefault": "320x180",
            "default": "120x90"
        }

        top_frame = tk.Frame(self, bg=DARK_BG)
        top_frame.pack(side="top", fill="x")
        
        ttk.Button(top_frame, text="Back", style="Rounded.TButton",
                command=lambda: controller.show_frame(StartPage)).pack(side="left", padx=10, pady=10)

        self.main_container = tk.Frame(self, bg=DARK_BG)
        self.main_container.pack(expand=True, fill="both")
        
        self.grid_frame = tk.Frame(self.main_container, bg=DARK_BG)
        self.grid_frame.pack(expand=True)

        for i in range(3):
            self.grid_frame.columnconfigure(i, weight=1)

        self.bottom_frame = tk.Frame(self, bg=DARK_BG)
        self.bottom_frame.pack(side="bottom", fill="x", pady=10)
        self.download_button = ttk.Button(self.bottom_frame, text="Download All", style="Rounded.TButton",
                                        command=self.download_thumbnails, state="normal")
        self.download_button.pack()

    def create_rounded_thumbnail(self, im, radius=10):
        mask = Image.new("L", im.size, 0)
        draw = ImageDraw.Draw(mask)
        
        draw.rectangle([(0, radius), (im.size[0], im.size[1]-radius)], fill=255)
        draw.rectangle([(radius, 0), (im.size[0]-radius, im.size[1])], fill=255)
        draw.pieslice([(0, 0), (radius*2, radius*2)], 180, 270, fill=255)
        draw.pieslice([(im.size[0]-radius*2, 0), (im.size[0], radius*2)], 270, 360, fill=255)
        draw.pieslice([(0, im.size[1]-radius*2), (radius*2, im.size[1])], 90, 180, fill=255)
        draw.pieslice([(im.size[0]-radius*2, im.size[1]-radius*2), (im.size[0], im.size[1])], 0, 90, fill=255)
        
        im.putalpha(mask)
        return im

    def load_thumbnails(self, video_id):
        self.video_id = video_id
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.thumbnails = []
        self.selected_indices = []
        self.download_button.config(state="normal", text="Download All")

        qualities = ["maxresdefault", "sddefault", "hqdefault", "mqdefault", "default"]
        thumbnail_size = (160, 90)
        border_size = 3

        for index, quality in enumerate(qualities):
            url = "https://img.youtube.com/vi/{0}/{1}.jpg".format(video_id, quality)
            try:
                with urllib.request.urlopen(url) as u:
                    raw_data = u.read()
                im = Image.open(io.BytesIO(raw_data)).convert("RGB")
                im = im.resize(thumbnail_size)
                im = ImageOps.expand(im, border=border_size, fill=DARK_BG)
                im = self.create_rounded_thumbnail(im, 8)
                photo = ImageTk.PhotoImage(im)

                resolution = self.resolutions[quality]
                self.thumbnails.append((url, photo, resolution))

                main_frame = tk.Frame(self.grid_frame, bg=DARK_BG)
                main_frame.grid(row=index // 3, column=index % 3, padx=10, pady=10, sticky="nsew")

                selection_frame = tk.Frame(main_frame, bg=DARK_BG, 
                                        highlightthickness=2, 
                                        highlightbackground=DARK_BG)
                selection_frame.pack()

                lbl = tk.Label(selection_frame, image=photo, bg=DARK_BG, cursor="hand2")
                lbl.image = photo
                lbl.pack()

                ttk.Label(main_frame, text=resolution,
                        background=DARK_BG, foreground=TEXT_COLOR).pack()

                lbl.bind("<Button-1>", lambda e, idx=index, sf=selection_frame: self.on_select(idx, sf))

            except Exception as e:
                print("Error loading Image: {}".format(str(e)))

    def on_select(self, index, selection_frame):
        if index in self.selected_indices:
            self.selected_indices.remove(index)
            selection_frame.config(highlightbackground=DARK_BG)
        else:
            self.selected_indices.append(index)
            selection_frame.config(highlightbackground=SELECT_COLOR)

        self.download_button.config(
            text="Download Selected" if self.selected_indices else "Download All"
        )

    def download_thumbnails(self):
        # Base Path
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        
        thumb_dir = os.path.join(base_dir, "thumb")
        try:
            os.makedirs(thumb_dir, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", "Could not create directory: {}".format(e))
            return

        indices = self.selected_indices if self.selected_indices else range(len(self.thumbnails))

        download_errors = []
        for idx in indices:
            url, _, resolution = self.thumbnails[idx]
            try:
                filename = "thumbnail_{}_{}.jpg".format(self.video_id, resolution)
                filepath = os.path.join(thumb_dir, filename)
                urllib.request.urlretrieve(url, filepath)
            except Exception as e:
                download_errors.append(str(e))

        if download_errors:
            error_msg = "Errors occurred:\n\n" + "\n".join(download_errors)
            messagebox.showerror("Error", error_msg)
        else:
            messagebox.showinfo("Success", "Thumbnails successfully saved in:\n{}".format(thumb_dir))
        
        self.selected_indices.clear()
        self.download_button.config(text="Download All")
        for child in self.grid_frame.winfo_children():
            for widget in child.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.config(highlightbackground=DARK_BG)

if __name__ == "__main__":
    app = YouTubeThumbnailApp()
    app.mainloop()