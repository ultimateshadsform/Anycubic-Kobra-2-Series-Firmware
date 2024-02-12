# Anycubic Kobra 2 Series Things

This repository contains things related to the Anycubic Kobra 2 Series 3D printer.

## Custom Firmware?

Not yet, but we are working on it. But don't expect anything soon. It will take a long long time.

## Discussion

- [Link (klipper.discourse.group)](https://klipper.discourse.group/t/printer-cfg-for-anycubic-kobra-2-plus-pro-max/11658)

## Community Links

- [Kobra2ProInsights](https://github.com/1coderookie/Kobra2ProInsights) (A collection of insights and findings about the Kobra 2 Pro and some other printers)

- [Kobra Unleashed](https://github.com/anjomro/kobra-unleashed) (A custom frontend/GUI for the Kobra 2 Series via mqtt)

## Firmware Update via USB

1. To update the firmware via USB, you need to do the following:

2. Format a USB drive to FAT32 or exFAT.

3. Create a folder called `update` on the USB drive.

4. Copy the `update.swu` file to the `update` folder.

5. Plug the USB drive into the printer.

6. Then it should be detected and you can update the firmware via usb.

   ### Notes:

   To update to version 3.05 you first need to update via 3.0.3.

   The firmwares are uploaded using git-lfs so you may need to download git-lfs to work with large files such as these.

## Root

At the moment the only way to get root access is to use the serial console. The serial console is available on the 4 pin header on the mainboard.

UART: 5 Volt 115200 baud rate.

If you cannot see anything on the serial console it's probably because you run newer firmware. You need to downgrade to 2.3.9 first before you can get root access. This is due to anycubic disabling the serial console in newer firmware versions in the `uboot` binary.

We have found a way to update to newest firmware and still have root access and uart enabled. A script will be developed sometime in the future.

Once basic serial communication is established, you can send the following commands to get root access:

1. Hold down the `S` key while powering on the printer.

2. Enter these commands to change bootargs:

```sh
setenv init /bin/sh
saveenv
bootd
```

Now you have a root shell.

3. Now you need to override the root password. To do this, you need to mount the overlay partition:

```sh
mount -t proc p /proc

. /lib/functions/preinit.sh

. /lib/preinit/80_mount_root

do_mount_root

. /etc/init.d/boot

link_by_name

. /lib/preinit/81_initramfs_config

do_initramfs_config
```

4. Then you can override the root password:

```sh
cp /etc/shadow /overlay/upper/etc/shadow
```

5. Just replace the password hash with something. You can use [this website](https://unix4lyfe.org/crypt/) to generate a password hash.

6. After that is done, you need to reboot into U-Boot again and change the bootargs back to normal:

```sh
setenv init /sbin/init
setenv bootdelay 3
saveenv
reset
```

Now you can login with the password you set.

That's it! You now have root access.

Thanks [rol](https://klipper.discourse.group/u/rol) for the commands!

For permanent ssh access, you can do the following:

```sh
wget http://bin.entware.net/armv7sf-k3.2/installer/generic.sh
chmod 755 generic.sh
./generic.sh
sed -i '$i\/opt/etc/init.d/rc.unslung start' /etc/rc.local
echo 'export PATH="$PATH:/opt/sbin:/opt/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"' >> /etc/profile
reboot

opkg update
opkg install dropbear
reboot
```

That's it! You now have permanent ssh access.

## Firmware Extraction

Thanks [Sineos](https://klipper.discourse.group/u/Sineos) for the firmware extraction commands!

To extract update.swu you can run:

```sh
cpio -idv < update.swu
```

To extract the rootfs you can run:

```sh
unsquashfs rootfs
```

## Encrypted firmware? WHAT THE HELL???

Check out: [my script](https://github.com/ultimateshadsform/Anycubic-Kobra-2-Series-Firmware/blob/main/scripts/firmwares/decryptthatbitch.py)
