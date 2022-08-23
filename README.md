# Qrious - Automated web server deployment using ansible

## Prerequisites
1. Linux user with sudo permission to execute ansible.
2. Install following tools in your execution environment.
> - Python and pip (Tested in version python2.7)
>    - Follow instructions on https://docs.python-guide.org/starting/install/linux/
> - Ansible 2.9
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
Example:

<img width="523" alt="image" src="https://user-images.githubusercontent.com/37226018/186189416-1ad58eaf-593d-469f-bae1-385c08ae9d46.png">


## Assignment Overview
### AWS infrastructure creation (IaC using ansible - playbooks/mainbook.yml)
- Create a new VPC group with public subnet and attached a new internet gteway.
https://github.com/erangaka/qrious/blob/98c5648b8d6b6795f75986af5fc186b334fe2099/playbooks/mainbook.yml#L25-L81
- Create a new security group with 22, 80, 8080, 443 ports open for public facing webservers.
https://github.com/erangaka/qrious/blob/98c5648b8d6b6795f75986af5fc186b334fe2099/playbooks/mainbook.yml#L83-L103
- Create a new EC2 instance using t2.micro size and Ubuntu server image.
https://github.com/erangaka/qrious/blob/98c5648b8d6b6795f75986af5fc186b334fe2099/playbooks/mainbook.yml#L125-L143

### Install docker and launch a NGINX container
- Install docker-ce using ansible role.
[roles/install_docker/tasks/main.yml](https://github.com/erangaka/qrious/blob/98c5648b8d6b6795f75986af5fc186b334fe2099/roles/install_docker/tasks/main.yml)
- Create customer docker container image using Dockerfile. 
https://github.com/erangaka/qrious/blob/98c5648b8d6b6795f75986af5fc186b334fe2099/playbooks/mainbook.yml#L177-L190
- Deploy and start container with http port mapping using custom image.
https://github.com/erangaka/qrious/blob/98c5648b8d6b6795f75986af5fc186b334fe2099/playbooks/mainbook.yml#L192-L211
- Copy container health check script and required files from repository to EC2 instance.
https://github.com/erangaka/qrious/blob/98c5648b8d6b6795f75986af5fc186b334fe2099/playbooks/mainbook.yml#L213-L232

### Log health status and resource usage of the NGINX container
- Create a python script to log container status and resource usage.
  - Script - [containerlogs.py](https://github.com/erangaka/qrious/blob/98c5648b8d6b6795f75986af5fc186b334fe2099/scripts/containerlogs.py)
  - Retrieve container stats using python Docker SDK and API.
    - References:
      - https://docker-py.readthedocs.io/en/stable/containers.html
      - https://docs.docker.com/engine/api/v1.41
      
- Create systemd config files to run health check script as a service in every 10seconds.
  - [container-check.service](https://github.com/erangaka/qrious/blob/98c5648b8d6b6795f75986af5fc186b334fe2099/files/container-check.service)
  
   <img width="609" alt="image" src="https://user-images.githubusercontent.com/37226018/186200021-434d70ea-ccea-4a9a-9f8f-0f2ac2b456d4.png">

  - [container-check.timer](https://github.com/erangaka/qrious/blob/98c5648b8d6b6795f75986af5fc186b334fe2099/files/container-check.timer)
  
   <img width="553" alt="image" src="https://user-images.githubusercontent.com/37226018/186200293-579c1041-e9f4-4e7b-842e-0021eb64fd6b.png">

    

