from scapy.all import *
from device import *

import urllib.request
import platform
import os


def who(time=10):
    plat = platform.system()
    dev = device()

    if ((plat == "Linux") or (plat == "Darwin")) and (os.getuid() == 1000):
        print("Please run this command as sudo! (for better result)")
        exit()

    WhoList, IPs, MACs, deviceNames = [], [], [], []
    name, product_name, MyMac, MyIP = dev[0], dev[1], dev[2], dev[4]
    gateway = dev[8]+"/24"

    MyDeviceList = ["IP Address:", MyIP, "Mac Address:", MyMac, "Device:", f"{name} {product_name} (Your device)"]
    start = 0

    while start <= time:
        start += 1

        eth = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp = ARP(pdst=gateway)
        devided = eth/arp
        answ = srp(devided, timeout=0.5, verbose=False)[0] # '0.5' because of double attempts per second 

        for res in answ:
            IP = res[1].psrc
            if IP not in IPs: 
                IPs.append(IP)
                
                MAC = res[1].hwsrc
                MACs.append(MAC)
                try:
                    deviceName = urllib.request.urlopen(f"http://api.macvendors.com/{MAC}")
                    deviceName = deviceName.read().decode("utf-8")
                    deviceNames.append(deviceName)
                        
                except:
                    try:
                        deviceName = urllib.request.urlopen(f"https://api.maclookup.app/v2/macs/{MAC}")
                        deviceName = (deviceName.read().decode("utf-8")).split(",")
                        deviceName = (deviceName[3]).replace('company":', "").replace('"', "")

                        if deviceName == "": deviceName = "unknown"

                        deviceNames.append(deviceName)
                    except:
                        deviceName="unknown"
                        deviceNames.append(deviceName)


    for i in range(0, len(IPs)):
        if IPs[i] == dev[8]: WhoList.append(["IP Address:", IPs[i], "Mac Address:", MACs[i], "Device:", f"{deviceNames[i]} (router)"])
        else: WhoList.append(["IP Address:", IPs[i], "Mac Address:", MACs[i], "Device:", deviceNames[i]])

    WhoList.append(MyDeviceList)

    return WhoList
