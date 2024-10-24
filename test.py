import os
lst = sorted(range(1120, -1, -32))
# print(lst,", Length: ", len(lst))
# https://hisab360.com/220009/220009_media/alumni/A_1727001974_2024-09-22.jpg
txt = int("1720669157")
result = txt - 8045926
print(result)
print(lst)


#! Total Numbers of file including subfolders:
def count_files_in_folder(folder_path):
    return sum(len(files) for root, dirs, files in os.walk(folder_path))

# folder_path = "./CPVP/IMAGES"
folder_path = "E:/"
print(f"Total number of files including subfolders: {count_files_in_folder(folder_path)}")

#! Total Numbers of file excluding subfolders:
def count_files_in_folder(folder_path):
    return sum(bool(os.path.isfile(os.path.join(folder_path, item)))
           for item in os.listdir(folder_path))

print(
    f"Total number of files excluding subfolders: {count_files_in_folder(folder_path)} | {bool(count_files_in_folder(folder_path))}"
)

# for i in range(len(lst)):
#     x = len(lst) -1
#     s = lst[x] - 32*i
#     print(s)