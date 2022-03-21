import boto3
from kubernetes import client, config
import itertools


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

class AWSInstances(RetrieveInstanceIPs):
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


class GKEInstance(RetrieveInstanceIPs):
    def __init__(self, namespace):
        self.namespace = namespace

    def getIps(self, service):
        config.load_kube_config()
        instances=[]
        v1 = client.CoreV1Api()
        ret = v1.list_namespaced_service(self.namespace, watch=False)
        for item in itertools.takewhile(lambda i : service == i.metadata.name, ret.items):
            if not item.status.load_balancer.ingress:
                continue

            for port in item.spec.ports:
                instances.append(Instance(name=service,
                                          ip=item.status.load_balancer.ingress[0].ip,
                                          port=port.port))
        return instances


