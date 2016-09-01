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


from datetime import datetime
from troposphere.ec2 import Instance
from troposphere.ec2 import InternetGateway
from troposphere.ec2 import NetworkInterfaceProperty
from troposphere.ec2 import Route
from troposphere.ec2 import RouteTable
from troposphere.ec2 import SecurityGroup
from troposphere.ec2 import SecurityGroupRule
from troposphere.ec2 import Subnet
from troposphere.ec2 import SubnetRouteTableAssociation
from troposphere.ec2 import VPC
from troposphere.ec2 import VPCGatewayAttachment
from troposphere import Base64
from troposphere import FindInMap
from troposphere import GetAtt
from troposphere import Join
from troposphere import Output
from troposphere import Ref
from troposphere import Template
from troposphere.policies import CreationPolicy
from troposphere.policies import ResourceSignal
from commons import *
import mappings
import nodes
import outputs
import parameters
import securitygroups


def _define_vpc(t, *args, **kwargs):
    vpc = t.add_resource(VPC(
        FLINK_VPC,
        CidrBlock=FindInMap("FlinkCidrBlock", "vpc", "CIDR"),
        EnableDnsSupport=True,
        EnableDnsHostnames=True
    ))

    igw = t.add_resource(InternetGateway(
        FLINK_INTERNET_GATEWAY,
    ))

    agw = t.add_resource(VPCGatewayAttachment(
        FLINK_VPC_GATEWAY_ATTACHMENT,
        VpcId=Ref(vpc),
        InternetGatewayId=Ref(igw),
        DependsOn=[
            FLINK_VPC,
            FLINK_INTERNET_GATEWAY
        ]
    ))

    #
    # public subnet (jobmanagers + nat)
    #

    subnet_pub = t.add_resource(Subnet(
        FLINK_PUBLIC_SUBNET,
        CidrBlock=FindInMap("FlinkCidrBlock", "public", "CIDR"),
        VpcId=Ref(vpc),
    ))

    # routes

    rt_pub = t.add_resource(RouteTable(
        FLINK_PUBLIC_ROUTE_TABLE,
        VpcId=Ref(vpc),
    ))

    t.add_resource(SubnetRouteTableAssociation(
        "FlinkPublicSubnetRouteTableAssociation",
        SubnetId=Ref(subnet_pub),
        RouteTableId=Ref(rt_pub),
    ))

    t.add_resource(Route(
        "FlinkPublicRoute",
        RouteTableId=Ref(rt_pub),
        DestinationCidrBlock="0.0.0.0/0",
        GatewayId=Ref(igw),
    ))

    # nat

    sg_nat = t.add_resource(SecurityGroup(
        FLINK_NAT_SECURITY_GROUP,
        GroupDescription=(
            "It allows incoming connections on ports 0-1024 from private " +
            "subnet while on port 22 from SSHLocation parameter."
        ),
        VpcId=Ref(vpc),
        SecurityGroupIngress=[
            SecurityGroupRule(
                IpProtocol="tcp",
                FromPort="0",
                ToPort="1024",
                CidrIp=FindInMap("FlinkCidrBlock", "private", "CIDR")
            ),
            SecurityGroupRule(
                IpProtocol="udp",
                FromPort="0",
                ToPort="1024",
                CidrIp=FindInMap("FlinkCidrBlock", "private", "CIDR")
            ),
            SecurityGroupRule(
                IpProtocol="tcp",
                FromPort="22",
                ToPort="22",
                CidrIp=Ref(parameters.ssh_location)
            ),
        ],
    ))

    nat = t.add_resource(Instance(
        FLINK_NAT,
        SourceDestCheck=False,
        InstanceType=Ref(parameters.nat_instance_type),
        ImageId=FindInMap("AWSNATAMI", Ref("AWS::Region"), "AMI"),
        KeyName=Ref(parameters.key_name),
        NetworkInterfaces=[
            NetworkInterfaceProperty(
                DeleteOnTermination=True,
                Description="Primary network interface",
                DeviceIndex=0,
                SubnetId=Ref(subnet_pub),
                GroupSet=[Ref(sg_nat)],
                AssociatePublicIpAddress=True
            ),
        ],
        UserData=Base64(Join("", [
            "#!/bin/bash -xe\n",
            "yum update -y aws-cfn-bootstrap\n",
            "# Signal the status from cfn-init\n",
            "/opt/aws/bin/cfn-signal -e $? ",
            "         --stack ",
            Ref('AWS::StackName'),
            "         --resource %s\n" % FLINK_NAT,
            "         --region ",
            Ref("AWS::Region"),
            "\n"
        ])),
        CreationPolicy=CreationPolicy(
            ResourceSignal=ResourceSignal(Timeout="PT15M")
        )
    ))

    t.add_output(outputs.ssh_to(nat, FLINK_NAT))

    #
    # private subnet (taskmanagers)
    #

    subnet_pri = t.add_resource(Subnet(
        FLINK_PRIVATE_SUBNET,
        CidrBlock=FindInMap("FlinkCidrBlock", "private", "CIDR"),
        VpcId=Ref(vpc),
    ))

    # routes

    rt_pri = t.add_resource(RouteTable(
        FLINK_PRIVATE_ROUTE_TABLE,
        VpcId=Ref(vpc),
    ))

    t.add_resource(SubnetRouteTableAssociation(
        "FlinkPrivateSubnetRouteTableAssociation",
        SubnetId=Ref(subnet_pri),
        RouteTableId=Ref(rt_pri),
    ))

    t.add_resource(Route(
        "FlinkPrivateRoute",
        RouteTableId=Ref(rt_pri),
        DestinationCidrBlock="0.0.0.0/0",
        InstanceId=Ref(nat),
    ))

    return (vpc, subnet_pri, subnet_pub)


