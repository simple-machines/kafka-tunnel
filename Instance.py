import boto3
import socket

class Instance:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port

class RetrieveInstanceIPs():
    def getIps(self,service,port):
        raise NotImplementedError("Subclass must implement abstract method")

class ManualInstances(RetrieveInstanceIPs):
    def getIps(self,service,ips,port):
        instances=[]
        for ip in ips.split(','):
            instances.append(Instance(name=service,ip=ip,port=port))
        return instances

class AWSEC2Instances(RetrieveInstanceIPs):
    def __init__(self,profile,region):
        self.profile = profile
        self.region = region
        self.session = boto3.Session(profile_name=profile, region_name=region)
    def getIps(self,service,port):
        instances=[]
        for ec2_ip in self.req_aws_ips(service, self.region):
            instances.append(Instance(name=service,ip=ec2_ip,port=port))
        return instances
    def req_aws_ips(self,service, region):
        ips=[]
        aws_filter = lambda name,value: [{'Name':'tag:'+name,'Values':[value]}]
        client = self.session.client('ec2')
        response = client.describe_instances(Filters=aws_filter('Name',service))
        for res in response.get('Reservations'):
            for instance in res.get('Instances'):
                ip = instance.get(u'PrivateIpAddress')
                if ip is not None:
                  ips.append(instance.get(u'PrivateIpAddress'))
        return ips


class AWSMSKInstances:
    def __init__(self, profile, region):
        self.profile = profile
        self.region = region
        self.session = boto3.Session(profile_name=profile, region_name=region)

    def get_instances(self, cluster_arn):
        client = self.session.client('kafka')
        cluster_info = client.describe_cluster(ClusterArn=cluster_arn)['ClusterInfo']
        brokers_info = client.get_bootstrap_brokers(ClusterArn=cluster_arn)
        print(brokers_info)

        hosts_as_string = ""
        if 'BootstrapBrokerString' in brokers_info:
            hosts_as_string = brokers_info['BootstrapBrokerString']
        if 'BootstrapBrokerStringSaslScram' in brokers_info:
            hosts_as_string = brokers_info['BootstrapBrokerStringSaslScram']

        hosts_as_string = hosts_as_string + "," + cluster_info['ZookeeperConnectString']
        instances = []
        for row in hosts_as_string.split(','):
            [host, port] = row.split(':')
            ip = socket.gethostbyname(host)
            instances.append(Instance(host, ip, port))

        return instances
