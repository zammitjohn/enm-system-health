from django.http import JsonResponse
import logging
from common.utils import connectSSH

def index(request):
    
    ## Logging
    logging.basicConfig(filename='logs/result.log', filemode='a', format='%(asctime)s : %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S' )
    logger = logging.getLogger()

    ## SSH
    if not (ssh := connectSSH(logger)):
        return JsonResponse({'status':'false'})        
    stdin, stdout, stderr = ssh.exec_command('cat enm-system-health-check-output.txt')
    exit_status = stdout.channel.recv_exit_status() # blocking call
    ssh.close() 
    
    ## Response
    if exit_status == 0:
        output = stdout.read().decode()
        if "Successfully Completed ENM System Healthcheck" in output:
            if "FAIL" in output: 
                return JsonResponse({'status':'true','healthy':'false','output':output})
            else:
                return JsonResponse({'status':'true','healthy':'true','output':output})
        else:
            return JsonResponse({'status':'pending'})
    else:
        logger.error("Output error: %s" % exit_status)
        return JsonResponse({'status':'false'})   