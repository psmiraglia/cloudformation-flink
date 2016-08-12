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

"""
Maps defined in

    https://s3-us-west-2.amazonaws.com/cloudformation-templates-us-west-2/
        EC2InstanceWithSecurityGroupSample.template
"""

AWSInstanceType2Arch = {
    "t1.micro": {"Arch": "PV64"},
    "t2.nano": {"Arch": "HVM64"},
    "t2.micro": {"Arch": "HVM64"},
    "t2.small": {"Arch": "HVM64"},
    "t2.medium": {"Arch": "HVM64"},
    "t2.large": {"Arch": "HVM64"},
    "m1.small": {"Arch": "PV64"},
    "m1.medium": {"Arch": "PV64"},
    "m1.large": {"Arch": "PV64"},
    "m1.xlarge": {"Arch": "PV64"},
    "m2.xlarge": {"Arch": "PV64"},
    "m2.2xlarge": {"Arch": "PV64"},
    "m2.4xlarge": {"Arch": "PV64"},
    "m3.medium": {"Arch": "HVM64"},
    "m3.large": {"Arch": "HVM64"},
    "m3.xlarge": {"Arch": "HVM64"},
    "m3.2xlarge": {"Arch": "HVM64"},
    "m4.large": {"Arch": "HVM64"},
    "m4.xlarge": {"Arch": "HVM64"},
    "m4.2xlarge": {"Arch": "HVM64"},
    "m4.4xlarge": {"Arch": "HVM64"},
    "m4.10xlarge": {"Arch": "HVM64"},
    "c1.medium": {"Arch": "PV64"},
    "c1.xlarge": {"Arch": "PV64"},
    "c3.large": {"Arch": "HVM64"},
    "c3.xlarge": {"Arch": "HVM64"},
    "c3.2xlarge": {"Arch": "HVM64"},
    "c3.4xlarge": {"Arch": "HVM64"},
    "c3.8xlarge": {"Arch": "HVM64"},
    "c4.large": {"Arch": "HVM64"},
    "c4.xlarge": {"Arch": "HVM64"},
    "c4.2xlarge": {"Arch": "HVM64"},
    "c4.4xlarge": {"Arch": "HVM64"},
    "c4.8xlarge": {"Arch": "HVM64"},
    "g2.2xlarge": {"Arch": "HVMG2"},
    "g2.8xlarge": {"Arch": "HVMG2"},
    "r3.large": {"Arch": "HVM64"},
    "r3.xlarge": {"Arch": "HVM64"},
    "r3.2xlarge": {"Arch": "HVM64"},
    "r3.4xlarge": {"Arch": "HVM64"},
    "r3.8xlarge": {"Arch": "HVM64"},
    "i2.xlarge": {"Arch": "HVM64"},
    "i2.2xlarge": {"Arch": "HVM64"},
    "i2.4xlarge": {"Arch": "HVM64"},
    "i2.8xlarge": {"Arch": "HVM64"},
    "d2.xlarge": {"Arch": "HVM64"},
    "d2.2xlarge": {"Arch": "HVM64"},
    "d2.4xlarge": {"Arch": "HVM64"},
    "d2.8xlarge": {"Arch": "HVM64"},
    "hi1.4xlarge": {"Arch": "HVM64"},
    "hs1.8xlarge": {"Arch": "HVM64"},
    "cr1.8xlarge": {"Arch": "HVM64"},
    "cc2.8xlarge": {"Arch": "HVM64"}
}

