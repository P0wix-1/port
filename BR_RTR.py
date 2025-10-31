#!/bin/python3
import os, subprocess

#Настройка портов
res = subprocess.run(["ip", "-c", "--br", "a"], capture_output=True, text=True, encoding='utf-8')
res=res.stdout.split()
ports=[iface for iface in res if iface.startswith("ens")]
os.system(f"mkdir /etc/net/ifaces/{ports[1]}")
os.system(f"echo '192.168.2.2/24' > /etc/net/ifaces/{ports[0]}/ipv4address")
os.system(f"echo '192.168.5.1/24' > /etc/net/ifaces/{ports[1]}/ipv4address")
os.system(f"cat << OEF > /etc/net/ifaces/{ports[0]}/options\n BOOTPROTO=static\n TYPE=eth\n CONFIG_WIRELESS=no\n SYSTEMD_BOOTPROTO=static\n CONFIG_IPV4=yes\n DISABLED=no\n NM_CONTROLLED=no\n SYSTEMD_CONTROLLED=no")
os.system(f"cat << OEF > /etc/net/ifaces/{ports[1]}/options\n BOOTPROTO=static\n TYPE=eth\n CONFIG_WIRELESS=no\n SYSTEMD_BOOTPROTO=static\n CONFIG_IPV4=yes\n DISABLED=no\n NM_CONTROLLED=no\n SYSTEMD_CONTROLLED=no")

#Мелкая настройка
os.system("hostnamectl set-hostname BR-RTR")
os.system("sysctl -w net.ipv4.ip_forward=1")
os.system("systemctl restart network")

#Настройка Firewall
os.system("apt-get update && apt-get -y install firewalld && systemctl enable --now firewalld")
os.system(f"firewall-cmd --permanent --zone=public --add-interface={ports[0]}")
os.system(f"firewall-cmd --permanent --zone=trusted --add-interface={ports[1]}")
os.system("firewall-cmd --permanent --zone=public --add-masquerade")
os.system("firewall-cmd --complete-reload")