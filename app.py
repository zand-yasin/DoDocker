import docker
client = docker.from_env()

print('1')

containers = client.containers.list()
print('2')

print(containers)


