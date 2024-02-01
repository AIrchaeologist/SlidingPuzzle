import unittest
import os
from PIL import Image
from img import NewImage


class TestNewImage(unittest.TestCase):
    """Тестовый класс, наследуется от unittest.TestCase."""
    def setUp(self):
        """Метод для создания тестового изображения."""
        Image.new("RGB", (500, 500), color="white").save("unittest_images/input.jpeg")

    def tearDown(self):
        """Метод для удаления тестовых изображений."""
        os.remove("unittest_images/input.jpeg")
        os.remove("unittest_images/output.jpeg")
        for i in range(1, 17):
            os.remove(f"unittest_images/{i}.jpeg")

    def test_change_resolution(self):
        """Тест, проверяющий соответствие разрешения после изменения."""
        NewImage(input_image="unittest_images/input.jpeg", output_image="unittest_images/output.jpeg")
        resized_image = Image.open("unittest_images/output.jpeg")
        self.assertEqual(resized_image.size, (320, 320))

    def test_image_divider(self):
        """Тест, проверяющий соответствие размер после обрезки (80x80)."""
        NewImage(input_image="unittest_images/input.jpeg", output_image="unittest_images/output.jpeg")
        for i in range(1, 17):
            part_image = Image.open(f"unittest_images/{i}.jpeg")
            self.assertEqual(part_image.size, (80, 80))


if __name__ == "__main__":
    unittest.main()
