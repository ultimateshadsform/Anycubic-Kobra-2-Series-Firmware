#!/bin/sh

# Set IP Variable
#IP=<YOUR COMPUTER IP>
IP=10.0.0.143
PORT=8000

ask_ip() {
    echo "Enter IP address:"
    read IP
    echo "Enter port:"
    read PORT

    echo "Is $IP:$PORT the correct IP address? (y/n)"
    echo "File should be hosted at http://$IP:$PORT/dropbearmulti"
    read answer
    if [ "$answer" != "${answer#[Yy]}" ] ;then
        echo "Yes"
    else
        ask_ip
    fi
}

# Ask if ip is correct
echo "Is $IP:$PORT the correct IP address? (y/n)"
echo "File should be hosted at http://$IP:$PORT/dropbearmulti"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
    echo "Yes"
else
    ask_ip
fi

mkdir -p /overlay/upper/usr/bin
mkdir -p /overlay/upper/etc/dropbear

wget http://$IP:$PORT/dropbearmulti -O /overlay/upper/usr/bin/dropbearmulti

chmod +x /overlay/upper/usr/bin/dropbearmulti

/usr/bin/dropbearmulti dropbearkey -t rsa -f /overlay/upper/etc/dropbear/dropbear_rsa_host_key
/usr/bin/dropbearmulti dropbearkey -t dss -f /overlay/upper/etc/dropbear/dropbear_dss_host_key
/usr/bin/dropbearmulti dropbearkey -t ecdsa -f /overlay/upper/etc/dropbear/dropbear_ecdsa_host_key
/usr/bin/dropbearmulti dropbearkey -t ed25519 -f /overlay/upper/etc/dropbear/dropbear_ed25519_host_key

# Put a startup script in /overlay/upper/etc/rc.local
# Put the contents before the exit 0 line

CONTENT=$(cat <<EOF
#!/bin/sh

ln -s /usr/bin/dropbearmulti /usr/bin/dropbear
ln -s /usr/bin/dropbearmulti /usr/bin/dbclient
ln -s /usr/bin/dropbearmulti /usr/bin/dropbearkey
ln -s /usr/bin/dropbearmulti /usr/bin/dropbearconvert
ln -s /usr/bin/dropbearmulti /usr/bin/scp

/usr/bin/dropbear -p 22

# Put your custom commands here that should be executed once
# the system init finished. By default this file does nothing.

if [ -f /app/app ]; then
    chmod 755 /app/app
    /app/app&
fi

exit 0
EOF
)

echo "$CONTENT" > /overlay/upper/etc/rc.local

chmod +x /overlay/upper/etc/rc.local

echo "Done! Reboot to start SSH server"