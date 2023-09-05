# from base64 import encode
from subprocess import run, PIPE, Popen

mac = input('mac: ')
run('gsettings set org.gnome.desktop.interface icon-theme breeze-icons-dark\n',shell=True)
run('gsettings set org.gnome.desktop.interface gtk-theme Nordian-Breeze-GTK\n',shell=True)
run('git clone https://aur.archlinux.org/auracle-git.git',shell=True)
run('git clone https://aur.archlinux.org/pacaur.git',stdin=PIPE,shell=True,text=True)
p = Popen('sudo pacman -S libvirt qemu-guest-agent qemu-base virt-manager dnsmasq iptables-nft dmidecode --noconfirm',stdin=PIPE,text=True,shell=True)
if p.stdin:
    p.stdin.write('35739517\n')
p = Popen('sudo usermod -aG libvirt viktor',shell=True,text=True,stdin=PIPE)
if p.stdin:
    p.stdin.write('35739517\n')
run(f'nmcli connection modify br0 bridge.mac-address {mac}',shell=True)
