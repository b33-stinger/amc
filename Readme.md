### Arch Mirror Checker v1.1.1
#### Check Arch ISO mirrors

##### Setup
###### Arch Linux
```bash
chmod +x amc.py
sudo pacman -S python-requests python-regex python-argparse-utils --needed
```
###### Ubuntu / Debian
```bash
chmod +x amc.py
pip install regex argparse futures requests || python -m pip install argparse regex futures requests
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
```