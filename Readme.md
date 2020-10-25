Microbit simulator in python
====================================================================
This is a Microbit simulator which runs your python code.

Just download and put the modules where your microbit scripts are, then you will be able to import them.

Requirements
============
- tkinter

- python 3.X

Currently Supported Modules
===========================

- [x] radio
- [x] Image
- [x] display
- [x] buttons
- [x] accelerometer
- [x] sleep
- [x] running_time
- [ ] reset
- [ ] panic
- [ ] temperature
- [ ] pins
- [ ] compass
- [ ] i2c
- [ ] uart
- [ ] spi

Notes
=====
There may be bugs or differences with the hardware (which I would be happy to fix if you find them).

If you close the inferface before the script finishes, then there will be an KeyboardInterrupt exception.

The radio module requires the synchronisation module.

There is some settings that you can modify in the modules.