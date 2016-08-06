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
from troposphere import Join
from troposphere import Ref
from troposphere.cloudformation import Init
from troposphere.cloudformation import InitConfig
from troposphere.cloudformation import InitConfigSets
from troposphere.cloudformation import InitFile
from troposphere.cloudformation import InitFiles
from troposphere.cloudformation import InitService
from troposphere.cloudformation import InitServices
from troposphere.cloudformation import Metadata
import parameters

# common

install = InitConfig(
    sources={
        "/opt": FindInMap(
            "AWSRegion2FlinkBinary",
            Ref("AWS::Region"),
            Ref(parameters.flink_version)
        )
    }
)

# JobManager

jm_metadata = Metadata(
    Init(
        InitConfigSets(ICR=["install", "configure", "run"]),
        install=install,
        configure=InitConfig(
            # packages=packages,
            # groups=groups,
            # users=users,
            # sources=sources,
            # files=InitFiles({}),
            # commands=commands,
            # services=InitServices({}),
        ),
        run=InitConfig(
            # packages=packages,
            # groups=groups,
            # users=users,
            # sources=sources,
            # files=InitFiles({}),
            commands={
                "000-run": {
                    "command": "sudo bin/jobmanager.sh start cluster",
                    "cwd": "/opt/flink-1.0.3"
                }
            },
            # services=InitServices({}),
        ),
    )
)

# TaskManager
tm_metadata = Metadata(
    Init(
        InitConfigSets(ICR=["install", "configure", "run"]),
        install=install,
        configure=InitConfig(
            # packages=packages,
            # groups=groups,
            # users=users,
            # sources=sources,
            # files=InitFiles({}),
            # commands=commands,
            # services=InitServices({}),
        ),
        run=InitConfig(
            # packages=packages,
            # groups=groups,
            # users=users,
            # sources=sources,
            # files=InitFiles({}),
            commands={
                "000-run": {
                    "command": "sudo bin/taskmanager.sh start",
                    "cwd": "/opt/flink-1.0.3"
                }
            },
            # services=InitServices({}),
        ),
    )
)
