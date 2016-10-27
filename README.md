
kafkatunnel.py
============
Access kafka (zookeeper) via ssh tunnel to consume and produce messages from your local machine

After hours of unsuccessful searching for a solution to tunnel kafka instances inside of AWS/ec2 instances, I created my own little script.

Requirements
------------
You need python3 in order to use kafkatunnel.py

* python3
* pip3

Install
-------

    $ make

Usage
-----

    $ kafkatunnel ec2-user@awsjumphost
