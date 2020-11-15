from kazoo.client import KazooClient

zk = KazooClient(hosts='zoo1:2181')
zk.start()