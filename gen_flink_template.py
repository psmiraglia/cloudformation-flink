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
    parser.add_argument(
        "-V",
        "--with-vpc",
        help="Enable VPC",
        action="store_true")
    args = parser.parse_args()

    tms = int(args.tms)
    output = args.output
    with_vpc = args.with_vpc

    template = ""
    if with_vpc:
        template = templates.with_vpc(tms)
    else:
        template = templates.without_vpc(tms)

    if output is None:
        print(template)
    else:
        with open(output, "w+") as f:
            f.write(template)
            f.close()

if __name__ == "__main__":
    main()
