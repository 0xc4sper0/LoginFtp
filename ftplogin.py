#!/usr/bin/python3

import sys
import socket
import ftplib
from termcolor import colored

print(colored('''
	          _  _                        ___  
              ___| || |  ___ _ __   ___ _ __ / _ \ 
             / __| || |_/ __| '_ \ / _ \ '__| | | |
            | (__|__   _\__ \ |_) |  __/ |  | |_| |
             \___|  |_| |___/ .__/ \___|_|   \___/ 
                             |_|                    
                                       
        ##############################################
        #| "Ftplogin" FTP Login Tester anonymous     #
        #|  Author: By C4sper0                       #
        #|  account Twitter(X): @C4sper0             #
        #|  Version: 1.0                             #
        ##############################################
        ''', 'green'))

# Function to test FTP login
def test_ftp_login(ip):
    try:
        ftp = ftplib.FTP(ip)
        # Attempt empty password login
        ftp.login("anonymous", "")
        ftp.quit()
        # Attempt same username and password login
        ftp = ftplib.FTP(ip)
        ftp.login("anonymous", "anonymous")
        ftp.quit()
        return True
    except ftplib.error_perm as e:
        if "530" in str(e):
            return False  # Authentication required
        else:
            return True  # Any other error indicates successful connection

# Main function
def main(filename, port=21):
    with open(filename, "r") as f:
        lines = f.readlines()
    for line in lines:
        ip = line.strip()
        try:
            # Check if FTP port is open
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(colored(f"FTP port ({port}) is open on {ip}.", "green"))
                if test_ftp_login(ip):
                    print(colored("FTP vulnerability found!", "green"))
                else:
                    print(colored("No FTP vulnerability found.", "red"))
            else:
                print(colored(f"FTP port ({port}) is closed on {ip}.", "red"))
            sock.close()
        except Exception as e:
            print(colored(f"Error checking FTP port ({port}) on {ip}: {e}", "red"))

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python3 ftplogin.py <filename> [port]")
        sys.exit(1)
    filename = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) == 3 else 21
    main(filename, port)
