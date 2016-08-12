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
from troposphere.ec2 import InternetGateway
from troposphere.ec2 import NetworkAcl
from troposphere.ec2 import Route
from troposphere.ec2 import RouteTable
from troposphere.ec2 import Subnet
from troposphere.ec2 import SubnetNetworkAclAssociation
from troposphere.ec2 import SubnetRouteTableAssociation
from troposphere.ec2 import VPC
from troposphere.ec2 import VPCGatewayAttachment

# cluster VPC
vpc_flink = VPC(
    'FlinkVPC',
    CidrBlock="10.0.0.0/16",
)

# JobManager subnet
sn_job_manager = Subnet(
    'JobManagerSubnet',
    CidrBlock="10.0.1.0/24",
    VpcId=Ref(vpc_flink),
)

# TaskManager subnet
sn_task_manager = Subnet(
    'TaskManagerSubnet',
    CidrBlock="10.0.2.0/24",
    VpcId=Ref(vpc_flink),
)

# Gateways
internet_gw = InternetGateway(
    'InternetGateway',
)

vpc_gw = VPCGatewayAttachment(
    'VpcGateway',
    VpcId=Ref(vpc_flink),
    InternetGatewayId=Ref(internet_gw)
)

# Routing
routing_table = RouteTable(
    'RoutingTable',
    VpcId=Ref(vpc_flink),
)

route = Route(
    'Route',
    DependsOn="VpcGateway",
    GatewayId=Ref(internet_gw),
    DestinationCidrBlock='0.0.0.0/0',
    RouteTableId=Ref(routing_table),
)

sn_job_manager_routing_table = SubnetRouteTableAssociation(
    'JobManagerSubnetRouteTableAssociation',
    SubnetId=Ref(sn_job_manager),
    RouteTableId=Ref(routing_table),
)

# JobManager Network ACL
nwacl_job_manager = NetworkAcl(
    'JobManagerNetworkAcl',
    VpcId=Ref(vpc_flink),
)

# ... populate ACL...

nwacl_sn_job_manager = SubnetNetworkAclAssociation(
    'JobManagerSubnetNetworkAclAssociation',
    SubnetId=Ref(sn_job_manager),
    NetworkAclId=Ref(nwacl_job_manager),
)


# TaskManager Network ACL
nwacl_task_manager = NetworkAcl(
    'TaskManagerNetworkAcl',
    VpcId=Ref(vpc_flink),
)

# ... populate ACL...

nwacl_sn_task_manager = SubnetNetworkAclAssociation(
    'TaskManagerSubnetNetworkAclAssociation',
    SubnetId=Ref(sn_task_manager),
    NetworkAclId=Ref(nwacl_task_manager),
)


def add_resources(t):
    t.add_resource(vpc_flink)
    t.add_resource(internet_gw)
    t.add_resource(vpc_gw)
    t.add_resource(routing_table)
    t.add_resource(route)
    t.add_resource(sn_job_manager_routing_table)

    t.add_resource(sn_job_manager)
    t.add_resource(nwacl_job_manager)
    t.add_resource(nwacl_sn_job_manager)

    t.add_resource(sn_task_manager)
    t.add_resource(nwacl_task_manager)
    t.add_resource(nwacl_sn_task_manager)

"""

route = t.add_resource(
))

subnetRouteTableAssociation = t.add_resource(
))

networkAcl = t.add_resource(
Tags=Tags(
Application=ref_stack_id),
))

inBoundPrivateNetworkAclEntry = t.add_resource(
NetworkAclEntry(
'InboundHTTPNetworkAclEntry',
NetworkAclId=Ref(networkAcl),
RuleNumber='100',
Protocol='6',
PortRange=PortRange(To='80', From='80'),
Egress='false',
RuleAction='allow',
CidrBlock='0.0.0.0/0',
))

inboundSSHNetworkAclEntry = t.add_resource(
NetworkAclEntry(
'InboundSSHNetworkAclEntry',
NetworkAclId=Ref(networkAcl),
RuleNumber='101',
Protocol='6',
PortRange=PortRange(To='22', From='22'),
Egress='false',
RuleAction='allow',
CidrBlock='0.0.0.0/0',
))

inboundResponsePortsNetworkAclEntry = t.add_resource(
NetworkAclEntry(
'InboundResponsePortsNetworkAclEntry',
NetworkAclId=Ref(networkAcl),
RuleNumber='102',
Protocol='6',
PortRange=PortRange(To='65535', From='1024'),
Egress='false',
RuleAction='allow',
CidrBlock='0.0.0.0/0',
))

outBoundHTTPNetworkAclEntry = t.add_resource(
NetworkAclEntry(
'OutBoundHTTPNetworkAclEntry',
NetworkAclId=Ref(networkAcl),
RuleNumber='100',
Protocol='6',
PortRange=PortRange(To='80', From='80'),
Egress='true',
RuleAction='allow',
CidrBlock='0.0.0.0/0',
))

outBoundHTTPSNetworkAclEntry = t.add_resource(
NetworkAclEntry(
'OutBoundHTTPSNetworkAclEntry',
NetworkAclId=Ref(networkAcl),
RuleNumber='101',
Protocol='6',
PortRange=PortRange(To='443', From='443'),
Egress='true',
RuleAction='allow',
CidrBlock='0.0.0.0/0',
))

outBoundResponsePortsNetworkAclEntry = t.add_resource(
NetworkAclEntry(
'OutBoundResponsePortsNetworkAclEntry',
NetworkAclId=Ref(networkAcl),
RuleNumber='102',
Protocol='6',
PortRange=PortRange(To='65535', From='1024'),
Egress='true',
RuleAction='allow',
CidrBlock='0.0.0.0/0',
))

subnetNetworkAclAssociation = t.add_resource(
SubnetNetworkAclAssociation(
'SubnetNetworkAclAssociation',
SubnetId=Ref(subnet),
NetworkAclId=Ref(networkAcl),
))
"""
