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

from troposphere import Base64
from troposphere import FindInMap
from troposphere import Join
from troposphere import Ref
from troposphere.ec2 import Instance
from troposphere.ec2 import NetworkInterfaceProperty
from troposphere.policies import CreationPolicy
from troposphere.policies import ResourceSignal
import metadatas
import parameters
import securitygroups
from commons import *

JOB_MANAGER_INAME = "JobManagerInstance"
TASK_MANAGER_INAME = "TaskManagerInstance"


def taskmanager(index, jobmanager, securitygroups=[], within_vpc=False,
                subnet=None):
    iname = "%s%2.2d" % (TASK_MANAGER_INAME, index)
    instance_type = Ref(parameters.taskmanager_instance_type)
    key_name = Ref(parameters.key_name)
    image_id = FindInMap(
        "AWSRegionArch2AMI",
        Ref("AWS::Region"),
        FindInMap(
            "AWSInstanceType2Arch",
            Ref(parameters.taskmanager_instance_type),
            "Arch"
        )
    )
    user_data = Base64(Join('', [
        "#!/bin/bash -xe\n",
        "yum update -y aws-cfn-bootstrap\n",
        "# Install the files and packages from the metadata\n",
        "/opt/aws/bin/cfn-init -v ",
        "         --stack ",
        Ref("AWS::StackName"),
        "         --resource %s " % iname,
        "         --configsets InstallConfigureRun ",
        "         --region ",
        Ref("AWS::Region"),
        "\n",
        "# Signal the status from cfn-init\n",
        "/opt/aws/bin/cfn-signal -e $? ",
        "         --stack ",
        Ref("AWS::StackName"),
        "         --resource %s " % iname,
        "         --region ",
        Ref("AWS::Region"),
        "\n"
    ]))
    creation_policy = CreationPolicy(
        ResourceSignal=ResourceSignal(Timeout="PT15M")
    )
    metadata = metadatas.taskmanager(jobmanager=jobmanager)

    if within_vpc:
        network_interfaces = [
            NetworkInterfaceProperty(
                GroupSet=securitygroups,
                AssociatePublicIpAddress='true',
                DeviceIndex='0',
                DeleteOnTermination='true',
                SubnetId=Ref(subnet)
            )
        ]
        depends_on = [
            # FLINK_VPC,
            # FLINK_PRIVATE_SUBNET,
            # FLINK_PRIVATE_ROUTE_TABLE,
            FLINK_NAT
        ]

        return Instance(iname, InstanceType=instance_type,
                        NetworkInterfaces=network_interfaces,
                        KeyName=key_name, ImageId=image_id, Metadata=metadata,
                        UserData=user_data, CreationPolicy=creation_policy,
                        DependsOn=depends_on)
    else:
        return Instance(iname, InstanceType=instance_type,
                        SecurityGroups=securitygroups, KeyName=key_name,
                        ImageId=image_id, Metadata=metadata,
                        UserData=user_data, CreationPolicy=creation_policy)


def jobmanager(index=0, securitygroups=[], within_vpc=False, subnet=None):
    iname = "%s%2.2d" % (JOB_MANAGER_INAME, index)
    instance_type = Ref(parameters.jobmanager_instance_type)
    key_name = Ref(parameters.key_name)
    image_id = FindInMap(
        "AWSRegionArch2AMI",
        Ref("AWS::Region"),
        FindInMap(
            "AWSInstanceType2Arch",
            Ref(parameters.jobmanager_instance_type),
            "Arch"
        )
    )
    metadata = metadatas.jobmanager()
    user_data = Base64(Join('', [
        "#!/bin/bash -xe\n",
        "yum update -y aws-cfn-bootstrap\n",
        "# Install the files and packages from the metadata\n",
        "/opt/aws/bin/cfn-init -v ",
        "         --stack ",
        Ref("AWS::StackName"),
        "         --resource %s " % iname,
        "         --configsets InstallConfigureRun ",
        "         --region ",
        Ref("AWS::Region"),
        "\n",
        "# Signal the status from cfn-init\n",
        "/opt/aws/bin/cfn-signal -e $? ",
        "         --stack ",
        Ref("AWS::StackName"),
        "         --resource %s " % iname,
        "         --region ",
        Ref("AWS::Region"),
        "\n"
    ]))
    creation_policy = CreationPolicy(
        ResourceSignal=ResourceSignal(Timeout="PT15M")
    )

    if within_vpc:
        network_interfaces = [
            NetworkInterfaceProperty(
                GroupSet=securitygroups,
                AssociatePublicIpAddress='true',
                DeviceIndex='0',
                DeleteOnTermination='true',
                SubnetId=Ref(subnet)
            )
        ]
        depends_on = [
            # FLINK_VPC,
            # FLINK_INTERNET_GATEWAY,
            # FLINK_PUBLIC_SUBNET,
            # FLINK_PUBLIC_ROUTE_TABLE,
            FLINK_NAT
        ]
        return Instance(iname, InstanceType=instance_type,
                        NetworkInterfaces=network_interfaces,
                        KeyName=key_name, ImageId=image_id, Metadata=metadata,
                        UserData=user_data, CreationPolicy=creation_policy,
                        DependsOn=depends_on)
    else:
        return Instance(iname, InstanceType=instance_type,
                        SecurityGroups=securitygroups, KeyName=key_name,
                        ImageId=image_id, Metadata=metadata,
                        UserData=user_data, CreationPolicy=creation_policy)