AWSInstanceType2NATArch = {
    "t1.micro": {"Arch": "NATPV64"},
    "t2.nano": {"Arch": "NATHVM64"},
    "t2.micro": {"Arch": "NATHVM64"},
    "t2.small": {"Arch": "NATHVM64"},
    "t2.medium": {"Arch": "NATHVM64"},
    "t2.large": {"Arch": "NATHVM64"},
    "m1.small": {"Arch": "NATPV64"},
    "m1.medium": {"Arch": "NATPV64"},
    "m1.large": {"Arch": "NATPV64"},
    "m1.xlarge": {"Arch": "NATPV64"},
    "m2.xlarge": {"Arch": "NATPV64"},
    "m2.2xlarge": {"Arch": "NATPV64"},
    "m2.4xlarge": {"Arch": "NATPV64"},
    "m3.medium": {"Arch": "NATHVM64"},
    "m3.large": {"Arch": "NATHVM64"},
    "m3.xlarge": {"Arch": "NATHVM64"},
    "m3.2xlarge": {"Arch": "NATHVM64"},
    "m4.large": {"Arch": "NATHVM64"},
    "m4.xlarge": {"Arch": "NATHVM64"},
    "m4.2xlarge": {"Arch": "NATHVM64"},
    "m4.4xlarge": {"Arch": "NATHVM64"},
    "m4.10xlarge": {"Arch": "NATHVM64"},
    "c1.medium": {"Arch": "NATPV64"},
    "c1.xlarge": {"Arch": "NATPV64"},
    "c3.large": {"Arch": "NATHVM64"},
    "c3.xlarge": {"Arch": "NATHVM64"},
    "c3.2xlarge": {"Arch": "NATHVM64"},
    "c3.4xlarge": {"Arch": "NATHVM64"},
    "c3.8xlarge": {"Arch": "NATHVM64"},
    "c4.large": {"Arch": "NATHVM64"},
    "c4.xlarge": {"Arch": "NATHVM64"},
    "c4.2xlarge": {"Arch": "NATHVM64"},
    "c4.4xlarge": {"Arch": "NATHVM64"},
    "c4.8xlarge": {"Arch": "NATHVM64"},
    "g2.2xlarge": {"Arch": "NATHVMG2"},
    "g2.8xlarge": {"Arch": "NATHVMG2"},
    "r3.large": {"Arch": "NATHVM64"},
    "r3.xlarge": {"Arch": "NATHVM64"},
    "r3.2xlarge": {"Arch": "NATHVM64"},
    "r3.4xlarge": {"Arch": "NATHVM64"},
    "r3.8xlarge": {"Arch": "NATHVM64"},
    "i2.xlarge": {"Arch": "NATHVM64"},
    "i2.2xlarge": {"Arch": "NATHVM64"},
    "i2.4xlarge": {"Arch": "NATHVM64"},
    "i2.8xlarge": {"Arch": "NATHVM64"},
    "d2.xlarge": {"Arch": "NATHVM64"},
    "d2.2xlarge": {"Arch": "NATHVM64"},
    "d2.4xlarge": {"Arch": "NATHVM64"},
    "d2.8xlarge": {"Arch": "NATHVM64"},
    "hi1.4xlarge": {"Arch": "NATHVM64"},
    "hs1.8xlarge": {"Arch": "NATHVM64"},
    "cr1.8xlarge": {"Arch": "NATHVM64"},
    "cc2.8xlarge": {"Arch": "NATHVM64"}
}

AWSRegionArch2AMI = {
    "us-east-1": {"PV64": "ami-2a69aa47", "HVM64": "ami-6869aa05",
                  "HVMG2": "ami-2e5e9c43"},
    "us-west-2": {"PV64": "ami-7f77b31f", "HVM64": "ami-7172b611",
                  "HVMG2": "ami-83b770e3"},
    "us-west-1": {"PV64": "ami-a2490dc2", "HVM64": "ami-31490d51",
                  "HVMG2": "ami-fd76329d"},
    "eu-west-1": {"PV64": "ami-4cdd453f", "HVM64": "ami-f9dd458a",
                  "HVMG2": "ami-b9bd25ca"},
    "eu-central-1": {"PV64": "ami-6527cf0a", "HVM64": "ami-ea26ce85",
                     "HVMG2": "ami-7f04ec10"},
    "ap-northeast-1": {"PV64": "ami-3e42b65f", "HVM64": "ami-374db956",
                       "HVMG2": "ami-e0ee1981"},
    "ap-northeast-2": {"PV64": "NOT_SUPPORTED", "HVM64": "ami-2b408b45",
                       "HVMG2": "NOT_SUPPORTED"},
    "ap-southeast-1": {"PV64": "ami-df9e4cbc", "HVM64": "ami-a59b49c6",
                       "HVMG2": "ami-0cb5676f"},
    "ap-southeast-2": {"PV64": "ami-63351d00", "HVM64": "ami-dc361ebf",
                       "HVMG2": "ami-a71c34c4"},
    "sa-east-1": {"PV64": "ami-1ad34676", "HVM64": "ami-6dd04501",
                  "HVMG2": "NOT_SUPPORTED"},
    "cn-north-1": {"PV64": "ami-77559f1a", "HVM64": "ami-8e6aa0e3",
                   "HVMG2": "NOT_SUPPORTED"}
}

