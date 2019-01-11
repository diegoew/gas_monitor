#!/bin/bash
# Make the device a wifi hotspot
# From https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md


# Install dhcp server and access point host software
apt update
apt upgrade
apt install dnsmasq hostapd
systemctl stop dnsmasq
systemctl stop hostapd
reboot


# Configure DHCP server
cat <<EOF > /etc/dhcpcd.conf
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
EOF

service dhcpcd restart

sed -i.0 -r 's/# *interface/interface=wlan\n  dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h/' /etc/dnsmasq.conf


# Configure access point software
cat <<EOF > /etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
ssid=gas_monitor
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=strawberry
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOF

sed -i.0 -r 's/#(DAEMON_CONF=")"/\1/etc/hostapd/hostapd.conf"/' /etc/default/hostapd


# Start services
systemctl start hostapd
systemctl start dnsmasq


# Add routing and masquerade and restart

sed -i.0 -r 's/#(/etc/sysctl.conf)/\1/'

iptables -t nat -A  POSTROUTING -o eth0 -j MASQUERADE
sh -c "iptables-save > /etc/iptables.ipv4.nat"

sed -i.0 -r '/^exit 0/i\
iptables-restore < /etc/iptables.ipv4.nat'

reboot
