import re
import os
import time
import pytest
import logging
from  library.device.basic.config.lib_cisco_login import Ciscossh, Mikrossh, Cumulusssh
logging.basicConfig(level=logging.DEBUG)


class Ciscossh_output():

    def __init__(self):
        self.logger = logging.getLogger()
        self.ssh_out = Ciscossh()

    ### Interface Cases ####
    def ssh_login_show_ouput(self, login_device, execute_cmd):
        """
        ssh login to devices output : show commands 
        """
        check_output = self.ssh_out.ssh_login_show(login_device, execute_cmd)
        cisco_product = False
        if str(execute_cmd) == "show version":
            for output in check_output:
                if "Cisco Systems" in output:
                    print("{} device is a CISCO product ".format(login_device["host"]))
                    cisco_product = True
                    break

            if cisco_product:
                assert True , "Its Cisco product"
            else:
                assert False , "Its n't Cisco product"

    def execute_show_ouput(self, login_device, execute_cmds, host_name):
        """
        ssh login to devices output : show commands 
        """
        self.ssh_out.execute_show_commands(login_device, execute_cmds, host_name)

    def config_interface_out(self, login_device, config_cmd):
        """
        ssh login to devices output : show commands 
        """
        check_cfg = self.ssh_out.config_interface(login_device, config_cmd)
        if check_cfg:
            print ("IP address configured successfully at {}".format(login_device["host"]))
            assert True
        else:
            print ("IP address failed to configure at {}".format(login_device["host"]))
            assert False

    def disable_interface_out(self, login_device, config_cmd):
        """
        ssh login to devices output : show commands 
        """
        check_cfg = self.ssh_out.disable_interface(login_device, config_cmd)
        if check_cfg:
            print ("Disabled : IP address at {}".format(login_device["host"]))
            assert True
        else:
            print ("Failed to disabled IP address at {}".format(login_device["host"]))
            assert False

    ### Interface Cases (END) ####

    ### RIP Cases ####
    def enable_rip_out(self, login_device, config_cmd):
        """
        ssh login to devices output : show commands 
        """
        check_cfg_rip = self.ssh_out.config_enable_rip(login_device, config_cmd)
        if check_cfg_rip:
            print ("RIP configured successfully at {}".format(login_device["host"]))
            assert True
        else:
            print ("RIP failed to configure at {}".format(login_device["host"]))
            assert False

    def check_rip_database_out(self, login_device, config_cmd):
        """
        ssh login to devices output : show commands 
        """
        check_rip_data = self.ssh_out.check_rip_database(login_device)
        for rip_data in config_cmd["router_rip"][0]["peer_network"]:
            if rip_data in check_rip_data:
                print ("RIP database route {} is available at {}".format(rip_data, login_device["host"]))
                assert True
            else:
                print ("RIP database route {} isn't available at {}".format(rip_data, login_device["host"]))
                assert False

    def check_ping_out(self, login_device, config_cmd):
        """
        ssh login to devices output : show commands 
        """
        for ip_data in config_cmd["router_rip"][0]["peer_ip_ping"]:
            check_ping_out = self.ssh_out.check_ping(login_device, str(ip_data))
            perct = re.search(".*percent \(([0-9])\/5\)", check_ping_out)
            if perct:
                perct_no = perct.group(1)
                if int(perct_no) > 3:
                    print ("Ping {} is success at {}".format(ip_data, login_device["host"]))
                    assert True
                else:
                    print ("Ping  {} is failed at {}".format(ip_data, login_device["host"]))
                    assert False

    def disable_rip_out(self, login_device, config_cmd):
        """
        ssh login to devices output : show commands 
        """
        check_cfg_rip = self.ssh_out.config_disable_rip(login_device, config_cmd)
        if check_cfg_rip:
            print ("RIP : routes are removed  successfully at {}".format(login_device["host"]))
            assert True
        else:
            print (" RIP : routes failed to removed at {}".format(login_device["host"]))
            assert False
    ### RIP Cases (END) ####

    ### Routing Cases ####
    def check_ip_route_out(self, login_device, config_cmd):
        """
        ssh login to devices output : show commands 
        """
        check_ip_route = self.ssh_out.check_ip_route(login_device)
        for ip_data in config_cmd["router_rip"][0]["peer_network"]:
            if ip_data in check_ip_route:
                print ("RIP database route {} is available at {}".format(ip_data, login_device["host"]))
                assert True
            else:
                print ("RIP database route {} isn't available at {}".format(ip_data, login_device["host"]))
                assert False

    def check_ip_route_out_non_exist(self, login_device, config_cmd):
        """
        ssh login to devices output : show commands 
        """
        check_ip_route = self.ssh_out.check_ip_route(login_device)
        for ip_data in config_cmd["router_rip"][0]["peer_network"]:
            if ip_data not in check_ip_route:
                print ("RIP database route {} isn't available at {}".format(ip_data, login_device["host"]))
                assert True
            else:
                print ("RIP database route {} is available at {}".format(ip_data, login_device["host"]))
                assert False

    def check_ping_out_non_exist(self, login_device, config_cmd):
        """
        ssh login to devices output : show commands 
        """
        for ip_data in config_cmd["router_rip"][0]["peer_ip_ping"]:
            check_ping_out = self.ssh_out.check_ping(login_device, str(ip_data))
            perct = re.search(".*percent \(([0-9])\/5\)", check_ping_out)
            if perct:
                perct_no = perct.group(1)
                if int(perct_no) == 0:
                    print ("Ping {} isn't success at {}".format(ip_data, login_device["host"]))
                    assert True
                else:
                    print ("Failed : Ping  {} is success at {}".format(ip_data, login_device["host"]))
                    assert False
    ### Routing Cases (END) ####

    ### System Cases ####
    def wr_mem_output(self, login_device):
        """
        ssh login to devices output : show commands 
        """
        output_c = self.ssh_out.wr_mem_cfg(login_device)
        if "[OK]" in output_c:
            print ("wr mem at device {}".format(login_device["host"]))
            assert True
        else:
            print ("Failed: to wr mem at device {}".format(login_device["host"]))
            assert False
    ### System Cases (END)####


