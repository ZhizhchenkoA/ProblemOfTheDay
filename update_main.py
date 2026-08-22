import os
import re

def update_main_tex():
    main_file = 'main.tex'
    problems_dir = 'problems'
    
    if not os.path.exists(main_file):
        print("❌ Файл main.tex не найден!")
        return
    
    if not os.path.exists(problems_dir):
        print("❌ Папка problems не найдена!")
        return
    
    # Читаем текущий main.tex
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Находим все папки с задачами
    task_numbers = []
    for item in sorted(os.listdir(problems_dir)):
        task_dir = os.path.join(problems_dir, item)
        if os.path.isdir(task_dir):
            sol_file = os.path.join(task_dir, 'solution.tex')
            if os.path.exists(sol_file):
                task_numbers.append(item)
    
    print(f"📁 Найдено задач в папке problems/: {len(task_numbers)}")
    
    # Ищем все существующие блоки задач в main.tex
    # ВАЖНО: Регулярка обновлена, чтобы находить и удалять старые \clearpage
    task_pattern = re.compile(
        r'(?:\\clearpage\s*\n)?(?:\\section\{Задача\s+\d+\}\s*\n)?\\input\{problems/\d+/solution\.tex\}\s*\n?',
        re.MULTILINE
    )
    
    existing_tasks = set()
    for match in task_pattern.finditer(content):
        task_num_match = re.search(r'\\input\{problems/(\d+)/solution\.tex\}', match.group(0))
        if task_num_match:
            existing_tasks.add(task_num_match.group(1))
    
    print(f"📄 Найдено задач в main.tex: {len(existing_tasks)}")
    
    # Удаляем все существующие блоки задач из main.tex
    content_cleaned = task_pattern.sub('', content)
    
    # Находим место для вставки задач
    marker_pattern = re.compile(r'%\s*=+\s*\n%\s*ЗДЕСЬ БОТ.*\n%\s*=+\s*\n')
    marker_match = marker_pattern.search(content_cleaned)
    
    if marker_match:
        insert_pos = marker_match.end()
        print("🎯 Найден маркер для вставки задач")
    else:
        end_doc_match = re.search(r'\\end\{document\}', content_cleaned)
        if not end_doc_match:
            print("❌ Не найден \\end{document} в main.tex!")
            return
        insert_pos = end_doc_match.start()
        print("⚠️ Маркер не найден, вставляем перед \\end{document}")
    
    # Формируем новый блок задач в правильном порядке
    tasks_content = ""
    for task_num in task_numbers:
        # ДОБАВЛЯЕМ \clearpage, чтобы каждая задача была с новой страницы
        # Если вам нужна просто новая строка (абзац) на той же странице, 
        # замените \\clearpage на \\par
        tasks_content += f"\\clearpage\n\\input{{problems/{task_num}/solution.tex}}\n"
    
    # Собираем новый контент
    new_content = content_cleaned[:insert_pos] + tasks_content + content_cleaned[insert_pos:]
    
    # Записываем обратно
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # Статистика изменений
    added = set(task_numbers) - existing_tasks
    removed = existing_tasks - set(task_numbers)
    
    if added:
        print(f"✅ Добавлено {len(added)} новых задач: {', '.join(sorted(added))}")
    if removed:
        print(f"🗑 Удалено {len(removed)} задач (нет в папке problems/): {', '.join(sorted(removed))}")
    if not added and not removed:
        print("✓ Список задач не изменился")
    
    print(f"📊 Итого задач в книге: {len(task_numbers)}")

if __name__ == "__main__":
    update_main_tex()