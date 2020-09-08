import subprocess

def WiredConName():
    WiredName = subprocess.Popen("nmcli c", shell=True, stdout=subprocess.PIPE)
    WiredName = WiredName.stdout.readlines()
    if WiredName == []:
        return "not connected"
    else:
        WiredName = WiredName[1].decode("utf-8").split("  ")
        WiredName = WiredName[0]
        return WiredName

def Host_to_Gateway(host):
    GatewayIP = host.split(".")
    GatewayIP[3] = "1"
    GatewayIP = ".".join(GatewayIP)
    return GatewayIP
