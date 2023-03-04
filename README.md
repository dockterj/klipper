# Mightyboard Rev E, G and H support - Fork of Klipper3d/klipper

This fork adds support for Makerbot Replicator 1/2/2X
(Mightyboard rev e, g and h).

**STATUS** - Replicator 2 and 2X profiles still need to be updated
to include certain printer specific macros and separate specific
configs. Replicator 1 config still needs to be created.

Printers that may use ADS1118 ADCs and may work with this
repo include:
- FlashForge DreamerNX
- FlashForge Dreamer
- FlashForge Inventor
- Dremel 3D20
- Dremel 3D40
- PowerSpec Ultra 3D
- Monoprice Inventor 1

**Changes include:**
* Documents what is necessary to flash the MCU (57600 baud and correct 
    avrdude protocol)
* Adds support for MCU reset (toggle connection baud rate to 57600)
* Adds support for ADS1118 and k-type thermocouples (one or two extruders)
* Adds support for hardware blinking of the LEDs
* Adds support for multiple buttons with same action in display
* Removes the need for specifying dummy pins for software spi devices
* Adds example g code macros to emulate some original Makerbot behaviors

/config/printer-makerbot-replicator2x-2012.cfg can be used as a starting point 
for 2x printers.  
/config/printer-makerbot-replicator2-2012.cfg can be used as a starting point
for Replicator 2 printers.

# Installation

To-do: (Add specific steps for cloning this repo manually and/or using KIUAH)

Clone this repo and do the normal installation steps.

Copy /config/printer-makerbot-replicator2x-2012.cfg to printer.cfg.  Edit this
file to add/remove features specific to your printer (e.g. remove HBP,
change the HBP sensor to match what you have, change x,y, and z limits).

Following the normal installation steps, run make menuconfig.  Choose 
an atmega1280, 16mhz, and uart0.  (see below for note about atmega2560).

Run make flash.  This should flash your mightyboard.  If not, I have
found times where I needed to power the mightboard off and back on
or attempt to connect and disconnect with Klipper (i.e. connect at a
speed other than 57600 first) before it would flash.

At this point you should have Klipper running on your Replicator.
Follow the normal Klipper documentation for further tuning.

# Notes
* The Sailfish firmware has profiles for mightyboard rev g and rev
h printers that have atmega2560 instead of atmega1280.  If you have
one of these please let me know so I can get a known working config.
I believe you should be able to get this working by changing the MCU
processor in make menuconfig and editing src/arv/Makefile and changing
the last line from "-C stk500v1" to "-C stk500v2".  Software reset
should work but needs to be tested to confirm.
* The generic-mightyboard.cfg in the main repo should NOT be use
for these printers.  That config file is for the original
Makerbot Replicator and clones and does not work with printers
that have ADS1118 adc and thermocouples.
* There is no specific error for a disconnected thermocouple however
the printer will shut down if a thermocouple is not attached (this
triggers a temperature out of range error).
* The included printer.cfg changes the origin (0,0) to be in the left 
front of the build plate to be consistent with other cartesian printers.  
Keeping the original Replicator origin (which resembles a delta printer) 
requires updating position_min, position_max, position_endstop, and 
bed_screws values for the x and y axis.
* Please watch or star this repo if you are interested.  The more
people that use this the better the chances of getting it included
upstream.  Feel free to file issues in this repo for questions or
problems (DON'T USE ISSUES IN UPSTREAM FOR THIS)

*************************************************************************
# Welcome to the Klipper project!

[![Klipper](docs/img/klipper-logo-small.png)](https://www.klipper3d.org/)

https://www.klipper3d.org/

Klipper is a 3d-Printer firmware. It combines the power of a general
purpose computer with one or more micro-controllers. See the
[features document](https://www.klipper3d.org/Features.html) for more
information on why you should use Klipper.

To begin using Klipper start by
[installing](https://www.klipper3d.org/Installation.html) it.

Klipper is Free Software. See the [license](COPYING) or read the
[documentation](https://www.klipper3d.org/Overview.html). We depend on
the generous support from our
[sponsors](https://www.klipper3d.org/Sponsors.html).
