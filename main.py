# from base64 import encode
from subprocess import run, Popen, PIPE

disk = input('Disk name:')
user = input('User:')
prefix = input('Prefix disk:')
pc_name = input('PC name:')
ip = input('IP:')
if user == '':
    user = 'viktor'
    password = '35739517'
else:
    password = input('Password:')
cpu = input('CPU:')
video = input('VIDEO:')
de = input('DE:')
autorun = input('AUTORUN:')
run('timedatectl set-ntp true',shell=True)
run('timedatectl set-timezone Asia/Irkutsk',shell=True)
p = Popen(f'gdisk /dev/{disk}',stdin=PIPE,shell=True,text=True)
if p.stdin:
    p.stdin.write('x\n')
    p.stdin.write('z\n')
    p.stdin.write('Y\n')
    p.stdin.write('Y')
    p.stdin.close()
    p.wait()
p = Popen(f'fdisk /dev/{disk}',stdin=PIPE,shell=True,text=True)
if p.stdin:
    p.stdin.write('g\n')
    p.stdin.write('n\n')
    p.stdin.write('\n')
    p.stdin.write('\n')
    p.stdin.write('+1G\n')
    p.stdin.write('t\n')
    p.stdin.write('1\n')
    p.stdin.write('n\n')
    p.stdin.write('\n')
    p.stdin.write('\n')
    p.stdin.write('\n')
    p.stdin.write('p\n')
    p.stdin.write('w\n')
    p.stdin.close()
    p.wait()
p = Popen(f'mkfs.ext4 -L "Arch" /dev/{disk}{prefix}2',stdin=PIPE,shell=True,text=True)
if p.stdin:
    p.stdin.write('y')
    p.stdin.close()
    p.wait()
