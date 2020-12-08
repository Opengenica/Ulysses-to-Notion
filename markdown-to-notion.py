import os
import time
from datetime import datetime
from notion.block import TextBlock
from notion.client import NotionClient
from md2notion.upload import convert, uploadBlock
from requests import HTTPError

API_RETRY_DELAY = 5

paths = []

for dir_path, _, filenames in os.walk(os.getenv('SOURCE')):
    for filename in [f for f in filenames if f.endswith('.md')]:
        paths.append(os.path.join(dir_path, filename))

paths = sorted(paths)
len_paths = len(paths)
offset = int(os.getenv('OFFSET', 0))
paths = paths[offset:]

current_row = None
error = False

for n, path in enumerate(paths):
    while True:
        print(f'\nProcessing path {n + 1 + offset} out of {len_paths}:')
        print(path)

        client = NotionClient(token_v2=os.getenv('TOKEN'))
        cv = client.get_collection_view(os.getenv('DESTINATION'))

        if current_row and error:
            print(f'Removing incomplete row {current_row}')
            current_row.remove()
            error = False

        try:
            with open(path, 'r', encoding='utf-8') as mdFile:
                rendered = convert(mdFile)
                title = rendered.pop(0).get('title').split('\n', 1)

                row = current_row = cv.collection.add_row()
                row.date_created = datetime.fromtimestamp(os.stat(os.path.dirname(path)).st_birthtime)
                row.name = title[0]

                if os.getenv('REPORT'):
                    row.report = os.getenv('REPORT')

                if len(title) == 2:
                    row.children.add_new(TextBlock, title=title[1])

                for blockDescriptor in rendered:
                    uploadBlock(blockDescriptor, row, mdFile.name)

        except HTTPError as err:
            print(f'Error: {err}')
            print(f'Retrying in {API_RETRY_DELAY} seconds...')
            time.sleep(API_RETRY_DELAY)
            error = True
            continue

        break
