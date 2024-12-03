#!/bin/bash

# Install nautilus-url-shortcut

echo "Installing nautilus-uri-bookmark..."

if type "pacman" > /dev/null 2>&1
then
    # check if already install, else install
    pacman -Qi python-nautilus &> /dev/null
    if [ `echo $?` -eq 1 ]
    then
        sudo pacman -S --noconfirm python-nautilus
    else
        echo "python-nautilus is already installed"
    fi
elif type "apt-get" > /dev/null 2>&1
then
    # Find Ubuntu python-nautilus package
    package_name="python-nautilus"
    found_package=$(apt-cache search --names-only $package_name)
    if [ -z "$found_package" ]
    then
        package_name="python3-nautilus"
    fi

    # Check if the package needs to be installed and install it
    installed=$(apt list --installed $package_name -qq 2> /dev/null)
    if [ -z "$installed" ]
    then
        sudo apt-get install -y $package_name
    else
        echo "$package_name is already installed."
    fi
elif type "dnf" > /dev/null 2>&1
then
    installed=`dnf list --installed nautilus-python 2> /dev/null`
    if [ -z "$installed" ]
    then
        sudo dnf install -y nautilus-python
    else
        echo "nautilus-python is already installed."
    fi
else
    echo "Failed to find python-nautilus, please install it manually."
fi

# Remove previous version and setup folder
echo "Removing previous version (if found)..."
mkdir -p ~/.local/share/nautilus-python/extensions
rm -f ~/.local/share/nautilus-python/extensions/nautilus-uri-bookmark.py

echo "Installing files..."

# Install mime type
mkdir -p ~/.local/share/mime/packages
cp application-vnd.dstaudt-nautilus-uri-bookmark.xml ~/.local/share/mime/packages
update-mime-database ~/.local/share/mime

# Install opener script
mkdir -p ~/.local/bin
cp application-vnd.dstaudt-nautilus-uri-bookmark ~/.local/bin/
chmod +x ~/.local/bin/application-vnd.dstaudt-nautilus-uri-bookmark

# Install desktop file
cp nautilus-uri-bookmark.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications/

# Install Nautilus extension
mkdir -p ~/.local/share/nautilus-python/extensions
cp nautilus-uri-bookmark.py ~/.local/share/nautilus-python/extensions/

# Restart nautilus
echo "Restarting nautilus..."
nautilus -q

echo "Installation Complete"
