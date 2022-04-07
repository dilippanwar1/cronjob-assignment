import boto3
from botocore.exceptions import ClientError
import time
import os
import logging
import sys
from pathlib import Path

bucket = os.environ["ENV"]+'-dilip-panwar-platform-challenge'
ACCESS_KEY_ID = os.environ["ACCESS_KEY_ID"]
SECRET_ACCESS_KEY = os.environ["SECRET_ACCESS_KEY"]
HOME_DIR = os.environ["HOME"]
def create_cred():

    """
    Create credentials file from credential.tmpl to authenticate with AWS.
    :return: Nothing
    """
    
    ACCESS_KEY_ID_PLACEHOLDER = "<ACCESS_KEY_ID_PLACEHOLDER>"
    SECRET_ACCESS_KEY_PLACEHOLDER = "<SECRET_ACCESS_KEY_PLACEHOLDER>"
    #ACCESS_KEY_ID = sys.argv[2]
    #SECRET_ACCESS_KEY = sys.argv[3]
    
    os.chdir(HOME_DIR)
    credential_file = Path('.aws/credentials')
    if credential_file.is_file():
        print("aws credentials file already exist.")
        return 
            
    with open('.aws/credentials', 'w+') as credf:
        with open('.aws/credential.tmpl', 'r') as f:
            new_line = ''
            for line in f:
                if "<ACCESS_KEY_ID_PLACEHOLDER>" in line:
                    new_line = line.replace("<ACCESS_KEY_ID_PLACEHOLDER>", ACCESS_KEY_ID)
                elif "<SECRET_ACCESS_KEY_PLACEHOLDER>" in line:
                    new_line = line.replace("<SECRET_ACCESS_KEY_PLACEHOLDER>", SECRET_ACCESS_KEY)
                else:
                    new_line = line
                credf.write(new_line)


def upload_file(object_name=None):

    """
    Upload a file to an S3 bucket
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    fname_suffix = "zenjob-challenge"
    file_name = time.strftime("%Y%m%d-%H%M%S")+"_"+fname_suffix
    os.chdir(HOME_DIR)
    with open(f'{file_name}', 'w') as fp:
        pass
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        #Delete file from OS after uploading to S3 
        os.remove(file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def delete_objects():

    """
    :return: Does not return anything
    This method will delete the objects from S3 from a given bucket.
    This method is able to delete the multiple files in a single go if required

    """
    s3_conn = boto3.client('s3')
    day_in_secs = 86400
    objects_to_delete = []
    for file in s3_conn.list_objects(Bucket=bucket)['Contents']:
        file_name = file['Key']
        file_time_prefix = file['Key'].split('_')[0]
        file_time = time.mktime(time.strptime(file_time_prefix, "%Y%m%d-%H%M%S"))
        current_time = time.time()
        file_age = int(current_time - file_time)
        print(f'Age of File: {file_name} is {int(file_age/60)}mins')
        if file_age > day_in_secs:
            objects_to_delete.append({'Key':file_name})
    
    if len(objects_to_delete):
        s3 = boto3.resource('s3')
        print(f'Deleting files older than 24h. File names: {objects_to_delete}')
        s3.meta.client.delete_objects(Bucket=bucket, Delete={'Objects': objects_to_delete})
    else:
        print('No file found older than 24hrs for deletion')

create_cred()
upload_file()
delete_objects()    
