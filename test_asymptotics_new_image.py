import timeit


def test_change_resolution_asymptotics():
    """Функция тестирование асимптотики класса NewImage."""
    setup_code = """
from img import NewImage
new_image = NewImage(input_image="images/test1.jpeg", new_width=320, new_height=320, output_image="images/test2.jpeg")
"""

    test_code = """
new_image.change_resolution()
"""

    print(f"100 итераций вызова класса NewImage заняло: {timeit.timeit(test_code, setup=setup_code, number=100)} секунд")


if __name__ == "__main__":
    test_change_resolution_asymptotics()
