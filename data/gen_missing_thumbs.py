import mysql.connector
import urllib.request
from webp_util import load_webp, compress_webp
import boto3
import os
import shutil

import multiprocessing as mp

from dotenv import load_dotenv

load_dotenv()

# constants
TMP_DIR = "/tmp/stickers/"
RESIZE_SIZE = 256
FRAME_SKIP = 0
QUALITY = 10

# Create an S3 client
s3 = boto3.client('s3',
      aws_access_key_id=os.getenv("AWS_ID"),
      aws_secret_access_key=os.getenv("AWS_SECRET"),
      region_name=os.getenv("AWS_REGION"),
)

def get_db_connection():
    # Connect to the database
    return mysql.connector.connect(
               host=os.getenv("DB_HOST"),
               user=os.getenv("DB_USER"),
               password=os.getenv("DB_PASS"),
               database=os.getenv("DB_NAME")
           )


def get_stickers():
    conn = get_db_connection()
    # Create a cursor object
    cursor = conn.cursor()

    # Execute the SQL query
    cursor.execute("select sticker_url, sticker_hash from stickers where preview_url is NULL")
    rows = cursor.fetchall()

    count = len(rows)
    print(f"{count} stickers missing preview_url")

    # Close the cursor and the database connection
    cursor.close()
    conn.close()
    return rows


def set_sticker_preview(hash, url):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE stickers SET preview_url = %s WHERE sticker_hash = %s";
    data = (url, hash)
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    conn.close()



def download_webp(url, hash):
    out_path = TMP_DIR + hash + ".webp"
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, out_path)
    return out_path


def compress_sticker(url, hash):
    print("downloading", url)
    in_file = download_webp(url, hash)
    image = load_webp(in_file)

    out_file = TMP_DIR + hash + ".webp"
    print("compressing", out_file)
    compress_webp(image, out_file, FRAME_SKIP, RESIZE_SIZE, QUALITY)
    return out_file

def upload_to_s3(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)
    
    print("uploading", object_name)
    s3.upload_file(file_name, bucket, object_name)
    return f"https://{bucket}/{object_name}"



def process_row(row):
    try:
        url, hash = row
        in_file = compress_sticker(url, hash)
        s3_url = upload_to_s3(in_file, "static.desh.app", f"stickify/thumbs/{hash}.webp")
        set_sticker_preview(hash, s3_url)
        print(s3_url)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # setup tmp dir
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    mp.freeze_support()
    rows = get_stickers()
    with mp.Pool() as p:
        p.map(process_row, rows)

    # cleanup tmp TMP_DIR
    shutil.rmtree(TMP_DIR)
