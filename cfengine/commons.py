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

# engine version

_MAJOR = 0
_MINOR = 2
_PATCH = 0
VERSION = "%d.%d.%d" % (_MAJOR, _MINOR, _PATCH)

TEMPLATE_DESCRIPTION = "Composes a Flink cluster on AWS"
AWS_TEMPLATE_VERSION = "2010-09-09"

FLINK_INTERNET_GATEWAY = "FlinkInternetGateway"
FLINK_NAT = "FlinkNATInstance"
FLINK_NAT_SECURITY_GROUP = "FlinkNATSecurityGroup"
FLINK_PRIVATE_ROUTE_TABLE = "FlinkPrivateRouteTable"
FLINK_PRIVATE_SUBNET = "FlinkPrivateSubnet"
FLINK_PUBLIC_ROUTE_TABLE = "FlinkPublicRouteTable"
FLINK_PUBLIC_SUBNET = "FlinkPublicSubnet"
FLINK_VPC = "FlinkVpc"
FLINK_VPC_GATEWAY_ATTACHMENT = "FlinkVpcAttachmentGateway"

SG_SSH = "SSHSecurityGroup"
SG_JM = "JobManagerSecurityGroup"
SG_TM = "TaskManagerSecurityGroup"
