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

from troposphere import Join
from troposphere.cloudformation import Init
from troposphere.cloudformation import InitConfig
from troposphere.cloudformation import InitFile
from troposphere.cloudformation import InitFiles
from troposphere.cloudformation import InitService
from troposphere.cloudformation import InitServices
from troposphere.cloudformation import Metadata

# commons settings

_packages = {
    "yum": {
        "httpd": [],
        "git": [],
        "wget": []
    }
}

_sources = {
    "/tmp/flink.tgz": ("http://www.apache.org/dyn/closer.lua/flink/" +
                       "flink-1.0.3/flink-1.0.3-bin-hadoop27-scala_2.11.tgz")
}

users = {
    "flink": {
        "groups": ["flink"],
        "uid": "100",
        "homeDir": "/home/flink"
    }
}

groups = {
   "flink": {}
}

services = {}

# JobManager settings

lines = []
with open("files/flink-conf.yaml", "r") as f:
    lines = f.readlines()
    f.close()

flink_conf_yaml = InitFile(
    content=Join("", lines),
    mode="0644",
    owner="flink",
    group="flink"
)

packages = _packages.copy()
packages["yum"].update({
    "nmap": []
})

sources = _sources.copy()
sources.update({
    "/foo/bar.txt": "http://www.example.com/bar.txt"
})

jm_metadata = Metadata(
    Init({
        "config": InitConfig(
            packages=packages,
            files=InitFiles({
                "/opt/flink/conf/flink-conf.yaml": flink_conf_yaml
            }),
            commands={
                "000-create-flink-base-dir": {
                    "command": "/usr/bin/mkdir -p /opt/flink",
                },
                "001-extract-flink-binaries": {
                    "command": "tar zxvf /tmp/flink.tgz"
                }
            },
            services=services,
            users=users,
            groups=groups,
            sources=sources
        )
    })
)

# TaskManager settings

packages = _packages.copy()

sources = _sources.copy()
sources.update({
    "/foo/bar.txt": "http://www.example.com/bar.txt",
    "/foo/barXXX.txt": "http://www.example.com/barXXX.txt",
})

tm_metadata = Metadata(
    Init({
        "config": InitConfig(
            packages=packages,
            commands={
                "000-create-flink-base-dir": {
                    "command": "/usr/bin/mkdir -p /opt/flink",
                },
                "001-extract-flink-binaries": {
                    "command": "tar zxvf /tmp/flink.tgz"
                }
            },
            services=services,
            users=users,
            groups=groups,
            sources=sources
        )
    })
)
