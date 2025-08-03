import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
from text_editor import TextEditor

class ProjectManager:
    def __init__(self):
        self.projects_file = "projects.json"
        self.companies_file = "companies.json"
        self.projects = self.load_projects()
        self.companies = self.load_companies()
        
    def load_projects(self):
        """پروژه‌ها رو از فایل می‌خونم"""
        if os.path.exists(self.projects_file):
            try:
                with open(self.projects_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_projects(self):
        """پروژه‌ها رو در فایل ذخیره می‌کنم"""
        with open(self.projects_file, 'w', encoding='utf-8') as f:
            json.dump(self.projects, f, ensure_ascii=False, indent=2)
    
    def load_companies(self):
        """شرکت‌ها رو از فایل می‌خونم"""
        if os.path.exists(self.companies_file):
            try:
                with open(self.companies_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_companies(self):
        """شرکت‌ها رو در فایل ذخیره می‌کنم"""
        with open(self.companies_file, 'w', encoding='utf-8') as f:
            json.dump(self.companies, f, ensure_ascii=False, indent=2)
    
    def show_project_management(self, parent, current_user):
        """پنجره مدیریت پروژه رو نشون می‌دم"""
        main_frame = tk.Frame(parent, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_label = tk.Label(
            main_frame,
            text="مدیریت پروژه‌ها",
            font=('Tahoma', 16, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        buttons_data = [
            ("ثبت پروژه جدید", self.show_add_project_form, '#2ecc71'),
            ("ثبت اطلاعات شرکت/کارفرما", self.show_add_company_form, '#3498db'),
            ("ویرایش پروژه", self.show_edit_project_form, '#f39c12'),
            ("حذف پروژه", self.delete_project, '#e74c3c')
        ]
        
        for text, command, color in buttons_data:
            btn = tk.Button(
                button_frame,
                text=text,
                command=lambda cmd=command: cmd(parent),
                font=('Tahoma', 10, 'bold'),
                bg=color,
                fg='white',
                relief=tk.RAISED,
                bd=2,
                width=20,
                height=2,
                cursor='hand2'
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        table_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=2)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_projects_table(table_frame)
        
        self.refresh_projects_table()
    
    def create_projects_table(self, parent):
        """ایجاد جدول پروژه‌ها"""
        header_frame = tk.Frame(parent, bg='#34495e', height=40)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        headers = ["نام پروژه", "کارفرما", "تاریخ شروع", "تاریخ پایان", "درآمد", "هزینه", "سود خالص", "وضعیت"]
        widths = [150, 120, 100, 100, 80, 80, 80, 80]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            label = tk.Label(
                header_frame,
                text=header,
                font=('Tahoma', 10, 'bold'),
                bg='#34495e',
                fg='white',
                width=width//10
            )
            label.pack(side=tk.LEFT, padx=2, pady=10)
        
        content_frame = tk.Frame(parent)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('name', 'client', 'start_date', 'end_date', 'income', 'cost', 'profit', 'status')
        self.tree = ttk.Treeview(content_frame, columns=columns, show='headings', height=15)
        
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
        
        for col, name in column_names.items():
            self.tree.heading(col, text=name)
            self.tree.column(col, width=widths[list(column_names.keys()).index(col)], anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind('<Double-1>', self.on_project_select)
    
    def refresh_projects_table(self):
        """به‌روزرسانی جدول پروژه‌ها"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for project in self.projects:
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
            
            self.tree.insert('', tk.END, values=(
                project.get('name', ''),
                project.get('client', ''),
                project.get('start_date', ''),
                project.get('end_date', ''),
                f"{income:,}",
                f"{cost:,}",
                f"{profit:,}",
                status
            ))
    
    def on_project_select(self, event):
        """در صورت انتخاب پروژه از جدول"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            project_name = item['values'][0]
            self.show_project_details(project_name)
    
    def show_add_project_form(self, parent):
        """نمایش فرم ثبت پروژه جدید"""
        form_window = tk.Toplevel(parent)
        form_window.title("ثبت پروژه جدید")
        form_window.geometry("600x700")
        form_window.configure(bg='#f0f0f0')
        form_window.transient(parent)
        form_window.grab_set()
        
        form_window.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        main_frame = tk.Frame(form_window, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = tk.Label(
            main_frame,
            text="ثبت پروژه جدید",
            font=('Tahoma', 16, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        form_frame = tk.Frame(main_frame, bg='#f0f0f0')
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(form_frame, text="نام پروژه:", font=('Tahoma', 10), bg='#f0f0f0').pack(anchor=tk.W)
        name_entry = tk.Entry(form_frame, font=('Tahoma', 10), width=40)
        name_entry.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(form_frame, text="کارفرما:", font=('Tahoma', 10), bg='#f0f0f0').pack(anchor=tk.W)
        client_combo = ttk.Combobox(form_frame, font=('Tahoma', 10), width=37)
        client_combo['values'] = [company['name'] for company in self.companies]
        client_combo.pack(fill=tk.X, pady=(0, 15))
        
        date_frame = tk.Frame(form_frame, bg='#f0f0f0')
        date_frame.pack(fill=tk.X, pady=(0, 15))
        
        start_frame = tk.Frame(date_frame, bg='#f0f0f0')
        start_frame.pack(side=tk.LEFT, padx=(0, 20))
        tk.Label(start_frame, text="تاریخ شروع:", font=('Tahoma', 10), bg='#f0f0f0').pack(anchor=tk.W)
        start_date_entry = tk.Entry(start_frame, font=('Tahoma', 10), width=15)
        start_date_entry.pack()
        start_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        end_frame = tk.Frame(date_frame, bg='#f0f0f0')
        end_frame.pack(side=tk.LEFT)
        tk.Label(end_frame, text="تاریخ پایان:", font=('Tahoma', 10), bg='#f0f0f0').pack(anchor=tk.W)
        end_date_entry = tk.Entry(end_frame, font=('Tahoma', 10), width=15)
        end_date_entry.pack()
        
        financial_frame = tk.Frame(form_frame, bg='#f0f0f0')
        financial_frame.pack(fill=tk.X, pady=(0, 15))
        
        income_frame = tk.Frame(financial_frame, bg='#f0f0f0')
        income_frame.pack(side=tk.LEFT, padx=(0, 20))
        tk.Label(income_frame, text="درآمد:", font=('Tahoma', 10), bg='#f0f0f0').pack(anchor=tk.W)
        income_entry = tk.Entry(income_frame, font=('Tahoma', 10), width=15)
        income_entry.pack()
        income_entry.insert(0, "0")
        
        cost_frame = tk.Frame(financial_frame, bg='#f0f0f0')
        cost_frame.pack(side=tk.LEFT)
        tk.Label(cost_frame, text="هزینه:", font=('Tahoma', 10), bg='#f0f0f0').pack(anchor=tk.W)
        cost_entry = tk.Entry(cost_frame, font=('Tahoma', 10), width=15)
        cost_entry.pack()
        cost_entry.insert(0, "0")
        
        tk.Label(form_frame, text="اعضای تیم (جدا شده با کاما):", font=('Tahoma', 10), bg='#f0f0f0').pack(anchor=tk.W)
        team_entry = tk.Entry(form_frame, font=('Tahoma', 10), width=40)
        team_entry.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(form_frame, text="شرح پروژه:", font=('Tahoma', 10), bg='#f0f0f0').pack(anchor=tk.W)
        description_text = tk.Text(form_frame, font=('Tahoma', 10), height=8, wrap=tk.WORD)
        description_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        status_label = tk.Label(
            form_frame,
            text="",
            font=('Tahoma', 9),
            bg='#f0f0f0',
            fg='#e74c3c'
        )
        status_label.pack(pady=(0, 15))
        
        def save_project():
            name = name_entry.get().strip()
            client = client_combo.get().strip()
            start_date = start_date_entry.get().strip()
            end_date = end_date_entry.get().strip()
            income = income_entry.get().strip()
            cost = cost_entry.get().strip()
            team = team_entry.get().strip()
            description = description_text.get("1.0", tk.END).strip()
            
            if not all([name, client, start_date, end_date]):
                status_label.config(text="لطفاً فیلدهای اجباری را پر کنید")
                return
            
            try:
                income = float(income)
                cost = float(cost)
            except ValueError:
                status_label.config(text="مقادیر مالی باید عددی باشند")
                return
            
            if any(p['name'] == name for p in self.projects):
                status_label.config(text="پروژه‌ای با این نام قبلاً ثبت شده است")
                return
            
            new_project = {
                'name': name,
                'client': client,
                'start_date': start_date,
                'end_date': end_date,
                'income': income,
                'cost': cost,
                'team': team,
                'description': description,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            self.projects.append(new_project)
            self.save_projects()
            
            status_label.config(text="پروژه با موفقیت ثبت شد!", fg='#27ae60')
            form_window.after(2000, form_window.destroy)
            self.refresh_projects_table()
        
        button_frame = tk.Frame(form_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X)
        
        save_btn = tk.Button(
            button_frame,
            text="ذخیره",
            command=save_project,
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
            command=form_window.destroy,
            font=('Tahoma', 10),
            bg='#95a5a6',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=15,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.LEFT)
    
    def show_add_company_form(self, parent):
        """نمایش فرم ثبت شرکت/کارفرما"""
        form_window = tk.Toplevel(parent)
        form_window.title("ثبت اطلاعات شرکت/کارفرما")
        form_window.geometry("500x400")
        form_window.configure(bg='#f0f0f0')
        form_window.transient(parent)
        form_window.grab_set()
        
        form_window.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        main_frame = tk.Frame(form_window, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = tk.Label(
            main_frame,
            text="ثبت اطلاعات شرکت/کارفرما",
            font=('Tahoma', 16, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 30))
        
        form_frame = tk.Frame(main_frame, bg='#f0f0f0')
        form_frame.pack(expand=True)
        
        tk.Label(form_frame, text="نام شرکت/کارفرما:", font=('Tahoma', 10), bg='#f0f0f0').pack(anchor=tk.W)
        name_entry = tk.Entry(form_frame, font=('Tahoma', 10), width=40)
        name_entry.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(form_frame, text="شماره تماس:", font=('Tahoma', 10), bg='#f0f0f0').pack(anchor=tk.W)
        phone_entry = tk.Entry(form_frame, font=('Tahoma', 10), width=40)
        phone_entry.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(form_frame, text="آدرس:", font=('Tahoma', 10), bg='#f0f0f0').pack(anchor=tk.W)
        address_text = tk.Text(form_frame, font=('Tahoma', 10), height=4, wrap=tk.WORD)
        address_text.pack(fill=tk.X, pady=(0, 15))
        
        status_label = tk.Label(
            form_frame,
            text="",
            font=('Tahoma', 9),
            bg='#f0f0f0',
            fg='#e74c3c'
        )
        status_label.pack(pady=(0, 15))
        
        def save_company():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            address = address_text.get("1.0", tk.END).strip()
            
            if not name:
                status_label.config(text="لطفاً نام شرکت را وارد کنید")
                return
            
            if any(c['name'] == name for c in self.companies):
                status_label.config(text="شرکتی با این نام قبلاً ثبت شده است")
                return
            
            new_company = {
                'name': name,
                'phone': phone,
                'address': address,
                'created_at': datetime.now().isoformat()
            }
            
            self.companies.append(new_company)
            self.save_companies()
            
            status_label.config(text="شرکت با موفقیت ثبت شد!", fg='#27ae60')
            form_window.after(2000, form_window.destroy)
        
        button_frame = tk.Frame(form_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X)
        
        save_btn = tk.Button(
            button_frame,
            text="ذخیره",
            command=save_company,
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
            command=form_window.destroy,
            font=('Tahoma', 10),
            bg='#95a5a6',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=15,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.LEFT)
    
    def show_edit_project_form(self, parent):
        """نمایش فرم ویرایش پروژه"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("هشدار", "لطفاً ابتدا پروژه‌ای را انتخاب کنید")
            return
        
        item = self.tree.item(selection[0])
        project_name = item['values'][0]
        
        project = None
        for p in self.projects:
            if p['name'] == project_name:
                project = p
                break
        
        if not project:
            messagebox.showerror("خطا", "پروژه یافت نشد")
            return
        
        self.show_add_project_form(parent)
    
    def delete_project(self, parent):
        """حذف پروژه"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("هشدار", "لطفاً ابتدا پروژه‌ای را انتخاب کنید")
            return
        
        item = self.tree.item(selection[0])
        project_name = item['values'][0]
        
        if messagebox.askyesno("تأیید", f"آیا مطمئن هستید که می‌خواهید پروژه '{project_name}' را حذف کنید؟"):
            self.projects = [p for p in self.projects if p['name'] != project_name]
            self.save_projects()
            self.refresh_projects_table()
            messagebox.showinfo("موفقیت", "پروژه با موفقیت حذف شد")
    
    def show_project_details(self, project_name):
        """نمایش جزئیات پروژه"""
        project = None
        for p in self.projects:
            if p['name'] == project_name:
                project = p
                break
        
        if not project:
            messagebox.showerror("خطا", "پروژه یافت نشد")
            return
        
        details_window = tk.Toplevel()
        details_window.title(f"جزئیات پروژه: {project_name}")
        details_window.geometry("800x600")
        details_window.configure(bg='#f0f0f0')
        
        main_frame = tk.Frame(details_window, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = tk.Label(
            main_frame,
            text=f"جزئیات پروژه: {project_name}",
            font=('Tahoma', 16, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        info_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=2)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        info_text = f"""
نام پروژه: {project.get('name', '')}
کارفرما: {project.get('client', '')}
تاریخ شروع: {project.get('start_date', '')}
تاریخ پایان: {project.get('end_date', '')}
درآمد: {project.get('income', 0):,} تومان
هزینه: {project.get('cost', 0):,} تومان
سود خالص: {float(project.get('income', 0)) - float(project.get('cost', 0)):,} تومان
اعضای تیم: {project.get('team', '')}
        """
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=('Tahoma', 10),
            bg='white',
            fg='#2c3e50',
            justify=tk.LEFT
        )
        info_label.pack(padx=20, pady=20)
        
        desc_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=2)
        desc_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            desc_frame,
            text="شرح پروژه:",
            font=('Tahoma', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        desc_text = tk.Text(
            desc_frame,
            font=('Tahoma', 10),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        desc_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        desc_text.config(state=tk.NORMAL)
        desc_text.insert("1.0", project.get('description', ''))
        desc_text.config(state=tk.DISABLED) 