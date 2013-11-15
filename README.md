PiPano
======

Python script for automatically generating panoramas with Raspberry PI using a stepper motor to rotate the Raspberry PI camera module.


L293D
=====

               ---U---   
    ENABLE1  1 |     | 16 VSS
     INPUT1  2 |     | 15 INPUT4
    OUTPUT1  3 |     | 14 OUTPUT4
        GND  4 |     | 13 GND
        GND  5 |     | 12 GND
    OUTPUT2  6 |     | 11 OUTPUT3
     INPUT2  7 |     | 10 INPUT3
         Vs  8 |     |  9 ENABLE2
               -------


Connect the L293D to the following Raspberry PI GPIO ports:

 1 ENABLE1 -> 5v0
 2 INPUT1  -> #24
 3 OUTPUT1 -> Coil A #1  (blue)
 4 GND     -> GND
 5 GND     -> GND
 6 OUTPUT2 -> Coil A #2  (white)
 7 INPUT2  -> #25
 8 Vs      -> battery +
 9 ENABLE2 -> 5v0
10 INPUT3  -> #18
11 OUTPUT3 -> Coil B #2  (blue black)
12 GND     -> GND
13 GND     -> GND
14 OUTPUT4 -> Coil B #1  (white black)
15 INPUT4  -> #23
16 VSS     -> 5v0

Connect battery - to GND

 
