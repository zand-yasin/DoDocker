import docker

# Initialize the Docker client
client = docker.from_env()

# Specify the name or ID of the container you want to inspect
container_name_or_id = "c28401f66ece"

try:
    # Get a reference to the container
    container = client.containers.get(container_name_or_id)

    # List the contents of the container's root directory
    container_root_dir = "/"
    contents = container.exec_run(["ls", container_root_dir])

    # Display the list of files and folders
    print("Contents of container {}:".format(container_name_or_id))
    print(contents.output.decode("utf-8"))

except docker.errors.NotFound:
    print("Container {} not found.".format(container_name_or_id))
except docker.errors.APIError as e:
    print("Error accessing container: {}".format(e))

