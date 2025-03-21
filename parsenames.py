import os
import requests
import zipfile

NAME_MIN_LENGTH = 3
NAME_MIN_FREQ = 10
DATA_URL = 'https://www.ssa.gov/oact/babynames/names.zip'
DATA_DIR = 'names'
ZIP_FILE = 'names.zip'

def get_folder_files(folder, extension):
    return [os.path.join(folder,f) for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder,f)) and f.endswith(extension)]

def download_and_extract_data(url, zip_file, extract_to):
    response = requests.get(url)
    with open(zip_file, 'wb') as f:
        f.write(response.content)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

print('starting...')
clear_directory(DATA_DIR)
os.remove(ZIP_FILE) if os.path.exists(ZIP_FILE) else None
download_and_extract_data(DATA_URL, ZIP_FILE, DATA_DIR)

names_set = set()
filenames = get_folder_files(DATA_DIR, '.txt')
for fn in filenames:
    with open(fn) as f:
        data = [line.split(',') for line in f]
        names = [d[0] for d in data if int(d[2])>NAME_MIN_FREQ] # min frencuency filter
        names = [n for n in names if len(n)>NAME_MIN_LENGTH] # name length filter
        names_set.update(names)

print(len(names_set), 'unique names')
with open('names-dataset.txt', 'w+') as f:
    f.write('\n'.join(names_set).lower() + '\n')
print('file written')
print('...finished')
