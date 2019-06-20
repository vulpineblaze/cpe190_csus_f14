# Light Pen - Senior Design Team 8 Repo CSUS F14-S15
> Light Pen IR based low-cost education tool to turn a stardard projector into a digital whiteboard. 

## Table of contents
* [General info](#general-info)
* [Screenshots](#screenshots)
* [Setup](#setup)
  * [Requirements](#requirements)
  * [Usage](#usage)
* [Features](#features)
* [Status](#status)
* [Contact](#contact)

## General info
*With an increase in technological growth, one major
problem in education is the inability to keep up with the
advancements that can benefit school systems. Not only could
upgrading school systems save time and money in the long run, it
could also increase learning capabilities of students as well. With
younger children being exposed to more and more interactive
technology each and every day, it would be wise to bring these
familiar interactive methods into schools for use in educational
purposes. The LightPen team has taken cost effective infrared
based interactive whiteboard technology that integrates with
other existing resources such as classroom installed projectors
and computers, and made it more intuitive for those who are
accustomed to traditional chalkboards or whiteboards to interact
in an evolving technological environment. This document records
the process of designing such a product over the course of two
semesters*

[Project Documentation](./LightPen_EOP_Doc.pdf)

## Screenshots
![Light Pen Concept Art](./IWB_Concept.png)

## Setup
Described in Section [VIII. USER MANUAL](./LightPen_EOP_Doc.pdf)

### Requirements
Hardware
* Wiimote (or other IR Positioning Human Interfacing
Device) connected to PC
* USB port for optional USB Receiver

Software
* gtkWhiteboard
* Ardesia

Operating System
* Linux

### Usage
The LightPen activates when the writing tip is within
a certain distance to the screen. This distance can be slightly
customized by putting the tip near the screen and pressing the
calibrate button on the LightPen when youre comfortable with
the distance. 
*Always make sure that the Wiimote has a clear
view of the writing tip of the LightPen when you expect it to
be active.*

* Make sure the LightPen is calibrated to activate when desired.

* Position the Wiimote so that it has a clear view of video displaywhere the LightPen will be used.

* Launch gtkwhiteboard.

* Press 1 & 2 button on Wiimote, then click Start in gtkwhiteboard to begin the calibration.

* Activate the LightPen at the four corners of the screen, as directed by gtkwhiteboard.

* Once successful calibration is complete, the LightPen will beready for use in Ardesia.

* Launch Ardesia and begin using the LightPen.


## Features
* The Pen will detect proximity to a flat surface
  *   Outcome: The Pen will detect when it is close to a
flat surface, and will detect when the Pen has moved
away from the surface.
* The Pen will emit IR when close to a flat surface
  *   Outcome: The Pen will be able to emit IR, given the
successful detection of the previous feature. The Pen
will not emit IR without the detection signal.
* The Receiver will receive IR
  *   Outcome: The Receiver will detect the IR signal and
pass that data to the View.
* Given the IR received, The Receiver/View will determine
the X,Y coordinate of The Pen near the flat surface.
  * Outcome: When the Pen is close enough to the flat
surface, the View will be able to determine where the
Pen is on the flat surface.
* The Receiver/View will change display on the flat surface, drawing lines
  *   Outcome: The View will draw on the flat surface
where the Pen is present.
* The View will be able to have different colors and be
able to erase
  *   Outcome: The View will draw in the correct color, to
include erasing.
* The Pen will take user input to determine
draw/color/erase state.
  *   Outcome: The User will be able to change the color
of what is written or be able to use erase mode, by
only having to interact with the Pen in some way

## Status
Project is: _finished_

## Contact
Created by [@vulpineblaze](https://github.com/vulpineblaze) - feel free to contact me!
