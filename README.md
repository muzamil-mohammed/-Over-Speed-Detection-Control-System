# 🚦 Over-Speed Detection & Control System

An embedded systems project that detects when a vehicle exceeds a predefined speed limit using IR sensors and automatically regulates motor speed (simulating a vehicle) through PWM control. Includes a buzzer/LED alert system and serial-monitor speed logging for real-time monitoring.

![Status](https://img.shields.io/badge/status-completed-brightgreen)
![Platform](https://img.shields.io/badge/platform-Arduino-00979D)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 📌 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Hardware Components](#hardware-components)
- [Circuit Diagram](#circuit-diagram)
- [Working Principle](#working-principle)
- [Software / Code](#software--code)
- [Installation & Setup](#installation--setup)
- [Calibration](#calibration)
- [Results](#results)
- [Project Structure](#project-structure)
- [Future Enhancements](#future-enhancements)
- [Tech Stack](#tech-stack)
- [License](#license)

---

## 🧭 Overview

Over-speeding is one of the leading causes of road accidents. This project implements a low-cost embedded system that:
1. **Detects** the real-time speed of a moving object (vehicle/wheel) using two IR sensors placed at a known distance apart.
2. **Calculates** speed using the time taken to travel between the two sensors.
3. **Compares** the calculated speed against a configurable speed limit.
4. **Controls** the system by automatically reducing motor speed (via PWM) and triggering visual/audible alerts (LED + buzzer) when the speed limit is exceeded.
5. **Logs** live speed data to the Serial Monitor for analysis/debugging.

This is designed as a scaled-down prototype (DC motor + wheel) demonstrating the same principle used in real-world speed governors and smart traffic-zone speed control systems (e.g., school zones, highway toll booths).

---

## ✨ Features

- Real-time speed calculation using dual IR sensor time-of-flight method
- Configurable speed threshold (`SPEED_LIMIT`)
- Automatic PWM-based motor speed reduction on over-speed detection
- Buzzer + LED alert system
- Live speed readout via Serial Monitor (can be extended to an LCD)
- Debounce handling for sensor noise
- Modular, well-commented code for easy customization
- Optional LCD (16x2 I2C) display support

---

## 🏗️ System Architecture

```
        ┌─────────────┐        ┌─────────────┐
        │  IR Sensor  │        │  IR Sensor  │
        │   (S1)      │        │   (S2)      │
        └──────┬──────┘        └──────┬──────┘
               │                      │
               ▼                      ▼
        ┌─────────────────────────────────┐
        │         Arduino UNO/Nano        │
        │  - Captures time(S1) & time(S2) │
        │  - Computes speed = d / Δt      │
        │  - Compares with SPEED_LIMIT    │
        └───────┬───────────────┬─────────┘
                │               │
        ┌───────▼─────┐  ┌──────▼──────┐
        │ Buzzer + LED│  │ Motor Driver│
        │   (Alert)   │  │  (L298N)    │
        └─────────────┘  └──────┬──────┘
                                │
                         ┌──────▼──────┐
                         │   DC Motor  │
                         │  (simulated │
                         │   vehicle)  │
                         └─────────────┘
```

---

## 🔧 Hardware Components

| Component | Quantity | Purpose |
|---|---|---|
| Arduino UNO / Nano | 1 | Main microcontroller |
| IR Obstacle Sensor Module | 2 | Detect object passing to measure speed |
| L298N Motor Driver Module | 1 | Controls DC motor speed via PWM |
| DC Geared Motor + Wheel | 1 | Simulates vehicle movement |
| Buzzer | 1 | Audible over-speed alert |
| LED (Red) | 1 | Visual over-speed alert |
| 16x2 LCD (I2C, optional) | 1 | Display live speed |
| Resistors (220Ω) | 2 | LED current limiting |
| Breadboard + Jumper Wires | - | Connections |
| 9V/12V Battery or Power Adapter | 1 | Motor power supply |

**Approx. cost:** ₹800–1200 / $10–15 depending on sourcing.

---

## 🔌 Circuit Diagram

```
IR Sensor 1 (S1) OUT  -> Arduino Pin D2  (interrupt)
IR Sensor 2 (S2) OUT  -> Arduino Pin D3  (interrupt)
Buzzer (+)             -> Arduino Pin D8
LED (+)                -> Arduino Pin D9  (with 220Ω resistor)
L298N IN1               -> Arduino Pin D5
L298N IN2               -> Arduino Pin D6
L298N ENA (PWM)         -> Arduino Pin D10
L298N OUT1/OUT2         -> DC Motor terminals
L298N 12V / GND         -> External battery / GND
Arduino GND              -> Common GND (L298N, sensors, buzzer)
```

A full schematic (Fritzing-style) image should be placed in `images/circuit_diagram.png` — see `docs/circuit_notes.md` for pin-by-pin wiring notes.

---

## ⚙️ Working Principle

1. The two IR sensors (S1 and S2) are fixed a **known distance `d`** apart (e.g., 0.20 m) along the path of the moving wheel/object.
2. When the object breaks the beam of **S1**, the Arduino records timestamp `t1` using `millis()`.
3. When the same object breaks the beam of **S2**, the Arduino records timestamp `t2`.
4. **Speed** is calculated as:

   ```
   Speed (m/s) = d / (t2 - t1)
   Speed (km/h) = Speed (m/s) × 3.6
   ```

5. If `Speed (km/h) > SPEED_LIMIT`:
   - Buzzer + LED are activated.
   - Motor PWM duty cycle is reduced (e.g., from 255 to 120) to bring the simulated vehicle back under the limit.
   - "OVER SPEED!" warning is printed to Serial Monitor.
6. If speed is within limits, the motor runs at normal PWM and alerts remain off.

---

## 💻 Software / Code

The main firmware is in [`src/over_speed_detection.ino`](src/over_speed_detection.ino).

Key configurable constants:

```cpp
const float SENSOR_DISTANCE = 0.20;   // distance between IR sensors in meters
const float SPEED_LIMIT     = 5.0;    // speed limit in km/h (tune to your setup)
const int NORMAL_PWM        = 255;    // normal motor speed
const int REDUCED_PWM       = 120;    // reduced motor speed on over-speed
```

---

## 🛠️ Installation & Setup

### Prerequisites
- [Arduino IDE](https://www.arduino.cc/en/software) (1.8.x or 2.x)
- USB cable for Arduino UNO/Nano
- Components listed above wired per the circuit diagram

### Steps
```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/over-speed-detection-control.git
cd over-speed-detection-control

# 2. Open src/over_speed_detection.ino in Arduino IDE
# 3. Select Board: Tools > Board > Arduino UNO (or your board)
# 4. Select correct COM Port: Tools > Port
# 5. Click Upload
```

After uploading, open **Tools > Serial Monitor** (baud rate `9600`) to view live speed readings and alerts.

---

## 🎯 Calibration

- Adjust `SENSOR_DISTANCE` to match your physical sensor spacing.
- Adjust `SPEED_LIMIT` based on your test setup (a small DC motor wheel typically reaches 3–8 km/h equivalent speeds at the prototype scale).
- If sensors trigger falsely due to ambient light/noise, add a debounce delay (`DEBOUNCE_MS`) — already included in code and tunable.

---

## 📊 Results

| Test Case | Motor PWM | Measured Speed | Limit | Action Taken |
|---|---|---|---|---|
| 1 | 150 | 3.8 km/h | 5.0 km/h | Normal operation |
| 2 | 255 | 7.2 km/h | 5.0 km/h | Buzzer + LED ON, PWM reduced to 120 |
| 3 | 120 (after reduction) | 4.1 km/h | 5.0 km/h | Alerts OFF, normal operation resumed |

*(Replace with your own measured values once you run the hardware test.)*

---

## 📁 Project Structure

```
over-speed-detection-control/
├── README.md
├── LICENSE
├── src/
│   └── over_speed_detection.ino     # Main Arduino firmware
├── docs/
│   ├── circuit_notes.md             # Pin mapping & wiring details
│   └── project_report.md            # Detailed write-up (abstract, methodology, conclusion)
├── images/
│   └── circuit_diagram.png          # (add your circuit screenshot/photo here)
└── test/
    └── speed_calc_simulation.py     # Python script to simulate/verify speed-calc logic
```

---

## 🚀 Future Enhancements

- Replace IR sensors with an ultrasonic sensor (HC-SR04) or radar module (RCWL-0516) for contactless detection
- Add GPS + GSM module to log and report over-speed events with location to a remote server
- Integrate with a camera module (ESP32-CAM) for automatic number-plate capture on violation
- Push live data to a cloud dashboard (Firebase / ThingSpeak / MQTT) for IoT-based traffic monitoring
- Replace fixed `SPEED_LIMIT` with dynamic zone-based limits (e.g., lower limit near "school zone")

---

## 🧰 Tech Stack

- **Microcontroller:** Arduino (C/C++)
- **Sensors:** IR Obstacle Detection Modules
- **Actuation:** L298N Motor Driver, DC Motor, PWM
- **Tools:** Arduino IDE, Fritzing (for circuit diagram), Python (for simulation/testing)

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## 🙋 Author

Muzamil Mohammed
📧 mdmuzamil1119@gmail.com | 🔗 http://linkedin.com/in/muzamilmohammed | 
 
