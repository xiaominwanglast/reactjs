#!/bin/sh
echo "172.16.0.44 gitlab.jr.2345.net" >> /etc/hosts
echo "172.16.0.232 jenkins.jr.2345.net" >> /etc/hosts
wget http://gitlab.jr.2345.net/finance_public/hosts/raw/master/hosts
cat hosts >> /etc/hosts
python manage.py runserver 0.0.0.0:7890