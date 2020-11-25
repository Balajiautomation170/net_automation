import sys
import os
import pytest
import json
import logging
import time
import bz2
from library.device.basic.cfg_output.lib_cisco_login_output import Ciscossh_output

logging.basicConfig(level=logging.DEBUG)


class Test_login_to_devices():

    @pytest.fixture(scope='class', autouse=True)
    def initial_setup (self, request):
        """
        Set the variables at global
        """
        request.cls.logger = logging.getLogger()
        request.cls.comm_path = ""
        request.cls.feat_path = ""
        request.cls.comm_path = sys.path[1] + "/testcases/cisco/input_data/common_input.json"
        request.cls.feat_path = sys.path[1] + "/testcases/cisco/input_data/feature_input_rip.json"
        request.cls.common_input_js = open(request.cls.comm_path, "r")
        request.cls.feature_input_js = open(request.cls.feat_path, "r")
        request.cls.common_input_dict = request.cls.common_input_js.read()
        request.cls.common_input = json.loads(request.cls.common_input_dict)
        request.cls.feature_input_dict = request.cls.feature_input_js.read()
        request.cls.feature_input = json.loads(request.cls.feature_input_dict)
        request.cls.all_devices = request.cls.common_input["cisco_devices"]["login_details"]
        request.cls.feature_config = request.cls.feature_input["group_configuration"]
        request.cls.feature_show = request.cls.feature_input["show_commands"]
        request.cls.cli_out = Routerssh_output()

    def test001_ssh_login_show_ouput(self):
        """
        Devices : login into all show version ,show ip int
        """
        for det in self.all_devices:
            self.cli_out.ssh_login_show_ouput(det, self.feature_show[0])

    def test002_configure_interface(self):
        """
        Devices : login into all show version ,show ip int
        """
        for det in self.all_devices:
            host_cfg = det["host"]
            self.cli_out.config_interface_out(det, self.feature_config[host_cfg])

    def test003_enable_check_rip(self):
        """
        Devices : login into all show version ,show ip int
        """
        for det in self.all_devices:
            host_cfg = det["host"]
            self.cli_out.enable_rip_out(det, self.feature_config[host_cfg])
        time.sleep(180)
        for det in self.all_devices:
            host_cfg = det["host"]
            self.cli_out.check_rip_database_out(det, self.feature_config[host_cfg])
            self.cli_out.check_ip_route_out(det, self.feature_config[host_cfg])
            self.cli_out.check_ping_out(det, self.feature_config[host_cfg])

    def test004_disable_interface(self):
        """
        Devices : login into all show version ,show ip int
        """
        for det in self.all_devices:
            host_cfg = det["host"]
            self.cli_out.disable_interface_out(det, self.feature_config[host_cfg])

    def test005_disable_check_rip(self):
        """
        
        Devices : Disable router rip
        """
        for det in self.all_devices:
            host_cfg = det["host"]
            self.cli_out.disable_rip_out(det, self.feature_config[host_cfg])
        time.sleep(5)
        for det in self.all_devices:
            host_cfg = det["host"]
            self.cli_out.check_ip_route_out_non_exist(det, self.feature_config[host_cfg])
            self.cli_out.check_ping_out_non_exist(det, self.feature_config[host_cfg])
            self.cli_out.wr_mem_output(det)
