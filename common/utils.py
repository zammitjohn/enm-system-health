import json
import paramiko
import socket

def connectSSH(logger):
    paramiko.util.log_to_file('logs/ssh.log')
    try:
        f = open('config.json') ## JSON config file
    except OSError:
        logger.error("Could not open config file")
        return None
    with f:
        try:
            config = json.load(f) # returns file JSON object as a dictionary
        except ValueError:
            logger.error("Decoding JSON has failed")
            return None
        try:
            hostname = config['hostname']
            port = config['port']
            username = config['username']
            password = config['password']
        except KeyError:
            logger.error("JSON not in correct format")
            return None
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_system_host_keys()
        ssh.connect(hostname, port, username, password) ## SSH Client connection
    except paramiko.AuthenticationException:
        logger.error("Authentication failed, please verify your credentials")
        return None
    except paramiko.SSHException as sshException:
        logger.error("Unable to establish SSH connection: %s" % sshException)
        return None
    except paramiko.BadHostKeyException as badHostKeyException:
        logger.error("Unable to verify server's host key: %s" % badHostKeyException)
        return None
    except socket.error:
        logger.error("A socket error occurred whilst connecting to server")
        return None
    
    return ssh