run(f'mkfs.vfat /dev/{disk}{prefix}1',shell=True)
run(f'mount /dev/{disk}{prefix}2 /mnt',shell=True)
run(f'mkdir -p /mnt/boot',shell=True)
run(f'mount /dev/{disk}{prefix}1 /mnt/boot',shell=True)
run('pacstrap /mnt base linux linux-firmware base-devel neovim vim vi efibootmgr netctl networkmanager dhcpcd bash-completion git zsh kitty openssh polkit',shell=True)
run(f'umount /mnt/dev',shell=True)
run('genfstab -L -p -P /mnt >> /mnt/etc/fstab',shell=True)
p = Popen('arch-chroot /mnt',stdin=PIPE,shell=True,text=True)
if p.stdin:
    p.stdin.write('pacman -Sy --noconfirm\n')
    p.stdin.write('systemctl enable NetworkManager\n')
    p.stdin.write('systemctl enable sshd\n')
    if cpu == 'intel':
        p.stdin.write('pacman -S intel-ucode --noconfirm\n')
    else:
        p.stdin.write('pacman -S amd-ucode --noconfirm\n')
    if video == 'intel':
        p.stdin.write('pacman -S xf86-video-intel --noconfirm\n')
    elif video == 'nvidia':
        p.stdin.write('pacman -S nvidia-dkms --noconfirm\n')
    else:
        p.stdin.write('pacman -S xf86-video-amdgpu --noconfirm\n')
    if de == 'sway':
        p.stdin.write('pacman -S sway firefox --noconfirm\n')
    if de == 'hyprland':
        p.stdin.write('pacman -S hyprland waybar firefox neofetch mc htop hyprpaper thunar ttf-jetbrains-mono-nerd ttf-font-awesome wofi --noconfirm\n')
    if de == 'hyprland' and autorun == 'yes':
        p.stdin.write(f'cat hyprland_profile >> /etc/profile\n')
    if de == 'sway' and autorun == 'yes':
        p.stdin.write(f'cat sway_profile >> /etc/profile\n')
    if autorun == 'yes':
        st = '[Service]\nExecStart=\nExecStart=-/usr/bin/agetty --autologin viktor --noclear %I $TERM'
        p.stdin.write(f'mkdir -p /etc/systemd/system/getty@tty1.service.d\n')
        p.stdin.write(f'echo "{st}" >> /etc/systemd/system/getty@tty1.service.d/override.conf\n')
        p.stdin.write(f'systemctl enable getty@.service\n')
    p.stdin.write('ln -sf /usr/share/zoneinfo/Asia/Irkutsk /etc/localtime\n')
    p.stdin.write('hwclock --systohc\n')
    st = 'en_US.UTF-8 UTF-8\nru_RU.UTF-8 UTF-8'
    p.stdin.write(f'echo "{st}" >> /etc/locale.gen\n')
    p.stdin.write('locale-gen\n')
    st = 'LANG=ru_RU.UTF-8'
    p.stdin.write(f'echo "{st}" >> /etc/locale.conf\n')
    st = 'KEYMAP=ru\nFONT=cyr-sun16'
    p.stdin.write(f'echo "{st}" >> /etc/vconsole.conf\n')
    p.stdin.write(f'echo "{pc_name}" >> /etc/hostname\n')
    st = f'127.0.0.1    localhost\n::1    localhost\n{ip}    {pc_name}.localdomain    {pc_name}'
    p.stdin.write(f'echo "{st}" >> /etc/hosts\n')
    p.stdin.write(f'passwd\n')
    p.stdin.write(password + '\n')
    p.stdin.write(password + '\n')
    p.stdin.write(f'useradd -m -g users -G wheel,audio -s /bin/bash {user}\n')
    p.stdin.write(f'passwd {user}\n')
    p.stdin.write(password + '\n')
    p.stdin.write(password + '\n')
    p.stdin.write('bootctl install\n')
    st = 'default arch\ntimeout 0\neditor 1'
    p.stdin.write(f'echo "{st}" >> /boot/loader/loader.conf\n')
    if cpu == 'intel' and video == 'nvidia':
        st = f'title Arch Linux\nlinux /vmlinuz-linux\ninitrd  /intel-ucode.img\nnvidia_drm.modeset=1\ninitrd /initramfs-linux.img\noptions root=/dev/{disk}{prefix}2 rwi'
    elif cpu == 'intel':
        st = f'title Arch Linux\nlinux /vmlinuz-linux\ninitrd  /intel-ucode.img\ninitrd /initramfs-linux.img\noptions root=/dev/{disk}{prefix}2 rwi'
    elif video == 'nvidia':
        st = f'title Arch Linux\nlinux /vmlinuz-linux\nnvidia_drm.modeset=1\ninitrd /initramfs-linux.img\noptions root=/dev/{disk}{prefix}2 rwi'
    else:
        st = f'title Arch Linux\nlinux /vmlinuz-linux\ninitrd /initramfs-linux.img\noptions root=/dev/{disk}{prefix}2 rwi'
    p.stdin.write(f'echo "{st}" >> /boot/loader/entries/arch.conf\n')
    p.stdin.write('exit')
    p.stdin.close()
    p.wait()
fin = open("/mnt/etc/sudoers", "rt")
data = fin.read()
data = data.replace('# %wheel ALL=(ALL) ALL', '%wheel ALL=(ALL) ALL').replace('# %wheel ALL=(ALL:ALL) ALL', '%wheel ALL=(ALL:ALL) ALL')
fin.close()
fin = open("/mnt/etc/sudoers", "wt")
fin.write(data)
fin.close()
fin = open("/mnt/etc/pacman.conf", "rt")
data = fin.read()
data = data.replace('#Color', 'Color').replace('#[multilib]\n#Include = /etc/pacman.d/mirrorlist','[multilib]\nInclude = /etc/pacman.d/mirrorlist')
fin.close()
fin = open("/mnt/etc/pacman.conf", "wt")
fin.write(data)
fin.close()
run('umount -R /mnt',shell=True)
run('reboot',shell=True)
