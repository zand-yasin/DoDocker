import docker
import subprocess


def getContainer(containers):
    for index, container in enumerate(containers):
      # Access and print attributes of the container
      container_id = container.id
      container_name = container.name
      container_status = container.status
      
      print("Container Index:", index, ", Container ID:", container_id, ", Container Name:", container_name, ", Container Status:", container_status)
        
    prompt = input('Please enter container index to show container directory or type \'exit\' to exit: ')
    return prompt;
      
 
# Initialize the Docker client
client = docker.from_env()
container_root_dir = "/"

while True:
  
  operation = input('Enter 1 for copy file \nEnter 2 for going throgh the container directories \nEnter exit for exit: ')
  
  if operation == 'exit':
    break;
  
  if operation == '1':
    print( 'copy')
    source = input('Enter the source file path from your host: ')
    destination = input('Enter the destination path in the container: ')

    containers = client.containers.list()
    prompt = getContainer(containers)

    if prompt == 'exit':
       break;
    elif not prompt.isnumeric():
      print('Only number is allowed')
    elif  len(containers) <= int(prompt) or int(prompt) < 0:
      print('Container not found')
    else:
     try:
       container_id = containers[int(prompt)].id
       container_id_with_path=container_id+":"+destination
       subprocess.call(["docker", "cp", source, container_id_with_path])

     except docker.errors.NotFound:
        print("Container {} not found.".format(container))
     except docker.errors.APIError as e:
        print("Error accessing container: {}".format(e))

  elif operation == '2':
    while True:

      path = ''

      print('Type any key to continue or type \'exit\' to exit')
      next = input('Reply..: ')
      
      if next == 'exit':
        break;
      
      containers = client.containers.list()
      prompt = getContainer(containers)
      
      if prompt == 'exit':
        break;
      elif not prompt.isnumeric():
        print('Only number is allowed')
      elif len(containers) <= int(prompt) or int(prompt) < 0:
        print('Container not found')
      else:
       try:
          # Get a reference to the container
          container = containers[int(prompt)]
      
          # List the contents of the container's root directory
          contents= container.exec_run(['ls', container_root_dir])
          
          # Display the list of files and folders
          lsContent = str(contents.output.decode('utf-8'))
          print("\n"+lsContent+"\n")
          path = ''
          isDirectoryFind=False
          while True:
            inputStr =  input ('\nEnter the directory name or type \'exit\' to exit: ')
            lastElement= path.rsplit('/', 1)[-1]
            
            action = ''
            if inputStr == 'exit':
              break;
            elif inputStr == 'back':
              action = 'cd ../'
              path = path.rsplit('/', 1)[0]
            elif  inputStr not in lsContent or not inputStr:
              isDirectoryFind=True
            else:
              action = 'cd'
              path += '/'+inputStr
    
            if not path:
              path = '/'
            
            if isDirectoryFind == True:
             print('Directory '+ path + 'didn\'t exist')
            else: 
             container.exec_run([action, path])

            contents = container.exec_run(["ls", path])
            lsContent = str(contents.output.decode('utf-8')) 
            # Display the list of files and folders
            print('\nDIRECTORIES: \n'+lsContent+"\n")
            print('CURRENT DIRECTORY: '+path)
            print('CURRENT ACTION: '+action)
            print('CURRENT lastElement: '+lastElement)
            # List the contents of the container's root directory
            
            isDirectoryFind = False
            
 
       except docker.errors.NotFound:
          print("Container {} not found.".format(container))
       except docker.errors.APIError as e:
          print("Error accessing container: {}".format(e))

  else: print('Try again')
