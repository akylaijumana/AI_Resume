"""
Modern Custom Widgets for AI Resume Generator
"""
import tkinter as tk


class ModernButton(tk.Canvas):
    """Custom modern button with hover effects"""
    def __init__(self, parent, text, command, bg_color="#4F46E5", hover_color="#4338CA",
                 text_color="white", width=200, height=50, **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent.cget('bg'),
                        highlightthickness=0, **kwargs)

        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.width = width
        self.height = height
        self.text = text

        self.draw_button(self.bg_color)

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def draw_button(self, color):
        self.delete("all")
        radius = 10
        self.create_rounded_rect(2, 2, self.width-2, self.height-2, radius, fill=color, outline="")
        self.create_text(self.width/2, self.height/2, text=self.text,
                        fill=self.text_color, font=("Segoe UI", 11, "bold"))

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_enter(self, e):
        self.draw_button(self.hover_color)
        self.config(cursor="hand2")

    def on_leave(self, e):
        self.draw_button(self.bg_color)

    def on_click(self, e):
        if self.command:
            self.command()

