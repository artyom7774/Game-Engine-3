from PIL import Image

# Открываем изображение
image = Image.open('grass.png')

# Устанавливаем новые размеры, кратные оригиналу (например, в два раза больше)
width, height = image.size
new_width = width * 2
new_height = height * 2

# Используем метод resize с различными методами интерполяции
resized_image_nearest = image.resize((new_width, new_height), resample=Image.NEAREST)
resized_image_bilinear = image.resize((new_width, new_height), resample=Image.BILINEAR)
resized_image_bicubic = image.resize((new_width, new_height), resample=Image.BICUBIC)
resized_image_lanczos = image.resize((new_width, new_height), resample=Image.LANCZOS)

# Сохраняем или отображаем результаты
resized_image_nearest.save('resized_image_nearest.png')
resized_image_bilinear.save('resized_image_bilinear.png')
resized_image_bicubic.save('resized_image_bicubic.png')
resized_image_lanczos.save('resized_image_lanczos.png')

resized_image_nearest.show()
resized_image_bilinear.show()
resized_image_bicubic.show()
resized_image_lanczos.show()
