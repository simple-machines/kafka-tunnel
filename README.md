
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

    zookeeper  on 10.11.85.128    port  2181
    zookeeper  on 10.11.82.30     port  2181
    zookeeper  on 10.11.83.9      port  2181
    kafka      on 10.11.80.7      port  2181
    kafka      on 10.11.80.123    port  2181
    kafka      on 10.11.81.13     port  2181
     * adding interface, user password might be needed
    Password:
    connecting to jump host
    Last login: Thu Oct 27 05:16:58 2016 from 203.44.116.49

       __|  __|_  )
       _|  (     /   Amazon Linux AMI
      ___|\___|___|

    [ec2-user@ip-10-13-89-119 ~]$ 
    
    $ kafka-topics --zookeeper 10.11.85.128:2181 --list
    
    
    

