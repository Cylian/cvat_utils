from cgitb import reset
from email.mime import image
from libs.version import __version__, __author__, __company__
from libs.style import style
import os
import hashlib
import json
from PIL import Image
from pathlib import Path

extenstions = ['.jpg','jpeg','png']
version_string = {"version":"1.1"}
meta_string = {"type":"images"}

def main_():
    os.system("CVAT Manifest Creator v." + __version__ + " by " + __author__ + " [" + __company__ + "]")
    os.system("cls")
    input_dir = input(style.YELLOW + "Enter input path: " + style.CYAN)
    if os.path.isdir(input_dir):
        dirs = fast_scandir(input_dir)
        if len(dirs) == 0:
            dirs = [input_dir]
        for dir_path in dirs:
            sub_dirs = fast_scandir(dir_path)
            if len(sub_dirs) == 0:
                save_path = input_dir.split(os.sep)[-1] + ".jsonl"
                create_manifest(input_dir, dir_path, save_path)
            else:
                for sub_dir_path in sub_dirs:
                    print(sub_dir_path)
                    save_path = dir_path.split(os.sep)[-1] + " - " + sub_dir_path.split(os.sep)[-1] + ".jsonl"
                    create_manifest(input_dir, sub_dir_path, save_path)


def main():
    os.system(
        "CVAT Manifest Creator v."
        + __version__
        + " by "
        + __author__
        + " ["
        + __company__
        + "]"
    )
    os.system("cls")
    input_dir = input(style.YELLOW + "Enter input path: " + style.CYAN)
    if os.path.isdir(input_dir):
        root_dir = str(Path(input_dir).parent.absolute())
        save_path = root_dir + os.sep + input_dir.split(os.sep)[-1] + ".jsonl"
         #print(root_dir)
         #print(save_path)
        create_manifest(root_dir, input_dir, save_path)


def create_manifest(root_dir, dir_path, save_path):
    manifest_file = open(save_path, "w")
    manifest_file.write(json.dumps(version_string))
    manifest_file.write('\n')
    manifest_file.write(json.dumps(meta_string))
    manifest_file.write('\n')
    list_of_files = get_files(dir_path, extenstions)
    total_files = len(list_of_files)
    #dir_name = dir_path.replace(root_dir, "").replace('\\', '/').strip('/')
    file_counter = 0
    if total_files > 0:
        list_of_lines = []
        for file_path in list_of_files:
            file_ext = '.' + file_path.split(os.sep)[-1].split('.')[1]
            file_name_part = file_path.replace(root_dir, "").replace(os.sep, '/').strip(file_ext).strip('/')
            file_counter+=1
            print(style.GREEN + str(file_counter) + style.WHITE + "/" + style.RED + str(total_files) + style.WHITE + " --> \t --> " + style.CYAN + file_path + style.RESET)
            img = Image.open(file_path)
            checksum_text = hashlib.md5(img.tobytes()).hexdigest()
            #print(style.GREEN + "\t\t--->" + checksum_text + style)
            name_value = file_name_part
            list_of_lines.append(json.dumps({"name":name_value,"extension":file_ext,"width":img.width,"height":img.height,"meta":{"related_images":[]},"checksum":checksum_text}) + '\n')
            img.close()
        manifest_file.writelines(list_of_lines)
    else:
        print(style.RED + "No files found..." + style.UNDERLINE + dir_path + style.RESET)


def main_old():
    os.system("")
    os.system("CVAT Manifest Creator v." + __version__ + " by " + __author__ + " [" + __company__ + "]")
    os.system("cls")
    input_dir = input(style.YELLOW + "Enter input path: " + style.CYAN)
    if os.path.isdir(input_dir):
        #dirs = fast_scandir(input_dir)
        #if len(dirs) == 0:
        #    dirs = [input_dir]
        dirs = [input_dir]
        manifest_file = open("manifest.jsonl", 'w')
        manifest_file.write(json.dumps(version_string))
        manifest_file.write('\n')
        manifest_file.write(json.dumps(meta_string))
        manifest_file.write('\n')
        for dir_path in dirs:
            #dir_name = dir_path.split(os.sep)[-1] # last part
            dir_name = dir_path
            print('Processing -->"' + dir_name + '"')
            #manifest_file = open(dir_name.replace(' ', "") + ".jsonl", 'w')
            list_of_lines = []
            list_of_files = get_files(dir_path, extenstions)
            total_files = len(list_of_files)
            file_counter = 0
            if total_files > 0:
                for file_name in list_of_files:
                    file_name_part_with_ext = file_name#.split(os.sep)[-1]
                    file_name_part = file_name_part_with_ext#.split('.')[0]
                    file_ext_part = '.' + file_name.split('.')[1]
                    file_counter+=1
                    print(style.GREEN + str(file_counter) + style.WHITE + "/" + style.RED + str(total_files) + style.WHITE + " --> \t --> " + style.CYAN + file_name + style.RESET)
                    img = Image.open(file_name)
                    checksum_text = hashlib.md5(img.tobytes()).hexdigest()
                    #print(style.GREEN + "\t\t--->" + checksum_text + style)
                    name_value = dir_name + "/" + file_name_part
                    list_of_lines.append(json.dumps({"name":name_value,"extension":file_ext_part,"width":img.width,"height":img.height,"meta":{"related_images":[]},"checksum":checksum_text}) + '\n')
                    img.close()
                manifest_file.writelines(list_of_lines)
            else:
                print(style.RED + "No files found..." + style.UNDERLINE + dir_path + style.RESET)

def get_files(dirname, exts):
    files = []
    for root, dirnames, filenames in os.walk(dirname):
        for file in filenames:
            fname, fext = os.path.splitext(file)
            #print (fext)
            #print (exts)
            #if fext in exts:
            files.append(os.path.join(root, file))
    return files

def fast_scandir(dirname, recursive=False):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    if recursive==True:
        for dirname in list(subfolders):
            subfolders.extend(fast_scandir(dirname))
    return subfolders

if __name__ == "__main__":
    main()
