# LG Television (WebOS) plugin for Domoticz
# Please also install pylgtv (pip3 install pylgtv) for this plugin to get it work!
# Author: Raymond Van de Voorde
#
#
"""
<plugin key="LGTV" name="LG Television" author="Raymond Van de Voorde" version="1.0.0" wikilink="https://github.com/rvdvoorde/Domoticz-LG-Television">
    <description>
        <h2>LG Television plugin</h2><br/>
            This plugin connects to a LG WebOS Television<br/>
            You can manage the volume and see the tv source<br/>
            <br/>
            Make sure you have pylgtv installed: sudo pip3 install pylgtv
        <br/>
        <br/>
        <h3>Setup information</h3>
        <br/>
            <ul style="list-style-type:square">
                <li>IP Address - The static IP Address of the Television</li>
                <li>Poll interval - The interval Domoticz uses to update the devices. Minimum 7, maximum 30</li>
                <li>Notifications - Show all notifications on the Television screen</li>
                <li>Debug - Set this to true when you experience problems with the plugin</li>
            </ul>
        <br/>
    </description>
    <br/>
    <params>
        <param field="Address" label="IP Address" width="200px" required="true" default="127.0.0.1" />
        <param field="Mode1" label="Poll interval" width="100px" required="true" default=10 />
        <param field="Mode2" label="Notifications" width="75px">
            <options>
                <option label="True" value="true" default="true"/>
                <option label="False" value="false"/>
            </options>
        </param>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="false" />
            </options>
        </param>
    </params>
</plugin>
"""

from pylgtv import WebOsClient
import sys
import logging

import Domoticz

class BasePlugin:

    def onStart(self):
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
            Domoticz.Trace(True)
            self.debug = True
            DumpConfigToLog()

        Domoticz.Debug("onStart called")
        updateInterval = int(Parameters["Mode1"])
        if updateInterval > 30 or updateInterval < 7:
            updateInterval = 10
            Domoticz.Error("Invalid interval setting, changed to 10")

        Domoticz.Heartbeat(updateInterval)
        self.webos_client = WebOsClient(Parameters["Address"], "NONE", 5)

        # First get some TV details
        try:
            tv_details = self.webos_client.get_software_info()
            Domoticz.Log("Product name: " + tv_details["product_name"])
            Domoticz.Log("Software version: " + tv_details["major_ver"] + "." + tv_details["minor_ver"])
            Domoticz.Log("MAC Address: " + tv_details["device_id"])
        except Exception as e:
            Domoticz.Error("Error at reading TV info")

        if not (1 in Devices):
            Domoticz.Device(Name="TV Status", Unit=1, Type=17, Switchtype=17).Create()

        if not (2 in Devices):
            Domoticz.Device(Name="TV Volume", Unit=2, Type=244, Subtype=73, Switchtype=7, Image=8).Create()

        return True


    def onStop(self):
        Domoticz.Debug("onStop called")


    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

        if Unit == 2:
            self.webos_client.set_volume(int(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Debug("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)
        if Parameters["Mode2"] == "true":
            self.webos_client.send_message(Subject)

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")
        try:
            tv_input = self.webos_client.get_input()
            if (tv_input.lower() == "none"):
                UpdateDevice(1, 0, "Off")
                return True
            else:
                UpdateDevice(1, 1, str(tv_input))

            UpdateDevice(2, 2, str(self.webos_client.get_volume()))
        except:
            #Domoticz.Error("Timeout connecting to television")
            UpdateDevice(1, 0, "Off")
            UpdateDevice(2, 0, "0")

    def GetValue(self, arr, sKey, defValue):
        try:
            if str(sKey) in arr:
                if ( str(arr[str(sKey)]).lower() == "none" ):
                    return defValue
                else:
                    return arr[str(sKey)]
            else:
                return defValue
        except:
            return defValue

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

def UpdateDevice(Unit, nValue, sValue, AlwaysUpdate=False):
    if (Unit in Devices):
        if ((Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue) or (AlwaysUpdate == True)):
            Devices[Unit].Update(nValue=nValue, sValue=str(sValue))
            Domoticz.Log("Update "+str(nValue)+":'"+str(sValue)+"' ("+Devices[Unit].Name+")")
    return
