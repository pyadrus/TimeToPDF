from PIL import Image, ImageDraw, ImageFont
import datetime
import os

# Путь к изображению
image_path = "photo.jpg"
# Путь для сохранения
output_path = "photo_with_date.jpg"

# Открываем изображение
image = Image.open(image_path)
draw = ImageDraw.Draw(image)

# Получаем текущую дату и время
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Выбираем шрифт (можно указать свой или использовать стандартный)
try:
    font = ImageFont.truetype("arial.ttf", 36)  # размер шрифта
except:
    font = ImageFont.load_default()

# Цвет текста (RGB или "white", "black" и т.д.)
text_color = (255, 0, 0)  # красный цвет

# Позиция текста (можно изменить)
position = (10, 10)  # слева сверху

# Добавляем текст на изображение
draw.text(position, current_time, fill=text_color, font=font)

# Сохраняем результат
image.save(output_path)

print(f"Дата добавлена. Файл сохранён как {output_path}")