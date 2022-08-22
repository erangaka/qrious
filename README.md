# Qrious - Automated deployment for webserver using ansible

## Prerequisites
Please install following tools in your execution environment.
>1. Python and pip (tested verion python2.7)
>    - Follow instructions on https://docs.python-guide.org/starting/install/linux/
>2. Ansible 2.9
>    - Follow instructions on https://docs.ansible.com/ansible/2.9/installation_guide/intro_installation.html

Create AWS IAM user with following access policies.
>    - AmazonEC2FullAccess
>    - AmazonVPCFullAccess

 ## Execute ansible playbooks
 1. Create AWS EC2 instance with docker
 ```
 ansible-playbook mainbook.yml --extra-vars "aws_access_key=<YOUR-ACCESS-KEY> aws_secret_key='<YOUR-SECRET-KEY>' aws_region=<Preferred-AWS-region>"
 ```
