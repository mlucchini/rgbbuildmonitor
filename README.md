# RGB Build Monitor

Supports Bamboo builds and deployments and Bitrise workflows. Copy `config.yml.template`
to `config.yml` and fill in username, password, token as appropriate.

## Install dependencies

### MacOSX

```sh
pip3 install untangle
pip3 install pyyaml
pip3 install git+https://github.com/nosix/raspberry-gpio-emulator/
```

### Raspbian

```sh
# Will SSH the Pi, copy the build monitor and install the dependencies
make install
```

## Run the build monitor

### MacOSX

```sh
python3 main.py
```

### Raspbian

```sh
ssh pi@raspberrypi.local
cd ws/buildmonitor
python3 main.py
```

## Misc

### Passwordless SSH

```sh
ssh-copy-id -i ~/.ssh/<your_key> pi@raspberrypi.local
```
