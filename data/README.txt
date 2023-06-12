# Install

Install packages from ./requirements.txt

```
pip install -r ./requirements.txt
```

# usage

## Script : ./gen_missing_thumbs.py

Run this script to generate missing thumbnails for stickers.


This script will read stickers from the DB and generate thumbnails.
Thumbnails are uploaded to the s3 bucket under `thumbs/` path.
Finally s3 urls are saved in the db under `preview_url` column.  

```
python ./gen_missing_thumbs.py
```

## Script : ./gen_thumb.py

Run this script to generate a thumbnail for a sticker.

Thumbnail is uploaded to the s3 bucket under `thumbs/` path.
Finally it's s3 url is saved in the db under `preview_url` column.  

```
python ./gen_thumb.py --hash STICKER_HASH
```
