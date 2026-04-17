import os 
import shutil
from datetime import datetime
import hashlib



## Stats Tracker
stats = {"total_files":0,"moved":0,"duplicates":0}




## Scans files only and generate info for each file
def scan_files(folder_path):
    files_data = []
    for file in os.listdir(folder_path):
        full_path = os.path.join(folder_path,file)
        if os.path.isfile(full_path):
            file_info = {"name": file,"path": full_path,
                         "size":os.path.getsize(full_path),
                         "extension": file.split(".")[-1].lower() if "." in file else ""}
            files_data.append(file_info)
    stats["total_files"] = len(files_data)
    return files_data




## Creating function which distinguish file based on extensions
def classify_file(extension):
    if extension in ["jpg","jpeg","png","gif","webp","svg","heic","heif","avif"]:
        return "Images"
    elif extension in ["mp4","mkv","avi","mov","webm","flv","wmv"]:
        return "Videos"
    elif extension in ["pdf","docx","txt","xlsx","pptx","doc","xml","csv"]:
        return "Documents"
    else:
        return "Others"



## Prints name and category of each file
# for i in all_files:
#     category = classify_file(i["extension"])
#     print(f"{i['name']} -> {category}")



## Creates folders automatically
def create_folders(base_path):
    folders = ["Images","Videos","Documents","Others"]
    for i in folders:
        folder_path = os.path.join(base_path, i)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)




## Function which renames the file
def gen_new_name(file_name, category, count):
    extension = file_name.split(".")[-1]
    today = datetime.now().strftime("%Y-%m-%d")
    if category == "Images":
        return f"image_{today}_{count}.{extension}"
    elif category == "Videos":
        return f"video_{count}.{extension}"
    elif category == "Documents":
        return f"document_{today}_{count}.{extension}"
    else:
        return file_name
    




## Move Files in the folders respectively
def move_files(all_files,base_path):
    counters = {"Images": 1,"Videos":1,"Documents":1,"Others":1}
    for i in all_files:
        category = classify_file(i["extension"])
        destiny_folder = os.path.join(base_path,category)
        new_name = gen_new_name(i["name"],category,counters[category])
        destiny_path = os.path.join(destiny_folder,i["name"])
        if not os.path.exists(destiny_path):
            shutil.move(i["path"],destiny_path)
            print(f"Moved & Renamed: {i['name']} -> {new_name}")
        else:
            print(f"Skipped (already exists): {new_name}")
    stats["moved"] += 1



def get_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path,"rb") as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()



def find_duplicates(all_files):
    hash_map = {}
    duplicates = []
    for i in all_files:
        file_hash = get_hash(i["path"])
        if file_hash in hash_map:
            duplicates.append(i)
        else:
            hash_map[file_hash] = i
    stats["duplicates"] = len(duplicates)
    return duplicates



def move_duplicates(duplicates,base_path):
    trash_folder = os.path.join(base_path,"Trash")
    if not os.path.exists(trash_folder):
        os.makedirs(trash_folder)
    for i in duplicates:
        destination = os.path.join(trash_folder,i["name"])
        if not os.path.exists(destination):
            shutil.move(i["path"],destination)
            print(f"Duplicates moved to Trash: {i['name']}")
        else:
            print(f"Duplicates skipped (name exists): {i['name']}")


def show_summary():
    print("\n===== SUMMARY =====")
    print(f"Total Files Scanned: {stats['total_files']}")
    print(f"Files Moved: {stats['moved']}")
    print(f"Duplicates Found: {stats['duplicates']}")


