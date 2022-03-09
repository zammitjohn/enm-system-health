from django.http import JsonResponse
import logging
from common.utils import connectSSH

def index(request):
    
    ## Logging
    logging.basicConfig(filename='logs/check.log', filemode='a', format='%(asctime)s : %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S' )
    logger = logging.getLogger()

    ## SSH
    if not (ssh := connectSSH(logger)):
        return JsonResponse({'status':'false'})        
    ssh.exec_command('nohup /opt/ericsson/enminst/bin/enm_healthcheck.sh > enm-system-health-check-output.txt')
    
    ## Response
    return JsonResponse({'status':'true', 'message':'ENM System Health Check executed'})