from datetime import datetime
import json
import logging
import os
import threading
from config import ABOVE_FILE_NAME, AWS_BUCKET_NAME, AWS_REGION, BELOW_FILE_NAME, FTP_FOLDER, FTP_HOST, FTP_PASSWORD, FTP_USERNAME
from ftp import SFTPClient
import xml.etree.ElementTree as ET
from s3 import S3Client


def convert_to_iso8601(time):
    dt = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
    return dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')

def transform(download_file, above_file_path, below_file_path):
    logging.info("Start transforming downloaded file")
    tree = ET.parse(download_file)
    root = tree.getroot()
    total = 0
    users = []
    for user in root.findall('User'):
        try: 
            user_data = {
                "UserID": user.find('UserID').text,
                "UserName": user.find('UserName').text,
                "UserAge": int(user.find('UserAge').text),
                "EventTime": convert_to_iso8601(user.find('EventTime').text),
            }
            total += user_data['UserAge']
            users.append(user_data)
        except Exception as e:
            logging.error(f"Error in processing user data and continue: {e}")
            continue 
    if len(users) == 0:
        logging.warn("There is no user record, abort following action")
        return []

    avg = total // len(users)
    above = [user for user in users if user['UserAge'] > avg]
    below = [user for user in users if user['UserAge'] <= avg]

    with open(above_file_path, 'w') as above_file:
        for user in above:
            json.dump(user, above_file)
            above_file.write('\n')

    with open(below_file_path, 'w') as below_file:
        for user in below:
            json.dump(user, below_file)
            below_file.write('\n')

    return [above_file_path, below_file_path]


if __name__ == "__main__":
    try:
        folder_needed = ['upload', 'download']
        for folder in folder_needed:
            if not os.path.exists(folder):
                os.makedirs(folder)

        # step 1 : download via ftp
        ftp_client = SFTPClient(host=FTP_HOST, username=FTP_USERNAME, password=FTP_PASSWORD)
        ftp_client.connect()
        download_file = ftp_client.download_today_file(FTP_FOLDER, 'download')
        ftp_client.disconnect()

        if not download_file:
            exit() 
        # step2 : transform file
        above_file_path = os.path.join('upload', ABOVE_FILE_NAME);
        below_file_path = os.path.join('upload', BELOW_FILE_NAME);
        output_files = transform(download_file, above_file_path, below_file_path)

        # step3 : upload to s3 if there is record
        if output_files:
            s3_client = S3Client(region_name=AWS_REGION, bucket_name=AWS_BUCKET_NAME)
            threads = []
            for file_path, s3_file_name in zip(output_files, [ABOVE_FILE_NAME, BELOW_FILE_NAME]):
                s3_path = f'output/{s3_file_name}'
                thread = threading.Thread(target=s3_client.upload_file, args=(file_path, s3_path))
                thread.start()
                threads.append(thread)
            
            for thread in threads:
                thread.join()
    except Exception as e:
        logging.error(e)
        




