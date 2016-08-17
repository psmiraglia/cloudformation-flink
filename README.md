# cloudformation-flink
Setup your own Apache Flink cluster on AWS with CloudFormation.

## Environment setup

    $ git clone https://github.com/psmiraglia/cloudformation-flink.git
    $ cd cloudformation-flink
    $ virtualenv .venv
    $ pip install -r requirements.txt

## Run it

Generate a template for a cluster with four TaskManagers and save it in
`myflinkcluster.template` file.

    $ ./gen_flink_template.py --task-managers 4 -o myflinkcluster.template

Generate a template for a cluster within a VPC with four TaskManagers and save
it in `myflinkcluster.template` file.

    $ ./gen_flink_template.py -t 4 --within-vpc -o myflinkcluster.template

To get more info

    $ ./gen_flink_template.py -h

## References

* [Apache Flink](https://flink.apache.org)
* [AWS CloudFormation](https://aws.amazon.com/cloudformation)
* [Troposphere](https://github.com/cloudtools/troposphere)
