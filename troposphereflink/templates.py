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

from commons import *
from troposphere import Base64
from troposphere import FindInMap
from troposphere import GetAtt
from troposphere import Join
from troposphere import Output
from troposphere import Ref
from troposphere import Template
from troposphere.ec2 import Instance
from troposphere.ec2 import InternetGateway
from troposphere.ec2 import NetworkAcl
from troposphere.ec2 import NetworkInterfaceProperty
from troposphere.ec2 import Route
from troposphere.ec2 import RouteTable
from troposphere.ec2 import SecurityGroup
from troposphere.ec2 import SecurityGroupIngress
from troposphere.ec2 import SecurityGroupRule
from troposphere.ec2 import Subnet
from troposphere.ec2 import SubnetNetworkAclAssociation
from troposphere.ec2 import SubnetRouteTableAssociation
from troposphere.ec2 import VPC
from troposphere.ec2 import VPCGatewayAttachment
from troposphere.policies import CreationPolicy
from troposphere.policies import ResourceSignal
import datetime
import instances
import mappings
import outputs
import parameters
import securitygroups


def _define_vpc(t, **kwargs):
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

    # acl (todo)
    """
    nwacl_pub = t.add_resource(NetworkAcl(
        "FlinkPublicNetworkAcl",
        VpcId=Ref(vpc),
    ))

    t.add_resource(SubnetNetworkAclAssociation(
        "FlinkPublicSubnetNetworkAclAssociation",
        SubnetId=Ref(subnet_pub),
        NetworkAclId=Ref(nwacl_pub)
    ))
    """

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

    # acl (todo)
    """
    nwacl_pri = t.add_resource(NetworkAcl(
        "FlinkPrivateNetworkAcl",
        VpcId=Ref(vpc),
    ))

    t.add_resource(SubnetNetworkAclAssociation(
        "FlinkPrivateSubnetNetworkAclAssociation",
        SubnetId=Ref(subnet_pri),
        NetworkAclId=Ref(nwacl_pri)
    ))
    """

    return (vpc, subnet_pri, subnet_pub)


def _generate_template(tms=1, within_vpc=False):
    t = Template()

    t.add_description(FLINK_TEMPLATE_DESCRIPTION)
    t.add_version(FLINK_TEMPLATE_VERSION)
    t.add_metadata({'LastUpdated': datetime.datetime.now().strftime('%c')})

    # mappings
    mappings.add_mappings(t)

    # parameters
    parameters.add_parameters(t)

    vpc = None
    subnet_pri = None
    subnet_pub = None
    if within_vpc:
        # networking resources
        vpc, subnet_pri, subnet_pub = _define_vpc(t)

    # security groups
    sg_ssh = t.add_resource(securitygroups.ssh(
        parameters.ssh_location, vpc))

    sg_jobmanager = t.add_resource(securitygroups.jobmanager(
        parameters.http_location, vpc))

    sg_taskmanager = t.add_resource(securitygroups.taskmanager(None, vpc))

    jobmanager = t.add_resource(instances.jobmanager(
        0,
        [Ref(sg_ssh), Ref(sg_jobmanager)],
        within_vpc,
        subnet_pub
    ))

    prefix = "JobManager00"
    t.add_output(outputs.ssh_to(jobmanager, prefix))
    t.add_output(Output(
        "FlinkWebGui",
        Description="Flink web interface",
        Value=Join("", [
            'http://', GetAtt(jobmanager, "PublicDnsName"), ':8081'
        ])
    ))

    for index in range(0, tms):
        i = t.add_resource(instances.taskmanager(
            index,
            jobmanager,
            [Ref(sg_ssh), Ref(sg_taskmanager)],
            within_vpc,
            subnet_pri
        ))
        prefix = "TaskManager%2.2d" % index
        t.add_output(outputs.ssh_to(i, prefix, bastion=jobmanager))

    return t.to_json()


def simple(tms=1):
    return _generate_template(tms, within_vpc=False)


def within_vpc(tms=1):
    return _generate_template(tms, within_vpc=True)
