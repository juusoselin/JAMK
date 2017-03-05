# Python-based web tools to add and remove flows using HPE VAN SDN Controllers REST API

## simple_flow_tool.py
This python script just inserts the same flows as presented in the assignment to the HPE VAN controller. However, controller variables, such as IP address, credentials as well as the swtich DPID should be changed prior the execution.

## flow_manipulator
This application allows user to run Python web server and using graphical user interface to add and delete flows from a switch. Controller variables should also be changed. 
Application can be run with 
```
python2 bin/app.py
```

> Please note, that these applications are far from finished, they are developed only enough to provide the functionality needed for the assignment. Therefore it might and probably will break at some point. No more development efforts are put to these applications.

Both applications use [HP SDN Client](https://github.com/dave-tucker/hp-sdn-client) by Dave Tucker
