# Qrious - Automated deployment for webserver using ansible

## Prerequisites
1. Linux user with sudo permission to execute ansible.
2. Install following tools in your execution environment.
>1. Python and pip (Tested in version python2.7)
>    - Follow instructions on https://docs.python-guide.org/starting/install/linux/
>2. Ansible 2.9
>    - Follow instructions on https://docs.ansible.com/ansible/2.9/installation_guide/intro_installation.html
3. AWS IAM user with following access policies to generate access keys.
>    - AmazonEC2FullAccess
>    - AmazonVPCFullAccess

 ## Execute ansible playbooks
 1. Download code Repository
 ```
 git clone https://github.com/erangaka/qrious.git
 ```
 2. Change directory to git local repository path
 ```
 cd qrious
 ```
 3. Create AWS EC2 instance with docker
 ```
 ansible-playbook playbooks/mainbook.yml --extra-vars "aws_access_key=<YOUR-ACCESS-KEY> aws_secret_key='<YOUR-SECRET-KEY>' aws_region=<Preferred-AWS-region>"
 ```

## How-to connect to the webserver
1. Find the public IP from ansible job logs
```
Search for "New webserver created"
```
2. Open in your browser to retrieve web content
```
https://<webserver-ip>
```

## How-to check docker container health status and resource usage
Docker container health and resource usage check script (containerlogs.py) is running as a systemd service in the background and writes to the following log file in EC2 instance.
```
/tmp/webserver-stats.log
```
