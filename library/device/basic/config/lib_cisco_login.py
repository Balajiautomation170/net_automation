import re
import time
import os
import json
import logging
import time
import pathlib
import paramiko
from netmiko import ConnectHandler, Netmiko
from netmiko.mikrotik.mikrotik_ssh import MikrotikRouterOsSSH
from netmiko.linux.linux_ssh import LinuxSSH
logging.basicConfig(level=logging.DEBUG)


class Ciscossh():

    def __init__(self):
        self.logger = logging.getLogger()

    def ssh_login_show(self, login_det, execute_cmd):
        """
        ssh login to devices : show commands
        """
        execute_cmd = str(execute_cmd)
        print ("#### Logged into device {}###".format(login_det["host"]))
        router_conn = ConnectHandler(**login_det)
        output = router_conn.send_command(execute_cmd)
        output_lst = output.split(",")
        # print (output_lst)
        router_conn.disconnect()
        print ("#### Logged out from device {}###".format(login_det["host"]))
        return output_lst

    def execute_show_commands(self, login_det, execute_cmds, host_name):
        """
        Execute the show commands
        """
        print ("#### Logged into device {}###".format(login_det["host"]))
        router_conn = ConnectHandler(**login_det)
        router_conn.enable()
        file_name = os.environ["PYTHONPATH"] + login_det["device_type"] + "_" + login_det["ip"] + ".txt"
        if os.path.exists(file_name):
          os.remove(file_name)
          create_cisco_file = open(file_name , "a")
        else:
          create_cisco_file = open(file_name , "a")
        for execute_cmd in execute_cmds:
            execute_cmd = str(execute_cmd)
            print_sh = "++++++++" + execute_cmd + "+++++++++"
            output = router_conn.send_command(execute_cmd)
            output_error_check = re.findall("invalid|error|failed|\^", output)
            if output_error_check:
                print ("{} command execution failed".format(execute_cmd))
                router_conn.disconnect()
                create_cisco_file.close()
                assert False
            else:
                output_lst = output.split(",")
                create_cisco_file.write(str(print_sh))
                create_cisco_file.write("\n======================\n")
                create_cisco_file.write(str(output))
                create_cisco_file.write("\n======================\n")
        create_cisco_file.close()
        router_conn.disconnect()
        print ("All show commands are executed, please refer the log")
        print ("log path {}".format(file_name))
        print ("#### Logged out from device {}###".format(login_det["host"]))

    def config_interface(self, login_det, config_cmd):
        """
        Devices: Configure interfaces
        """
        print ("#### Logged into device {}###".format(login_det["host"]))
        router_conn = ConnectHandler(**login_det)
        router_conn.enable()
        output = []
        for int in config_cmd["interfaces"]:
            output.append ("int {}".format(int["name"]))
            output.append ("no ip add")
            output.append("ip address {} {}".format(int["ip_address"], int["net_mask"]))
            output.append("no shut")
        output_config = router_conn.send_config_set(output)
        print (output_config)
        # Close connection.
        router_conn.disconnect()
        print("#### Logged out from device {}###".format(login_det["host"]))
        ip_add = False
        for int in config_cmd["interfaces"]:
            if int["ip_address"]  in output_config :
                ip_add = True
            else:
                ip_add = False
        return ip_add

    def config_enable_rip(self, login_det, config_cmd):
        """
        Devices: Configure rip
        """
        print ("#### Logged into device {}###".format(login_det["host"]))
        router_conn = ConnectHandler(**login_det)
        router_conn.enable()
        output = []
        output.append ("router rip")
        output.append ("version 2")
        for net in config_cmd["router_rip"][0]["network"]:
            output.append("network {}".format(net))
        output.append("no auto-summary")
        output_config = router_conn.send_config_set(output)
        print (output_config)
        # Close connection.
        router_conn.disconnect()
        print("#### Logged out from device {}###".format(login_det["host"]))
        net_add = False
        for net in config_cmd["router_rip"][0]["network"]:
            if net  in output_config :
                net_add = True
            else:
                net_add = False
        return net_add

    def check_rip_database(self, login_det):
        """
        Devices: Configure rip
        """
        print ("#### Logged into device {}###".format(login_det["host"]))
        router_conn = ConnectHandler(**login_det)
        router_conn.enable()
        output = router_conn.send_command("show ip rip database")
        # Close connection.
        router_conn.disconnect()
        return output

    def check_ip_route(self, login_det):
        """
        Devices: Configure rip
        """
        print ("#### Logged into device {}###".format(login_det["host"]))
        router_conn = ConnectHandler(**login_det)
        router_conn.enable()
        output = router_conn.send_command("show ip route")
        # Close connection.
        router_conn.disconnect()
        return output

    def check_ping(self, login_det, ip_add):
        """
        Devices: Configure rip
        """
        print ("#### Logged into device {}###".format(login_det["host"]))
        router_conn = ConnectHandler(**login_det)
        router_conn.enable()
        ping_in = "ping {}".format(ip_add)
        output = router_conn.send_command(ping_in)
        # Close connection.
        router_conn.disconnect()
        return output

    def config_disable_rip(self, login_det, config_cmd):
        """
        Devices: Configure rip disable
        """
        print ("#### Logged into device {}###".format(login_det["host"]))
        router_conn = ConnectHandler(**login_det)
        router_conn.enable()
        output = []
        output.append ("router rip")
        for net in config_cmd["router_rip"][0]["network"]:
            output.append("no network {}".format(net))
        output.append("no auto-summary")
        output_config = router_conn.send_config_set(output)
        print (output_config)
        # Close connection.
        router_conn.disconnect()
        print("#### Logged out from device {}###".format(login_det["host"]))
        net_add = False
        network_rem = config_cmd["router_rip"][0]["network"]
        if "invalid"  not in output_config :
            print("#### RIP Routes {} removed from the device {}###".format(network_rem, login_det["host"]))
            net_add = True
        else:
            print("#### Failed to remove RIP Routes {} from the device {}###".format(network_rem, login_det["host"]))
            net_add = False
        return net_add

    def disable_interface(self, login_det, config_cmd):
        """
        Devices: Configure interfaces
        """
        print ("#### Logged into device {}###".format(login_det["host"]))
        router_conn = ConnectHandler(**login_det)
        router_conn.enable()
        output = []
        for int in config_cmd["interfaces"]:
            output.append ("int {}".format(int["name"]))
            output.append ("no ip add")
            output.append("shut")
        output_config = router_conn.send_config_set(output)
        print (output_config)
        # Close connection.
        router_conn.disconnect()
        print("#### Logged out from device {}###".format(login_det["host"]))
        ip_add = False
        for int in config_cmd["interfaces"]:
            if int["ip_address"] not in output_config :
                ip_add = True
            else:
                ip_add = False
        return ip_add

    def wr_mem_cfg(self, login_det):
        """
        ssh login to devices : show commands
        """
        print ("#### Logged into device {}###".format(login_det["host"]))
        router_conn = ConnectHandler(**login_det)
        router_conn.enable()
        output = router_conn.send_command("wr mem")
        router_conn.disconnect()
        print ("#### Logged out from device {}###".format(login_det["host"]))
        return output


