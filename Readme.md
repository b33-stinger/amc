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

### Mirror file format
```
[URL], [Domain], [Country]
URL is required, if Country is not set it will be defaulted to "Uknown"
If domain is not set amc will get the domain from the URL using urlparse

As of now, you can't set the Country if you didn't set the domain. Will be fixed next update
```

#### Rust Version
##### https://github.com/b33-stinger/ramc
#### Comparison
```
time ./amc.py -t 10 -n 10     time ./ramc

real    0m51.352s             real    0m15.982s   -3.21× (68.93% faster)
user    0m2.207s              user    0m0.695s    -3.18× (68.51% faster)
sys     0m0.300s              sys     0m0.247s    -1.21× (17.67% faster)
```