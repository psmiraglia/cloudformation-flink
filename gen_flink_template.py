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

from troposphereflink import templates
import argparse
import troposphereflink
import sys

DEFAULT_TASK_MANAGERS = 2
DEFAULT_JOB_MANAGERS = 1


def main():

    parser = argparse.ArgumentParser(
        description=("Generates an AWS CloudFormation template " +
                     "to setup a Flink cluster."))

    parser.add_argument(
        "-v",
        "--version",
        help="show version and exit",
        action="store_true")

    parser.add_argument(
        "-t",
        "--task-managers",
        type=int,
        default=DEFAULT_TASK_MANAGERS,
        help=("number of TaskManager instances in the cluster (defautl: %d)" %
              DEFAULT_TASK_MANAGERS)
    )

    parser.add_argument(
        "-j",
        "--job-managers",
        type=int,
        default=DEFAULT_JOB_MANAGERS,
        help=("number of JobManager instances in the cluster (defautl: %d)" %
              DEFAULT_JOB_MANAGERS)
    )

    parser.add_argument(
        "-o",
        "--output",
        help="CloudFormation template OUTPUT file")

    parser.add_argument(
        "--within-vpc",
        help="create the cluster within a VPC",
        action="store_true")

    args = parser.parse_args()

    if args.version:
        print(troposphereflink.VERSION)
        sys.exit(0)

    tms = args.task_managers
    output = args.output
    within_vpc = args.within_vpc

    template = ""
    if within_vpc:
        template = templates.within_vpc(tms)
    else:
        template = templates.simple(tms)

    if output is None:
        print(template)
    else:
        with open(output, "w+") as f:
            f.write(template)
            f.close()

if __name__ == "__main__":
    main()
