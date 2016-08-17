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

from troposphere import GetAtt
from troposphere import Output
from troposphere import Ref


def instance_id(instance, prefix):
    return Output(
        "%sInstanceId" % (prefix),
        Description="InstanceId of the newly created EC2 instance",
        Value=Ref(instance)
    )


def az(instance, prefix):
    return Output(
        "%sAvailabilityZone" % (prefix),
        Description="availability Zone of the newly created EC2 instance",
        Value=GetAtt(instance, "AvailabilityZone")
    )


def public_dns(instance, prefix):
    return Output(
        "%sPublicDnsName" % (prefix),
        Description="Public DNSName of the newly created EC2 instance",
        Value=GetAtt(instance, "PublicDnsName")
    )


def public_ip(instance, prefix):
    return Output(
        "%sPublicIp" % (prefix),
        Description="Public IP address of the newly created EC2 instance",
        Value=GetAtt(instance, "PublicIp")
    )


def ssh_to(instance, prefix, bastion=None):
    out = None
    if bastion is not None:
        out = Output(
            "SSH2%s" % prefix,
            Description="SSH connection string",
            Value=Join("", ['slogin -o ProxyCommand="slogin ec2-user@',
                            GetAtt(bastion, "PublicDnsName"),
                            ' -W %h:%p" ec2-user@',
                            GetAtt(instance, "PrivateDnsName")])
        )
    else:
        out = Output(
            "SSH2%s" % prefix,
            Description="SSH connection string",
            Value=Join("", ['slogin ec2-user@',
                            GetAtt(instance, "PublicDnsName")])
        )
    return out
