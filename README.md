# "Swan" station flip-clock project files:
![image 1](https://github.com/paolorussian/lostClock/blob/5f43896d0ff5e7c20ffe9cf4e77e6e32e430e3fd/images/image1.jpg)

## THIS IS NOT A TUTORIAL

This LOST clock replica is a raspberry pi - based device which emulates the 108 minute countdown from the show, but can also function as a regular clock. Mode switch can be made by pushing an html button in a web server running from the same single python file.

Please note that, believe it or not, the clock in the show was added in computer graphics, meaning that some of its features cannot be 100% accurate in any replica: not only the case has no visible bolts or screws, but also the flaps should "magically change" from being only digits to only hieroglyphs. In the real world, we need bolts and also accommodate digits and hieroglyphs in the same flap drums, meaning that as the clocks runs through the digit flaps and then is supposed to start over (9,8,7,6,5,4,3,2,1,0.... 9 again) you will see the hieroglyphs briefly passing by, as the hieroglyph flap does exist and must be placed somewhere.

Also note that in this project the numbering is [0,1,2,3,4,5,6,7,8, BLANK, HIEROGLYPH, 9,8,7,6,5,4,3,2,1] totalling 20 flaps each drum. You may have noticed that the digits are duplicated: this is not an error, as in order to function also as a regular clock we should have also ascending numbers. This is because in split-flap displays like this drums can only turn in one direction meaning that if you want to obtain a countdown timer (like the one from the show) you should have descending numbers to minimize the amount of flaps skipped minute after minute. But if you want it to also function as a regular clock then without ascending numbers you would have to use the descending, but each time the drum advances one digit, to get to the next flap it would need to run through all the 19 following flaps every minute (or second). Having both descending and ascending numbering, we can use only the descending for the countdown mode, and only the ascending for the clock mode. 0 is shared intentionally and also the 9 because I'm lazy and I didn't modify my print to accommodate 21 flaps instead of 20.

### required materials and components
- a raspberry pi (Pi3B+, PI4, or Zero W)
- 5 * 28BYJ-48 stepper motors with 
- 5 * motor drivers UNL2003
- 5 * KY-010 photo interrupters
- 5 * ball bearings 5mm * 11mm * 4mm
- 5V 3A stabilized power adapter (to power the thing from regular 220v lines or plugs)
- lots of dupont cables or whatever you prefer to use for connections
- a couple of 3.5mm * 1mm * 1m flat aluminum profiles
- a couple of 6mm diameter * 1m cylinder hollow alumunum profiles 
- a couple of 4mm * 1m screw bar (metal rods that basically are endless screws, like in 3d printer shafts). this and the previous are needed to hold the frame together
- m4 nuts and bolts of various length
- m2 nuts and bolts for the photo interrupter tiny holes
- 1mm headless nails (you need to insert one of these nails in the drum little hole so that it passes through the photo interrupter each drum turn, auto-configuring the motor initial position, which in case you power off the device there is no way to know otherwise)
- black spray paint (not really necessary)

### what do you need to 3D print (stl included in the project's stl directory)
- 5 * drum L
- 5 * drum R
- 100 flaps (20 each drum)

## Assembly

![fully assembled](https://github.com/paolorussian/lostClock/blob/451074e7f9f27683f22044545b78cf1b7188a1a2/images/Image1.png) *an assembled single drum*

![disassembled](https://github.com/paolorussian/lostClock/blob/451074e7f9f27683f22044545b78cf1b7188a1a2/images/Image2.png) *an exploded single drum*

![nail and photo interrupter](https://github.com/paolorussian/lostClock/blob/451074e7f9f27683f22044545b78cf1b7188a1a2/images/Image3.png) *nail and photo interrupter*

![frame assembled partial](https://github.com/paolorussian/lostClock/blob/451074e7f9f27683f22044545b78cf1b7188a1a2/images/imageA.jpg) *unfinished frame assembled*

![photo interrupter](https://github.com/paolorussian/lostClock/blob/451074e7f9f27683f22044545b78cf1b7188a1a2/images/imageB.jpg) *photo interrupter*

![webserver](https://github.com/paolorussian/lostClock/blob/7ecc90296b30de98ed7c18913465e39b8d1c72f9/images/webserver.png) *web interface to switch or reset mode*


credits:
https://www.thingiverse.com/thing:3493999 Martin1111 for the drum and flap design, which, however got modified to accommodate other components.


