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

from troposphere import Template
import datetime
import instances
import mappings
import networking
import outputs
import parameters
import securitygroups

TEMPLATE_DESCRIPTION = "Composes a Flink cluster on AWS"
TEMPLATE_VERSION = "2010-09-09"
LAST_UPDATE = datetime.datetime.now().strftime('%c')


def _generate_template(tms=1, within_vpc=False):
    t = Template()

    t.add_description(TEMPLATE_DESCRIPTION)
    t.add_version(TEMPLATE_VERSION)
    t.add_metadata({'LastUpdated': LAST_UPDATE})

    # mappings
    mappings.add_mappings(t)

    # parameters
    parameters.add_parameters(t)

    # security groups
    securitygroups.add_resources(t)

    if within_vpc:
        # networking resources
        networking.add_resources(t)

    jobmanager = t.add_resource(instances.jobmanager(within_vpc=within_vpc))
    prefix = "JobManager00"
    t.add_output(outputs.instance_id(jobmanager, prefix))
    t.add_output(outputs.az(jobmanager, prefix))
    t.add_output(outputs.public_dns(jobmanager, prefix))
    t.add_output(outputs.public_ip(jobmanager, prefix))

    for n in range(0, tms):
        i = t.add_resource(instances.taskmanager(n, jobmanager, within_vpc))
        prefix = "TaskManager%2.2d" % n
        t.add_output(outputs.instance_id(i, prefix))
        t.add_output(outputs.az(i, prefix))
        t.add_output(outputs.public_dns(i, prefix))
        t.add_output(outputs.public_ip(i, prefix))

    return t.to_json()


def simple(tms=1):
    return _generate_template(tms, within_vpc=False)


def within_vpc(tms=1):
    return _generate_template(tms, within_vpc=True)
