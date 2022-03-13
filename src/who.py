from scapy.all import *
<<<<<<< HEAD
=======
from urllib import *
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac
from device import *

import urllib.request
import platform
<<<<<<< HEAD
=======
import getmac
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac
import os


def who(time=10):
    plat = platform.system()
    dev = device()

<<<<<<< HEAD
    if ((plat == "Linux") or (plat == "Darwin")) and (os.getuid() == 1000):
        print("Please run this command as sudo! (for better result)")
        exit()

    WhoList, IPs, MACs, deviceNames = [], [], [], []
    name, product_name, MyMac, MyIP = dev[0], dev[1], dev[2], dev[4]
    gateway = dev[8]+"/24"

    MyDeviceList = ["IP Address:", MyIP, "Mac Address:", MyMac, "Device:", f"{name} {product_name} (Your device)"]
    print(MyDeviceList)
=======
    if plat == "Linux" or plat == "Darwin":
        if os.getuid() == 1000:
            print("Please run this command as sudo! (for better result)")
            exit()
        else:
            pass

    WhoList = []
    IPs = []
    MACs = []
    deviceNames = []

    MyIP = dev[4]
    MyMac = dev[2]
    name = dev[0]
    product_name = dev[1]
    gateway = dev[8]+"/24"

    YourDeviceList = ["IP Address:", MyIP, "Mac Address:", MyMac, "Device:", f"{name} {product_name} (Your device)"]
        
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac
    start = 0

    while start <= time:
        start += 1

        eth = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp = ARP(pdst=gateway)
        devided = eth/arp
        answ = srp(devided, timeout=0.5, verbose=False)[0] # '0.5' because of double attempts per second 

        for res in answ:
            IP = res[1].psrc
<<<<<<< HEAD
            if IP not in IPs: IPs.append(IP)
=======
            if IP not in IPs:
                IPs.append(IP)
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac

            MAC = res[1].hwsrc
            if MAC not in MACs:
                MACs.append(MAC)
                try:
                    deviceName = urllib.request.urlopen(f"http://api.macvendors.com/{MAC}")
                    deviceName = deviceName.read().decode("utf-8")
                    deviceNames.append(deviceName)
                        
                except:
                    try:
                        deviceName = urllib.request.urlopen(f"https://api.maclookup.app/v2/macs/{MAC}")
<<<<<<< HEAD
                        deviceName = (deviceName.read().decode("utf-8")).split(",")
                        deviceName = (deviceName[3]).replace('company":', "").replace('"', "")

                        if deviceName == "": deviceName = "unknown"

=======
                        deviceName = deviceName.read().decode("utf-8")
                        deviceName = deviceName.split(",")
                        deviceName = deviceName[3]
                        deviceName = deviceName.replace('company":', "").replace('"', "")
                        if deviceName == "":
                            deviceName = "unknown"
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac
                        deviceNames.append(deviceName)
                    except:
                        deviceName="unknown"
                        deviceNames.append(deviceName)

<<<<<<< HEAD
    print(IPs, len(IPs))
    for i in range(0, len(IPs)-1):
        print(i)
        if IPs[i] == dev[8]: WhoList.append(["IP Address:", IPs[i], "Mac Address:", MACs[i], "Device:", f"{deviceNames[i]} (router)"])
        else: WhoList.append(["IP Address:", IPs[i], "Mac Address:", MACs[i], "Device:", deviceNames[i]])

    WhoList.append(MyDeviceList)
=======
    for i in range(0, len(IPs)):
        if IPs[i] == dev[8]:
            WhoList.append(["IP Address:", IPs[i], "Mac Address:", MACs[i], "Device:", f"{deviceNames[i]} (router)"])
        else:
            WhoList.append(["IP Address:", IPs[i], "Mac Address:", MACs[i], "Device:", deviceNames[i]])

    WhoList.append(YourDeviceList)
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac

    return WhoList