import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, font
import tkinter.scrolledtext as scrolledtext

class TextEditor:
    def __init__(self, parent, title="ویرایشگر متن"):
        self.parent = parent
        self.title = title
        self.text_widget = None
        self.current_font = ('Tahoma', 10)
        self.current_fg_color = '#000000'
        self.current_bg_color = '#ffffff'
        
    def show_editor(self, initial_text="", on_save_callback=None):
        """ویرایشگر متن رو نشون می‌دم"""
        editor_window = tk.Toplevel(self.parent)
        editor_window.title(self.title)
        editor_window.geometry("800x600")
        editor_window.configure(bg='#f0f0f0')
        editor_window.transient(self.parent)
        
        editor_window.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        main_frame = tk.Frame(editor_window, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        toolbar_frame = tk.Frame(main_frame, bg='#ecf0f1', relief=tk.RAISED, bd=1)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.create_toolbar(toolbar_frame)
        
        editor_frame = tk.Frame(main_frame, bg='white', relief=tk.SUNKEN, bd=2)
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_widget = scrolledtext.ScrolledText(
            editor_frame,
            font=self.current_font,
            fg=self.current_fg_color,
            bg=self.current_bg_color,
            wrap=tk.WORD,
            undo=True,
            maxundo=0
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        if initial_text:
            self.text_widget.insert("1.0", initial_text)
        
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        save_btn = tk.Button(
            button_frame,
            text="ذخیره",
            command=lambda: self.save_text(on_save_callback, editor_window),
            font=('Tahoma', 10, 'bold'),
            bg='#2ecc71',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=15,
            cursor='hand2'
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(
            button_frame,
            text="لغو",
            command=editor_window.destroy,
            font=('Tahoma', 10),
            bg='#95a5a6',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=15,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.LEFT)
        
        editor_window.bind('<Control-s>', lambda e: self.save_text(on_save_callback, editor_window))
        editor_window.bind('<Control-z>', lambda e: self.text_widget.edit_undo())
        editor_window.bind('<Control-y>', lambda e: self.text_widget.edit_redo())
        editor_window.bind('<Escape>', lambda e: editor_window.destroy())
        
        self.text_widget.focus_set()
        
        return editor_window
    
    def create_toolbar(self, parent):
        """ایجاد نوار ابزار"""
        cut_btn = tk.Button(
            parent,
            text="برش",
            command=self.cut_text,
            font=('Tahoma', 9),
            bg='#e74c3c',
            fg='white',
            relief=tk.FLAT,
            bd=1,
            width=8,
            cursor='hand2'
        )
        cut_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        copy_btn = tk.Button(
            parent,
            text="کپی",
            command=self.copy_text,
            font=('Tahoma', 9),
            bg='#3498db',
            fg='white',
            relief=tk.FLAT,
            bd=1,
            width=8,
            cursor='hand2'
        )
        copy_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        paste_btn = tk.Button(
            parent,
            text="چسباندن",
            command=self.paste_text,
            font=('Tahoma', 9),
            bg='#2ecc71',
            fg='white',
            relief=tk.FLAT,
            bd=1,
            width=8,
            cursor='hand2'
        )
        paste_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        separator1 = tk.Frame(parent, width=2, bg='#bdc3c7')
        separator1.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
        fg_color_btn = tk.Button(
            parent,
            text="رنگ متن",
            command=self.change_fg_color,
            font=('Tahoma', 9),
            bg='#9b59b6',
            fg='white',
            relief=tk.FLAT,
            bd=1,
            width=10,
            cursor='hand2'
        )
        fg_color_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        bg_color_btn = tk.Button(
            parent,
            text="رنگ پس‌زمینه",
            command=self.change_bg_color,
            font=('Tahoma', 9),
            bg='#f39c12',
            fg='white',
            relief=tk.FLAT,
            bd=1,
            width=12,
            cursor='hand2'
        )
        bg_color_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        separator2 = tk.Frame(parent, width=2, bg='#bdc3c7')
        separator2.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
        tk.Label(parent, text="فونت:", font=('Tahoma', 9), bg='#ecf0f1').pack(side=tk.LEFT, padx=(5, 2))
        
        font_combo = ttk.Combobox(
            parent,
            font=('Tahoma', 9),
            width=15,
            state='readonly'
        )
        font_combo['values'] = ['Tahoma', 'Arial', 'Times New Roman', 'Courier New', 'Verdana']
        font_combo.set('Tahoma')
        font_combo.pack(side=tk.LEFT, padx=2, pady=2)
        font_combo.bind('<<ComboboxSelected>>', self.change_font)
        
        tk.Label(parent, text="اندازه:", font=('Tahoma', 9), bg='#ecf0f1').pack(side=tk.LEFT, padx=(5, 2))
        
        size_combo = ttk.Combobox(
            parent,
            font=('Tahoma', 9),
            width=8,
            state='readonly'
        )
        size_combo['values'] = [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32]
        size_combo.set(10)
        size_combo.pack(side=tk.LEFT, padx=2, pady=2)
        size_combo.bind('<<ComboboxSelected>>', self.change_font_size)
        
        separator3 = tk.Frame(parent, width=2, bg='#bdc3c7')
        separator3.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
        undo_btn = tk.Button(
            parent,
            text="بازگشت",
            command=self.undo_text,
            font=('Tahoma', 9),
            bg='#34495e',
            fg='white',
            relief=tk.FLAT,
            bd=1,
            width=8,
            cursor='hand2'
        )
        undo_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        redo_btn = tk.Button(
            parent,
            text="تکرار",
            command=self.redo_text,
            font=('Tahoma', 9),
            bg='#34495e',
            fg='white',
            relief=tk.FLAT,
            bd=1,
            width=8,
            cursor='hand2'
        )
        redo_btn.pack(side=tk.LEFT, padx=2, pady=2)
    
    def cut_text(self):
        """متن انتخاب شده رو برش می‌دم"""
        try:
            self.text_widget.event_generate("<<Cut>>")
        except:
            pass
    
    def copy_text(self):
        """متن انتخاب شده رو کپی می‌کنم"""
        try:
            self.text_widget.event_generate("<<Copy>>")
        except:
            pass
    
    def paste_text(self):
        """متن رو چسبوندم"""
        try:
            self.text_widget.event_generate("<<Paste>>")
        except:
            pass
    
    def change_fg_color(self):
        """رنگ متن رو عوض می‌کنم"""
        color = colorchooser.askcolor(title="انتخاب رنگ متن")
        if color[1]:
            self.current_fg_color = color[1]
            self.text_widget.config(fg=self.current_fg_color)
    
    def change_bg_color(self):
        """رنگ پس‌زمینه رو عوض می‌کنم"""
        color = colorchooser.askcolor(title="انتخاب رنگ پس‌زمینه")
        if color[1]:
            self.current_bg_color = color[1]
            self.text_widget.config(bg=self.current_bg_color)
    
    def change_font(self, event=None):
        """فونت رو عوض می‌کنم"""
        pass
    
    def change_font_size(self, event=None):
        """اندازه فونت رو عوض می‌کنم"""
        pass
    
    def undo_text(self):
        """آخرین کار رو لغو می‌کنم"""
        try:
            self.text_widget.edit_undo()
        except:
            pass
    
    def redo_text(self):
        """آخرین کار رو تکرار می‌کنم"""
        try:
            self.text_widget.edit_redo()
        except:
            pass
    
    def save_text(self, callback, window):
        """متن رو ذخیره می‌کنم"""
        text_content = self.text_widget.get("1.0", tk.END).strip()
        
        if callback:
            callback(text_content)
        
        messagebox.showinfo("موفقیت", "متن با موفقیت ذخیره شد!")
        window.destroy()
    
    def get_text(self):
        """متن فعلی رو برمی‌گردونم"""
        if self.text_widget:
            return self.text_widget.get("1.0", tk.END).strip()
        return "" 