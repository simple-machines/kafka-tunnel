#!/usr/bin/env python3
import click
import boto3
import sys
import subprocess


@click.command()
@click.argument('jump_host')
@click.option('-zp','--zookeeper_port',default='2181')
@click.option('-kp','--kafka_port',default='9091')
@click.option('-r','--region',default='ap-southeast-2')
@click.option('-p','--profile',default='default')
def cli(jump_host, zookeeper_port, kafka_port, region, profile):
    instances=[]
    click.echo('accessing kafka & zookeeper via ssh ...')
    boto3.setup_default_session(profile_name=profile)
    instances += req_instances('zookeeper', zookeeper_port, region)
    instances += req_instances('kafka', kafka_port, region)
    print_instances(instances)
    add_local_interfaces(instances)
    connect_ssh_tunnel(jump_host,instances)
    remove_local_interfaces(instances)

def req_instances(service, port, region):
    instances=[]
    for ec2_ip in req_aws_ips(service, region):
        instances.append(Instance(name=service,ip=ec2_ip,port=port))
    return instances

aws_filter = lambda name,value: [{'Name':'tag:'+name,'Values':[value]}]

def req_aws_ips(service, region):
    ips=[]
    client = boto3.client('ec2')
    response = client.describe_instances(Filters=aws_filter('Name',service))
    for res in response.get('Reservations'):
        for instance in res.get('Instances'):
            ips.append(instance.get(u'PrivateIpAddress'))
    return ips

def add_local_interfaces(instances):
    click.echo(' * adding interface, user password might be needed')
    for instance in instances:
        if sys.platform == 'darwin':
            cmd = ['sudo', 'ifconfig', 'lo0', 'alias', instance.ip]
        else:
            cmd = ['sudo', 'ip', 'add', 'a', 'dev', 'lo', instance.ip]
        subprocess.call(cmd)

def remove_local_interfaces(instances):
    click.echo(' * removing interface, user password might be needed')
    for instance in instances:
        if sys.platform == 'darwin':
            cmd = ['sudo', 'ifconfig', 'lo0', '-alias', instance.ip]
        else:
            cmd = ['sudo', 'ip', 'del', 'a', 'dev', 'lo', instance.ip]
        subprocess.call(cmd)

def print_instances(instances):
    click.echo('')
    for i in instances:
        click.echo('{:<10} on {:<15} port {:>5}'.format(i.name,i.ip,i.port))
    click.echo('')

def connect_ssh_tunnel(jump_host,instances):
    click.echo('connecting to jump host')
    opts = []
    for i in instances:
        opts += ['-L','{ip}:{port}:{ip}:{port}'.format(ip=i.ip,port=i.port)]
    subprocess.call(['ssh'] + opts + [jump_host])

class Instance:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port

if __name__ == '__main__':
    cli()
