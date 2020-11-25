import re
import time
import json
import logging
import time
from netmiko import ConnectHandler
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
        router_conn.enable()
        output = router_conn.send_command(execute_cmd)
        output_lst = output.split(",")
        # print (output_lst)
        router_conn.disconnect()
        print ("#### Logged out from device {}###".format(login_det["host"]))
        return output_lst

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


if __name__ == "__main__":
    print("hi")
