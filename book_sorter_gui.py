import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

class BookSorterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Сортировщик книг")
        self.root.geometry("800x600")
        
        # Словарь жанров
        self.GENRES = {
            'Devops': ['epub', 'fb2', 'txt'],
            'C++': ['pdf', 'djvu'],
            'Учебники': ['pdf'],
            'Художка': ['pdf', 'djvu']
        }
        
        self.create_widgets()
        self.create_folders()
        self.load_files()

    def create_widgets(self):
        # Левая панель с файлами
        left_frame = ttk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(left_frame, text="Список файлов:").pack(anchor=tk.W)
        
        self.file_listbox = tk.Listbox(left_frame, selectmode=tk.SINGLE)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Правая панель с жанрами и логом
        right_frame = ttk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(right_frame, text="Выберите жанр:").pack(anchor=tk.W)
        
        # Кнопки жанров
        for genre in self.GENRES.keys():
            ttk.Button(right_frame, text=genre, 
                      command=lambda g=genre: self.move_to_genre(g)).pack(fill=tk.X, pady=2)
        
        ttk.Label(right_frame, text="Лог операций:").pack(anchor=tk.W, pady=(10,0))
        
        # Лог операций
        self.log_text = ScrolledText(right_frame, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def create_folders(self):
        """Создание папок для каждого жанра"""
        for genre in self.GENRES.keys():
            Path(genre).mkdir(exist_ok=True)

    def load_files(self):
        """Загрузка списка файлов"""
        self.file_listbox.delete(0, tk.END)
        for file in os.listdir("."):
            if file != os.path.basename(__file__) and os.path.isfile(file):
                self.file_listbox.insert(tk.END, file)

    def move_to_genre(self, genre):
        """Перемещение выбранного файла в папку жанра"""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите файл для перемещения!")
            return
            
        file = self.file_listbox.get(selection[0])
        source = os.path.join(".", file)
        destination = os.path.join(genre, file)
        
        try:
            shutil.move(source, destination)
            self.log_text.insert(tk.END, f"Перемещен файл: {file} в папку {genre}\n")
            self.log_text.see(tk.END)
            self.load_files()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось переместить файл: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookSorterGUI(root)
    root.mainloop() 