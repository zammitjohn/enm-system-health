from django.http import JsonResponse
import paramiko
import socket
import json
import logging

def index(request):

    logging.basicConfig(filename='check.log', filemode='a', format='%(asctime)s : %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S' )
    logger = logging.getLogger()
    
    ## JSON config file
    try:
        f = open('config.json') 
    except OSError:
        logger.error("Could not open config file")
        return JsonResponse({'status':'false'})
    with f:
        try:
            config = json.load(f) # returns file JSON object as a dictionary
        except ValueError:
            logger.error("Decoding JSON has failed")
            return JsonResponse({'status':'false'})
        try:
            hostname = config['hostname']
            port = config['port']
            username = config['username']
            password = config['password']
        except KeyError:
            logger.error("JSON not in correct format")
            return JsonResponse({'status':'false'})
    
    
    ## SSH Client connection
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_system_host_keys()
        ssh.connect(hostname, port, username, password)
        
    except paramiko.AuthenticationException:
        logger.error("Authentication failed, please verify your credentials")
        return JsonResponse({'status':'false'})
    except paramiko.SSHException as sshException:
        logger.error("Unable to establish SSH connection: %s" % sshException)
        return JsonResponse({'status':'false'})
    except paramiko.BadHostKeyException as badHostKeyException:
        logger.error("Unable to verify server's host key: %s" % badHostKeyException)
        return JsonResponse({'status':'false'})
    except socket.error:
        logger.error("A socket error occurred whilst connecting to server")
        return JsonResponse({'status':'false'})
    
    stdin, stdout, stderr = ssh.exec_command('/opt/ericsson/enminst/bin/enm_healthcheck.sh', get_pty=True)
    exit_status = stdout.channel.recv_exit_status() # blocking call
    ssh.close()
    
    
    ## Response
    if exit_status == 0:
        output = stdout.read().decode()
        if "FAIL" in output: 
            return JsonResponse({'status':'true','healthy':'false', 'message':'Errors detected!', 'output':output})
        else:
            return JsonResponse({'status':'true','healthy':'true', 'message':'No issues found!', 'output':output})
    else:
        logger.error("Output error: %s" % exit_status)
        return JsonResponse({'status':'false'})   