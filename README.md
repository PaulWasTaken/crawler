# Crawler
Simple crawler, written in python.
## Installation.
You will need python >= 3.5 and pip preinstalled.
Run `pip install -r requirements.txt`

## Using.
Type `python launch.py [command] [url] <options>`

### Commands.
1. `load` - to load url and its links.
   - `--depth` - sets how many times the program should perform `load` for suburls. __Default__: 1
2. `get` - to get associated urls.
   - `-n` - sets amount of urls to be loaded out of db. Negative value is used to get all urls. __Default__: 1
### Options.
- `--timeout` - sets timeout in seconds on loading process. __Default__: 90
- `--ssl` - if sets, then ssl check will be performed.
- `--size` - sets storage size in bytes. __Default__: 10000000 (10 Mb)