class BaseCluster(object):

    def __init__(self, n_tm, *args, **kwargs):
        self.n_tm = n_tm
        self.template = Template()
        self.template_metadata = {}

    def _define_vpc(self):
        raise NotImplementedError()

    def to_template(self):
        t = self.template
        t.add_description(TEMPLATE_DESCRIPTION)
        t.add_version(AWS_TEMPLATE_VERSION)
        self.template_metadata["LastUpdated"] = datetime.now().strftime('%c')
        self.template_metadata["TaskManager"] = self.n_tm
        t.add_metadata(self.template_metadata)

        # define mappings
        mappings.add_mappings(t)

        # define parameters
        parameters.add_parameters(t)

        # define vpc
        (vpc, subnet_pri, subnet_pub) = self._define_vpc()

        # define security groups
        sg_ssh = t.add_resource(
            securitygroups.ssh(parameters.ssh_location, vpc)
        )
        sg_jobmanager = t.add_resource(
            securitygroups.jobmanager(parameters.flink_web_location, vpc)
        )
        sg_taskmanager = t.add_resource(
            securitygroups.taskmanager(None, vpc)
        )

        # define jobmanager instance
        sgs = [Ref(sg_ssh), Ref(sg_jobmanager)]
        jm_obj = nodes.JobManagerNode(sgs, vpc, subnet_pub)
        jm = self.template.add_resource(jm_obj.to_resource())

        t.add_output(outputs.ssh_to(jm, jm_obj.instance_name))
        t.add_output(Output(
            "FlinkWebGui",
            Description="Flink web interface",
            Value=Join("", ['http://', GetAtt(jm, "PublicDnsName"), ':8081'])
        ))

        # define taskmanager instances
        sgs = [Ref(sg_ssh), Ref(sg_taskmanager)]
        for i in range(0, self.n_tm):
            tm_obj = nodes.TaskManagerNode(jm, i, sgs, vpc, subnet_pri)
            tm = t.add_resource(tm_obj.to_resource())
            t.add_output(outputs.ssh_to(tm, tm_obj.instance_name, jm))

        return t.to_json()


class StandaloneCluster(BaseCluster):

    def __init__(self, n_tm, *args, **kwargs):
        super(StandaloneCluster, self).__init__(n_tm, *args, **kwargs)
        self.template_metadata["WithinVpc"] = False

    def _define_vpc(self):
        return (None, None, None)


class VpcCluster(BaseCluster):

    def __init__(self, n_tm, *args, **kwargs):
        super(VpcCluster, self).__init__(n_tm, *args, **kwargs)
        self.template_metadata["WithinVpc"] = True

    def _define_vpc(self):
        return _define_vpc(self.template)
