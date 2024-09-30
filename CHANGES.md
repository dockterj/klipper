# Breaking Changes

* 2024-09-30 (in running_version branch) Removed support for multiple buttons in the menu.  Instead, a forward_button is configured
that will behave the same as the click_button.  You will need to update your printer.cfg file when
upgrading to this release.  See note in changelog below.

# Change log

* 2024-09-30 (in running_version branch) Button pins in sample configs are now defined correctly (inverted).  Menu behavior will
function much faster with the correct polarity specified.  If you are upgrading, confirm the pin
polarities in your printer.cfg file match what is in the sample config files.
* 2024-09-30 Misc menu enhancements.  Fast up/down is now supported and works in temperature
adjustment and percentage adjustments (fan speeds).
