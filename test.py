import os
# lst = [32,64,96,128,160,192,224,1120]
lst = []

x = 1120
while x >= 0:
    lst.append(x)
    x -= 32

lst.sort()
# print(lst,", Length: ", len(lst))
# https://hisab360.com/220009/220009_media/alumni/A_1727001974_2024-09-22.jpg
txt = int("1720669157")
result = txt - 8045926
print(result)


#! Total Numbers of file including subfolders:
def count_files_in_folder(folder_path):
    total_files = 0
    for root, dirs, files in os.walk(folder_path):
        total_files += len(files)
    return total_files

folder_path = "./CPVP"
print(f"Total number of files including subfolders: {count_files_in_folder(folder_path)}")

#! Total Numbers of file excluding subfolders:
def count_files_in_folder(folder_path):
    total_files = 0
    for item in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, item)):
            total_files += 1
    return total_files

print(f"Total number of files excluding subfolders: {count_files_in_folder(folder_path)}")

# for i in range(len(lst)):
#     x = len(lst) -1
#     s = lst[x] - 32*i
#     print(s)