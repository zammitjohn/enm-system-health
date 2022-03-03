# enm-system-health
ENM System Health web endpoint built on Django

This web endpoint is an interface which executes the ENM System Healthcheck script on the ENM Management Server, and the results provide information on the state of various aspects of an ENM deployment. Checks include:
- All servers in the clusters are available and running.
- ENM applications and services are available and online.
- Filesystem usage on the servers is not exceeding critical levels.
- PostgreSQL Database Administrator Password expiration status.
- Key system level services are running (for example: sshd, puppet, vcs, rhq-agent, litpd, ddc, mcollective)

This can be run after an ENM Installation, Upgrade, or Restore from Backup procedure has occurred. However, it can be run at any point in time, to determine the health of the ENM system.

## Prerequisites
- ENM has been deployed.
- User has root access to the ENM Management Server. Configuration file ```config.json``` must be created in root directory with the attribute–value pairs: hostname, port, username, password.
- File ```secret_key.txt``` must be created in root directory containing a large random value.

## Endpoints
| URL    | Action                                                                                          |
|--------|-------------------------------------------------------------------------------------------------|
| /check | Runs all the health checks except for ```ombs_backup_healthcheck``` and ```fcaps_healthcheck``` |