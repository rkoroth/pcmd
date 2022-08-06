# pcmd
pcmd is a simple command line tool for running different commands on multiple remote servers in parallel.It uses SSH connection to connect the servers so no agent is required. SSH authentication should be taken care prior running this tool using SSH keys.

Below is a simple example shows how we can get DNS server details from two remote servers.

create a file called nodelist in the same directory with all your server names and the command seperated by ";". (Assuming servers are configured with password less SSH)

now simply run pcmd.py as below

./pcmd.py 

```
[root@localhost pcmd]# more nodelist 
k8s-node1 ; "cat /etc/resolv.conf"
k8s-node2 ; "cat /etc/resolv.conf"
[root@localhost pcmd]# 
[root@localhost pcmd]# ./pcmd.py "cat /etc/resolv.conf"
2019-05-05 18:12:03   [SUCCESS]  SSH connectivity k8s-node1
2019-05-05 18:12:03   [SUCCESS]  SSH connectivity k8s-node2
2019-05-05 18:12:03   [SUCCESS]  Command execution on k8s-node2
Server Name k8s-node2
# Generated by NetworkManager
domain domain.name
search domain.name
nameserver 192.168.1.1

2019-05-05 18:12:03   [SUCCESS]  Command execution on k8s-node1
Server Name k8s-node1
# Generated by NetworkManager
domain domain.name
search domain.name
nameserver 192.168.1.1

[root@localhost pcmd]# 
```
Similary any command can be run on thousands of machines in parallel.


