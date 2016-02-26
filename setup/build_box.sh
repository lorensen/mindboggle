#!/bin/bash
#=============================================================================
# This program runs a Vagrantfile, then packages the running VirtualBox
# environment into a reusable box.  The Vagrantfile installs Mindboggle
# (http://mindboggle.info) and dependencies in a VirtualBox environment
# by calling a bash setup script in the same folder: setup_mindboggle.sh.
# Vagrant (vagrantup.com) and VirtualBox (virtualbox.org) should be installed,
# and there needs to be a good Internet connection.
#
# Usage:
#     bash build_box.sh <Mindboggle version>
#
# Upload the box to a website for others to download:
#     rsync -avz --sparse -e /usr/bin/ssh mindboggle.<version>.box
#         binarybottle@binarybottle.com:media.mindboggle.info/vm/
#
#
# Authors:
#     - Arno Klein, 2014-2016  (arno@mindboggle.info)  http://binarybottle.com
#
# Copyright 2016,  Mindboggle team, Apache v2.0 License
#=============================================================================

VERSION=$1

vagrant up
vagrant package --output mindboggle.$VERSION.box