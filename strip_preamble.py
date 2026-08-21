import os
import glob
import shutil
import re

ALLOWED_FILES = {'solution.tex'}
ALLOWED_DIRS = {'img'}

LATEX_TEMP_EXTENSIONS = {
    '.aux', '.log', '.out', '.toc', '.lof', '.lot',
    '.synctex.gz', '.synctex', '.fls', '.fdb_latexmk',
    '.xdv', '.dvi', '.bbl', '.blg', '.idx', '.ilg', '.ind'
}

def clean_solution_file(filepath, task_num):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Удаляем преамбулу (ИСПРАВЛЕНО: добавлены обратные слеши)
    if '\\begin{document}' in content:
        content = content.split('\\begin{document}', 1)[1]
    
    content = content.replace('\\end{document}', '')
    content = content.strip() + '\n'

    # 2. АВТОМАТИЧЕСКИ ИСПРАВЛЯЕМ ПУТИ К КАРТИНКАМ (с поддержкой пробелов)
    content = re.sub(r'\{\s*img/', '{problems/' + task_num + '/img/', content)
    content = re.sub(r'\[\s*img/', '[problems/' + task_num + '/img/', content)
    content = re.sub(r'\{\s*\./img/', '{problems/' + task_num + '/img/', content)
    content = re.sub(r'\[\s*\./img/', '[problems/' + task_num + '/img/', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ Очищена преамбула и исправлены пути: {filepath}")

def clean_task_folder(task_dir):
    if not os.path.isdir(task_dir):
        return
    
    for item in os.listdir(task_dir):
        item_path = os.path.join(task_dir, item)
        
        if os.path.isdir(item_path):
            if item not in ALLOWED_DIRS:
                print(f"  🗑 Удалена папка: {item_path}")
                shutil.rmtree(item_path)
            else:
                for img_file in os.listdir(item_path):
                    img_path = os.path.join(item_path, img_file)
                    if any(img_file.endswith(ext) for ext in LATEX_TEMP_EXTENSIONS):
                        print(f"  🗑 Удален временный файл: {img_path}")
                        os.remove(img_path)
        
        elif os.path.isfile(item_path):
            if item.endswith('.pdf'):
                continue
            
            if item not in ALLOWED_FILES:
                if any(item.endswith(ext) for ext in LATEX_TEMP_EXTENSIONS):
                    print(f"  🗑 Удален временный файл: {item_path}")
                    os.remove(item_path)
                elif item == '.gitkeep':
                    print(f"  🗑 Удален .gitkeep: {item_path}")
                    os.remove(item_path)
                else:
                    print(f"  🗑 Удален неизвестный файл: {item_path}")
                    os.remove(item_path)

print("🔍 Поиск папок задач...")
task_dirs = glob.glob('problems/*')

for task_dir in sorted(task_dirs):
    if os.path.isdir(task_dir):
        task_num = os.path.basename(task_dir)
        print(f"\n📁 Обработка: {task_dir} (Задача {task_num})")
        
        sol_file = os.path.join(task_dir, 'solution.tex')
        if os.path.exists(sol_file):
            clean_solution_file(sol_file, task_num)
        
        clean_task_folder(task_dir)

print("\n✅ Очистка и исправление путей завершены!")