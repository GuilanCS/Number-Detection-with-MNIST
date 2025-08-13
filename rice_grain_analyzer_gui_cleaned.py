#!/usr/bin/env python3
"""
Rice Grain Analyzer GUI

A comprehensive GUI application for analyzing rice grain properties including
dimensional measurements, shape characteristics, and classification.

Build command:
pyinstaller --onefile --noconsole --add-data "fonts/Vazirmatn.ttf;fonts" rice_grain_analyzer_gui_cleaned.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import sys
import os
from typing import Optional, Tuple, Dict, Any
import arabic_reshaper
from bidi.algorithm import get_display

# Constants
WINDOW_TITLE = "Rice Grain Analyzer"
WINDOW_SIZE = "1920x1080"
BG_COLOR = "#eaffd0"
FRAME_BG_COLOR = "#f6ffcc"
FRAME_BORDER_WIDTH = 2

# Font configurations
FONT_SIZES = {
    'small': 10,
    'medium': 13,
    'large': 18
}

# Layout positions and sizes
LAYOUT_CONFIG = {
    'left_up': {'x': 10, 'y': 70, 'width': 410, 'height': 570},
    'left_mid': {'x': 10, 'y': 640, 'width': 410, 'height': 190},
    'left_down': {'x': 10, 'y': 830, 'width': 410, 'height': 180},
    'center_left': {'x': 430, 'y': 70, 'width': 540, 'height': 940},
    'center_right_up': {'x': 980, 'y': 70, 'width': 540, 'height': 530},
    'center_right_down': {'x': 980, 'y': 610, 'width': 540, 'height': 400},
    'right': {'x': 1530, 'y': 70, 'width': 380, 'height': 940}
}

# Text content
TEXTS = {
    'title': "رابط کاربری آنالیز برنج",
    'operation_menu': "منوی عملیاتی",
    'dimensional_props': "خصوصیات ابعادی",
    'shape_props': "ویژگی های شکلی",
    'dimensional_classification': "طبقه بندی ابعادی",
    'fracture_props': "خصوصیات شکستگی",
    'other_visual_props': "سایر ویژگی های ظاهری",
    'grain_grading': "درجه بندی دانه ها",
    'single_grain_analysis': "انتخاب و آنالیز یک دانه"
}

# Button configurations
OPERATION_BUTTONS = [
    ("اسکن تصویر جدید", "red"),
    ("بارگذاری تصویر", "red"),
    ("اندازه گیری طول و عرض", "red"),
    ("ذخیره ابعاد", "red"),
    ("آنالیز کلی دانه ها", "green"),
]

SAVE_LOAD_BUTTONS = [
    ("ذخیره اطلاعات", "red"),
    ("باز کردن فایل اکسل", "red")
]

# Data categories
DIMENSIONAL_LABELS = ["طول (میلی متر)", "عرض (میلی متر)", "ضخامت (میلی متر)"]
SHAPE_LABELS = ["گردی", "ضریب رعنایی"]
GRAIN_TYPES = ["دانه کامل", "خیلی بلند", "بلند", "متوسط", "کوتاه"]
BROKEN_TYPES = ["دانه سرشکسته", "دانه شکسته", "شکسته درشت", "شکسته متوسط", "شکسته کوچک", "ریزه"]
OTHER_FEATURES = [
    "دانه گچی", "دانه قرمز", "دانه با رگه قرمز", "دانه با لکه سیاه",
    "دانه های قهوه ای", "دانه های نارس", "دانه های ترک دار"
]
SINGLE_GRAIN_FEATURES = [
    "دانه ی شماره", "طول دانه (میلی متر)", "عرض دانه (میلی متر)",
    "ضریب رعنایی دانه", "گردی دانه", "سفیدی دانه (درصد)",
    "گچی بیشتر از 50 درصد", "لکه قرمز (درصد)", "لکه سیاه (درصد)"
]


class FontManager:
    """Manages font loading and configuration."""
    
    def __init__(self):
        self.fonts = {}
        self._setup_fonts()
    
    def _setup_fonts(self) -> None:
        """Setup fonts based on platform."""
        if sys.platform.startswith("win"):
            persian_font_family = "Vazir"
            font_path = os.path.join(os.path.dirname(__file__), "fonts", "Vazirmatn.ttf")
        else:
            persian_font_family = "B Nazanin"
            font_path = os.path.join(os.path.dirname(__file__), "fonts", "B Nazanin.ttf")
        
        # Load fonts with different sizes
        self.fonts['small'] = self._load_custom_font(
            persian_font_family, font_path, FONT_SIZES['small']
        )
        self.fonts['medium'] = self._load_custom_font(
            persian_font_family, font_path, FONT_SIZES['medium']
        )
        self.fonts['large'] = self._load_custom_font(
            persian_font_family, font_path, FONT_SIZES['large'], weight="bold"
        )
    
    def _load_custom_font(self, font_name: str, font_path: str, 
                         size: int, weight: str = "normal") -> font.Font:
        """Load custom font with fallback to Arial."""
        try:
            if os.path.exists(font_path):
                return font.Font(family=font_name, size=size, weight=weight)
            else:
                print(f"Font file {font_path} not found, falling back to Arial")
                return font.Font(family="Arial", size=size, weight=weight)
        except Exception as e:
            print(f"Error loading font {font_name}: {e}, falling back to Arial")
            return font.Font(family="Arial", size=size, weight=weight)
    
    def get_font(self, size: str) -> font.Font:
        """Get font by size category."""
        return self.fonts.get(size, self.fonts['medium'])


class StatusIndicator(tk.Canvas):
    """A circular status indicator widget."""
    
    def __init__(self, parent: tk.Widget, color: str = "red", **kwargs):
        super().__init__(parent, width=20, height=20, highlightthickness=0, **kwargs)
        self.color = color
        self._draw_circle()
    
    def _draw_circle(self) -> None:
        """Draw the status circle."""
        self.create_oval(2, 2, 18, 18, fill=self.color, outline="black")
    
    def set_color(self, color: str) -> None:
        """Update the status indicator color."""
        self.color = color
        self.delete("all")
        self._draw_circle()


class UIComponents:
    """Factory class for creating UI components."""
    
    @staticmethod
    def create_readonly_entry(parent: tk.Widget, width: int = 10, 
                            value: str = "", font_obj: Optional[font.Font] = None, 
                            ipady: int = 0) -> tk.Entry:
        """Create a readonly entry widget."""
        if font_obj is None:
            font_obj = ("Arial", 10)
        
        entry = tk.Entry(parent, width=width, justify="center", font=font_obj)
        entry.insert(0, value)
        entry.config(state="readonly")
        
        if ipady:
            entry.grid_configure(ipady=ipady)
        
        return entry
    
    @staticmethod
    def create_labeled_entry(parent: tk.Widget, label: str, width: int = 10, 
                           value: str = "") -> Tuple[tk.Frame, tk.Entry]:
        """Create a labeled entry widget."""
        frame = tk.Frame(parent)
        tk.Label(frame, text=label, font=("Arial", 10), anchor="e").pack(side=tk.RIGHT)
        entry = UIComponents.create_readonly_entry(frame, width, value)
        entry.pack(side=tk.RIGHT, padx=2)
        return frame, entry
    
    @staticmethod
    def create_frame(parent: tk.Widget, layout_key: str) -> tk.Frame:
        """Create a frame with predefined layout configuration."""
        config = LAYOUT_CONFIG[layout_key]
        frame = tk.Frame(parent, bg=FRAME_BG_COLOR, bd=FRAME_BORDER_WIDTH, relief=tk.GROOVE)
        frame.place(x=config['x'], y=config['y'], 
                   width=config['width'], height=config['height'])
        return frame


def setup_dpi_awareness() -> None:
    """Enable DPI awareness for Windows."""
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass


def format_persian_text(text: str) -> str:
    """Format Persian text for proper display."""
    return get_display(arabic_reshaper.reshape(text))


class RiceGrainAnalyzer:
    """Main application class for Rice Grain Analyzer."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.font_manager = FontManager()
        self._setup_window()
        self._create_ui()
    
    def _setup_window(self) -> None:
        """Configure the main window."""
        setup_dpi_awareness()
        
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=BG_COLOR)
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self.root.resizable(False, False)
    
    def _create_ui(self) -> None:
        """Create the user interface."""
        self._create_banner()
        self._create_frames()
        self._populate_frames()
    
    def _create_banner(self) -> None:
        """Create the top banner."""
        banner = tk.Frame(self.root, bg=BG_COLOR)
        banner.pack(fill=tk.X, pady=5)
        tk.Label(banner, text=format_persian_text(TEXTS['title']),
                font=self.font_manager.get_font('medium'), 
                bg=BG_COLOR, fg="brown", anchor="e").pack(anchor="center")
    
    def _create_frames(self) -> None:
        """Create all main frames."""
        self.frames = {}
        for layout_key in LAYOUT_CONFIG.keys():
            self.frames[layout_key] = UIComponents.create_frame(self.root, layout_key)
    
    def _populate_frames(self) -> None:
        """Populate all frames with content."""
        self._populate_left_panel()
        self._populate_center_panel()
        self._populate_right_panel()
    
    def _populate_left_panel(self) -> None:
        """Populate the left panel with operation menu and properties."""
        self._create_operation_menu()
        self._create_dimensional_properties()
        self._create_shape_properties()
    
    def _create_operation_menu(self) -> None:
        """Create the operation menu in the left upper frame."""
        frame = self.frames['left_up']
        
        # Title
        tk.Label(frame, text=format_persian_text(TEXTS['operation_menu']),
                font=self.font_manager.get_font('large'), 
                bg=FRAME_BG_COLOR, anchor="e").pack(pady=5)
        
        # Operation buttons with status indicators
        for text, color in OPERATION_BUTTONS:
            btn_frame = tk.Frame(frame, bg=FRAME_BG_COLOR)
            tk.Button(btn_frame, text=format_persian_text(text), width=20,
                     font=self.font_manager.get_font('small'), 
                     anchor="center").pack(side=tk.LEFT, pady=3)
            StatusIndicator(btn_frame, color=color).pack(side=tk.LEFT, padx=5)
            btn_frame.pack(pady=1)
        
        # Checkboxes
        checkboxes = [
            "دانه معمولی",
            "دانه بسیار سفید مانند علی کاظمی و بی نام",
            "دانه شفاف"
        ]
        for checkbox_text in checkboxes:
            tk.Checkbutton(frame, text=format_persian_text(checkbox_text),
                          width=15 if len(checkbox_text) < 20 else 20,
                          font=self.font_manager.get_font('small'), 
                          bg=FRAME_BG_COLOR, anchor="center").pack()
        
        # Save/Load buttons
        for text, color in SAVE_LOAD_BUTTONS:
            btn_frame = tk.Frame(frame, bg=FRAME_BG_COLOR)
            tk.Button(btn_frame, text=format_persian_text(text), width=25,
                     font=self.font_manager.get_font('small'), 
                     anchor="e").pack(side=tk.RIGHT)
            StatusIndicator(btn_frame, color=color).pack(side=tk.RIGHT, padx=5)
            btn_frame.pack(pady=3)
    
    def _create_dimensional_properties(self) -> None:
        """Create dimensional properties section."""
        frame = self.frames['left_mid']
        
        tk.Label(frame, text=format_persian_text(TEXTS['dimensional_props']),
                font=self.font_manager.get_font('large'), 
                bg=FRAME_BG_COLOR, anchor="e").pack(pady=3)
        
        dim_frame = tk.Frame(frame, bg=FRAME_BG_COLOR)
        dim_frame.pack(pady=0)
        
        # Headers
        tk.Label(dim_frame, text=format_persian_text("انحراف معیار"),
                font=self.font_manager.get_font('small'), 
                bg=FRAME_BG_COLOR, anchor="e").grid(row=0, column=2)
        tk.Label(dim_frame, text=format_persian_text("میانگین"),
                font=self.font_manager.get_font('small'), 
                bg=FRAME_BG_COLOR, anchor="e").grid(row=0, column=1)
        
        # Dimensional measurements
        for i, label in enumerate(DIMENSIONAL_LABELS):
            tk.Label(dim_frame, text=format_persian_text(label),
                    font=self.font_manager.get_font('small'), 
                    bg=FRAME_BG_COLOR, anchor="center").grid(row=i+1, column=0, sticky="e")
            UIComponents.create_readonly_entry(dim_frame, 10, "N/A").grid(row=i+1, column=1)
            UIComponents.create_readonly_entry(dim_frame, 10, "N/A").grid(row=i+1, column=2)
    
    def _create_shape_properties(self) -> None:
        """Create shape properties section."""
        frame = self.frames['left_down']
        
        tk.Label(frame, text=format_persian_text(TEXTS['shape_props']),
                font=self.font_manager.get_font('large'), 
                bg=FRAME_BG_COLOR, anchor="e").pack(pady=3)
        
        shape_frame = tk.Frame(frame, bg=FRAME_BG_COLOR)
        shape_frame.pack()
        
        # Headers
        tk.Label(shape_frame, text=format_persian_text("انحراف معیار"),
                font=self.font_manager.get_font('small'), 
                bg=FRAME_BG_COLOR, anchor="e").grid(row=0, column=2)
        tk.Label(shape_frame, text=format_persian_text("میانگین"),
                font=self.font_manager.get_font('small'), 
                bg=FRAME_BG_COLOR, anchor="e").grid(row=0, column=1)
        
        # Shape measurements
        for i, label in enumerate(SHAPE_LABELS):
            tk.Label(shape_frame, text=format_persian_text(label),
                    font=self.font_manager.get_font('small'), 
                    bg=FRAME_BG_COLOR, anchor="e").grid(row=i+1, column=0, sticky="e")
            UIComponents.create_readonly_entry(shape_frame, 10, "0.000").grid(row=i+1, column=1)
            UIComponents.create_readonly_entry(shape_frame, 10, "0.000").grid(row=i+1, column=2)
    
    def _populate_center_panel(self) -> None:
        """Populate the center panels."""
        self._create_dimensional_classification()
        self._create_other_features()
        self._create_grading_section()
    
    def _create_dimensional_classification(self) -> None:
        """Create dimensional classification section."""
        frame = self.frames['center_left']
        
        tk.Label(frame, text=format_persian_text(TEXTS['dimensional_classification']),
                font=self.font_manager.get_font('large'), 
                bg=FRAME_BG_COLOR).pack(pady=5)
        
        # Total grains count
        total_frame = tk.Frame(frame, bg=FRAME_BG_COLOR)
        total_frame.pack(pady=2)
        tk.Label(total_frame, text=format_persian_text("تعداد کل دانه ها"), 
                font=self.font_manager.get_font('small'), 
                bg=FRAME_BG_COLOR).pack(side=tk.LEFT)
        UIComponents.create_readonly_entry(total_frame, 15, format_persian_text("۰"), 
                                         font_obj=self.font_manager.get_font('medium')).pack(
                                         side=tk.LEFT, padx=5, pady=15)
        
        # Classification table
        class_frame = tk.Frame(frame, bg=FRAME_BG_COLOR)
        class_frame.pack(pady=2)
        
        tk.Label(class_frame, text=format_persian_text("تعداد"), 
                font=self.font_manager.get_font('small'), 
                bg=FRAME_BG_COLOR).grid(row=0, column=1)
        tk.Label(class_frame, text=format_persian_text("درصد"), 
                font=self.font_manager.get_font('small'), 
                bg=FRAME_BG_COLOR).grid(row=0, column=2)
        
        for i, grain_type in enumerate(GRAIN_TYPES):
            tk.Label(class_frame, text=format_persian_text(grain_type), 
                    font=self.font_manager.get_font('medium'), 
                    bg=FRAME_BG_COLOR).grid(row=i+1, column=0, sticky="w")
            UIComponents.create_readonly_entry(class_frame, 10, format_persian_text("۰"), 
                                             font_obj=self.font_manager.get_font('medium'), 
                                             ipady=5).grid(row=i+1, column=1, pady=3)
            UIComponents.create_readonly_entry(class_frame, 10, format_persian_text("۰"), 
                                             font_obj=self.font_manager.get_font('medium'), 
                                             ipady=5).grid(row=i+1, column=2, pady=3)
        
        # Fracture properties
        tk.Label(frame, text=format_persian_text(TEXTS['fracture_props']), 
                font=self.font_manager.get_font('medium'), 
                bg=FRAME_BG_COLOR).pack(pady=30)
        
        broken_frame = tk.Frame(frame, bg=FRAME_BG_COLOR)
        broken_frame.pack()
        
        for i, broken_type in enumerate(BROKEN_TYPES):
            tk.Label(broken_frame, text=format_persian_text(broken_type), 
                    font=self.font_manager.get_font('medium'), 
                    bg=FRAME_BG_COLOR).grid(row=i, column=0, sticky="w")
            UIComponents.create_readonly_entry(broken_frame, 10, format_persian_text("۰"), 
                                             font_obj=self.font_manager.get_font('medium'), 
                                             ipady=5).grid(row=i, column=1, pady=3)
            UIComponents.create_readonly_entry(broken_frame, 10, format_persian_text("۰"), 
                                             font_obj=self.font_manager.get_font('medium'), 
                                             ipady=5).grid(row=i, column=2, pady=3)
    
    def _create_other_features(self) -> None:
        """Create other visual features section."""
        frame = self.frames['center_right_up']
        
        tk.Label(frame, text=format_persian_text(TEXTS['other_visual_props']), 
                font=self.font_manager.get_font('large'), 
                bg=FRAME_BG_COLOR).pack(pady=5)
        
        other_frame = tk.Frame(frame, bg=FRAME_BG_COLOR)
        other_frame.pack(pady=40)
        
        for i, feature in enumerate(OTHER_FEATURES):
            tk.Label(other_frame, text=format_persian_text(feature), 
                    font=self.font_manager.get_font('medium'), 
                    bg=FRAME_BG_COLOR).grid(row=i, column=0, sticky="w")
            UIComponents.create_readonly_entry(other_frame, 8, format_persian_text("۰"), 
                                             font_obj=self.font_manager.get_font('medium'), 
                                             ipady=5).grid(row=i, column=1, pady=3)
            UIComponents.create_readonly_entry(other_frame, 8, format_persian_text("۰"), 
                                             font_obj=self.font_manager.get_font('medium'), 
                                             ipady=5).grid(row=i, column=2, pady=3)
    
    def _create_grading_section(self) -> None:
        """Create grading section."""
        frame = self.frames['center_right_down']
        
        deg_frame = tk.Frame(frame, bg=FRAME_BG_COLOR)
        deg_frame.pack(pady=10)
        
        # Title
        tk.Label(deg_frame, text=format_persian_text(TEXTS['grain_grading']),
                font=self.font_manager.get_font('large'), 
                bg=FRAME_BG_COLOR).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Rice type selection
        tk.Label(deg_frame, text=format_persian_text("نوع برنج را انتخاب کنید"),
                font=self.font_manager.get_font('medium'), 
                bg=FRAME_BG_COLOR, anchor="e").grid(row=1, column=1, sticky="e", pady=5, padx=5)
        
        ttk.Combobox(deg_frame, values=["Type 1", "Type 2", "Type 3"], 
                    width=30).grid(row=1, column=0, sticky="w", pady=5)
        
        # Checkbox
        tk.Checkbutton(deg_frame, text=format_persian_text("عدم احتساب دانه های شکم گچی"),
                      font=self.font_manager.get_font('small'), 
                      bg=FRAME_BG_COLOR, anchor="w").grid(row=2, column=0, columnspan=2, 
                                                         sticky="w", pady=20, padx=100)
        
        # Grading button with status
        btn_frame = tk.Frame(deg_frame, bg=FRAME_BG_COLOR)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text=format_persian_text("درجه بندی دانه ها"),
                 width=25, font=self.font_manager.get_font('small'), 
                 anchor="center").pack(side="left", padx=(0, 10))
        StatusIndicator(btn_frame, color="red").pack(side="left")
        
        # Degree output
        degree_frame = tk.Frame(deg_frame, bg=FRAME_BG_COLOR)
        degree_frame.grid(row=4, column=0, columnspan=2, sticky="e", pady=20)
        degree_frame.columnconfigure(0, weight=1)
        degree_frame.columnconfigure(1, minsize=100)
        
        tk.Label(degree_frame, text=format_persian_text("درجه:"),
                font=self.font_manager.get_font('medium'), 
                bg=FRAME_BG_COLOR, anchor="e").grid(row=0, column=1, sticky="e", padx=(10, 180))
        UIComponents.create_readonly_entry(degree_frame, 8, "0").grid(row=0, column=0, sticky="w")
    
    def _populate_right_panel(self) -> None:
        """Populate the right panel with single grain analysis."""
        self._create_single_grain_analysis()
    
    def _create_single_grain_analysis(self) -> None:
        """Create single grain analysis section."""
        frame = self.frames['right']
        
        tk.Label(frame, text=format_persian_text(TEXTS['single_grain_analysis']),
                font=self.font_manager.get_font('large'), 
                bg=FRAME_BG_COLOR).pack(pady=5)
        
        # Sound controls
        sound_frame = tk.Frame(frame, bg=FRAME_BG_COLOR)
        sound_frame.pack(pady=2)
        tk.Label(sound_frame, text="Sound:", font=("Arial", 10), 
                bg=FRAME_BG_COLOR).pack(side=tk.LEFT)
        tk.Radiobutton(sound_frame, text="On", value=1, 
                      bg=FRAME_BG_COLOR).pack(side=tk.LEFT)
        tk.Radiobutton(sound_frame, text="Off", value=0, 
                      bg=FRAME_BG_COLOR).pack(side=tk.LEFT)
        
        # Control buttons
        tk.Button(frame, text=format_persian_text("نمایش دانه های شماره گذاری شده"), 
                 width=30, font=self.font_manager.get_font('small')).pack(pady=2)
        
        tk.Label(frame, text=format_persian_text("شماره دانه را وارد کنید:"), 
                font=self.font_manager.get_font('small'), 
                bg=FRAME_BG_COLOR).pack()
        UIComponents.create_readonly_entry(frame, 8, "0").pack(pady=2)
        
        tk.Button(frame, text=format_persian_text("آنالیز دانه ی انتخاب شده"), 
                 width=22, font=self.font_manager.get_font('small')).pack(pady=2)
        StatusIndicator(frame, color="red").pack(pady=2)
        
        # Spacer
        tk.Label(frame, text="", font=self.font_manager.get_font('medium'), 
                bg=FRAME_BG_COLOR).pack()
        
        tk.Label(frame, text=format_persian_text("ویژگی های دانه ی انتخاب شده"),
                font=self.font_manager.get_font('medium'), 
                bg=FRAME_BG_COLOR).pack()
        
        # Single grain features
        features_frame = tk.Frame(frame, bg=FRAME_BG_COLOR)
        features_frame.pack(pady=50)
        
        for i, feature in enumerate(SINGLE_GRAIN_FEATURES):
            tk.Label(features_frame, text=format_persian_text(feature), 
                    font=self.font_manager.get_font('medium'), 
                    bg=FRAME_BG_COLOR).grid(row=i, column=0, sticky="w")
            UIComponents.create_readonly_entry(features_frame, 8, format_persian_text("۰"), 
                                             font_obj=self.font_manager.get_font('medium')).grid(
                                             row=i, column=1, pady=4)
        
        # Footer
        tk.Button(frame, text=format_persian_text("دریافت"), width=18, 
                 font=self.font_manager.get_font('small')).pack(side=tk.BOTTOM)
        tk.Label(frame, text=format_persian_text("استاندارد شماره 127 و اصلاحیه شماره 1 سال 1400"),
                font=self.font_manager.get_font('small'), 
                bg=FRAME_BG_COLOR, fg="blue").pack(side=tk.BOTTOM)
    
    def run(self) -> None:
        """Start the application."""
        self.root.mainloop()


def main() -> None:
    """Main entry point of the application."""
    app = RiceGrainAnalyzer()
    app.run()


if __name__ == "__main__":
    main()