import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta
import hashlib

class AuthManager:
    def __init__(self):
        self.users_file = "users.json"
        self.lock_file = "account_locks.json"
        self.users = self.load_users()
        self.account_locks = self.load_account_locks()
        
    def load_users(self):
        """کاربران رو از فایل می‌خونم"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_users(self):
        """کاربران رو در فایل ذخیره می‌کنم"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
    
    def load_account_locks(self):
        """اطلاعات قفل حساب‌ها رو از فایل می‌خونم"""
        if os.path.exists(self.lock_file):
            try:
                with open(self.lock_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_account_locks(self):
        """اطلاعات قفل حساب‌ها رو در فایل ذخیره می‌کنم"""
        with open(self.lock_file, 'w', encoding='utf-8') as f:
            json.dump(self.account_locks, f, ensure_ascii=False, indent=2)
    
    def hash_password(self, password):
        """رمز عبور رو هش می‌کنم"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def is_account_locked(self, username):
        """چک می‌کنم که حساب قفل شده باشه یا نه"""
        if username not in self.account_locks:
            return False, None
        
        lock_info = self.account_locks[username]
        
        if lock_info.get('lock_time') is None:
            return False, None
            
        lock_time = datetime.fromisoformat(lock_info['lock_time'])
        unlock_time = lock_time + timedelta(minutes=5)
        
        if datetime.now() < unlock_time:
            remaining = unlock_time - datetime.now()
            minutes = int(remaining.total_seconds() // 60)
            seconds = int(remaining.total_seconds() % 60)
            return True, f"{minutes:02d}:{seconds:02d}"
        
        del self.account_locks[username]
        self.save_account_locks()
        return False, None
    
    def record_failed_login(self, username):
        """تلاش ناموفق ورود رو ثبت می‌کنم"""
        if username not in self.account_locks:
            self.account_locks[username] = {
                'failed_attempts': 1,
                'lock_time': None
            }
        else:
            self.account_locks[username]['failed_attempts'] += 1
        
        if self.account_locks[username]['failed_attempts'] >= 3:
            self.account_locks[username]['lock_time'] = datetime.now().isoformat()
            self.save_account_locks()
    
    def reset_failed_attempts(self, username):
        """تلاش‌های ناموفق رو پاک می‌کنم"""
        if username in self.account_locks:
            del self.account_locks[username]
            self.save_account_locks()
    
    def show_login_form(self, parent, on_success_callback):
        """فرم ورود رو نشون می‌دم"""
        main_frame = tk.Frame(parent, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = tk.Label(
            main_frame,
            text="ورود به سیستم",
            font=('Tahoma', 16, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 30))
        
        form_frame = tk.Frame(main_frame, bg='#f0f0f0')
        form_frame.pack(expand=True)
        
        tk.Label(
            form_frame,
            text="نام کاربری:",
            font=('Tahoma', 10),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(anchor=tk.W, pady=(0, 5))
        
        username_entry = tk.Entry(
            form_frame,
            font=('Tahoma', 10),
            width=30,
            relief=tk.SUNKEN,
            bd=2
        )
        username_entry.pack(pady=(0, 15))
        username_entry.focus()
        
        tk.Label(
            form_frame,
            text="رمز عبور:",
            font=('Tahoma', 10),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(anchor=tk.W, pady=(0, 5))
        
        password_entry = tk.Entry(
            form_frame,
            font=('Tahoma', 10),
            width=30,
            show="*",
            relief=tk.SUNKEN,
            bd=2
        )
        password_entry.pack(pady=(0, 25))
        
        status_label = tk.Label(
            form_frame,
            text="",
            font=('Tahoma', 9),
            bg='#f0f0f0',
            fg='#e74c3c'
        )
        status_label.pack(pady=(0, 15))
        
        def login():
            username = username_entry.get().strip()
            password = password_entry.get()
            
            if not username or not password:
                status_label.config(text="لطفاً تمام فیلدها را پر کنید")
                return
            
            is_locked, remaining_time = self.is_account_locked(username)
            if is_locked:
                status_label.config(text=f"حساب قفل شده است. زمان باقی‌مانده: {remaining_time}")
                return
            
            if username in self.users:
                if self.users[username]['password'] == self.hash_password(password):
                    self.reset_failed_attempts(username)
                    status_label.config(text="ورود موفق!", fg='#27ae60')
                    parent.after(1000, lambda: [parent.destroy(), on_success_callback(username)])
                else:
                    self.record_failed_login(username)
                    remaining_attempts = 3 - self.account_locks[username]['failed_attempts']
                    if remaining_attempts > 0:
                        status_label.config(text=f"رمز عبور اشتباه. {remaining_attempts} تلاش باقی‌مانده")
                    else:
                        status_label.config(text="حساب شما به مدت 5 دقیقه قفل شد")
            else:
                status_label.config(text="کاربری با این نام یافت نشد")
        
        login_btn = tk.Button(
            form_frame,
            text="ورود",
            command=login,
            font=('Tahoma', 10, 'bold'),
            bg='#3498db',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=15,
            cursor='hand2'
        )
        login_btn.pack(pady=(0, 10))
        
        cancel_btn = tk.Button(
            form_frame,
            text="لغو",
            command=parent.destroy,
            font=('Tahoma', 10),
            bg='#95a5a6',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=15,
            cursor='hand2'
        )
        cancel_btn.pack()
        
        parent.bind('<Return>', lambda e: login())
        parent.bind('<Escape>', lambda e: parent.destroy())
    
    def show_register_form(self, parent):
        """فرم ثبت‌نام رو نشون می‌دم"""
        main_frame = tk.Frame(parent, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = tk.Label(
            main_frame,
            text="ثبت‌نام کاربر جدید",
            font=('Tahoma', 16, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 30))
        
        form_frame = tk.Frame(main_frame, bg='#f0f0f0')
        form_frame.pack(expand=True)
        
        tk.Label(
            form_frame,
            text="نام کاربری:",
            font=('Tahoma', 10),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(anchor=tk.W, pady=(0, 5))
        
        username_entry = tk.Entry(
            form_frame,
            font=('Tahoma', 10),
            width=30,
            relief=tk.SUNKEN,
            bd=2
        )
        username_entry.pack(pady=(0, 15))
        
        tk.Label(
            form_frame,
            text="رمز عبور:",
            font=('Tahoma', 10),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(anchor=tk.W, pady=(0, 5))
        
        password_entry = tk.Entry(
            form_frame,
            font=('Tahoma', 10),
            width=30,
            show="*",
            relief=tk.SUNKEN,
            bd=2
        )
        password_entry.pack(pady=(0, 15))
        
        tk.Label(
            form_frame,
            text="تکرار رمز عبور:",
            font=('Tahoma', 10),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(anchor=tk.W, pady=(0, 5))
        
        confirm_password_entry = tk.Entry(
            form_frame,
            font=('Tahoma', 10),
            width=30,
            show="*",
            relief=tk.SUNKEN,
            bd=2
        )
        confirm_password_entry.pack(pady=(0, 25))
        
        status_label = tk.Label(
            form_frame,
            text="",
            font=('Tahoma', 9),
            bg='#f0f0f0',
            fg='#e74c3c'
        )
        status_label.pack(pady=(0, 15))
        
        def register():
            username = username_entry.get().strip()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            
            if not username or not password or not confirm_password:
                status_label.config(text="لطفاً تمام فیلدها را پر کنید")
                return
            
            if len(username) < 3:
                status_label.config(text="نام کاربری باید حداقل 3 کاراکتر باشد")
                return
            
            if len(password) < 6:
                status_label.config(text="رمز عبور باید حداقل 6 کاراکتر باشد")
                return
            
            if password != confirm_password:
                status_label.config(text="رمز عبور و تکرار آن یکسان نیستند")
                return
            
            if username in self.users:
                status_label.config(text="این نام کاربری قبلاً ثبت شده است")
                return
            
            self.users[username] = {
                'password': self.hash_password(password),
                'created_at': datetime.now().isoformat()
            }
            self.save_users()
            
            status_label.config(text="ثبت‌نام با موفقیت انجام شد!", fg='#27ae60')
            parent.after(2000, parent.destroy)
        
        register_btn = tk.Button(
            form_frame,
            text="ثبت‌نام",
            command=register,
            font=('Tahoma', 10, 'bold'),
            bg='#2ecc71',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=15,
            cursor='hand2'
        )
        register_btn.pack(pady=(0, 10))
        
        cancel_btn = tk.Button(
            form_frame,
            text="لغو",
            command=parent.destroy,
            font=('Tahoma', 10),
            bg='#95a5a6',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=15,
            cursor='hand2'
        )
        cancel_btn.pack()
        
        parent.bind('<Return>', lambda e: register())
        parent.bind('<Escape>', lambda e: parent.destroy()) 