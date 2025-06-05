import os
import tkinter as tk
from tkinter import messagebox, colorchooser
from PIL import Image, ImageDraw, ImageFont
from tkcalendar import Calendar

# --- НАСТРОЙКИ ПУТЕЙ ---
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

# --- ПЕРЕМЕННЫЕ ДЛЯ НАСТРОЕК (после создания окна root) ---
selected_color = "#FF0000"


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

def choose_color():
    global selected_color
    color_code = colorchooser.askcolor(title="Выбор цвета текста")
    if color_code[1]:
        selected_color = color_code[1]
        color_display.config(bg=selected_color)

def put_the_date_on_all_photos():
    try:
        font_size = int(font_size_var.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Размер шрифта должен быть числом.")
        return

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
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()

            # Получение размеров изображения и текста
            image_width, image_height = image.size
            bbox = font.getbbox(date_str)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Координаты правого нижнего угла с отступами
            padding = 25
            vertical_offset = 25  # Поднимаем дату на 25 пикселей вверх
            
            x = image_width - text_width - padding
            y = image_height - text_height - padding - vertical_offset

            # Наносим текст по выбранным координатам
            draw.text((x, y), date_str, fill=selected_color, font=font)

            output_path = os.path.join(OUTPUT_FOLDER, filename)
            
            image.save(output_path)
            processed += 1
        except Exception as e:
            failed += 1
            print(f"Ошибка при обработке {filename}: {e}")

    messagebox.showinfo("Результат", f"Обработано: {processed} файлов\nНеудачно: {failed} файлов")

# --- ИНТЕРФЕЙС ---
root = tk.Tk()
font_size_var = tk.StringVar(value="36")
root.title("Добавление даты ко всем изображениям")
root.geometry("550x600")
root.resizable(False, False)

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# --- Календарь ---
tk.Label(main_frame, text="Выберите дату для добавления на изображения:", font=("Arial", 12)).pack(anchor='w')
cal = Calendar(main_frame, selectmode='day', year=2025, month=1, day=1, locale='ru')
cal.pack(pady=5)

# --- НАСТРОЙКИ ЦВЕТА И ШРИФТА ---
settings_frame = tk.Frame(main_frame)
settings_frame.pack(fill=tk.X, pady=10)

# Цвет
tk.Label(settings_frame, text="Цвет текста:", font=("Arial", 10)).grid(row=0, column=0, sticky='w')
tk.Button(settings_frame, text="Выбрать цвет", command=choose_color).grid(row=0, column=1, sticky='w', padx=5)
color_display = tk.Label(settings_frame, width=3, bg=selected_color, relief="ridge")
color_display.grid(row=0, column=2, padx=5)

# Размер шрифта
tk.Label(settings_frame, text="Размер шрифта:", font=("Arial", 10)).grid(row=1, column=0, sticky='w', pady=5)
tk.Entry(settings_frame, textvariable=font_size_var, width=5).grid(row=1, column=1, sticky='w', padx=5)

# --- Кнопка обработки ---
tk.Button(main_frame, text="Добавить дату ко всем изображениям",
          command=put_the_date_on_all_photos,
          bg="green", fg="white", font=("Arial", 12), height=2).pack(pady=10, fill=tk.X)

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

# --- Запуск ---
root.mainloop()