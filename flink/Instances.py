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

from troposphere import FindInMap
from troposphere import Ref
from troposphere.ec2 import Instance
from troposphere.ec2 import NetworkInterfaceProperty
import Metadatas
import Networking
import Parameters
import SecurityGroups


def task_manager(n):
    return Instance(
        "TaskManager%2.2d" % n,
        InstanceType=Ref(Parameters.instance_type),
        KeyName=Ref(Parameters.key_name),
        ImageId=FindInMap(
            "AWSRegionArch2AMI",
            Ref("AWS::Region"),
            FindInMap(
                "AWSInstanceType2Arch",
                Ref(Parameters.instance_type),
                "Arch"
            )
        ),
        NetworkInterfaces=[
            NetworkInterfaceProperty(
                GroupSet=[
                    Ref(SecurityGroups.sg_ssh),
                    Ref(SecurityGroups.sg_taskmanager),
                ],
                AssociatePublicIpAddress='true',
                DeviceIndex='0',
                DeleteOnTermination='true',
                SubnetId=Ref(Networking.sn_task_manager)
            )
        ],
        Metadata=Metadatas.tm_metadata
    )


def job_manager():
    return Instance(
        "JobManager",
        InstanceType=Ref(Parameters.instance_type),
        SecurityGroups=[
            Ref(SecurityGroups.sg_ssh),
            Ref(SecurityGroups.sg_jobmanager),
        ],
        KeyName=Ref(Parameters.key_name),
        ImageId=FindInMap(
            "AWSRegionArch2AMI",
            Ref("AWS::Region"),
            FindInMap(
                "AWSInstanceType2Arch",
                Ref(Parameters.instance_type),
                "Arch"
            )
        ),
        NetworkInterfaces=[
            NetworkInterfaceProperty(
                GroupSet=[
                    Ref(SecurityGroups.sg_ssh),
                    Ref(SecurityGroups.sg_jobmanager),
                ],
                AssociatePublicIpAddress='true',
                DeviceIndex='0',
                DeleteOnTermination='true',
                SubnetId=Ref(Networking.sn_job_manager)
            ),
            NetworkInterfaceProperty(
                GroupSet=[
                    Ref(SecurityGroups.sg_ssh),
                    Ref(SecurityGroups.sg_taskmanager),
                ],
                AssociatePublicIpAddress='true',
                DeviceIndex='1',
                DeleteOnTermination='true',
                SubnetId=Ref(Networking.sn_task_manager)
            ),
        ],
        Metadata=Metadatas.jm_metadata
    )
