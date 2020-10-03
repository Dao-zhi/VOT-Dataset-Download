import json
import os
import wget,tarfile,zipfile
import gc

# get home_page
def get_home_page(json_path):
    with open(json_path,'r') as json_file:
        json_data = json.load(json_file)
        home_page = json_data['homepage']
    return json_data, home_page

# read history
def read_history():
    count = 0
    if os.path.exists('history'):
        with open('history', 'r') as history_file:
            line = history_file.readline()
            count = int(line)
    else:
        count = 0
        with open('history', 'w') as history_file:
            history_file.write(str(count))
    return count

# download annotations
def download_annotations(json_data, home_page, anno_vot):
    for i,sequence in enumerate(json_data['sequences']):
        count = read_history()
        if i < count:
            continue
        print('download the {} annotation...'.format(i+1))
        # get annotations url
        annotation_url = sequence['annotations']['url']
        annotation_name = annotation_url.split('.')[0]
        name = annotation_url.split('.')[0]
        file_name = annotation_url.split('.')[0] + '.zip'
        download_annotation_url = home_page + anno_vot + '/' + annotation_url
        anno_output_name = os.path.join(destination_path,name,file_name)
        out_dir = os.path.dirname(anno_output_name)
        # creat out dir
        if os.path.exists(out_dir) == False:
            os.mkdir(out_dir)
        # annotations download and unzip and remove it
        wget.download(download_annotation_url, anno_output_name)
        print('\nunzip {} annotation...'.format(name))
        # unzip
        file_zip = zipfile.ZipFile(anno_output_name,'r')
        for file in file_zip.namelist():
            file_zip.extract(file, out_dir)
            # print('extract annotation {}/{}'.format(name,file))
        file_zip.close()
        os.remove(anno_output_name)
        print('remove annotation {}.zip!'.format(name))
        print('annotation {} Completed!\n'.format(i+1))
        write_history()
        gc.collect()

# download sequences
def download_sequences(json_data, home_page, destination_path):
    for i,sequence in enumerate(json_data['sequences']):
        count = read_history()
        if i < count:
            continue
        print('download the {} sequence...'.format(i+1))
        # get data url
        annotation_url = sequence['annotations']['url']
        data_url = sequence['channels']['color']['url'].split('../../')[-1]
        download_data_url = home_page + '/' + data_url
        name = annotation_url.split('.')[0]
        file_name = annotation_url.split('.')[0] + '.zip'
        image_output_name = destination_path + name + '/color/' + file_name
        out_dir = os.path.dirname(image_output_name)
        if os.path.exists(out_dir) == False:
            os.mkdir(out_dir)
        wget.download(download_data_url,image_output_name)
        print('\nunzip {} sequence...'.format(name))
        # unzip
        file_zip = zipfile.ZipFile(image_output_name,'r')
        for file  in file_zip.namelist():
            file_zip.extract(file,out_dir)
            # print('extract image {}'.format(file))
        file_zip.close()
        os.remove(image_output_name)
        print('remove image file {}.zip!'.format(name))
        print('sequence {} Completed!\n'.format(i+1))
        write_history()
        gc.collect()

# unzip files downloaded
def unzip_files(json_data, download_path):
    for i,sequence in enumerate(json_data['sequences']):
        count = read_history()
        if i < count:
            continue
        annotation_url = sequence['annotations']['url']
        annotation_name = annotations_url.split('.')[0]
        name = annotations_url.split('.')[0]
        file_name = annotations_url.split('.')[0] + '.zip'
        image_output_name = os.path.join(destination_path,name,'color',file_name)
        out_dir = os.path.dirname(image_output_name)
        zip_file_name = download_path + sequence['channels']['color']['uid'] + ".zip"
        file_zip = zipfile.ZipFile(zip_file_name,'r')
        print('unzip image file {}.zip...'.format(zip_file_name))
        for file in file_zip.namelist():
            file_zip.extract(file,out_dir)
            # print('extract image {}'.format(file))
        file_zip.close()
        os.remove(zip_file_name)
        print('remove image file {}.zip!'.format(name))
        print('unzip {} Completed!\n'.format(zip_file_name))
        write_history()
        gc.collect()

# Generate Download URL
def generate_download_urls(json_data, home_page):
    count = read_history()
    for i,sequence in enumerate(json_data['sequences']):
        if i < count:
            continue
        data_url = sequence['channels']['color']['url'].split('../../')[-1]
        download_data_url = home_page + '/' + data_url
        with open("DownloadURL.txt", 'a') as history_file:
            history_file.write(download_data_url + "\n")

# write history
def write_history():
    count = 0
    with open("history", 'r') as history_file:
        line = history_file.readline()
        count = int(line)
    with open("history", 'w') as history_file:
        history_file.write(str(count + 1))

if __name__ == "__main__":
    destination_path = './vot_lt2019/'    # destination path
    json_path = './description.json'      # vot 2019 json file
    anno_vot = 'vot2019/longterm'         # vot2019 or vot2018 or vot2017
    download_path = './vot_lt2019/'       # download path, use to extract downloaded file
    json_data, home_page = get_home_page(json_path)    # get json_data and home_page
    # generate_download_urls(json_data, home_page)    # Generate Download URL
    # download_annotations(json_data, home_page, anno_vot)    # download annotations
    # download_sequences(json_data, home_page, destination_path)    # download sequences
    # unzip_files(json_path, download_path)    # unzip files downloaded
    # config