class Mikrossh_output():

    def __init__(self):
        self.logger = logging.getLogger()
        self.mssh_out = Mikrossh()

    ### Interface Cases ####
    def ssh_login_show_ouput(self, login_device, execute_cmd):
        """
        ssh login to devices output : show commands 
        """
        check_output = self.ssh_out.ssh_login_show(login_device, execute_cmd)
        cisco_product = False
        if str(execute_cmd) == "show version":
            for output in check_output:
                if "Cisco Systems" in output:
                    print("{} device is a CISCO product ".format(login_device["host"]))
                    cisco_product = True
                    break

            if cisco_product:
                assert True , "Its Cisco product"
            else:
                assert False , "Its n't Cisco product"

    def m_execute_show_ouput(self, login_device, execute_cmds, host_name):
        """
        ssh login to devices output : show commands 
        """
        self.mssh_out.m_execute_show_commands(login_device, execute_cmds, host_name)


class Cumulusssh_output():

    def __init__(self):
        self.logger = logging.getLogger()
        self.cssh_out = Cumulusssh()

    ### Interface Cases ####
    def ssh_login_show_ouput(self, login_device, execute_cmd):
        """
        ssh login to devices output : show commands 
        """
        check_output = self.ssh_out.ssh_login_show(login_device, execute_cmd)
        cisco_product = False
        if str(execute_cmd) == "show version":
            for output in check_output:
                if "Cisco Systems" in output:
                    print("{} device is a CISCO product ".format(login_device["host"]))
                    cisco_product = True
                    break

            if cisco_product:
                assert True , "Its Cisco product"
            else:
                assert False , "Its n't Cisco product"

    def c_execute_show_ouput(self, login_device, execute_cmds, host_name):
        """
        ssh login to devices output : show commands 
        """
        self.cssh_out.c_execute_show_commands(login_device, execute_cmds, host_name)
