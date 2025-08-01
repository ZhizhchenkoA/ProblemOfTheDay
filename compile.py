import re
import argparse


def get_information(num):
    with open(f"problems/{num}/main.tex") as f:
        text = f.read()
        text = re.findall(r"(?<=\\begin{document})(.*?)(?=\\end{document})", text, re.DOTALL)[0]
        images = re.findall(r"{img/.*}", text)
    return text, images
        
def replace_image_path(text, images, num):
    for i in images:
        text = text.replace(i, i[0] + f"problems/{num}/{i[1::]}")
    return text

def write_num_tex(text, num):
    with open(f"problems/{num}/{num}.tex", "w") as f:
        f.write(text)
    return

def create_tex(num):
    text, images = get_information(num)
    text = replace_image_path(text, images, num)
    write_num_tex(text, num)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Компиляция полного проекта")
    parser.add_argument("number", type=int, default=0, help="Номер задачи")
    args = parser.parse_args()

    if args.number != 0:
        create_tex(args.number)