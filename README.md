# Anycubic Kobra 2 Series Things

This repository contains things related to the Anycubic Kobra 2 Series 3D printer.

## Discussion

[Link (klipper.discourse.group)](https://klipper.discourse.group/t/printer-cfg-for-anycubic-kobra-2-plus-pro-max/11658)

## Firmware Update via USB

1. To update the firmware via USB, you need to do the following:

2. Format a USB drive to FAT32 or exFAT.

3. Create a folder called `update` on the USB drive.

4. Copy the `update.swu` file to the `update` folder.

5. Plug the USB drive into the printer.

6. Then it should be detected and you can update the firmware via usb.

## Root

At the moment the only way to get root access is to use the serial console. The serial console is available on the 4 pin header on the mainboard.

UART: 3 Volt 115200 baud rate.

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

For permanent ssh access, you can do the following:

1. Download and extract https://bitfab.org/dropbear-static-builds/dropbear-v2020.81-arm-none-linux-gnueabi-static.tgz 2 to somewhere.

2. Keep extracting until you can see the file called: `dropbearmulti`.

3. Then start a temporary HTTP server using python:

```sh
python -m http.server
```

4. Make sure to run the command in the same directory as the `dropbearmulti` file.
   The URL should be something like:
   `http://10.0.0.143:8000/dropbearmulti`

5. Download the ssh script in the `ssh` folder in this repository.
   Also place the script in the same folder as `dropbearmulti`:
   `http://10.0.0.143:8000/installssh.sh`

Make sure you change the IP to your computer.

6. Then run on the busybox on the printer:

```sh
wget http://10.0.0.143:8000/installssh.sh -O /tmp/
chmod +x /tmp/installssh.sh
/tmp/installssh.sh
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
