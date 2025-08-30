import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, timedelta
import calendar

class ReportsManager:
    def __init__(self):
        self.projects_file = "projects.json"
        
    def load_projects(self):
        """پروژه‌ها رو از فایل می‌خونم"""
        if os.path.exists(self.projects_file):
            try:
                with open(self.projects_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def show_reports_window(self, parent):
        """پنجره گزارش‌گیری رو نشون می‌دم"""
        main_frame = tk.Frame(parent, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_label = tk.Label(
            main_frame,
            text="گزارش‌گیری",
            font=('Tahoma', 16, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        reports_data = [
            ("گزارش بر اساس نام پروژه", self.report_by_project_name, '#3498db'),
            ("گزارش بر اساس نام شرکت/کارفرما", self.report_by_client, '#2ecc71'),
            ("گزارش بر اساس تاریخ شروع", self.report_by_start_date, '#f39c12'),
            ("گزارش بر اساس تاریخ پایان", self.report_by_end_date, '#e74c3c'),
            ("گزارش پروژه‌های یک ماه خاص", self.report_by_month, '#9b59b6'),
            ("گزارش مالی هفتگی", self.financial_report_weekly, '#1abc9c'),
            ("گزارش مالی ماهانه", self.financial_report_monthly, '#34495e'),
            ("گزارش مالی سالانه", self.financial_report_yearly, '#e67e22')
        ]
        
        for i, (text, command, color) in enumerate(reports_data):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(
                button_frame,
                text=text,
                command=lambda cmd=command: cmd(parent),
                font=('Tahoma', 10, 'bold'),
                bg=color,
                fg='white',
                relief=tk.RAISED,
                bd=2,
                width=25,
                height=2,
                cursor='hand2'
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
        
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        results_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=2)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        results_title = tk.Label(
            results_frame,
            text="نتایج گزارش",
            font=('Tahoma', 12, 'bold'),
            bg='#34495e',
            fg='white'
        )
        results_title.pack(fill=tk.X, pady=10)
        
        content_frame = tk.Frame(results_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('name', 'client', 'start_date', 'end_date', 'income', 'cost', 'profit', 'status')
        self.results_tree = ttk.Treeview(content_frame, columns=columns, show='headings', height=15)
        
        column_names = {
            'name': 'نام پروژه',
            'client': 'کارفرما',
            'start_date': 'تاریخ شروع',
            'end_date': 'تاریخ پایان',
            'income': 'درآمد',
            'cost': 'هزینه',
            'profit': 'سود خالص',
            'status': 'وضعیت'
        }
        
        widths = [150, 120, 100, 100, 80, 80, 80, 80]
        
        for col, name in column_names.items():
            self.results_tree.heading(col, text=name)
            self.results_tree.column(col, width=widths[list(column_names.keys()).index(col)], anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.count_label = tk.Label(
            results_frame,
            text="تعداد نتایج: 0",
            font=('Tahoma', 10),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        self.count_label.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
    
    def clear_results(self):
        """پاک کردن نتایج قبلی"""
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.update_count_label()
    
    def add_project_to_results(self, project):
        """اضافه کردن پروژه به نتایج"""
        income = float(project.get('income', 0))
        cost = float(project.get('cost', 0))
        profit = income - cost
        
        end_date = datetime.strptime(project.get('end_date', ''), '%Y-%m-%d')
        today = datetime.now()
        if end_date < today:
            status = "پایان یافته"
        elif end_date == today:
            status = "امروز"
        else:
            status = "در حال اجرا"
        
        self.results_tree.insert('', tk.END, values=(
            project.get('name', ''),
            project.get('client', ''),
            project.get('start_date', ''),
            project.get('end_date', ''),
            f"{income:,}",
            f"{cost:,}",
            f"{profit:,}",
            status
        ))
    
    def update_count_label(self):
        """به‌روزرسانی برچسب تعداد نتایج"""
        count = len(self.results_tree.get_children())
        self.count_label.config(text=f"تعداد نتایج: {count}")
    
    def report_by_project_name(self, parent):
        """گزارش بر اساس نام پروژه"""
        search_window = tk.Toplevel(parent)
        search_window.title("جستجو بر اساس نام پروژه")
        search_window.geometry("400x200")
        search_window.configure(bg='#f0f0f0')
        search_window.transient(parent)
        search_window.grab_set()
        
        main_frame = tk.Frame(search_window, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            main_frame,
            text="نام پروژه (یا بخشی از آن):",
            font=('Tahoma', 10),
            bg='#f0f0f0'
        ).pack(anchor=tk.W, pady=(0, 10))
        
        search_entry = tk.Entry(main_frame, font=('Tahoma', 10), width=40)
        search_entry.pack(fill=tk.X, pady=(0, 20))
        search_entry.focus()
        
        def search():
            search_term = search_entry.get().strip().lower()
            if not search_term:
                messagebox.showwarning("هشدار", "لطفاً نام پروژه را وارد کنید")
                return
            
            self.clear_results()
            found_projects = []
            projects = self.load_projects()
            
            for project in projects:
                if search_term in project.get('name', '').lower():
                    found_projects.append(project)
                    self.add_project_to_results(project)
            
            self.update_count_label()
            search_window.destroy()
            
            if not found_projects:
                messagebox.showinfo("اطلاع", "پروژه‌ای با این نام یافت نشد")
        
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X)
        
        search_btn = tk.Button(
            button_frame,
            text="جستجو",
            command=search,
            font=('Tahoma', 10, 'bold'),
            bg='#3498db',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=15,
            cursor='hand2'
        )
        search_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(
            button_frame,
            text="لغو",
            command=search_window.destroy,
            font=('Tahoma', 10),
            bg='#95a5a6',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=15,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.LEFT)
        
        search_window.bind('<Return>', lambda e: search())
        search_window.bind('<Escape>', lambda e: search_window.destroy())
    
    def report_by_client(self, parent):
        """گزارش بر اساس نام شرکت/کارفرما"""
        projects = self.load_projects()
        clients = list(set(project.get('client', '') for project in projects if project.get('client')))
        
        if not clients:
            messagebox.showinfo("اطلاع", "هیچ شرکت/کارفرمایی یافت نشد")
            return
        
        client_window = tk.Toplevel(parent)
        client_window.title("انتخاب شرکت/کارفرما")
        client_window.geometry("400x300")
        client_window.configure(bg='#f0f0f0')
        client_window.transient(parent)
        client_window.grab_set()
        
        main_frame = tk.Frame(client_window, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            main_frame,
            text="شرکت/کارفرما را انتخاب کنید:",
            font=('Tahoma', 10),
            bg='#f0f0f0'
        ).pack(anchor=tk.W, pady=(0, 10))
        
        client_listbox = tk.Listbox(main_frame, font=('Tahoma', 10), height=10)
        client_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        for client in sorted(clients):
            client_listbox.insert(tk.END, client)
        
        def select_client():
            selection = client_listbox.curselection()
            if not selection:
                messagebox.showwarning("هشدار", "لطفاً یک شرکت را انتخاب کنید")
                return
            
            selected_client = client_listbox.get(selection[0])
            
            self.clear_results()
            found_projects = []
            
            for project in projects:
                if project.get('client', '') == selected_client:
                    found_projects.append(project)
                    self.add_project_to_results(project)
            
            self.update_count_label()
            client_window.destroy()
            
            if not found_projects:
                messagebox.showinfo("اطلاع", f"پروژه‌ای برای شرکت '{selected_client}' یافت نشد")
        
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X)
        
        select_btn = tk.Button(
            button_frame,
            text="انتخاب",
            command=select_client,
            font=('Tahoma', 10, 'bold'),
            bg='#2ecc71',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=15,
            cursor='hand2'
        )
        select_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(
            button_frame,
            text="لغو",
            command=client_window.destroy,
            font=('Tahoma', 10),
            bg='#95a5a6',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=15,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.LEFT)
        
        client_window.bind('<Double-1>', lambda e: select_client())
        client_window.bind('<Escape>', lambda e: client_window.destroy())
    
    def report_by_start_date(self, parent):
        """گزارش بر اساس تاریخ شروع"""
        date_window = tk.Toplevel(parent)
        date_window.title("جستجو بر اساس تاریخ شروع")
        date_window.geometry("400x200")
        date_window.configure(bg='#f0f0f0')
        date_window.transient(parent)
        date_window.grab_set()
        
        main_frame = tk.Frame(date_window, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            main_frame,
            text="تاریخ شروع (YYYY-MM-DD):",
            font=('Tahoma', 10),
            bg='#f0f0f0'
        ).pack(anchor=tk.W, pady=(0, 10))
        
        date_entry = tk.Entry(main_frame, font=('Tahoma', 10), width=20)
        date_entry.pack(fill=tk.X, pady=(0, 20))
        date_entry.focus()
        
        def search():
            date_str = date_entry.get().strip()
            if not date_str:
                messagebox.showwarning("هشدار", "لطفاً تاریخ را وارد کنید")
                return
            
            try:
                search_date = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("خطا", "فرمت تاریخ صحیح نیست. از فرمت YYYY-MM-DD استفاده کنید")
                return
            
            self.clear_results()
            found_projects = []
            
            for project in projects:
                try:
                    project_date = datetime.strptime(project.get('start_date', ''), '%Y-%m-%d')
                    if project_date == search_date:
                        found_projects.append(project)
                        self.add_project_to_results(project)
                except:
                    continue
            
            self.update_count_label()
            date_window.destroy()
            
            if not found_projects:
                messagebox.showinfo("اطلاع", f"پروژه‌ای با تاریخ شروع {date_str} یافت نشد")
        
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X)
        
        search_btn = tk.Button(
            button_frame,
            text="جستجو",
            command=search,
            font=('Tahoma', 10, 'bold'),
            bg='#f39c12',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=15,
            cursor='hand2'
        )
        search_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(
            button_frame,
            text="لغو",
            command=date_window.destroy,
            font=('Tahoma', 10),
            bg='#95a5a6',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=15,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.LEFT)
        
        date_window.bind('<Return>', lambda e: search())
        date_window.bind('<Escape>', lambda e: date_window.destroy())
    
    def report_by_end_date(self, parent):
        """گزارش بر اساس تاریخ پایان"""
        date_window = tk.Toplevel(parent)
        date_window.title("جستجو بر اساس تاریخ پایان")
        date_window.geometry("400x200")
        date_window.configure(bg='#f0f0f0')
        date_window.transient(parent)
        date_window.grab_set()
        
        main_frame = tk.Frame(date_window, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            main_frame,
            text="تاریخ پایان (YYYY-MM-DD):",
            font=('Tahoma', 10),
            bg='#f0f0f0'
        ).pack(anchor=tk.W, pady=(0, 10))
        
        date_entry = tk.Entry(main_frame, font=('Tahoma', 10), width=20)
        date_entry.pack(fill=tk.X, pady=(0, 20))
        date_entry.focus()
        
        def search():
            date_str = date_entry.get().strip()
            if not date_str:
                messagebox.showwarning("هشدار", "لطفاً تاریخ را وارد کنید")
                return
            
            try:
                search_date = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("خطا", "فرمت تاریخ صحیح نیست. از فرمت YYYY-MM-DD استفاده کنید")
                return
            
            self.clear_results()
            found_projects = []
            
            for project in projects:
                try:
                    project_date = datetime.strptime(project.get('end_date', ''), '%Y-%m-%d')
                    if project_date == search_date:
                        found_projects.append(project)
                        self.add_project_to_results(project)
                except:
                    continue
            
            self.update_count_label()
            date_window.destroy()
            
            if not found_projects:
                messagebox.showinfo("اطلاع", f"پروژه‌ای با تاریخ پایان {date_str} یافت نشد")
        
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X)
        
        search_btn = tk.Button(
            button_frame,
            text="جستجو",
            command=search,
            font=('Tahoma', 10, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=15,
            cursor='hand2'
        )
        search_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(
            button_frame,
            text="لغو",
            command=date_window.destroy,
            font=('Tahoma', 10),
            bg='#95a5a6',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=15,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.LEFT)
        
        date_window.bind('<Return>', lambda e: search())
        date_window.bind('<Escape>', lambda e: date_window.destroy())
    
    def report_by_month(self, parent):
        """گزارش پروژه‌های یک ماه خاص"""
        month_window = tk.Toplevel(parent)
        month_window.title("گزارش ماهانه")
        month_window.geometry("400x250")
        month_window.configure(bg='#f0f0f0')
        month_window.transient(parent)
        month_window.grab_set()
        
        main_frame = tk.Frame(month_window, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            main_frame,
            text="سال و ماه را انتخاب کنید:",
            font=('Tahoma', 10),
            bg='#f0f0f0'
        ).pack(anchor=tk.W, pady=(0, 10))
        
        year_frame = tk.Frame(main_frame, bg='#f0f0f0')
        year_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(year_frame, text="سال:", font=('Tahoma', 10), bg='#f0f0f0').pack(side=tk.LEFT)
        year_entry = tk.Entry(year_frame, font=('Tahoma', 10), width=10)
        year_entry.pack(side=tk.LEFT, padx=(10, 0))
        year_entry.insert(0, str(datetime.now().year))
        
        month_frame = tk.Frame(main_frame, bg='#f0f0f0')
        month_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(month_frame, text="ماه:", font=('Tahoma', 10), bg='#f0f0f0').pack(side=tk.LEFT)
        month_combo = ttk.Combobox(month_frame, font=('Tahoma', 10), width=15)
        month_combo['values'] = list(range(1, 13))
        month_combo.set(datetime.now().month)
        month_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        def search():
            try:
                year = int(year_entry.get())
                month = int(month_combo.get())
                if not (1 <= month <= 12):
                    raise ValueError
            except ValueError:
                messagebox.showerror("خطا", "لطفاً سال و ماه معتبر وارد کنید")
                return
            
            self.clear_results()
            found_projects = []
            
            for project in projects:
                try:
                    start_date = datetime.strptime(project.get('start_date', ''), '%Y-%m-%d')
                    end_date = datetime.strptime(project.get('end_date', ''), '%Y-%m-%d')
                    
                    if start_date.year == year and start_date.month == month:
                        found_projects.append(project)
                        self.add_project_to_results(project)
                except:
                    continue
            
            self.update_count_label()
            month_window.destroy()
            
            if not found_projects:
                messagebox.showinfo("اطلاع", f"پروژه‌ای در ماه {month}/{year} یافت نشد")
        
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X)
        
        search_btn = tk.Button(
            button_frame,
            text="جستجو",
            command=search,
            font=('Tahoma', 10, 'bold'),
            bg='#9b59b6',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=15,
            cursor='hand2'
        )
        search_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(
            button_frame,
            text="لغو",
            command=month_window.destroy,
            font=('Tahoma', 10),
            bg='#95a5a6',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=15,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.LEFT)
        
        month_window.bind('<Return>', lambda e: search())
        month_window.bind('<Escape>', lambda e: month_window.destroy())
    
    def financial_report_weekly(self, parent):
        """گزارش مالی هفتگی"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        self.clear_results()
        found_projects = []
        total_income = 0
        total_cost = 0
        
        projects = self.load_projects()
        for project in projects:
            try:
                end_date = datetime.strptime(project.get('end_date', ''), '%Y-%m-%d')
                if week_start <= end_date <= week_end:
                    found_projects.append(project)
                    self.add_project_to_results(project)
                    total_income += float(project.get('income', 0))
                    total_cost += float(project.get('cost', 0))
            except:
                continue
        
        self.update_count_label()
        
        if found_projects:
            total_profit = total_income - total_cost
            messagebox.showinfo("خلاصه مالی هفتگی", 
                              f"هفته جاری ({week_start.strftime('%Y-%m-%d')} تا {week_end.strftime('%Y-%m-%d')})\n\n"
                              f"تعداد پروژه‌ها: {len(found_projects)}\n"
                              f"کل درآمد: {total_income:,} تومان\n"
                              f"کل هزینه: {total_cost:,} تومان\n"
                              f"سود خالص: {total_profit:,} تومان")
        else:
            messagebox.showinfo("اطلاع", "پروژه‌ای در هفته جاری یافت نشد")
    
    def financial_report_monthly(self, parent):
        """گزارش مالی ماهانه"""
        today = datetime.now()
        month_start = today.replace(day=1)
        if today.month == 12:
            month_end = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            month_end = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
        self.clear_results()
        found_projects = []
        total_income = 0
        total_cost = 0
        
        projects = self.load_projects()
        for project in projects:
            try:
                end_date = datetime.strptime(project.get('end_date', ''), '%Y-%m-%d')
                if month_start <= end_date <= month_end:
                    found_projects.append(project)
                    self.add_project_to_results(project)
                    total_income += float(project.get('income', 0))
                    total_cost += float(project.get('cost', 0))
            except:
                continue
        
        self.update_count_label()
        
        if found_projects:
            total_profit = total_income - total_cost
            messagebox.showinfo("خلاصه مالی ماهانه", 
                              f"ماه جاری ({month_start.strftime('%Y-%m')})\n\n"
                              f"تعداد پروژه‌ها: {len(found_projects)}\n"
                              f"کل درآمد: {total_income:,} تومان\n"
                              f"کل هزینه: {total_cost:,} تومان\n"
                              f"سود خالص: {total_profit:,} تومان")
        else:
            messagebox.showinfo("اطلاع", "پروژه‌ای در ماه جاری یافت نشد")
    
    def financial_report_yearly(self, parent):
        """گزارش مالی سالانه"""
        today = datetime.now()
        year_start = today.replace(month=1, day=1)
        year_end = today.replace(month=12, day=31)
        
        self.clear_results()
        found_projects = []
        total_income = 0
        total_cost = 0
        
        projects = self.load_projects()
        for project in projects:
            try:
                end_date = datetime.strptime(project.get('end_date', ''), '%Y-%m-%d')
                if year_start <= end_date <= year_end:
                    found_projects.append(project)
                    self.add_project_to_results(project)
                    total_income += float(project.get('income', 0))
                    total_cost += float(project.get('cost', 0))
            except:
                continue
        
        self.update_count_label()
        
        if found_projects:
            total_profit = total_income - total_cost
            messagebox.showinfo("خلاصه مالی سالانه", 
                              f"سال جاری ({today.year})\n\n"
                              f"تعداد پروژه‌ها: {len(found_projects)}\n"
                              f"کل درآمد: {total_income:,} تومان\n"
                              f"کل هزینه: {total_cost:,} تومان\n"
                              f"سود خالص: {total_profit:,} تومان")
        else:
            messagebox.showinfo("اطلاع", "پروژه‌ای در سال جاری یافت نشد") 