import os
import tkinter as tk
from tkinter import colorchooser
from tkinter import messagebox

import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
from tkcalendar import Calendar

# --- НАСТРОЙКИ ПУТЕЙ ---
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

# --- ПЕРЕМЕННЫЕ ДЛЯ НАСТРОЕК (после создания окна root) ---
selected_color = "#FF0000"


# --- ФУНКЦИИ ---
def scan_images(folder_path):
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"]
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


def ensure_folder_exists(folder_path):
    """Функция для создания папки, если она не существует"""
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            print(f"Папка {folder_path} успешно создана.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать папку {folder_path}:\n{e}")
            return False
    return True


# Перед использованием папок, убедитесь в их существовании
ensure_folder_exists(INPUT_FOLDER)
ensure_folder_exists(OUTPUT_FOLDER)


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
        messagebox.showwarning(
            "Предупреждение", "В папке нет изображений для обработки."
        )
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

            try:
                padding = int(padding_right_var.get())
                vertical_offset = int(padding_bottom_var.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Отступы должны быть числовыми значениями.")
                return

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

    messagebox.showinfo(
        "Результат", f"Обработано: {processed} файлов\nНеудачно: {failed} файлов"
    )


def put_date_and_name_on_all_photos():
    try:
        font_size = int(font_size_var.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Размер шрифта должен быть числом.")
        return

    selected_date = cal.selection_get()
    images = scan_images(INPUT_FOLDER)

    if not images:
        messagebox.showwarning(
            "Предупреждение", "В папке нет изображений для обработки."
        )
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

            # Удаляем расширение из имени файла
            filename_without_ext = os.path.splitext(filename)[0]

            # Получение размеров изображения и текста
            image_width, image_height = image.size
            bbox_date = font.getbbox(date_str)
            bbox_name = font.getbbox(filename_without_ext)
            text_width_date = bbox_date[2] - bbox_date[0]
            text_height_date = bbox_date[3] - bbox_date[1]
            text_width_name = bbox_name[2] - bbox_name[0]
            text_height_name = bbox_name[3] - bbox_name[1]

            # Координаты правого нижнего угла с отступами
            try:
                padding = int(padding_right_var.get())
                vertical_offset = int(padding_bottom_var.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Отступы должны быть числовыми значениями.")
                return
            line_spacing = 10  # Отступ между именем файла и датой

            # Координаты для имени файла (выше даты)
            x_name = image_width - text_width_name - padding
            y_name = image_height - text_height_date - text_height_name - padding - vertical_offset - line_spacing

            # Координаты для даты
            x_date = image_width - text_width_date - padding
            y_date = image_height - text_height_date - padding - vertical_offset

            # Наносим имя файла (без расширения) и дату
            draw.text((x_name, y_name), filename_without_ext, fill=selected_color, font=font)
            draw.text((x_date, y_date), date_str, fill=selected_color, font=font)

            output_path = os.path.join(OUTPUT_FOLDER, filename)
            image.save(output_path)
            processed += 1
        except Exception as e:
            failed += 1
            print(f"Ошибка при обработке {filename}: {e}")

    messagebox.showinfo(
        "Результат", f"Обработано: {processed} файлов\nНеудачно: {failed} файлов"
    )


def convert_pdfs_to_jpgs():
    pdf_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".pdf")]

    if not pdf_files:
        messagebox.showwarning("Предупреждение", "В папке input нет PDF-файлов.")
        return

    processed = 0
    failed = 0

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for pdf_file in pdf_files:
        input_path = os.path.join(INPUT_FOLDER, pdf_file)
        output_name = os.path.splitext(pdf_file)[0] + ".jpg"
        output_path = os.path.join(OUTPUT_FOLDER, output_name)

        try:
            doc = fitz.open(input_path)
            page = doc.load_page(0)  # Первая страница
            image_list = page.get_images(full=True)

            if image_list:
                # Берём первое изображение на странице
                xref = image_list[0][0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                # Сохраняем как JPG
                with open(output_path, "wb") as img_file:
                    img_file.write(image_bytes)

                processed += 1
            else:
                failed += 1
                print(f"Нет изображений в файле {pdf_file}")
        except Exception as e:
            failed += 1
            print(f"Ошибка при обработке {pdf_file}: {e}")
        finally:
            doc.close()

    messagebox.showinfo(
        "Результат конвертации",
        f"Успешно: {processed} файлов\nНеудачно: {failed} файлов",
    )
    refresh_image_list()


# --- ИНТЕРФЕЙС ---
root = tk.Tk()
font_size_var = tk.StringVar(value="36")
root.title("Добавление даты ко всем изображениям")
root.geometry("550x600")
root.resizable(False, False)

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# --- Календарь ---
tk.Label(
    main_frame, text="Выберите дату для добавления на изображения:", font=("Arial", 12)
).pack(anchor="w")
cal = Calendar(main_frame, selectmode="day", year=2025, month=1, day=1, locale="ru")
cal.pack(pady=5)

# --- НАСТРОЙКИ ЦВЕТА И ШРИФТА ---
settings_frame = tk.Frame(main_frame)
settings_frame.pack(fill=tk.X, pady=10)

# Цвет
tk.Label(settings_frame, text="Цвет текста:", font=("Arial", 10)).grid(
    row=0, column=0, sticky="w"
)
tk.Button(settings_frame, text="Выбрать цвет", command=choose_color).grid(
    row=0, column=1, sticky="w", padx=5
)
color_display = tk.Label(settings_frame, width=3, bg=selected_color, relief="ridge")
color_display.grid(row=0, column=2, padx=5)

padding_right_var = tk.StringVar(value="50")
padding_bottom_var = tk.StringVar(value="50")

# Отступ справа
tk.Label(settings_frame, text="Отступ справа:", font=("Arial", 10)).grid(row=0, column=3, sticky="w", padx=(10, 0))
tk.Entry(settings_frame, textvariable=padding_right_var, width=5).grid(row=0, column=4, sticky="w")

# Отступ снизу
tk.Label(settings_frame, text="Отступ снизу:", font=("Arial", 10)).grid(row=0, column=5, sticky="w", padx=(10, 0))
tk.Entry(settings_frame, textvariable=padding_bottom_var, width=5).grid(row=0, column=6, sticky="w")

# Размер шрифта
tk.Label(settings_frame, text="Размер шрифта:", font=("Arial", 10)).grid(
    row=1, column=0, sticky="w", pady=5
)
tk.Entry(settings_frame, textvariable=font_size_var, width=5).grid(
    row=1, column=1, sticky="w", padx=5
)

# --- Кнопка обработки (только дата) ---
tk.Button(
    main_frame,
    text="Добавить дату ко всем изображениям",
    command=put_the_date_on_all_photos,
    bg="green",
    fg="white",
    font=("Arial", 12),
    height=2,
).pack(pady=10, fill=tk.X)

# --- Новая кнопка обработки (дата + имя файла) ---
tk.Button(
    main_frame,
    text="Добавить дату и имя файла ко всем изображениям",
    command=put_date_and_name_on_all_photos,
    bg="purple",
    fg="white",
    font=("Arial", 12),
    height=2,
).pack(pady=5, fill=tk.X)

# --- Кнопка конвертации PDF в JPG ---
tk.Button(
    main_frame,
    text="Конвертировать PDF в JPG",
    command=convert_pdfs_to_jpgs,
    bg="blue",
    fg="white",
    font=("Arial", 12),
    height=2,
).pack(pady=5, fill=tk.X)

# --- Список изображений ---
list_frame = tk.LabelFrame(
    main_frame, text="Изображения в папке input", padx=10, pady=10, font=("Arial", 10)
)
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
