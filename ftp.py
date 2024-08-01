import logging
import pysftp
import os
from datetime import datetime


class SFTPClient:
    # assume port default port
    def __init__(self, host, username, password, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port 
    
    def connect(self):
        try:
            # Get the sftp connection object
            self.connection = pysftp.Connection(
                host=self.host,
                username=self.username,
                password=self.password,
                port=self.port,
            )
            logging.info(f"Connected to {self.host} as {self.username}.")
        except Exception as e:
            logging.error(f"Unexpected error occurred : {e}")
            raise (e)

    def disconnect(self):
        self.connection.close()
        logging.info(f"Disconnected to {self.host} as {self.username}.")

    def download_today_file(self, remote_path, local_dist):
        # assume only one file
        try:
            logging.info(f"Start downloading file from {remote_path}")

            files = self.connection.listdir_attr(remote_path)
            today = datetime.today().date()

            for f in files:
                try:
                    #  change from unix time to date time
                    file_modified_time = datetime.fromtimestamp(f.st_mtime)
                    if file_modified_time.date() == today:
                        source = f'{remote_path}/{f.filename}'
                        dist = os.path.join(local_dist, f.filename)
                        self.connection.get(source, dist)
                        logging.info(f"File downloaded to {dist}")
                        return dist
                except Exception as e:
                    logging.error(f"Error in processing file {f.filename} : {e}")

            logging.warning("No files found for today")
            return None
        except IOError as e:
            logging.error(f"IO error occurred :{e}")
            raise(e)
        except Exception as e:
            logging.error(f"Unexpected error occurred :{e}")
            raise(e)



