### Arch Mirror Checker v1.4.1
#### Check Arch ISO mirrors

##### Setup
###### Arch Linux
```bash
chmod +x amc.py
sudo pacman -S python-requests python-regex python-argparse-utils --needed
yay -S python-bs4 --needed
```
###### Ubuntu / Debian
```bash
chmod +x amc.py
pip install regex argparse futures requests beautifulsoup4 || python -m pip install argparse regex futures requests beautifulsoup4
```

### Start
##### 1.
    python3 amc.py
##### 2.
    ./amc.py


### Usage
```
options:
  -h, --help                    show this help message and exit
  --ask-custom-url, -a          Ask for a custom Download URL
  --max-check, -c [int]         Check only the first X Mirrors (0 = no limit)
  --download-url, -d [str]      URL to get the Mirrors from (https://archlinux.org/download/)
  --exclude-country, -e [str]   Skip Mirrors from countries. COUNTRY1,COUNTRY2,COUNTRY3....
  --force-ascii, -f             force ASCII for output file (non-ASCII chars will be escaped to unicode)
  --include-country, -i [str]   Check Mirrors from countries. COUNTRY1,COUNTRY2,COUNTRY3....
  --country-spacing, -l [int]   Spacing between Country and Status
  --mirror-file, -m [str]       Check mirrors from a file not URL
  --threads, -n [int]           thread amount
  --log-file, -o [str]          log output file
  --silent, -q                  Don't print just log
  --disable-ssl, -s             skip SSL/TLS verifying
  --timeout, -t [int]           Request timeout (seconds)
  --url-spacing, -u [int]       Spacing between URL and Country
  --no-log                      Don't log into file
```