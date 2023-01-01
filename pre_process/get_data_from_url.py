import os
import requests
##======================================================##
'''Downloading data from URL'''
##======================================================##
def download_data(file_list, dest_folder):
    dest_folder = dest_folder
    if not os.path.exists(dest_folder):
           os.makedirs(dest_folder)  # create folder if it does not exist

    for file in file_list:
        dest_file = file.split('/')[-1].replace(" ", "_")
        dest_path = os.path.join(dest_folder, dest_file)
        response  = requests.get(file, stream=True)

        if response.ok:
            print("saving to", os.path.abspath(dest_path))
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024 * 8):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())
        else:  # HTTP status code 4XX/5XX
            print("Download failed: status code {}\n{}".format(response.status_code, response.text))

    return print('downloaded to folder', dest_folder)
