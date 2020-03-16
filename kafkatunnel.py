#!/usr/bin/env python3
import click
import sys
import subprocess

from Instance import ManualInstances, AWSInstances

@click.group(help='Access kafka/zookeeper via ssh tunnel to consume and produce messages from your local machine')
def cli():
    pass

@cli.command(help='retrieve kafka/zookeeper ip\'s from AWS (important: a resource tag with Name=kafka/zookeeper is needed)')
@click.argument('jump_host')
@click.option('-zp','--zookeeper_port',default='2181')
@click.option('-kp','--kafka_port',default='9092')
@click.option('-r','--region',default='ap-southeast-2')
@click.option('-p','--profile',default='default')
def aws(jump_host,zookeeper_port,kafka_port,region,profile):
    instances=[]
    click.echo(' * retrieving ip\'s from AWS ({},{}) zookeeper/kafka ec2 instances by tag_name ...'.format(profile,region))
    aws = AWSInstances(profile,region)
    instances += aws.getIps('zookeeper',zookeeper_port)
    instances += aws.getIps('kafka',kafka_port)
    connect(jump_host,instances)


@cli.command(help='provide the IP\'s of your zookeeper/kafka')
@click.argument('jump_host')
@click.argument('zookeeper_ips')
@click.argument('kafka_ips')
@click.argument('schemaregistry_ips',default='')
@click.option('-zp','--zookeeper_port',default='2181')
@click.option('-kp','--kafka_port',default='9092')
@click.option('-sp','--schemaregistry_port',default='8081')
def manual(jump_host,zookeeper_ips, kafka_ips, schemaregistry_ips, zookeeper_port, kafka_port, schemaregistry_port):
    instances=[]
    click.echo(' * using manual ip\'s ...')
    man = ManualInstances()
    instances += man.getIps('zookeeper',zookeeper_ips, zookeeper_port)
    instances += man.getIps('kafka',kafka_ips, kafka_port)
    if schemaregistry_ips:
        instances += man.getIps('schemareg', schemaregistry_ips, schemaregistry_port)
    connect(jump_host,instances)


def connect(jump_host,instances):
    print_instances(instances)
    add_local_interfaces(instances)
    connect_ssh_tunnel(jump_host,instances)
    remove_local_interfaces(instances)

def add_local_interfaces(instances):
    click.echo(' * adding interface, user password might be needed')
    for instance in instances:
        if sys.platform == 'darwin':
            cmd = ['sudo', 'ifconfig', 'lo0', 'alias', instance.ip]
        else:
            cmd = ['sudo', 'ip', 'add', 'a', 'dev', 'lo', instance.ip]
        subprocess.call(cmd)

def remove_local_interfaces(instances):
    click.echo(' * removing interface, user/root password might be needed')
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
    click.echo(' * connecting to jump host ' + jump_host)
    opts = []
    for i in instances:
        opts += ['-L','{ip}:{port}:{ip}:{port}'.format(ip=i.ip,port=i.port)]
    subprocess.call(['ssh'] + opts + [jump_host])

if __name__ == '__main__':
    cli()
