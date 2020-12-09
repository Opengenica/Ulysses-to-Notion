# Ulysses-to-Notion

Ulysses-to-Notion (utn, for short) imports [Ulysses](https://ulysses.app/) Textbundle files to [Notion](https://www.notion.so/) database.

## How to use

1. Export Ulysses entries or groups by right-clicking on an entry and selecting "Quick Export..."
2. Put the root folder where Ulysses entries were exported to `SOURCE` ENV variable
3. Create a new database in Notion, copy its full URL (with https://www.notion.so/...) and put to `DESTINATION` ENV variable
4. Open Chrome Developer Console, go to Application, select Cookies and copy value of `token_v2` cookie to `TOKEN` ENV variable
5. Launch `utn.py` and enjoy!

## Notes

### Import Restart

- `OFFSET` ENV variable is for restarting import if it stops for some reason.
- Put a number there: `N-1` from the last `Processing path N out of M:` message.
- Restart `utn.py`

### Additional Fields

- I have a field called `Report` configured for some of my entries
- It's configured with `REPORT` ENV variable
- Feel free to add your own fields

## Acknowledgements

This tool wouldn't be possible without two awesome packages: [notion-py](https://github.com/jamalex/notion-py) and [md2notion](https://github.com/Cobertos/md2notion).

Please check them out: they have more docs on how to work with Notion APIs.

# LICENSE

Ulysses-to-Notion
Copyright (C) 2020 Xiveti Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
