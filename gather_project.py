import os

# Папки и файлы, которые нужно игнорировать (чтобы избежать мусора)
IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', '.idea', '.vscode', 'build', 'dist'}
IGNORE_FILES = {'project_full_files_info.txt', 'gather_project.py', '.DS_Store', 'package-lock.json'}

# Текстовые и программные расширения, которые стоит читать
VALID_EXTENSIONS = {
    '.txt', '.py', '.js', '.ts', '.html', '.css', '.json', '.md', 
    '.cpp', '.h', '.cs', '.java', '.go', '.rs', '.php', '.yaml', '.yml'
}

def generate_tree(dir_path, prefix=""):
    """Рекурсивно строит дерево проекта в виде списка строк."""
    tree_lines = []
    try:
        items = sorted(os.listdir(dir_path))
    except PermissionError:
        return []

    # Фильтруем элементы
    items = [item for item in items if item not in IGNORE_DIRS and item not in IGNORE_FILES]
    
    for i, item in enumerate(items):
        is_last = (i == len(items) - 1)
        connector = "└── " if is_last else "├── "
        full_path = os.path.join(dir_path, item)
        
        tree_lines.append(f"{prefix}{connector}{item}")
        
        if os.path.isdir(full_path):
            extension_prefix = "    " if is_last else "│   "
            tree_lines.extend(generate_tree(full_path, prefix + extension_prefix))
            
    return tree_lines

def collect_files_content(root_dir, output_file):
    """Обходит проект, генерирует дерево и записывает содержимое файлов."""
    with open(output_file, 'w', encoding='utf-8') as out:
        # 1. Записываем заголовок и дерево проекта
        out.write("==================================================\n")
        out.write("СТРУКТУРА ПРОЕКТА\n")
        out.write("==================================================\n")
        out.write(os.path.basename(os.path.abspath(root_dir)) + "\n")
        
        tree_lines = generate_tree(root_dir)
        out.write("\n".join(tree_lines) + "\n\n")
        
        # 2. Обходим файлы и записываем их содержимое
        out.write("==================================================\n")
        out.write("СОДЕРЖИМОЕ ФАЙЛОВ\n")
        out.write("==================================================\n\n")
        
        for root, dirs, files in os.walk(root_dir):
            # Исключаем ненужные папки на лету
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in sorted(files):
                if file in IGNORE_FILES:
                    continue
                
                # Проверяем расширение файла
                _, ext = os.path.splitext(file)
                if ext.lower() not in VALID_EXTENSIONS:
                    continue
                    
                full_path = os.path.join(root, file)
                # Получаем относительный путь для красивого отображения в заголовке
                rel_path = os.path.relpath(full_path, root_dir)
                
                out.write(f"--- НАЧАЛО ФАЙЛА: {rel_path} ---\n")
                
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                        out.write(content)
                except Exception as e:
                    out.write(f"[Ошибка чтения файла: {e}]\n")
                
                out.write(f"\n--- КОНЕЦ ФАЙЛА: {rel_path} ---\n\n")

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    output_name = "project_full_files_info.txt"
    
    print("Сканирование проекта и сборка данных...")
    collect_files_content(project_root, output_name)
    print(f"Готово! Данные успешно сохранены в файл: {output_name}")
