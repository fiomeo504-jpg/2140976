import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator - Мигунова Ольга")
        self.root.geometry("700650")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0e6d2')
        
        # Предопределённые задачи
        self.predefined_tasks = [
            ("Прочитать 20 страниц книги", "учёба"),
            ("Сделать зарядку 15 минут", "спорт"),
            ("Написать пост в соцсети", "работа"),
            ("Выпить стакан воды", "спорт"),
            ("Выучить 10 новых слов", "учёба"),
            ("Составить список дел", "работа"),
            ("Убрать на столе", "работа"),
            ("Погулять на свежем воздухе", "спорт"),
            ("Решить 3 задачи", "учёба"),
            ("Посмотреть вебинар", "учёба"),
            ("Сделать растяжку", "спорт"),
            ("Позвонить родителям", "работа"),
            ("Повторить конспекты", "учёба"),
            ("Сходить в магазин", "работа")
        ]
        
        self.task_types = ["учёба", "спорт", "работа", "все"]
        self.filter_type = tk.StringVar(value="все")
        
        # Загружаем историю
        self.history = self.load_history()
        
        self.create_widgets()
        self.display_history()
        self.update_stats()
    
    def create_widgets(self):
        # Заголовок с иконкой
        title_label = tk.Label(self.root, text="🌸 Random Task Generator 🌸", 
                                font=('Segoe UI', 18, 'bold'), bg='#f0e6d2', fg='#b76e79')
        title_label.pack(pady=15)
        
        subtitle = tk.Label(self.root, text="Планируй день с удовольствием!", 
                            font=('Segoe UI', 10, 'italic'), bg='#f0e6d2', fg='#a0522d')
        subtitle.pack(pady=0)
        
        # --- Рамка генерации ---
        frame_gen = tk.LabelFrame(self.root, text="🎲 Случайная задача", 
                                   font=('Segoe UI', 12, 'bold'), bg='#f0e6d2', 
                                   fg='#b76e79', padx=10, pady=12)
        frame_gen.pack(fill="x", padx=15, pady=8)
        
        self.gen_button = tk.Button(frame_gen, text="✨ Сгенерировать задачу ✨",
                                     command=self.generate_task,
                                     bg='#e8c4c8', fg='#8b4513', font=('Segoe UI', 12, 'bold'),
                                     padx=15, pady=8, cursor='hand2', relief='raised', width=28)
        self.gen_button.pack(pady=8)
        
        self.current_task_label = tk.Label(frame_gen, text="", font=('Segoe UI', 11, 'bold'),
                                            fg='#228b22', bg='#f0e6d2', wraplength=600)
        self.current_task_label.pack(pady=5)
        
        # --- Рамка добавления ---
        frame_add = tk.LabelFrame(self.root, text="📝 Добавить свою задачу",
                                   font=('Segoe UI', 12, 'bold'), bg='#f0e6d2',
                                   fg='#b76e79', padx=10, pady=12)
        frame_add.pack(fill="x", padx=15, pady=8)
        
        tk.Label(frame_add, text="Что нужно сделать:", bg='#f0e6d2', font=('Segoe UI', 10), fg='#5c4033').grid(row=0, column=0, padx=8, pady=8, sticky='e')
        self.new_task_entry = tk.Entry(frame_add, width=45, font=('Segoe UI', 10), relief='solid', borderwidth=1, bg='#fff8f0')
        self.new_task_entry.grid(row=0, column=1, padx=8, pady=8)
        
        tk.Label(frame_add, text="Тип задачи:", bg='#f0e6d2', font=('Segoe UI', 10), fg='#5c4033').grid(row=1, column=0, padx=8, pady=8, sticky='e')
        self.new_type_combo = ttk.Combobox(frame_add, values=self.task_types[:-1],
                                            state="readonly", width=42, font=('Segoe UI', 10))
        self.new_type_combo.current(0)
        self.new_type_combo.grid(row=1, column=1, padx=8, pady=8)
        
        self.add_button = tk.Button(frame_add, text="➕ Добавить задачу", command=self.add_task,
                                     bg='#c8a2c8', fg='white', font=('Segoe UI', 10, 'bold'),
                                     padx=10, pady=5, cursor='hand2', width=18)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # --- Рамка фильтрации ---
        frame_filter = tk.LabelFrame(self.root, text="🔍 Фильтр задач",
                                      font=('Segoe UI', 12, 'bold'), bg='#f0e6d2',
                                      fg='#b76e79', padx=10, pady=10)
        frame_filter.pack(fill="x", padx=15, pady=8)
        
        filter_buttons_frame = tk.Frame(frame_filter, bg='#f0e6d2')
        filter_buttons_frame.pack()
        
        for t in self.task_types:
            rb = tk.Radiobutton(filter_buttons_frame, text=t.capitalize(), variable=self.filter_type,
                                value=t, command=self.display_history, bg='#f0e6d2',
                                font=('Segoe UI', 11), selectcolor='#f0e6d2', fg='#5c4033')
            rb.pack(side="left", padx=25)
        
        # --- Рамка истории ---
        frame_history = tk.LabelFrame(self.root, text="📜 История моих задач",
                                       font=('Segoe UI', 12, 'bold'), bg='#f0e6d2',
                                       fg='#b76e79', padx=10, pady=12)
        frame_history.pack(fill="both", expand=True, padx=15, pady=8)
        
        list_frame = tk.Frame(frame_history, bg='#f0e6d2')
        list_frame.pack(fill="both", expand=True)
        
        self.history_listbox = tk.Listbox(list_frame, height=12, font=('Segoe UI', 10),
                                           selectmode=tk.SINGLE, bg='#fff8f0', fg='#4a3728',
                                           relief='solid', borderwidth=1, selectbackground='#e8c4c8')
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.history_listbox.yview, bg='#f0e6d2')
        self.history_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.history_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # --- Нижняя панель ---
        bottom_frame = tk.Frame(self.root, bg='#f0e6d2')
        bottom_frame.pack(fill="x", padx=15, pady=12)
        
        self.save_button = tk.Button(bottom_frame, text="💾 Сохранить историю", 
                                      command=self.save_history_to_json,
                                      bg='#d4a5a5', fg='white', font=('Segoe UI', 10, 'bold'),
                                      padx=12, pady=5, cursor='hand2')
        self.save_button.pack(side="left", padx=5)
        
        self.stats_label = tk.Label(bottom_frame, text="", bg='#f0e6d2', font=('Segoe UI', 10, 'italic'), fg='#a0522d')
        self.stats_label.pack(side="right", padx=5)
        
        self.clear_button = tk.Button(bottom_frame, text="🗑 Очистить историю", 
                                       command=self.clear_history,
                                       bg='#cd9b9b', fg='white', font=('Segoe UI', 9),
                                       padx=8, pady=5, cursor='hand2')
        self.clear_button.pack(side="left", padx=5)
        
        self.export_button = tk.Button(bottom_frame, text="📄 Экспорт в CSV", 
                                        command=self.export_to_csv,
                                        bg='#9bcd9b', fg='white', font=('Segoe UI', 9),
                                        padx=8, pady=5, cursor='hand2')
        self.export_button.pack(side="left", padx=5)
        
        # --- Информационная строка ---
        info_frame = tk.Frame(self.root, bg='#f0e6d2')
        info_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        self.info_label = tk.Label(info_frame, text="✨ Желаю продуктивного дня! ✨", 
                                    bg='#f0e6d2', font=('Segoe UI', 9, 'italic'), fg='#b76e79')
        self.info_label.pack()
    
    def update_stats(self):
        total = len(self.history)
        if total > 0:
            study_count = sum(1 for item in self.history if item["type"] == "учёба")
            sport_count = sum(1 for item in self.history if item["type"] == "спорт")
            work_count = sum(1 for item in self.history if item["type"] == "работа")
            self.stats_label.config(text=f"📊 Всего: {total}  |  📚 Учёба: {study_count}  |  🏃 Спорт: {sport_count}  |  💼 Работа: {work_count}")
        else:
            self.stats_label.config(text="📊 Пока нет задач. Начните с генерации или добавления!")
    
    def generate_task(self):
        task, task_type = random.choice(self.predefined_tasks)
        self.history.append({"task": task, "type": task_type})
        self.current_task_label.config(text=f"🎉 {task} [{task_type}] 🎉")
        self.display_history()
        self.save_history_to_json()
        self.update_stats()
    
    def add_task(self):
        task = self.new_task_entry.get().strip()
        task_type = self.new_type_combo.get()
        
        # Валидация
        if not task:
            messagebox.showerror("Ошибка", "❌ Название задачи не может быть пустым!")
            return
        
        if len(task) < 2:
            messagebox.showerror("Ошибка", "❌ Название слишком короткое (минимум 2 символа)!")
            return
        
        if len(task) > 80:
            messagebox.showerror("Ошибка", "❌ Название слишком длинное (максимум 80 символов)!")
            return
        
        # Проверка на дубликаты с предупреждением
        for existing in self.predefined_tasks:
            if existing[0].lower() == task.lower():
                if messagebox.askyesno("Дубликат", f"Задача '{task}' уже существует в списке.\nДобавить всё равно?"):
                    break
                return
        
        self.predefined_tasks.append((task, task_type))
        self.history.append({"task": task, "type": task_type})
        
        self.new_task_entry.delete(0, tk.END)
        self.current_task_label.config(text=f"✨ Добавлено: {task} ✨")
        self.display_history()
        self.save_history_to_json()
        self.update_stats()
        
        messagebox.showinfo("Успех", f"✅ Задача '{task}' успешно добавлена!")
    
    def display_history(self):
        self.history_listbox.delete(0, tk.END)
        current_filter = self.filter_type.get()
        
        if not self.history:
            self.history_listbox.insert(tk.END, "🌸 История пока пуста. Сгенерируйте или добавьте задачу!")
            self.history_listbox.itemconfig(0, fg='#cd5c5c')
            return
        
        filtered = [item for item in self.history if current_filter == "все" or item["type"] == current_filter]
        
        if not filtered:
            self.history_listbox.insert(tk.END, f"✨ Нет задач типа '{current_filter}'")
            return
        
        for i, item in enumerate(filtered, 1):
            emoji = "📚" if item["type"] == "учёба" else "🏃" if item["type"] == "спорт" else "💼"
            display_text = f"{i:2d}. {emoji} {item['task']}"
            self.history_listbox.insert(tk.END, display_text)
    
    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю задач?"):
            self.history = []
            self.display_history()
            self.save_history_to_json()
            self.update_stats()
            self.current_task_label.config(text="История очищена")
            messagebox.showinfo("Готово", "История успешно очищена!")
    
    def export_to_csv(self):
        """Экспорт истории в CSV файл"""
        if not self.history:
            messagebox.showwarning("Нет данных", "История пуста. Нечего экспортировать!")
            return
        
        try:
            import csv
            filename = f"tasks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['№', 'Задача', 'Тип'])
                for i, item in enumerate(self.history, 1):
                    writer.writerow([i, item['task'], item['type']])
            messagebox.showinfo("Экспорт", f"✅ История экспортирована в файл:\n{filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {e}")
    
    def load_history(self):
        if not os.path.exists("tasks.json"):
            return []
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError):
            return []
    
    def save_history_to_json(self):
        try:
            with open("tasks.json", "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=4, ensure_ascii=False)
            # messagebox.showinfo("Сохранено", "✅ История сохранена!")  # Раскомментировать, если нужно уведомление
        except IOError:
            messagebox.showerror("Ошибка", "❌ Не удалось сохранить историю!")


if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()
  
