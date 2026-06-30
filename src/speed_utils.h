#ifndef SPEED_UTILS_H
#define SPEED_UTILS_H

/*
  speed_utils.h
  --------------
  Small helper functions for speed calculation, kept separate from
  main firmware logic so they can be reasoned about (and unit-tested
  via the Python simulation in test/) independent of hardware I/O.
*/

inline float calculateSpeedMps(float distanceMeters, unsigned long deltaTimeMs) {
  if (deltaTimeMs == 0) return 0.0;
  float deltaTimeSec = deltaTimeMs / 1000.0;
  return distanceMeters / deltaTimeSec;
}

inline float mpsToKmph(float speedMps) {
  return speedMps * 3.6;
}

inline bool isOverSpeed(float speedKmph, float limitKmph) {
  return speedKmph > limitKmph;
}

#endif
