import os
import subprocess
import shutil

PREAMBLE = r"""\documentclass[12pt,a4paper]{article}
\usepackage{DayProblem}
\begin{document}
"""
POSTAMBLE = r"\end{document}"

for folder in sorted(os.listdir('problems')):
    sol_path = os.path.join('problems', folder, 'solution.tex')
    if os.path.isfile(sol_path):
        with open('temp_compile.tex', 'w', encoding='utf-8') as f:
            f.write(PREAMBLE)
            f.write(f"\\input{{problems/{folder}/solution.tex}}\n")
            f.write(POSTAMBLE)
        
        subprocess.run(['pdflatex', '-interaction=nonstopmode', 'temp_compile.tex'], 
                       cwd=os.getcwd(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists('temp_compile.pdf'):
            # Сохраняем PDF прямо в папку задачи
            dest = os.path.join('problems', folder, f'problem_{folder}.pdf')
            shutil.copy('temp_compile.pdf', dest)
            print(f"✅ Скомпилировано: {dest}")
            
for f in ['temp_compile.tex', 'temp_compile.aux', 'temp_compile.log']:
    if os.path.exists(f): os.remove(f)