# AI Finger Counter LED Controller (ESP32 + OpenCV)

Show fingers to your webcam, and an ESP32 lights up LEDs matching the count in real time — no touch, no buttons. Built using OpenCV + MediaPipe for hand tracking on a PC, sending the finger count to an ESP32 over serial.

## How it works

1. Webcam feed is processed on your PC using OpenCV + MediaPipe hand tracking.
2. The number of raised fingers (0–5) is detected each frame.
3. A smoothing filter waits for the same count across several consecutive frames before accepting it, avoiding flicker.
4. The stable count is sent to the ESP32 over USB serial.
5. The ESP32 lights up that many LEDs.

## Hardware required

- ESP32 Dev Board
- 5x LEDs
- 5x 220 ohm resistors
- Breadboard + jumper wires
- USB data cable
- A laptop with a webcam

## Wiring

| LED | ESP32 GPIO |
|-----|-----------|
| LED1 | 15 |
| LED2 | 2 |
| LED3 | 4 |
| LED4 | 5 |
| LED5 | 18 |

Each LED: long leg (anode) through a 220 ohm resistor to the GPIO pin. Short leg (cathode) to GND. All LED cathodes share the same GND rail, connected back to ESP32 GND.

Note: GPIO 2 is the onboard LED on many ESP32 boards, so LED1 may blink along with the board's built-in LED too — this is normal.

## Software setup

### 1. Arduino IDE (ESP32 side)

- Install Arduino IDE and add ESP32 board support (Boards Manager -> search "esp32" -> install).
- Open `esp32_finger_led.ino`.
- Select board: ESP32 Dev Module.
- Select the correct COM port.
- Upload the sketch.
- Close the Serial Monitor after uploading (Python needs the port).

### 2. Python (PC side)

Requires Python 3.11 (MediaPipe does not yet support the latest Python releases).

```
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

Open `finger_counter.py` and change the COM port on this line to match your ESP32:

```python
ser = serial.Serial('COM5', 115200, timeout=1)
```

Run it:

```
python finger_counter.py
```

A webcam window opens. Raise fingers to control the LEDs. Press `q` to quit.

## Troubleshooting

- **LEDs don't respond:** Check the COM port matches on both Arduino IDE and the Python script. Close Serial Monitor before running Python (only one program can use the port at a time).
- **`ModuleNotFoundError`:** Make sure `venv` is activated (prompt shows `(venv)`) and use `python -m pip install ...` instead of plain `pip install ...` to guarantee packages install into the virtual environment.
- **`AttributeError: module 'mediapipe' has no attribute 'solutions'`:** You have a mediapipe version that removed the legacy API. Install the pinned version: `python -m pip install mediapipe==0.10.14`.
- **LED flickering on/off rapidly:** Already handled by the built-in smoothing filter in `finger_counter.py` (waits for 7 consistent frames before updating).

## Demo

ESP32 x OpenCV — AI-powered hand controlled LEDs.

---
Built by TechTadka360
