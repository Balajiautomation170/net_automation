import sys
import os
import pytest
import json
import logging
import time
import bz2
from library.device.basic.cfg_output.lib_cisco_login_output import Ciscossh_output, Mikrossh_output, Cumulusssh_output

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
        request.cls.comm_path = os.environ["PYTHONPATH"] + "/testcases/device/input_data/common_input.json"
        request.cls.feat_path = os.environ["PYTHONPATH"] + "/testcases/device/input_data/feature_input_show.json"
        request.cls.common_input_js = open(request.cls.comm_path, "r")
        request.cls.feature_input_js = open(request.cls.feat_path, "r")
        request.cls.common_input_dict = request.cls.common_input_js.read()
        request.cls.common_input = json.loads(request.cls.common_input_dict)
        request.cls.feature_input_dict = request.cls.feature_input_js.read()
        request.cls.feature_input = json.loads(request.cls.feature_input_dict)
        request.cls.all_devices = request.cls.common_input["cisco_devices"]["login_details"]
        request.cls.feature_config = request.cls.feature_input["group_configuration"]
        request.cls.device_cli_out = Ciscossh_output()
        request.cls.mikro_cli_out = Mikrossh_output()

    def test001_ssh_login_show_ouput(self):
        """
        Devices : login into all show version ,show ip int
        """
        for det in self.all_devices:
            if det["device_type"] == "cisco_ios":
                show_commands = self.feature_config[host_cfg]
                self.cisco_cli_out.ssh_login_show_ouput(det, show_commands["show commands"])
            if det["device_type"] == "mikrotik-routeros":
                show_commands = self.feature_config[host_cfg]
                self.mikro_cli_out.ssh_login_show_ouput(det, show_commands["show commands"])

    def test002_show_commands(self):
        """
        Devices : login into all show version ,show ip int
        """
        for det in self.all_devices:
            host_cfg = det["host"]
            if det["device_type"] == "mikrotik_routeros":
                show_commands = self.feature_config[host_cfg]
                self.mikro_cli_out.m_execute_show_ouput(det, show_commands["show commands"], host_cfg)
            else:
                show_commands = self.feature_config[host_cfg]
                self.device_cli_out.execute_show_ouput(det, show_commands["show commands"], host_cfg)
