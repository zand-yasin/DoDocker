import docker

# Initialize the Docker client
client = docker.from_env()

# Specify the name or ID of the container you want to inspect
while True:

  path = ''

  print('Type any key to continue or type \'exit\' to exit')
  next = input('Reply..: ')
  
  if next == 'exit':
    break;
  
  containers = client.containers.list()
  print(containers)
  
  for index, container in enumerate(containers):
    # Access and print attributes of the container
    container_id = container.id
    container_name = container.name
    container_status = container.status
    
    print("Container Index:", index, ", Container ID:", container_id, ", Container Name:", container_name, ", Container Status:", container_status)
    
  promptId = input('Please enter container index to show container directory or type \'exit\' to exit: ')
  
  if promptId == 'exit':
    break;
  
  try:
      # Get a reference to the container
      container = client.containers.get(containers[int(promptId)].id)
  
      # List the contents of the container's root directory
      container_root_dir = "/"
      contents = container.exec_run(["ls", container_root_dir])

      # Display the list of files and folders
      print("Contents of container {}:".format(promptId))
      print(contents.output.decode("utf-8"))
      
      
  
  except docker.errors.NotFound:
      print("Container {} not found.".format(containers[int(promptId)]))
  except docker.errors.APIError as e:
      print("Error accessing container: {}".format(e))