FlinkVersion2Env = {
    "flink1.1.0-hadoop27-scala2.11": {
        "dirname": "flink-1.1.0",
        "binurl": (
            "http://www-us.apache.org/dist/flink/flink-1.1.0/" +
            "flink-1.1.0-bin-hadoop27-scala_2.11.tgz"
        )
    },
    "flink1.1.0-hadoop27-scala2.10": {
        "dirname": "flink-1.1.0",
        "binurl": (
            "http://www-us.apache.org/dist/flink/flink-1.1.0/" +
            "flink-1.1.0-bin-hadoop27-scala_2.10.tgz"
        )
    },
    "flink1.1.0-hadoop26-scala2.11": {
        "dirname": "flink-1.1.0",
        "binurl": (
            "http://www-us.apache.org/dist/flink/flink-1.1.0/" +
            "flink-1.1.0-bin-hadoop26-scala_2.11.tgz"
        )
    },
    "flink1.1.0-hadoop26-scala2.10": {
        "dirname": "flink-1.1.0",
        "binurl": (
            "http://www-us.apache.org/dist/flink/flink-1.1.0/" +
            "flink-1.1.0-bin-hadoop26-scala_2.10.tgz"
        )
    },
    "flink1.1.0-hadoop24-scala2.11": {
        "dirname": "flink-1.1.0",
        "binurl": (
            "http://www-us.apache.org/dist/flink/flink-1.1.0/" +
            "flink-1.1.0-bin-hadoop24-scala_2.11.tgz"
        )
    },
    "flink1.1.0-hadoop24-scala2.10": {
        "dirname": "flink-1.1.0",
        "binurl": (
            "http://www-us.apache.org/dist/flink/flink-1.1.0/" +
            "flink-1.1.0-bin-hadoop24-scala_2.10.tgz"
        )
    },
    "flink1.1.0-hadoop2-scala2.11": {
        "dirname": "flink-1.1.0",
        "binurl": (
            "http://www-us.apache.org/dist/flink/flink-1.1.0/" +
            "flink-1.1.0-bin-hadoop2-scala_2.11.tgz"
        )
    },
    "flink1.1.0-hadoop2-scala2.10": {
        "dirname": "flink-1.1.0",
        "binurl": (
            "http://www-us.apache.org/dist/flink/flink-1.1.0/" +
            "flink-1.1.0-bin-hadoop2-scala_2.10.tgz"
        )
    },
    "flink1.0.3-hadoop27-scala2.11": {
        "dirname": "flink-1.0.3",
        "binurl": (
            "http://www-us.apache.org/dist/flink/flink-1.0.3/" +
            "flink-1.0.3-bin-hadoop27-scala_2.11.tgz"
        )
    },
    "flink1.0.3-hadoop27-scala2.10": {
        "dirname": "flink-1.0.3",
        "binurl": (
            "http://www-us.apache.org/dist/flink/flink-1.0.3/" +
            "flink-1.0.3-bin-hadoop27-scala_2.10.tgz"
        )
    },
    "flink1.0.3-hadoop26-scala2.11": {
        "dirname": "flink-1.0.3",
        "binurl": (
            "http://www-us.apache.org/dist/flink/flink-1.0.3/" +
            "flink-1.0.3-bin-hadoop26-scala_2.11.tgz"
        )
    },
    "flink1.0.3-hadoop26-scala2.10": {
        "dirname": "flink-1.0.3",
        "binurl": (
            "http://www-us.apache.org/dist/flink/flink-1.0.3/" +
            "flink-1.0.3-bin-hadoop26-scala_2.10.tgz"
        )
    },
    "flink1.0.3-hadoop24-scala2.11": {
        "dirname": "flink-1.0.3",
        "binurl": (
            "http://www-us.apache.org/dist/flink/flink-1.0.3/" +
            "flink-1.0.3-bin-hadoop24-scala_2.11.tgz"
        )
    },
    "flink1.0.3-hadoop24-scala2.10": {
        "dirname": "flink-1.0.3",
        "binurl": (
            "http://www-us.apache.org/dist/flink/flink-1.0.3/" +
            "flink-1.0.3-bin-hadoop24-scala_2.10.tgz"
        )
    },
    "flink1.0.3-hadoop2-scala2.11": {
        "dirname": "flink-1.0.3",
        "binurl": (
            "http://www-us.apache.org/dist/flink/flink-1.0.3/" +
            "flink-1.0.3-bin-hadoop2-scala_2.11.tgz"
        )
    },
    "flink1.0.3-hadoop2-scala2.10": {
        "dirname": "flink-1.0.3",
        "binurl": (
            "http://www-us.apache.org/dist/flink/flink-1.0.3/" +
            "flink-1.0.3-bin-hadoop2-scala_2.10.tgz"
        )
    },
}


def add_mappings(t):
    t.add_mapping("AWSInstanceType2Arch", AWSInstanceType2Arch)
    t.add_mapping("AWSInstanceType2NATArch", AWSInstanceType2NATArch)
    t.add_mapping("AWSRegionArch2AMI", AWSRegionArch2AMI)
    t.add_mapping("FlinkVersion2Env", FlinkVersion2Env)
