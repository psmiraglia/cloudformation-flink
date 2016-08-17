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

from troposphere import Parameter

key_name = Parameter(
    "KeyName",
    Description=("Name of an existing EC2 KeyPair " +
                 "to enable SSH access to the instance"),
    Type="AWS::EC2::KeyPair::KeyName",
    ConstraintDescription="Must be the name of an existing EC2 KeyPair"
)

jobmanager_instance_type = Parameter(
    "JobManagerInstanceType",
    Description="JobManager EC2 instance type",
    Type="String",
    Default="t1.micro",
    AllowedValues=["t1.micro", "t2.nano", "t2.micro", "t2.small", "t2.medium",
                   "t2.large", "m1.small", "m1.medium", "m1.large",
                   "m1.xlarge", "m2.xlarge", "m2.2xlarge", "m2.4xlarge",
                   "m3.medium", "m3.large", "m3.xlarge", "m3.2xlarge",
                   "m4.large", "m4.xlarge", "m4.2xlarge", "m4.4xlarge",
                   "m4.10xlarge", "c1.medium", "c1.xlarge", "c3.large",
                   "c3.xlarge", "c3.2xlarge", "c3.4xlarge", "c3.8xlarge",
                   "c4.large", "c4.xlarge", "c4.2xlarge", "c4.4xlarge",
                   "c4.8xlarge", "g2.2xlarge", "g2.8xlarge", "r3.large",
                   "r3.xlarge", "r3.2xlarge", "r3.4xlarge", "r3.8xlarge",
                   "i2.xlarge", "i2.2xlarge", "i2.4xlarge", "i2.8xlarge",
                   "d2.xlarge", "d2.2xlarge", "d2.4xlarge", "d2.8xlarge",
                   "hi1.4xlarge", "hs1.8xlarge", "cr1.8xlarge", "cc2.8xlarge",
                   "cg1.4xlarge"],
    ConstraintDescription="Must be a valid EC2 instance type"
)

taskmanager_instance_type = Parameter(
    "TaskManagerInstanceType",
    Description="TaskManager EC2 instance type",
    Type="String",
    Default="t1.micro",
    AllowedValues=["t1.micro", "t2.nano", "t2.micro", "t2.small", "t2.medium",
                   "t2.large", "m1.small", "m1.medium", "m1.large",
                   "m1.xlarge", "m2.xlarge", "m2.2xlarge", "m2.4xlarge",
                   "m3.medium", "m3.large", "m3.xlarge", "m3.2xlarge",
                   "m4.large", "m4.xlarge", "m4.2xlarge", "m4.4xlarge",
                   "m4.10xlarge", "c1.medium", "c1.xlarge", "c3.large",
                   "c3.xlarge", "c3.2xlarge", "c3.4xlarge", "c3.8xlarge",
                   "c4.large", "c4.xlarge", "c4.2xlarge", "c4.4xlarge",
                   "c4.8xlarge", "g2.2xlarge", "g2.8xlarge", "r3.large",
                   "r3.xlarge", "r3.2xlarge", "r3.4xlarge", "r3.8xlarge",
                   "i2.xlarge", "i2.2xlarge", "i2.4xlarge", "i2.8xlarge",
                   "d2.xlarge", "d2.2xlarge", "d2.4xlarge", "d2.8xlarge",
                   "hi1.4xlarge", "hs1.8xlarge", "cr1.8xlarge", "cc2.8xlarge",
                   "cg1.4xlarge"],
    ConstraintDescription="Must be a valid EC2 instance type"
)

