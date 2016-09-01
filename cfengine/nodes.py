"""
The MIT License (MIT)

Copyright (c) 2016 Paolo Smiraglia <paolo.smiraglia@gmail.com>

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
from troposphere import Base64
from troposphere import Join
from troposphere import FindInMap
from troposphere.ec2 import Instance
from troposphere.ec2 import NetworkInterfaceProperty
from troposphere.policies import CreationPolicy
from troposphere.policies import ResourceSignal
import commons
import parameters
import metadatas


def _get_image_id(key):
    return FindInMap("AWSRegionArch2AMI", Ref("AWS::Region"),
                     FindInMap("AWSInstanceType2Arch", key, "Arch"))


def _get_user_data(instance_name):
    cfg_set = "InstallConfigureRun"
    return Base64(Join('', [
        "#!/bin/bash -xe\n",
        "yum update -y aws-cfn-bootstrap\n",
        "# Install the files and packages from the metadata\n",
        "/opt/aws/bin/cfn-init -v ",
        "         --stack ", Ref("AWS::StackName"),
        "         --resource %s " % instance_name,
        "         --configsets %s " % cfg_set,
        "         --region ", Ref("AWS::Region"),
        "\n",
        "# Signal the status from cfn-init\n",
        "/opt/aws/bin/cfn-signal -e $? ",
        "         --stack ", Ref("AWS::StackName"),
        "         --resource %s " % instance_name,
        "         --region ", Ref("AWS::Region"),
        "\n"
    ]))


class FlinkClusterNode(object):

    def __init__(self, instance_name, securitygroups, vpc, subnet, *args,
                 **kwargs):
        self.instance_name = instance_name
        self.securitygroups = securitygroups
        self.vpc = vpc
        self.subnet = subnet
        self.instance_type = None
        self.image_id = None
        self.metadata = None

    def to_resource(self):

        c_policy = CreationPolicy(
            ResourceSignal=ResourceSignal(Timeout="PT15M")
        )

        if self.vpc and self.subnet:
            i = Instance(
                # common settings
                self.instance_name,
                InstanceType=self.instance_type,
                KeyName=Ref(parameters.key_name),
                ImageId=self.image_id,
                CreationPolicy=c_policy,
                UserData=_get_user_data(self.instance_name),
                Metadata=self.metadata,
                # VPC specific
                NetworkInterfaces=[
                    NetworkInterfaceProperty(
                        AssociatePublicIpAddress='true',
                        DeleteOnTermination='true',
                        DeviceIndex='0',
                        GroupSet=self.securitygroups,
                        SubnetId=Ref(self.subnet),
                    )
                ],
                DependsOn=[
                    commons.FLINK_NAT
                ]
            )
        else:
            i = Instance(
                # common settings
                self.instance_name,
                InstanceType=self.instance_type,
                KeyName=Ref(parameters.key_name),
                ImageId=self.image_id,
                CreationPolicy=c_policy,
                UserData=_get_user_data(self.instance_name),
                Metadata=self.metadata,
                # standalone specific
                SecurityGroups=self.securitygroups
            )
        return i


class JobManagerNode(FlinkClusterNode):

    def __init__(self, securitygroups, vpc, subnet, *args, **kwargs):
        super(JobManagerNode, self).__init__(
            "JobManager", securitygroups, vpc, subnet, *args, **kwargs
        )

        self.metadata = metadatas.JobManagerMetadata().to_resource()
        self.instance_type = Ref(parameters.jobmanager_instance_type)
        self.image_id = _get_image_id(Ref(parameters.jobmanager_instance_type))


class TaskManagerNode(FlinkClusterNode):

    def __init__(self, jm, index, securitygroups, vpc, subnet, *args,
                 **kwargs):
        super(TaskManagerNode, self).__init__(
            ("TaskManager%3.3d" % index), securitygroups, vpc, subnet,
            *args, **kwargs
        )
        self.metadata = metadatas.TaskManagerMetadata(jm).to_resource()
        self.instance_type = Ref(parameters.taskmanager_instance_type)
        self.image_id = _get_image_id(
            Ref(parameters.taskmanager_instance_type)
        )
