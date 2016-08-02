#!/usr/bin/env python

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

from troposphere import FindInMap
from troposphere import Parameter
from troposphere import Ref
from troposphere import Template
import Instances
import Mappings
import Outputs
import Parameters
import SecurityGroups
import Networking
import argparse
import troposphere.ec2 as ec2

TEMPLATE_DESCRIPTION = "Composes a Flink cluster on AWS"
TEMPLATE_VERSION = "2010-09-09"


def generate_template(tms=1):
    t = Template()

    t.add_description(TEMPLATE_DESCRIPTION)
    t.add_version(TEMPLATE_VERSION)

    # mappings
    Mappings.add_mappings(t)

    # parameters
    Parameters.add_parameters(t)

    # networking resources
    Networking.add_resources(t)

    # security groups
    SecurityGroups.add_resources(t)

    """
    job_manager = t.add_resource(Instances.job_manager())
    prefix = "JM"
    t.add_output(Outputs.instance_id(job_manager, prefix))
    t.add_output(Outputs.az(job_manager, prefix))
    t.add_output(Outputs.public_dns(job_manager, prefix))
    t.add_output(Outputs.public_ip(job_manager, prefix))

    for n in range(0, tms):
        i = t.add_resource(Instances.task_manager(n))
        prefix = "TM"
        t.add_output(Outputs.instance_id(i, prefix, n))
        t.add_output(Outputs.az(i, prefix, n))
        t.add_output(Outputs.public_dns(i, prefix, n))
        t.add_output(Outputs.public_ip(i, prefix, n))
    """

    return t


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--tms",
        default="1",
        help="Number of TaskManager's"
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output template file")
    args = parser.parse_args()

    tms = int(args.tms)
    output = args.output

    t = generate_template(tms)
    template = t.to_json()

    if output is None:
        print(template)
    else:
        with open(output, "w+") as f:
            f.write(template)
            f.close()

if __name__ == "__main__":
    main()
