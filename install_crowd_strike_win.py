import sys
import subprocess
import json
from datetime import datetime
import os
import socket


def install_crowdstrike(installer_path, installer, CID):
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        Output = subprocess.run(['powershell.exe', 'Get-Service', '-Name', 'CSFalconService'], shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print("Output: " + str(Output.returncode))
        if (Output.returncode == 0):
            print("Already Present. Exiting")
        else:
            print("CrowdStrike is not installed !")
            print("Copying CrowdStrike installer to D:")
            print("Copying INstaller from: " + str(installer_path))
            complete_path = installer_path + "/" + installer
            print(complete_path.replace("\"",""))
            Output = subprocess.run(
                ['powershell.exe', 'Copy-Item', '-Path', complete_path.replace("\"",""), '-Destination', 'D:\\'],
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(":" + str(Output.stderr))
            if (Output.returncode == 0):
                print("Installing CrowdStrike...")
                start = datetime.now()
                print("Installation started at: ", start)
                print("installer: " + installer)
                d_path = "D:\\" + installer
                Output = subprocess.run(
                    [d_path.replace("\"","") , '/CID=' + CID,
                     '/S', '/SILENT'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                end = datetime.now()
                print("Installation finished at: ", end)

                print(str(Output))
            else:
                print("Error: Failed while copying CrowdStrike installer")
                print(str(Output.stderr))
    except Exception as ex:
        print(ex)


# main
#

def main(argv):
    print("Crowd Strike installation Started....")

    #input_data = sys.stdin.read()

    #with open("D:\input.json", "w") as fh:
    #    fh.write(input_data.replace("'", ""))

    #fh = open("D:\input.json")

    #input_json_data = json.load(fh)
    #print(input_json_data)
    #installer = input_json_data["installer"]
    #installer_path = input_json_data["installer_path"]
    print(os.environ)
    installer_path = os.environ['installer_path']

    installer = os.environ['installer']
    CID = os.environ['CID']

    #print(input_json_data)
    print("installer_path: " + installer_path)
    print("installer Name: " + installer)
    # "\\\\10.1.1.6\CloudManagerUtils\crowdstrike-windowssensorcid-6.54.16808.1-w64-3812128.exe"
    install_crowdstrike(installer_path, installer, CID)


if __name__ == '__main__':
    main(sys.argv[1:])