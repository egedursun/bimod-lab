#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: ssh_connection_mtest.py
#  Last Modified: 2024-08-07 16:37:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:37:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#

import json
from pprint import pprint

import paramiko
from paramiko import SSHClient


def parse_ls_r_output(output):
    lines = output.strip().split('\n')
    root = {}
    current_dir = root
    dir_stack = [root]

    for line in lines:
        if line.endswith(':'):
            current_path = line[:-1]
            dirs = current_path.split('/')
            if current_path.startswith('.'):
                current_dir = root
                for d in dirs[1:]:
                    current_dir = current_dir.setdefault(d, {})
                dir_stack = dir_stack[:len(dirs)]
                dir_stack.append(current_dir)
            else:
                current_dir = dir_stack[-1]
        else:
            if line:
                current_dir[line] = {}

    return root


ssh_connection_host = "185.170.198.44"
ssh_port = 22
ssh_username = "root"
ssh_password = "t@G0trEhboeOWWDSi5Bg"


ssh = SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ssh_connection_host, port=ssh_port, username=ssh_username, password=ssh_password, banner_timeout=200)
stdin, stdout, stderr = ssh.exec_command("ls -R")
# replacte all one or more linebreaks with regex
file_directory_tree = stdout.read().decode()
# convert directory tree to json
directory_dict = json.dumps(parse_ls_r_output(file_directory_tree), default=str)
current_directory = ""


stdin.close()
stdout.close()
stderr.close()
ssh.close()

pprint(directory_dict)
