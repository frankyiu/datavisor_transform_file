Overview
--
This is a small simple tool in python3.12 for competing the datavisor offline accessment, which include 

1. Download file from SFTP
2. Transform file to output files 
3. Upload back to S3


The solution uses the pysftp package to download the desired file. If the file does not exist, the process will abort. Next, it transforms the file by looping through the User tags in the XML file using Python's default library, ElementTree, and writes the data to output files. Finally, the files are uploaded to S3 using boto3 in a multithreaded manner to avoid the uploading time becoming a bottleneck.

To Run
--
1. create .env file, you may refer to env.example
2. run `pip install -r rquirements.txt`
2. run `python main.py`


Libray
--
Main package used:
- boto3 (S3 upload)
- ElementTree (Parse XML file)
- pysftp (SFTP connection)

check requirements.txt for the full package


Assumption 
--
- Assume the aws zone is in us-east-2 as it is not mentioned in test pdf
- Assume the timezone of sftp server and local machine are same
- Assume only one valid file will be generated each day
- Assume the downloaded file data can be fitted in memory

