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

JOB_MANAGER_INAME = "JobManagerInstance"
TASK_MANAGER_INAME = "TaskManagerInstance"


def taskmanager(index, jobmanager, securitygroups=[], within_vpc=False):
    iname = "%s%2.2d" % (TASK_MANAGER_INAME, index)
    return Instance(
        iname,
        InstanceType=Ref(parameters.taskmanager_instance_type),
        SecurityGroups=securitygroups,
        KeyName=Ref(parameters.key_name),
        ImageId=FindInMap(
            "AWSRegionArch2AMI",
            Ref("AWS::Region"),
            FindInMap(
                "AWSInstanceType2Arch",
                Ref(parameters.taskmanager_instance_type),
                "Arch"
            )
        ),
        Metadata=metadatas.taskmanager(jobmanager=jobmanager),
        UserData=Base64(
            Join('', [
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
            ])
        ),
    )


def jobmanager(index=0, securitygroups=[], within_vpc=False):
    iname = "%s%2.2d" % (JOB_MANAGER_INAME, index)
    return Instance(
        iname,
        InstanceType=Ref(parameters.jobmanager_instance_type),
        SecurityGroups=securitygroups,
        KeyName=Ref(parameters.key_name),
        ImageId=FindInMap(
            "AWSRegionArch2AMI",
            Ref("AWS::Region"),
            FindInMap(
                "AWSInstanceType2Arch",
                Ref(parameters.jobmanager_instance_type),
                "Arch"
            )
        ),
        Metadata=metadatas.jobmanager(),
        UserData=Base64(
            Join('', [
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
            ])
        ),
    )

# CreationPolicy=CreationPolicy(
# ResourceSignal=ResourceSignal(
# Timeout='PT15M'
# )
# ),
