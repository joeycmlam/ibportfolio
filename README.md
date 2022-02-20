# README
# Requirement
# Python 3

#reference 
# https://towardsdatascience.com/all-pandas-json-normalize-you-should-know-for-flattening-json-13eae1dfb7dd


#jsonUtil.py
## convert JSON message into a list of key-value pair dictionary with flatten format and then write into excel file
# limitation
# 1) could only handle one 

# RabitMQ setup
Referene link: https://www.architect.io/blog/2021-01-19/rabbitmq-docker-tutorial

Rerfer to docker-compose.yml as setting up
docker pull rabbitmq:3-management
docker run --rm -it -p 15672:15672 -p 5672:5672 rabbitmq:3-management
Raibbit MQ admin console: http://localhost:15672 
