import os
import sys
import subprocess

PREAMBLE = r"""\documentclass[12pt,a4paper]{article}
\usepackage{DayProblem}
\begin{document}
"""
POSTAMBLE = r"\end{document}"

def compile_task(task_number):
    task_dir = f"problems/{task_number}"
    sol_file = os.path.join(task_dir, "solution.tex")
    temp_file = "temp_compile.tex"
    
    if not os.path.exists(sol_file):
        print(f"Ошибка: Файл {sol_file} не найден!")
        return

    with open(sol_file, 'r', encoding='utf-8') as f:
        content = f.read()

    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(PREAMBLE)
        f.write(content)
        f.write(POSTAMBLE)

    print(f"Компиляция задачи {task_number}...")
    
    for _ in range(2):
        subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', temp_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    output_pdf = os.path.join(task_dir, f"problem_{task_number}.pdf")
    if os.path.exists("temp_compile.pdf"):
        os.rename("temp_compile.pdf", output_pdf)
        print(f"✅ Успешно! PDF сохранен как: {output_pdf}")
    else:
        print("❌ Ошибка компиляции. Проверьте код в solution.tex")

    for ext in ['.tex', '.aux', '.log', '.out']:
        temp_path = f"temp_compile{ext}"
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python local_build.py <номер_задачи>")
        print("Пример: python local_build.py 001")
    else:
        compile_task(sys.argv[1])