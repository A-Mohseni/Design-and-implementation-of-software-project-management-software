import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta
from auth_manager import AuthManager
from project_manager import ProjectManager
from reports_manager import ReportsManager
from text_editor import TextEditor

class ProjectManagementApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("نرمافزار مدیریت پروژههای نرمافزاری")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        self.setup_fonts()
        
        self.auth_manager = AuthManager()
        self.project_manager = ProjectManager()
        self.reports_manager = ReportsManager()
        
        self.current_user = None
        self.is_logged_in = False
        
        self.setup_ui()
        
    def setup_fonts(self):
        """فونت‌ها رو تنظیم می‌کنم"""
        try:
            self.title_font = ('Tahoma', 16, 'bold')
            self.header_font = ('Tahoma', 12, 'bold')
            self.normal_font = ('Tahoma', 10)
            self.small_font = ('Tahoma', 9)
        except:
            self.title_font = ('Arial', 16, 'bold')
            self.header_font = ('Arial', 12, 'bold')
            self.normal_font = ('Arial', 10)
            self.small_font = ('Arial', 9)
    
    def setup_ui(self):
        """رابط کاربری رو می‌سازم"""
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = tk.Label(
            main_frame,
            text="نرمافزار مدیریت پروژههای نرمافزاری",
            font=self.title_font,
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 30))
        
        menu_frame = tk.Frame(main_frame, bg='#f0f0f0')
        menu_frame.pack(expand=True)
        
        self.create_menu_buttons(menu_frame)
        
        self.status_frame = tk.Frame(main_frame, bg='#ecf0f1', relief=tk.RAISED, bd=1)
        self.status_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.status_label = tk.Label(
            self.status_frame,
            text="وضعیت: خارج از سیستم",
            font=self.small_font,
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.update_status()
    
    def create_menu_buttons(self, parent):
        """دکمه‌های منو رو می‌سازم"""
        buttons_data = [
            ("ورود به سیستم", self.show_login, '#3498db'),
            ("ثبت‌نام", self.show_register, '#2ecc71'),
            ("مدیریت پروژه", self.show_project_management, '#e74c3c'),
            ("گزارش‌گیری", self.show_reports, '#f39c12'),
            ("خروج", self.quit_app, '#95a5a6')
        ]
        
        for text, command, color in buttons_data:
            btn = tk.Button(
                parent,
                text=text,
                command=command,
                font=self.header_font,
                bg=color,
                fg='white',
                relief=tk.RAISED,
                bd=2,
                width=20,
                height=2,
                cursor='hand2'
            )
            btn.pack(pady=10)
            
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg=self.lighten_color(color)))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.configure(bg=c))
    
    def lighten_color(self, color):
        """رنگ رو روشن‌تر می‌کنم تا افکت hover داشته باشه"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        light_rgb = tuple(min(255, int(c * 1.2)) for c in rgb)
        return f'#{light_rgb[0]:02x}{light_rgb[1]:02x}{light_rgb[2]:02x}'
    
    def show_login(self):
        """پنجره ورود رو نشون می‌دم"""
        if self.is_logged_in:
            messagebox.showinfo("اطلاع", "شما قبلاً وارد شده‌اید!")
            return
        
        login_window = tk.Toplevel(self.root)
        login_window.title("ورود به سیستم")
        login_window.geometry("400x300")
        login_window.configure(bg='#f0f0f0')
        login_window.transient(self.root)
        login_window.grab_set()
        
        login_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50
        ))
        
        self.auth_manager.show_login_form(login_window, self.on_login_success)
    
    def show_register(self):
        """پنجره ثبت‌نام رو نشون می‌دم"""
        register_window = tk.Toplevel(self.root)
        register_window.title("ثبت‌نام")
        register_window.geometry("450x400")
        register_window.configure(bg='#f0f0f0')
        register_window.transient(self.root)
        register_window.grab_set()
        
        register_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50
        ))
        
        self.auth_manager.show_register_form(register_window)
    
    def show_project_management(self):
        """پنجره مدیریت پروژه رو نشون می‌دم"""
        if not self.is_logged_in:
            messagebox.showwarning("هشدار", "لطفاً ابتدا وارد سیستم شوید!")
            return
        
        project_window = tk.Toplevel(self.root)
        project_window.title("مدیریت پروژه")
        project_window.geometry("1000x700")
        project_window.configure(bg='#f0f0f0')
        project_window.transient(self.root)
        
        project_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50
        ))
        
        self.project_manager.show_project_management(project_window, self.current_user)
    
    def show_reports(self):
        """پنجره گزارش‌گیری رو نشون می‌دم"""
        if not self.is_logged_in:
            messagebox.showwarning("هشدار", "لطفاً ابتدا وارد سیستم شوید!")
            return
        
        reports_window = tk.Toplevel(self.root)
        reports_window.title("گزارش‌گیری")
        reports_window.geometry("900x600")
        reports_window.configure(bg='#f0f0f0')
        reports_window.transient(self.root)
        
        reports_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50
        ))
        
        self.reports_manager.show_reports_window(reports_window)
    
    def on_login_success(self, username):
        """وقتی کاربر با موفقیت وارد شد"""
        self.current_user = username
        self.is_logged_in = True
        self.update_status()
        messagebox.showinfo("موفقیت", f"خوش آمدید {username}!")
    
    def update_status(self):
        """وضعیت کاربر رو آپدیت می‌کنم"""
        if self.is_logged_in:
            self.status_label.config(
                text=f"وضعیت: وارد شده به عنوان {self.current_user}",
                fg='#27ae60'
            )
        else:
            self.status_label.config(
                text="وضعیت: خارج از سیستم",
                fg='#7f8c8d'
            )
    
    def quit_app(self):
        """از برنامه خارج می‌شم"""
        if messagebox.askyesno("تأیید", "آیا مطمئن هستید که می‌خواهید خارج شوید؟"):
            self.root.quit()
    
    def run(self):
        """برنامه رو اجرا می‌کنم"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ProjectManagementApp()
    app.run() 