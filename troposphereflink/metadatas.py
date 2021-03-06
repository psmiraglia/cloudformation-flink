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
from troposphere import GetAtt
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

install_flink_binaries = InitConfig(
    sources={
        "/opt": FindInMap(
            "FlinkVersion2Env",
            Ref(parameters.flink_version),
            "binurl"
        )
    },
    files=InitFiles({
        "/opt/flink": InitFile(
            content=FindInMap(
                "FlinkVersion2Env",
                Ref(parameters.flink_version),
                "dirname"
            ),
            mode="120000"
        )
    }),
)

# JobManager


def jobmanager(**kwargs):
    return Metadata(Init(
            InitConfigSets(InstallConfigureRun=[
                "install",
                "configure",
                "run"]),
            install=install_flink_binaries,
            configure=InitConfig(
                files=InitFiles({
                    "/opt/flink/conf/flink-conf.yaml": InitFile(
                        content=Join("", [
                            "jobmanager.rpc.address: %HOSTNAME%\n",
                            "jobmanager.rpc.port: 6123\n",
                            "jobmanager.heap.mb: 256\n",
                            "taskmanager.heap.mb: 512\n",
                            "taskmanager.numberOfTaskSlots: 1\n",
                            "taskmanager.memory.preallocate: false\n",
                            "parallelism.default: 1\n",
                            "jobmanager.web.port: 8081\n",
                        ])
                    )
                }),
                commands={
                    "000-set-binding-hostname": {
                        "command": (
                            'sudo sed -i.bak "s/%HOSTNAME%/`' +
                            'curl http://169.254.169.254/latest/' +
                            'meta-data/local-ipv4`/g" conf/flink-conf.yaml'),
                        "cwd": "/opt/flink"
                    },
                },
            ),
            run=InitConfig(
                commands={
                    "000-run": {
                        "command": "sudo bin/jobmanager.sh start cluster",
                        "cwd": "/opt/flink"
                    }
                },
            ),
        )
    )

# TaskManager


def taskmanager(**kwargs):
    # temp
    jobmanager = kwargs["jobmanager"]
    #
    return Metadata(Init(
            InitConfigSets(InstallConfigureRun=[
                "install",
                "configure",
                "run"]),
            install=install_flink_binaries,
            configure=InitConfig(
                files=InitFiles({
                    "/opt/flink/conf/flink-conf.yaml": InitFile(
                        content=Join("", [
                            "jobmanager.rpc.address: ",
                            GetAtt(jobmanager, "PrivateIp"),
                            "\n",
                            "jobmanager.rpc.port: 6123\n",
                            "jobmanager.heap.mb: 256\n",
                            "taskmanager.heap.mb: 512\n",
                            "taskmanager.numberOfTaskSlots: 1\n",
                            "taskmanager.memory.preallocate: false\n",
                            "parallelism.default: 1\n",
                            "jobmanager.web.port: 8081\n",
                        ])
                    )
                }),
            ),
            run=InitConfig(
                commands={
                    "000-run": {
                        "command": "sudo bin/taskmanager.sh start",
                        "cwd": "/opt/flink"
                    }
                },
            ),
        )
    )
