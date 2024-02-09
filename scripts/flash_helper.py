#!/usr/bin/env python3
# Tool for writing micro-controller code
#
# Copyright (C) 2021  Kevin O'Connor <kevin@koconnor.net>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import sys, os, optparse, subprocess

def get_flash_types():
    srcdir = os.path.dirname(os.path.realpath(__file__))
    
    flash_types = ["makeflash", "makeserialflash", "file", "linux"]

    sdcard_types = subprocess.check_output([os.path.join(srcdir,
                                           "flash-sdcard.sh"), "-l"]
                                           ).decode('utf-8')
    for type in sdcard_types.split('\n')[1:]:
        flash_types.append("sdcard," + type) 
    
    # usb - flash_usb.py -l (no code today)
    # not clear this is needed as make flash targets exist for this

    # spi - spi_flash/spi_flash.py -l
    # not clear this is needed as this is handled by flash-sdcard.sh    

    return flash_types

def list_flash_types():
    for t in get_flash_types():
        sys.stdout.write('%s\n' % (t,))

def list_devices(flash_type):
    if flash_type == "makeflash" or flash_type == "makeserialflash":
        devices = os.listdir("/dev/serial/by-id")
        for d in devices:
            sys.stdout.write('%s\n' % ("/dev/serial/by-id/" + d,))
        devices = os.listdir("/dev/serial/by-path")
        for d in devices:
            sys.stdout.write('%s\n' % ("/dev/serial/by-path/" + d,))
    elif flash_type.startswith('sdcard,'):
        devices = os.listdir("/dev")
        for d in devices:
            if d.startswith("ttyA") or d.startswith("ttyU"):
                sys.stdout.write('%s\n' % ("/dev/" + d,))

######################################################################
# Flashing code
######################################################################

def do_makeflash(device, kconfig, out):
    srcdir = os.path.dirname(os.path.realpath(__file__))
    makedir = os.path.join(srcdir, '..')
    os.system("make -C '%s' OUT='%s' KCONFIG_CONFIG='%s' FLASH_DEVICE='%s'"
              " flash" % (makedir, out, kconfig, device))

def do_makeserialflash(device, kconfig, out):
    srcdir = os.path.dirname(os.path.realpath(__file__))
    makedir = os.path.join(srcdir, '..')
    os.system("make -C '%s' OUT='%s' KCONFIG_CONFIG='%s' FLASH_DEVICE='%s'"
              " serialflash" % (makedir, out, kconfig, device))

def do_file(device, kconfig, out):
    srcdir = os.path.dirname(os.path.realpath(__file__))
    makedir = os.path.join(srcdir, '..')
    os.system("make -C '%s' OUT='%s' KCONFIG_CONFIG='%s' FLASH_DEVICE='%s'"
              " serialflash" % (makedir, out, kconfig, device))

def do_sdcard(sdcard_method, device, out):
    # XXX - this is just dummy testing code - should import spi_flash code
    srcdir = os.path.dirname(os.path.realpath(__file__))
    kbin = os.path.join(out, "klipper.bin")
    os.system("%s/flash-sdcard.sh -f %s %s %s"
              % (srcdir, kbin, device, sdcard_method))

def do_flash(flash_type, device, kconfig, out):
    if flash_type == "makeflash":
        do_makeflash(device, kconfig, out)
    elif flash_type == "makeserialflash":
        do_makeserialflash(device, kconfig, out)
    elif flash_type.startswith('sdcard,'):
        do_sdcard(flash_type[7:], device, out)
    elif flash_type.startswith('file'):
        do_file(device, kconfig, out)

######################################################################
# Startup
######################################################################

def main():
    usage = "%prog [options]"
    opts = optparse.OptionParser(usage)
    opts.add_option("-T", "--listtype", action="store_true",
                    help="list available flash types")
    opts.add_option("-D", "--listdevice", action="store_true",
                    help="list available target devices")
    opts.add_option("-t", "--type", type="string", dest="flash_type",
                    help="flash method to attempt")
    opts.add_option("-d", "--device", type="string", dest="device",
                    help="device to flash")
    opts.add_option("-k", "--kconfig", type="string", dest="kconfig",
                    help="kconfig file of build")
    opts.add_option("-o", "--out", type="string", dest="out",
                    help="build directory")
    options, args = opts.parse_args()
    if len(args) != 0:
        opts.error("Incorrect number of arguments")
    if options.listtype:
        list_flash_types()
        return
    if options.flash_type not in get_flash_types():
        opts.error("Must specify a valid flash type")
    if options.listdevice:
        list_devices(options.flash_type)
        return
    if not options.device or not options.kconfig or not options.out:
        opts.error("Must specify device, kconfig, and out options")
    do_flash(options.flash_type, options.device, options.kconfig, options.out)

if __name__ == '__main__':
    main()
