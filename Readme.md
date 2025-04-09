### Arch Mirror Checker v1.0
#### Check Arch ISO mirrors

##### Setup
###### Arch Linux
```bash
chmod +x amc.py
sudo pacman -S python-requests python-regex --needed
```
###### Ubuntu / Debian
```bash
chmod +x amc.py
pip install regex threading requests || python -m pip install regex threading requests
```

### Start
##### 1.
    python3 amc.py
##### 2.
    ./amc.py
