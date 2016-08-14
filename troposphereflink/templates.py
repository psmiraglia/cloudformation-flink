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
from troposphere import Template
from troposphere.ec2 import InternetGateway
from troposphere.ec2 import NetworkAcl
from troposphere.ec2 import Route
from troposphere.ec2 import RouteTable
from troposphere.ec2 import Subnet
from troposphere.ec2 import SubnetNetworkAclAssociation
from troposphere.ec2 import SubnetRouteTableAssociation
from troposphere.ec2 import VPC
from troposphere.ec2 import VPCGatewayAttachment
import datetime
import instances
import mappings
import outputs
import parameters
import securitygroups

TEMPLATE_DESCRIPTION = "Composes a Flink cluster on AWS"
TEMPLATE_VERSION = "2010-09-09"
LAST_UPDATE = datetime.datetime.now().strftime('%c')


def _define_vpc(t, **kwargs):
    vpc = t.add_resource(VPC(
        "FlinkVpc",
        CidrBlock="10.0.0.0/16",
    ))

    igw = t.add_resource(InternetGateway(
        "FlinkInternetGateway",
    ))

    agw = t.add_resource(VPCGatewayAttachment(
        "FlinkVpcAttachmentGateway",
        VpcId=Ref(vpc),
        InternetGatewayId=Ref(igw)
    ))

    #
    # private subnet (taskmanagers)
    #

    subnet_pri = t.add_resource(Subnet(
        "FlinkPrivateSubnet",
        CidrBlock="10.0.1.0/24",
        VpcId=Ref(vpc),
    ))

    # routes...

    rt_pri = t.add_resource(RouteTable(
        "FlinkPrivateRouteTable",
        VpcId=Ref(vpc),
    ))

    t.add_resource(SubnetRouteTableAssociation(
        "FlinkPrivateSubnetRouteTableAssociation",
        SubnetId=Ref(subnet_pri),
        RouteTableId=Ref(rt_pri)
    ))

    t.add_resource(Route(
        "FlinkPrivateRoute",
        RouteTableId=Ref(rt_pri),
        DestinationCidrBlock="0.0.0.0/0",
    ))

    # acl...

    nwacl_pri = t.add_resource(NetworkAcl(
        "FlinkPrivateNetworkAcl",
        VpcId=Ref(vpc),
    ))

    t.add_resource(SubnetNetworkAclAssociation(
        "FlinkPrivateSubnetNetworkAclAssociation",
        SubnetId=Ref(subnet_pri),
        NetworkAclId=Ref(nwacl_pri)
    ))

    #
    # public subnet (jobmanagers)
    #

    subnet_pub = t.add_resource(Subnet(
        "FlinkPublicSubnet",
        CidrBlock="10.0.2.0/24",
        VpcId=Ref(vpc),
    ))

    # routes...

    rt_pub = t.add_resource(RouteTable(
        "FlinkPublicRouteTable",
        VpcId=Ref(vpc),
    ))

    t.add_resource(SubnetRouteTableAssociation(
        "FlinkPublicSubnetRouteTableAssociation",
        SubnetId=Ref(subnet_pub),
        RouteTableId=Ref(rt_pub)
    ))

    t.add_resource(Route(
        "FlinkPublicRoute",
        RouteTableId=Ref(rt_pub),
        DestinationCidrBlock="0.0.0.0/0",
    ))

    # acl...

    nwacl_pub = t.add_resource(NetworkAcl(
        "FlinkPublicNetworkAcl",
        VpcId=Ref(vpc),
    ))

    t.add_resource(SubnetNetworkAclAssociation(
        "FlinkPublicSubnetNetworkAclAssociation",
        SubnetId=Ref(subnet_pub),
        NetworkAclId=Ref(nwacl_pub)
    ))

    return (vpc, subnet_pri, subnet_pub)


def _generate_template(tms=1, within_vpc=False):
    t = Template()

    t.add_description(TEMPLATE_DESCRIPTION)
    t.add_version(TEMPLATE_VERSION)
    t.add_metadata({'LastUpdated': LAST_UPDATE})

    # mappings
    mappings.add_mappings(t)

    # parameters
    parameters.add_parameters(t)

    vpc = None
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
        within_vpc
    ))

    prefix = "JobManager00"
    t.add_output(outputs.instance_id(jobmanager, prefix))
    t.add_output(outputs.az(jobmanager, prefix))
    t.add_output(outputs.public_dns(jobmanager, prefix))
    t.add_output(outputs.public_ip(jobmanager, prefix))

    for index in range(0, tms):
        i = t.add_resource(instances.taskmanager(
            index,
            jobmanager,
            [Ref(sg_ssh), Ref(sg_taskmanager)],
            within_vpc
        ))
        prefix = "TaskManager%2.2d" % index
        t.add_output(outputs.instance_id(i, prefix))
        t.add_output(outputs.az(i, prefix))
        t.add_output(outputs.public_dns(i, prefix))
        t.add_output(outputs.public_ip(i, prefix))

    return t.to_json()


def simple(tms=1):
    return _generate_template(tms, within_vpc=False)


def within_vpc(tms=1):
    return _generate_template(tms, within_vpc=True)
