import os
from datetime import datetime
from notion.block import TextBlock
from notion.client import NotionClient
from md2notion.upload import convert, uploadBlock

client = NotionClient(token_v2=os.getenv('TOKEN'))
cv = client.get_collection_view(os.getenv('DESTINATION'))

paths = []

for dir_path, _, filenames in os.walk(os.getenv('SOURCE')):
    for filename in [f for f in filenames if f.endswith('.md')]:
        paths.append(os.path.join(dir_path, filename))

paths = sorted(paths)
len_paths = len(paths)
offset = int(os.getenv('OFFSET', 0))
paths = paths[offset:]

for n, path in enumerate(paths):
    print(f'\nProcessing path {n + 1 + offset} out of {len_paths}:')
    print(path)

    with open(path, 'r', encoding='utf-8') as mdFile:
        rendered = convert(mdFile)
        title = rendered.pop(0).get('title').split('\n', 1)

        row = cv.collection.add_row()
        row.date_created = datetime.fromtimestamp(os.stat(os.path.dirname(path)).st_birthtime)
        row.name = title[0]

        if os.getenv('REPORT'):
            row.report = os.getenv('REPORT')

        if len(title) == 2:
            row.children.add_new(TextBlock, title=title[1])

        for blockDescriptor in rendered:
            uploadBlock(blockDescriptor, row, mdFile.name)
