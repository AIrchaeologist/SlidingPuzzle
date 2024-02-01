from PIL import Image


class NewImage(object):
    """Класс, изменяющий изображения. Меняет разрешение исходного (input.jpeg), делит его на 16 частей."""
    def __init__(self, input_image="images/input.jpeg", output_image="images/output.jpeg", new_width=320, new_height=320):
        self.input_image = input_image
        self.output_image = output_image
        self.new_width = new_width
        self.new_height = new_height

        self.change_resolution()
        self.image_divider()

    def change_resolution(self):
        """Метод для изменения разрешения изображения."""
        self.image = Image.open(self.input_image).resize((self.new_width, self.new_height))
        self.image.save(self.output_image)

    def image_divider(self):
        """
        Метод делит высоту ширину изображения на 4 части, высчитывает координаты,
        с помощью image.crop обрезает изображение и сохраняет с порядковым номер (слева направо, сверху вниз).
        """
        self.width, self.height = Image.open(self.output_image).size
        part_width = self.width // 4
        part_height = self.height // 4
        part_number = 1
        for i in range(4):
            for j in range(4):
                left = j * part_width
                upper = i * part_height
                right = left + part_width
                lower = upper + part_height
                part_image = self.image.crop((left, upper, right, lower))
                part_image.save(f"{self.input_image[:-11]}/{part_number}.jpeg")
                part_number += 1


if __name__ == "__main__":
    NewImage()
