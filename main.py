import csv
import hashlib
import os


root_folder = './Cautare'
output_file = 'duplicates.csv'


def list_files(root_folder: str) -> dict[str, list[str]]:
    file_list = []
    for dir_path, _, filenames in os.walk(root_folder):
        for filename in filenames:
            file_list.append(os.path.join(dir_path, filename))
    return file_list


def get_file_fingerprint(filename):
    with open(filename, 'rb') as f:
        file_contents = f.read()
        return hashlib.md5(file_contents).hexdigest()


def find_duplicate_files(file_list):
    duplicates = {}
    for filename in file_list:
        fingerprint = get_file_fingerprint(filename)
        if fingerprint in duplicates:
            duplicates[fingerprint].append(filename)
        else:
            duplicates[fingerprint] = [filename]
    return duplicates


def save_duplicate_files(duplicates, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        for fingerprint, filenames in duplicates.items():
            writer.writerow([fingerprint])
            for i, filename in enumerate(filenames, start=1):
                writer.writerow([i, filename])


def duplicate_file_stat(duplicate):
    for _, filenames in duplicate.items():
        for filename in filenames[1:]:
            file_size = os.path.getsize(filename)
            print(round(file_size) / 1024)
            print(filenames)


file_list = list_files(root_folder)
duplicates = find_duplicate_files(file_list)
save_duplicate_files(duplicates, output_file)
duplicate_file_stat(duplicates)
