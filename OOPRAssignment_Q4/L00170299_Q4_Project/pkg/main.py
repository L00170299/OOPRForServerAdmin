"""
#
# File          : main.py
# Created       : 05/12/2021 16:23
# Author        : Luis Gonzalez (L00170299)
# Version       : v1.0.0
# Licencing     : (C) 2021 Luis Gonzalez
                  Available under GNU Public License (GPL)
# Description   : Script to scan open ports using socket
# 
"""

import socket
import subprocess
import sys

# Common ports and their usage. Feel free to amend.
ports_dict = {
    20: "FTP",        # FTP Data Transfer
    21: "FTP",        # FTP Command Control
    22: "SSH",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    135: "SMB",       # Samba
    139: "SMB",
    445: "SMB",
    1025: "SMB",
    1026: "SMB",
    1028: "SMB",
    5000: "SMB",
    143: "IMAP",
    443: "HTTPS",
    531: "AOL",       # AOL Instant Messenger
    666: "DOOM",      # Doom, first online first-person shooter
    3389: "RDP",      # Windows Remote Desktop. In linux you can install xrdp, start service and open port.
    3724: "WOC",	  # Game: World of Warcraft
    6667: "IRC",
    5900: "VNC"
}


def scan_ports(ip_address, port_from, port_to):
    """
        It scans ports on a given IP address and returns list of open ports
        Parameters:
            ip_address      Ip Address of pc to scan
            port_from       First port on the range to start scanning
            port_to         Last port on the range to start scanning
        Returns:
            list            List of ports open
    """
    try:
        open_ports = []                                 # Initialize an empty list to add port that found open
        remote_ip = socket.gethostbyname(ip_address)    # Get Ip Address in case a name was given

        for i in range(port_from, port_to + 1):         # +1 to avoid missing the last element in the range
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remote_ip, i))
            if result == 0:                             # If port open, add it to the list
                open_ports.append(i)
            sock.close()

        return open_ports

    except socket.gaierror:
        sys.exit("*** Hostname could not be resolved. Exiting")
    except socket.error:
        sys.exit("*** Couldn't connect to server. Exiting")
    except Exception as e:
        sys.exit("*** Caught exception: " + str(e.__class__) + ": " + str(e))
    finally:
        try:
            # Just in case still open, try to close the connection.
            sock.close()
        except Exception:
            pass


if __name__ == '__main__':
    """
        Main method of application      
        Parameters:
            none      
        Returns:
            none
    """

    # List with machines to scan. In case many
    machines_list = ["localhost", "192.168.0.222"]

    # per each machine, scan and show results
    for machine in machines_list:
        print("=" * 50)
        print(f"Scanning ports on : {machine}")
        result_list = scan_ports(machine, 1, 65000)        # Maybe a long range. Reduce if you want

        # Lets print out open ports and possible service name (if in the dictionary)
        print(f"\tPorts open :")
        print("\t{}".format("-" * 15))
        for open_port in result_list:
            # If there is no name in dictionary for a port, then just show '--'
            print("\t{} => {}".format(open_port, ports_dict.get(open_port, "--")))

