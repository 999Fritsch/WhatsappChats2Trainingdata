import os
from zipfile import ZipFile
import unicodedata

def clean_unicode(text):
    cleaned_text = ""
    for char in text:
        if unicodedata.category(char)[0] != 'C' or char.isspace():
            cleaned_text += char
    return cleaned_text

def clean_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    cleaned_text = clean_unicode(text)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

def clean_all():
    for file in os.listdir("chats"):
        if file.endswith(".txt"):
            clean_file(f"chats/{file}")

def unzip_file(path):
    contact_name = path.replace("chats/", "").replace("WhatsApp Chat - ", "").replace(".zip", "")
    path_to_newtext = f"chats/{contact_name}.txt"
    with ZipFile("chats/"+path, "r") as zipfile:
        zipfile.extractall()
    os.rename("_chat.txt", path_to_newtext)
    os.remove("chats/"+path)
    return path_to_newtext

def unzip_all():
    new_folders = []
    for file in os.listdir("chats"):
        if file.endswith(".zip"):
            new_folders.append(unzip_file(file))
    print(new_folders)

if __name__ == "__main__":
    unzip_all()
    clean_all()