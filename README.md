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

A simple Domoticz LUA script to handle the maximum volume
```script
commandArray = {}

-- Get the changed device
tc=next(devicechanged)
Device=tostring(tc)

-- Get current time
time = {}
time.hour = os.date("%H") 
time.min = os.date("%M") 


myDevice = 'LG - TV Volume'
DayLimit = 20
NightLimit = 15


if ( Device == myDevice ) then
    if ( tonumber(time.hour) > 21 and tonumber(time.hour) < 9 ) then
        if ( tonumber(otherdevices_svalues[myDevice]) > NightLimit ) then    
            commandArray[myDevice] = 'Set Level ' .. NightLimit    
        end
    else
        if ( tonumber(otherdevices_svalues[myDevice]) > DayLimit ) then    
            commandArray[myDevice] = 'Set Level ' .. DayLimit    
        end
    end
end

return commandArray

```
