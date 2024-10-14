# Anycubic Kobra 2 Series Things

This repository contains things related to the Anycubic Kobra 2 Series 3D printer.

## Custom Firmware?

> [!NOTE]
> REAL Custom firmware is not yet available, as far as we know. But you can use the tools in this repository to create your own "custom" firmware. Which is really just a modified stock firmware.

## Community Resources

### Discussion Forums

- [Telegram Group](https://t.me/kobra2modding)
- [Klipper Discourse Thread](https://klipper.discourse.group/t/printer-cfg-for-anycubic-kobra-2-plus-pro-max/11658)

### Related Projects

- [Kobra2ProInsights](https://github.com/1coderookie/Kobra2ProInsights): A collection of insights and findings about the Kobra 2 Pro and some other printers
- [Kobra Unleashed](https://github.com/anjomro/kobra-unleashed): A custom frontend/GUI for the Kobra 2 Series via MQTT

## Firmware Update via USB

> [!CAUTION]
> The K2 Pro firmware is **NOT COMPATIBLE** with the K2 Machine. These machines are completely different in firmware, so ensure you have the correct firmware for the correct machine.

To update the firmware via USB:

1. Format a USB drive to FAT32 or exFAT.
2. Create a folder called `update` on the USB drive.
3. Copy the `update.swu` file to the `update` folder.
4. Plug the USB drive into the printer.
5. The printer should detect it, and you can update the firmware via USB.

> [!IMPORTANT]
>
> - To update to version 3.0.5, you first need to update via 3.0.3.
> - The firmwares are uploaded using git-lfs, so you may need to download git-lfs to work with large files such as these.

## Root Access

> [!NOTE]
> Currently, the only way to get root access is through the serial console, available on the 4-pin header on the mainboard.

UART specifications: 5 Volt, 115200 baud rate.

> [!WARNING]
> If you can't see anything on the serial console, it's likely because you're running newer firmware. You need to downgrade to 2.3.9 first to get root access, as Anycubic disabled the serial console in newer firmware versions in the `uboot` binary.

To establish root access:

1. Hold down the `S` key while powering on the printer.
2. Enter these commands to change bootargs:

```sh
setenv init /bin/sh
saveenv
bootd
```

3. Mount the overlay partition:

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

4. Override the root password:

```sh
cp /etc/shadow /overlay/upper/etc/shadow
```

5. Replace the password hash. You can use [unix4lyfe.org](https://unix4lyfe.org/crypt/) website to generate a password hash.

6. Reboot into U-Boot and change the bootargs back to normal:

```sh
setenv init /sbin/init
setenv bootdelay 3
saveenv
reset
```

Now you can login with the password you set.

> [!TIP]
> Thanks to [rol](https://klipper.discourse.group/u/rol) for providing these commands! 👏

For permanent SSH access:

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

## Firmware Extraction

> [!TIP]
> Thanks to [Sineos](https://klipper.discourse.group/u/Sineos) for the firmware extraction commands! 👏

To extract update.swu:

```sh
cpio -idv < update.swu
```

To extract the rootfs:

```sh
unsquashfs rootfs
```

## Encrypted Firmware? 🙄

Check out: [Anycubic Kobra 2 SWU Decryption Script](./scripts/ack2_swu_decrypt.py) 😊
