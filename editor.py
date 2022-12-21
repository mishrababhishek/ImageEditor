"""
Py Image Editor
Developed By : Abhishek Mishra
Contact : mishrababhishek.2899@gmail.com
Description : A Simple Python Gui Application Using Tkinter For Apply Different Filters on Image
"""

import abc
import os
from PIL import Image, ImageTk, ImageFilter


class EditorCallbacks(abc.ABC):
    @abc.abstractmethod
    def image_update(self, img: ImageTk):
        pass

    @abc.abstractmethod
    def on_error(self, msg):
        pass


class Editor:
    name: str
    extension: str
    _img: Image = None
    _reset: Image

    def __init__(self, callback: EditorCallbacks):
        self._callback = callback

    def set_image(self, path: str):
        self._img = Image.open(path)
        self._reset = self._img
        self.name, self.extension = os.path.splitext(path)
        self._callback.image_update(ImageTk.PhotoImage(self._img.resize((525, 476), Image.ANTIALIAS)))

    def reset_image(self):
        if not self.can_save():
            self._callback.on_error("No Image Loaded To Reset")
            return
        self._img = self._reset
        self._callback.image_update(ImageTk.PhotoImage(self._img.resize((525, 476), Image.ANTIALIAS)))

    def apply_blur(self, blur: bool, box_blur: float, gaussian_blur: float):
        if not self.can_save():
            self._callback.on_error("No Image Loaded To Blur")
            return
        if blur:
            self._img = self._img.filter(ImageFilter.BLUR)
        self._img = self._img.filter(ImageFilter.BoxBlur(box_blur))
        self._img = self._img.filter(ImageFilter.GaussianBlur(gaussian_blur))
        self._callback.image_update(ImageTk.PhotoImage(self._img.resize((525, 476), Image.ANTIALIAS)))

    def apply_contour(self, contour: bool):
        if not self.can_save():
            self._callback.on_error("No Image Loaded To Contour")
            return
        if contour:
            self._img = self._img.filter(ImageFilter.CONTOUR())
            self._callback.image_update(ImageTk.PhotoImage(self._img.resize((525, 476), Image.ANTIALIAS)))

    def apply_detail(self, detail: bool):
        if not self.can_save():
            self._callback.on_error("No Image Loaded To Detail")
            return
        if detail:
            self._img = self._img.filter(ImageFilter.DETAIL())
            self._callback.image_update(ImageTk.PhotoImage(self._img.resize((525, 476), Image.ANTIALIAS)))

    def apply_edge_enhance(self, enhance: bool):
        if not self.can_save():
            self._callback.on_error("No Image Loaded To Enhance")
            return
        if enhance:
            self._img = self._img.filter(ImageFilter.EDGE_ENHANCE())
            self._callback.image_update(ImageTk.PhotoImage(self._img.resize((525, 476), Image.ANTIALIAS)))

    def apply_emboss(self, emboss: bool):
        if not self.can_save():
            self._callback.on_error("No Image Loaded To Emboss")
            return
        if emboss:
            self._img = self._img.filter(ImageFilter.EMBOSS())
            self._callback.image_update(ImageTk.PhotoImage(self._img.resize((525, 476), Image.ANTIALIAS)))

    def apply_sharpen(self, sharpen: bool):
        if not self.can_save():
            self._callback.on_error("No Image Loaded To Sharpen")
            return
        if sharpen:
            self._img = self._img.filter(ImageFilter.SHARPEN())
            self._callback.image_update(ImageTk.PhotoImage(self._img.resize((525, 476), Image.ANTIALIAS)))

    def apply_smooth(self, smooth):
        if not self.can_save():
            self._callback.on_error("No Image Loaded To Smooth")
            return
        if smooth:
            self._img = self._img.filter(ImageFilter.SMOOTH())
            self._callback.image_update(ImageTk.PhotoImage(self._img.resize((525, 476), Image.ANTIALIAS)))

    def save_image(self, path: str):
        self._img.save(path)

    def can_save(self):
        return self._img is not None