nat_instance_type = Parameter(
    "NATInstanceType",
    Description="NAT EC2 instance type",
    Type="String",
    Default="t1.micro",
    AllowedValues=["t1.micro", "t2.nano", "t2.micro", "t2.small", "t2.medium",
                   "t2.large", "m1.small", "m1.medium", "m1.large",
                   "m1.xlarge", "m2.xlarge", "m2.2xlarge", "m2.4xlarge",
                   "m3.medium", "m3.large", "m3.xlarge", "m3.2xlarge",
                   "m4.large", "m4.xlarge", "m4.2xlarge", "m4.4xlarge",
                   "m4.10xlarge", "c1.medium", "c1.xlarge", "c3.large",
                   "c3.xlarge", "c3.2xlarge", "c3.4xlarge", "c3.8xlarge",
                   "c4.large", "c4.xlarge", "c4.2xlarge", "c4.4xlarge",
                   "c4.8xlarge", "g2.2xlarge", "g2.8xlarge", "r3.large",
                   "r3.xlarge", "r3.2xlarge", "r3.4xlarge", "r3.8xlarge",
                   "i2.xlarge", "i2.2xlarge", "i2.4xlarge", "i2.8xlarge",
                   "d2.xlarge", "d2.2xlarge", "d2.4xlarge", "d2.8xlarge",
                   "hi1.4xlarge", "hs1.8xlarge", "cr1.8xlarge", "cc2.8xlarge",
                   "cg1.4xlarge"],
    ConstraintDescription="Must be a valid EC2 instance type"
)

ssh_location = Parameter(
    "SSHLocation",
    Description=("The IP address range that can be used" +
                 "to SSH to the EC2 instances"),
    Type="String",
    MinLength="9",
    MaxLength="18",
    Default="0.0.0.0/0",
    AllowedPattern=("(\\d{1,3})\\.(\\d{1,3})" +
                    "\\.(\\d{1,3})\\.(\\d{1,3})/(\\d{1,2})"),
    ConstraintDescription=("Must be a valid IP CIDR range " +
                           "of the form x.x.x.x/x")
)

http_location = Parameter(
    "HTTPLocation",
    Description=("The IP address range that can be used" +
                 "to HTTP to the EC2 instances"),
    Type="String",
    MinLength="9",
    MaxLength="18",
    Default="0.0.0.0/0",
    AllowedPattern=("(\\d{1,3})\\.(\\d{1,3})" +
                    "\\.(\\d{1,3})\\.(\\d{1,3})/(\\d{1,2})"),
    ConstraintDescription=("Must be a valid IP CIDR range " +
                           "of the form x.x.x.x/x")
)

flink_version = Parameter(
    "FlinkVersion",
    Description="Flink's version to be installed",
    Type="String",
    Default="flink1.1.1-hadoop27-scala2.11",
    AllowedValues=[
        "flink1.0.3-hadoop2-scala2.11",
        "flink1.0.3-hadoop24-scala2.10",
        "flink1.0.3-hadoop24-scala2.11",
        "flink1.0.3-hadoop26-scala2.10",
        "flink1.0.3-hadoop26-scala2.11",
        "flink1.0.3-hadoop27-scala2.10",
        "flink1.0.3-hadoop27-scala2.11",
        "flink1.1.0-hadoop2-scala2.10",
        "flink1.1.0-hadoop2-scala2.11",
        "flink1.1.0-hadoop24-scala2.10",
        "flink1.1.0-hadoop24-scala2.11",
        "flink1.1.0-hadoop26-scala2.10",
        "flink1.1.0-hadoop26-scala2.11",
        "flink1.1.0-hadoop27-scala2.10",
        "flink1.1.0-hadoop27-scala2.11",
        "flink1.1.1-hadoop2-scala2.10",
        "flink1.1.1-hadoop2-scala2.11",
        "flink1.1.1-hadoop24-scala2.10",
        "flink1.1.1-hadoop24-scala2.11",
        "flink1.1.1-hadoop26-scala2.10",
        "flink1.1.1-hadoop26-scala2.11",
        "flink1.1.1-hadoop27-scala2.10",
        "flink1.1.1-hadoop27-scala2.11",
    ]
)


def add_parameters(t):
    t.add_parameter(flink_version)
    t.add_parameter(http_location)
    t.add_parameter(jobmanager_instance_type)
    t.add_parameter(key_name)
    t.add_parameter(nat_instance_type)
    t.add_parameter(ssh_location)
    t.add_parameter(taskmanager_instance_type)
