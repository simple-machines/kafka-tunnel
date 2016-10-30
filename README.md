
kafkatunnel.py
============
Access kafka/zookeeper via ssh tunnel to consume and produce messages from your local machine

After hours of unsuccessful searching for a solution to tunnel kafka instances inside of AWS/ec2 instances, I created my own little script.

Requirements
------------
You need python3 in order to use kafkatunnel.py

* python3
* pip3

**Note:** for AWS mode: you need to tag your ec2 zookeeper and kafka instances with Name=kafka/zookeper

see https://aws.amazon.com/premiumsupport/knowledge-center/ec2-resource-tags/

Install
-------

    $ git clone https://github.com/simple-machines/kafka-tunnel
    $ make

Usage
-----

`kafkatool.py` supports two ways of passing the remote zookeeper/kafka ip's:

* automatic retrival by ec2 resource tags (Name=zookeeper/kafka)

    $ kafkatunnel aws ec2-user@awsjumphost

* manual passing the ip's

    $ kafkatunnel manual 10.11.85.128,10.11.82.30,10.11.83.9 10.11.80.7,10.11.80.123,10.11.81.13

afterwards you have to provide your root password in order to create the interfaces

    zookeeper  on 10.11.85.128    port  2181
    zookeeper  on 10.11.82.30     port  2181
    zookeeper  on 10.11.83.9      port  2181
    kafka      on 10.11.80.7      port  9091
    kafka      on 10.11.80.123    port  9091
    kafka      on 10.11.81.13     port  9091
     * adding interface, user password might be needed
    Password:
    connecting to jump host
    Last login: Thu Oct 27 05:16:58 2016 from 203.44.116.49

       __|  __|_  )
       _|  (     /   Amazon Linux AMI
      ___|\___|___|

    [ec2-user@ip-10-13-89-119 ~]$

On a second screen just do whatever you want, e.g. list all topics.

    $ kafka-topics --zookeeper 10.11.85.128:2181 --list
