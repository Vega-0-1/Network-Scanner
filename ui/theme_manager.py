import tkinter as tk
from tkinter import ttk


class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.dark_mode = False

    def apply_light_theme(self):
        """Apply light theme styles to the application."""
        self.dark_mode = False
        self._set_global_style(bg="#FFFFFF", fg="#000000", progress_bg="#0078D7")

    def apply_dark_theme(self):
        """Apply dark theme styles to the application."""
        self.dark_mode = True
        self._set_global_style(bg="#2E2E2E", fg="#FFFFFF", progress_bg="#FFA500")

    def _set_global_style(self, bg, fg, progress_bg):
        """Set global styles for the application."""
        self.root.tk_setPalette(background=bg, foreground=fg)
        for widget in self.root.winfo_children():
            self._set_widget_style(widget, bg, fg, progress_bg)

    def _set_widget_style(self, widget, bg, fg, progress_bg):
        """Recursively apply styles to all widgets."""
        if isinstance(widget, (tk.Tk, tk.Toplevel)):
            for child in widget.winfo_children():
                self._set_widget_style(child, bg, fg, progress_bg)
        else:
            try:
                widget.configure(background=bg, foreground=fg)
                if isinstance(widget, ttk.Progressbar):
                    widget.configure(style="Custom.Horizontal.TProgressbar")
            except tk.TclError:
                pass
