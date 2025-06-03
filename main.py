import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont
from tkcalendar import Calendar

# --- НАСТРОЙКИ ПУТЕЙ ---
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

# --- ФУНКЦИИ ---
def scan_images(folder_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']
    try:
        files = os.listdir(folder_path)
        return [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть папку:\n{e}")
        return []

def refresh_image_list():
    image_list.delete(0, tk.END)
    images = scan_images(INPUT_FOLDER)
    for img in images:
        image_list.insert(tk.END, img)

def put_the_date_on_all_photos():
    selected_date = cal.selection_get()
    images = scan_images(INPUT_FOLDER)

    if not images:
        messagebox.showwarning("Предупреждение", "В папке нет изображений для обработки.")
        return

    processed, failed = 0, 0
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    date_str = selected_date.strftime("%Y-%m-%d")

    for filename in images:
        input_path = os.path.join(INPUT_FOLDER, filename)
        try:
            image = Image.open(input_path)
            draw = ImageDraw.Draw(image)

            try:
                font = ImageFont.truetype("arial.ttf", 36)
            except:
                font = ImageFont.load_default()

            text_color = (255, 0, 0)
            position = (10, 10)
            draw.text(position, date_str, fill=text_color, font=font)

            output_path = os.path.join(
                OUTPUT_FOLDER,
                f"{os.path.splitext(filename)[0]}_with_date{os.path.splitext(filename)[1]}"
            )
            image.save(output_path)
            processed += 1
        except Exception as e:
            failed += 1
            print(f"Ошибка при обработке {filename}: {e}")

    messagebox.showinfo("Результат", f"Обработано: {processed} файлов\nНеудачно: {failed} файлов")

# --- ИНТЕРФЕЙС ---
root = tk.Tk()
root.title("Добавление даты ко всем изображениям")
root.geometry("500x500")
root.resizable(False, False)

# --- Основной контейнер ---
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# --- Календарь ---
tk.Label(main_frame, text="Выберите дату для добавления на изображения:",
         font=("Arial", 12)).pack(anchor='w', pady=(0, 5))

cal = Calendar(main_frame, selectmode='day', year=2025, month=1, day=1, locale='ru')
cal.pack(pady=5)

# --- Кнопка обработки ---
tk.Button(main_frame, text="Добавить дату ко всем изображениям",
          command=put_the_date_on_all_photos,
          bg="green", fg="white", font=("Arial", 12), height=2).pack(pady=15, fill=tk.X)

# --- Список изображений ---
list_frame = tk.LabelFrame(main_frame, text="Изображения в папке input", padx=10, pady=10, font=("Arial", 10))
list_frame.pack(fill=tk.BOTH, expand=True)

image_list = tk.Listbox(list_frame, height=12, width=60, font=("Courier New", 10))
image_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=image_list.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
image_list.config(yscrollcommand=scrollbar.set)

# --- Заполнение списка изображений ---
refresh_image_list()

# --- Запуск интерфейса ---
root.mainloop()

