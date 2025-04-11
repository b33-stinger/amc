### Arch Mirror Checker v1.3.1
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


### Arguments
```
options:
  -h, --help            show this help message and exit
  --workers, -w [int]            Worker Count

  --timeout, -t [float]          Request timeout (seconds)

  --max-check, -c [int]         Check only the first X Mirrors (0 = no limit)

  --download-url, -d [str]      URL to get the Mirrors from (https://archlinux.org/download/)
  --ask-custom-url, -a          Ask for a custom Download URL
  --log-file, -o [str]          log output file
  --force-ascii -f              force ASCII for output file (non-ASCII chars will be escaped to unicode)
  --disable-ssl -s              skip SSL/TLS verifying
  --include-country -i [str]    Check Mirrors from countries. COUNTRY1,COUNTRY2,COUNTRY3....
  --exclude-country -e [str]    Skip  Mirrors from countries. COUNTRY1,COUNTRY2,COUNTRY3....
```