class Mikrossh():

    def __init__(self):
        self.logger = logging.getLogger()

    def m_execute_show_commands(self, login_det, execute_cmds, host_name):
        """
        Execute the show commands
        """
        print ("#### Logged into device {}###".format(login_det["host"]))
        router_conn = paramiko.SSHClient()
        router_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        router_conn.connect(login_det["ip"], username=login_det["username"], password=login_det["password"])

        file_name = os.environ["PYTHONPATH"] + login_det["device_type"] + "_" + login_det["ip"] + ".txt"
        if os.path.exists(file_name):
          os.remove(file_name)
          create_cisco_file = open(file_name , "a")
        else:
          create_cisco_file = open(file_name , "a")
        for execute_cmd in execute_cmds:
            print_sh = "++++++++" + execute_cmd + "+++++++++"
            stdin, stdout, stderr = router_conn.exec_command(execute_cmd)
            output_lst = stdout.readlines()
            output = ""
            output = output.join(output_lst)
            output_error_check = re.findall("invalid|error|failed|\^", output)
            if output_error_check:
                print ("{} command execution failed".format(execute_cmd))
                router_conn.close()
                create_cisco_file.close()
                assert False
            else:
                output_lst = output.split(",")
                create_cisco_file.write(str(print_sh))
                create_cisco_file.write("\n======================\n")
                create_cisco_file.write(str(output))
                create_cisco_file.write("\n======================\n")
        router_conn.close()
        create_cisco_file.close()
        print ("All show commands are executed, please refer the log")
        print ("log path {}".format(file_name))
        print ("#### Logged out from device {}###".format(login_det["host"]))


class Cumulusssh():

    def __init__(self):
        self.logger = logging.getLogger()

    def c_execute_show_commands(self, login_det, execute_cmds, host_name):
        """
        Execute the show commands
        """

        print ("#### Logged into device {}###".format(login_det["host"]))
        router_conn = paramiko.SSHClient()
        router_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        import pdb; pdb.set_trace()
        router_conn.connect(login_det["ip"], username=login_det["username"], password=login_det["password"])

        file_name = os.environ["PYTHONPATH"] + "cumulus" + host_name + ".txt"
        if os.path.exists(file_name):
          os.remove(file_name)
          create_cisco_file = open(file_name , "a")
        else:
          create_cisco_file = open(file_name , "a")
        for execute_cmd in execute_cmds:
            print_sh = "++++++++" + execute_cmd + "+++++++++"
            stdin, stdout, stderr = router_conn.exec_command(execute_cmd)
            output_lst = stdout.readlines()
            output = ""
            output = output.join(output_lst)
            output_error_check = re.findall("invalid|error|failed|\^", output)
            if output_error_check:
                print ("{} command execution failed".format(execute_cmd))
                router_conn.close()
                create_cisco_file.close()
                assert False
            else:
                output_lst = output.split(",")
                create_cisco_file.write(str(print_sh))
                create_cisco_file.write("\n======================\n")
                create_cisco_file.write(str(output))
                create_cisco_file.write("\n======================\n")
        router_conn.close()
        create_cisco_file.close()
        print ("All show commands are executed, please refer the log")
        print ("log path {}".format(file_name))
        print ("#### Logged out from device {}###".format(login_det["host"]))


if __name__ == "__main__":
    print("hi")
