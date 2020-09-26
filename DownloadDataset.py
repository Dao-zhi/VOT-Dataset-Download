import json
import os
import wget,tarfile,zipfile
 
destination_path = './vot_lt2019/'    # destination path
json_path = './description.json'      # vot 2019 json file
anno_vot = 'vot2019/longterm'                  # vot2019 or vot2018 or vot2017
 
 
with open(json_path,'r') as json_file:
    json_data = json.load(json_file)
home_page = json_data['homepage']
 
for i,sequence in enumerate(json_data['sequences']):
    print('download the {} sequences'.format(i+1))

    # get annotations_url and data_url
    annotations_url = sequence['annotations']['url']
    data_url = sequence['channels']['color']['url'].split('../../')[-1]
 
    # get name from  annotations_url and construct file_name
    name = annotations_url.split('.')[0]
    file_name = annotations_url.split('.')[0] + '.zip'
 
    # construct annotations download url and data download url
    download_annotations_url = home_page + anno_vot + '/' + annotations_url
    download_data_url = home_page + '/' + data_url

    # construct annotations path and data path
    image_output_name = os.path.join(destination_path,name,'color',file_name)
    anno_output_name = os.path.join(destination_path,name,file_name)
    out_dir = os.path.dirname(anno_output_name)
    if os.path.exists(out_dir) == False:
        os.mkdir(out_dir)
 
    # annotations download and unzip and remove it
    wget.download(download_annotations_url, anno_output_name)
    print('loading {} annotation'.format(name))
    # unzip
    file_zip = zipfile.ZipFile(anno_output_name,'r')
    for file in file_zip.namelist():
        file_zip.extract(file, out_dir)
        print('extract annotation {}/{}'.format(name,file))
    file_zip.close()
    os.remove(anno_output_name)
    print('remove annotation {}.zip'.format(name))
 
    # image download and unzip and remove it
    out_dir = os.path.dirname(image_output_name)
    if os.path.exists(out_dir) == False:
        os.mkdir(out_dir)
    wget.download(download_data_url,image_output_name)
    print('loading {} sequence'.format(name))
    # unzip
    file_zip = zipfile.ZipFile(image_output_name,'r')
    for file  in file_zip.namelist():
        file_zip.extract(file,out_dir)
        print('extract image {}'.format(file))
    file_zip.close()
    os.remove(image_output_name)
    print('remove image file {}.zip'.format(name))

    # download completed
    print('sequence  {} Completed!'.format(i+1))