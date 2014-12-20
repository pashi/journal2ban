#!/bin/bash

/usr/sbin/ipset create ssh-whitelist hash:ip
/usr/sbin/ipset create blacksix hash:ip family inet6 hashsize 1024 maxelem 65536 timeout 3600
/usr/sbin/ipset create blackfour hash:ip family inet hashsize 1024 maxelem 65536 timeout 3600


/sbin/iptables -N ssh-block
/sbin/iptables -F ssh-block 
/sbin/iptables -A ssh-block -m set --match-set ssh-whitelist src -j ACCEPT
/sbin/iptables -A ssh-block -m set --match-set blackfour src -j DROP
/sbin/iptables -A ssh-block -j ACCEPT

exit 0
