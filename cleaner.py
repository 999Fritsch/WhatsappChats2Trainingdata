import os

def process_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    processed_lines = []
    current_message = ""

    for line in lines:
        if line.startswith("["):
            if current_message:
                processed_lines.append(current_message.strip().replace('\n', ' '))
                current_message = ""
            processed_lines.append(line.strip())
            
        else:
            if processed_lines.__len__() > 0:
                    processed_lines[-1] = processed_lines[-1] +". "+ line.strip().replace('\n', ' ')

    if current_message:
        processed_lines.append(current_message.strip().replace('\n', ' '))

    with open(file_path, 'w', encoding='utf-8') as file:
        for line in processed_lines:
            file.write(line + '\n')

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                process_text_file(file_path)

def clean_file(file_path):
    lines_to_remove = [
        "Your security code with",
        "Messages and calls are end-to-end encrypted.",
        "created this group",
        "changed their phone number to a new number",
        "sticker omitted",
        "image omitted",
        "audio omitted",
        "video omitted"
    ]
    with open(file_path, 'r') as file:
        lines = file.readlines()

    cleaned_lines = []
    removed = 0
    for line in lines:
        if not any(pattern in line for pattern in lines_to_remove):
            cleaned_lines.append(line)
        else:
            removed += 1

    with open(file_path, 'w') as file:
        file.writelines(cleaned_lines)

    print(f"{file_path} removed: {removed}")


def clean_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                clean_file(file_path)


if __name__ == "__main__":

    folder_path = "chats"
    clean_folder(folder_path)
    process_folder(folder_path)