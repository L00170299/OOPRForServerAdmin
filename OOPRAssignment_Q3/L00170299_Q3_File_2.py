"""
#
# File          : main.py
# Created       : 04/12/2021 09:44
# Author        : Luis Gonzalez (L00170299)
# Version       : v1.0.0
# Licencing     : (C) 2021 Luis Gonzalez
                  Available under GNU Public License (GPL)
# Description   : Script to connect to remote pc/server through ssh and run a few commands
# 
"""

import sys
import paramiko
import time

# These variables should be in a config file, json, etc... but just for now
g_ssh = None
g_username = "vserver"
g_password = "vserver"
g_hostname = "192.168.0.222"
g_port = 22  # I doubt this port would change, but still


def get_connection():
    """
        It tries to establish ssh connection.
        If any error it will print it out and finish execution
        Parameters:
            none
        Returns:
            ssh session object
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(username=g_username, password=g_password, hostname=g_hostname, port=g_port)

        print(f"*** Connection established successfully with: {g_username}@{g_hostname}")
        return ssh
    # except paramiko.SSHException as e:        # This is nice but it requires to specify each type of error
    except Exception as e:                      # But this one allows to make more generic. It's you call :)
        sys.exit("*** Caught exception: " + str(e.__class__) + ": " + str(e))


def run_command(command, sudo=False):
    """
        It tries to execute a given command on a ssh session
        It expects to have a global ssh session open already.
            e.g.: g_ssh = get_connection()
        Parameters:
            command     String with command to execute
            sudo        If true it will try to run command with admin rights. Default: False
        Returns:
            response    Dictionary with output from command executed.
                        keys: output_str, error_str, exit_code
    """
    response = {
        "output_str": None,
        "error_str": None,
        "exit_code": None
    }
    try:
        if sudo:
            stdin, stdout, stderr = g_ssh.exec_command(f"sudo -S {command}")
            stdin.write(f"{g_password}\n")
        else:
            stdin, stdout, stderr = g_ssh.exec_command(command)

        time.sleep(1)

        response["output_str"] = stdout.read().splitlines()
        response["error_str"] = stderr.read().splitlines()
        response["exit_code"] = stdout.channel.recv_exit_status()
    except Exception as e:
        response["error_str"] = 'Error! Code: {c}, Message, {m}'.format(c=type(e).__name__, m=str(e))
        response["exit_code"] = type(e).__name__
    finally:
        return response


def update_system(error_continue=False):
    """
        It runs command to update system on a given ssh session
        Parameters:
            error_continue      If True it will return error and continue execution.
                                If False it will show error and stop execution. Default: False
        Returns:
            response            Dictionary with output from command executed.
                                keys: output_str, error_str, exit_code
    """
    response = run_command("dnf update -y", sudo=True)

    # If an error and not needed to continue then show error and finish
    if int(response["exit_code"]) != 0 and not error_continue:
        sys.exit("*** Error Updating: ".format(response["exit_code"]))

    # Otherwise return response to be handled after
    return response


if __name__ == '__main__':
    """
        Main method of application      
        Parameters:
            none      
        Returns:
            none
    """

    try:
        g_ssh = get_connection()

        print(f"*** Updating System...")
        response = update_system()      # This was just a function to simplify a bit the update command
        print(f"\tSuccess!!")           # I ran update with default 'error_continue=False'. So success at this point.

        # What else can we do??... well a lot. We could have more functions like the 'update' one for common tasks.
        # Or we could just run the commands we need:
        print(f"*** Getting OS Details...")
        response = run_command("cat /etc/os-release")
        # And handle output as we want
        print(f"\tResponse:")
        for line in response["output_str"]:
            print(f"\t{line.decode('UTF-8')}")

        # Or something else like, install software, create files/folders, star/stop services, etc...

    finally:
        try:
            # Close the session as very last step.
            g_ssh.close()
        except Exception:
            pass
