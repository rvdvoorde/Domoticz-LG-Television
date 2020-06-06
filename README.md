<b>Python plugin for Domoticz with a LG WebOS Television</b>

<hr/>

<b>Installation Raspberry PI</b>

First install the Python LG library
```bash
sudo pip3 install pylgtv
```

To install this plugin on your raspberry pi enter the following commands using putty
```bash
cd domoticz/plugins
git clone https://github.com/rvdvoorde/Domoticz-LG-Television.git
sudo systemctl restart domoticz
```

Update the plugin (if available)
```bash
cd domoticz/plugins/Domoticz-LG-Television
git pull
sudo systemctl restart domoticz
```
