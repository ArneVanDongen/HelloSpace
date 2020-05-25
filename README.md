# HelloSpace

## Goals
* Sub-orbital flight to the next continent, firing upper stage 10 s more
* Get into orbit
* Get into orbit with enough fuel to land booster

## Achievements
* 500m hop, separate both stages, and recover both: 21-05-2020

## TODO
- [ ] Figure out a trajectory function that is straight up, through the thickest part of the atmosphere, and levels out at 75km altitude over 150km horizontal distance traveled
- [ ] Write a guidance module that follows an altitude over distance, plus inclination function
- [ ] Fix the suicide burn timing issue (strobe firing)
- [ ] Calculate when to end hop burn in order to reach goal altitude instead of stopping after
- [ ] Move to debug logging
- [ ] Write own SAS module
- [x] Figure out how to control two vessels at the same time
    > space_center.active_vessel is writable. After staging, the newest vessel can be found at the last index of space_center.vessels not containing 'Debris'
- [x] Bug in ascend speed
- [x] Use CelestialBody object of Kerbin
- [x] calculate throttle for ascent also
- [x] add air resistance to throttle calculator
- [x] Calculate when to last start suicide burn instead of taking altitude
- [x] Take ground dynamic distance to ground instead of launch attitude
- [x] Add RCSs to vehicle to prevent tip over on landing, and stabilize horizontal movement
- [x] Instead of changing throttle reactively, calculate how much thrust is needed and apply it

## Contributors
* Hydraulixxd
