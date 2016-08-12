"""
The MIT License (MIT)

Copyright (c) 2016 Paolo Smiraglia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from troposphere import Ref
from troposphere.ec2 import SecurityGroup
from troposphere.ec2 import SecurityGroupRule
import networking
import parameters

ssh = SecurityGroup(
    "SSHSecurityGroup",
    GroupDescription="Enable SSH access via port 22",
    SecurityGroupIngress=[
        SecurityGroupRule(
            IpProtocol="tcp",
            FromPort="22",
            ToPort="22",
            CidrIp=Ref(parameters.ssh_location)
        )
    ],
    # VpcId=Ref(networking.vpc_flink)
)

jobmanager = SecurityGroup(
    "JobManagerSecurityGroup",
    GroupDescription="Regulates the accesses to JobManager",
    SecurityGroupIngress=[
        SecurityGroupRule(
            IpProtocol="tcp",
            FromPort="6123",
            ToPort="6123",
            CidrIp="0.0.0.0/0"
        ),
        SecurityGroupRule(
            IpProtocol="tcp",
            FromPort="8081",
            ToPort="8081",
            CidrIp=Ref(parameters.http_location)
        )
    ],
    # VpcId=Ref(networking.vpc_flink)
)

taskmanager = SecurityGroup(
    "TaskManagerSecurityGroup",
    GroupDescription="Regulates the accesses to TaskManager",
    SecurityGroupIngress=[],
    # VpcId=Ref(networking.vpc_flink)
)


def add_resources(t):
    t.add_resource(ssh)
    t.add_resource(jobmanager)
    t.add_resource(taskmanager)
