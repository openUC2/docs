# openUC2 Xiao AI Microscope hardware control PCB

**Overview:**

This PCB connects a Seeed Studio Xiao ESP32S3 module to the openUC2 modular cube system. It features a range of components for illumination and control of motors or servos, providing an I2C bus for integration with the UC2 ecosystem. The board is primarily designed for controlling a motorized system such as peristaltic pumps and driving Neopixel LEDs, with additional support for PWM-driven components and touch inputs.

![](./IMAGES/xiao-insert-with-illumination/capture-2024-10-16T18_45_33.539Z.png)

### **Components:**

1. **Microcontroller:**
   - **Seeed Studio Xiao ESP32S3**: A small ESP32-based microcontroller module, mounted via header sockets. The microcontroller is responsible for handling the firmware (UC2-ESP) and communicating with the peripherals.

2. **Power:**
   - Powered via **5V** input from the Xiao USB port, with a power distribution setup across the board.
   - **Voltage regulators and capacitors** (such as 100uF, 16V) ensure stable power to the motors and peripherals.

3. **Neopixel LED:**
   - **WS2812B Neopixel** mounted on the PCB, connected to the Xiao (TX/A6 pin).
   - **Optional extension connector** for additional Neopixels, allowing external LED strips or panels to be driven.
   - A **cuttable solder jumper** disables the onboard Neopixel if needed.

4. **Touch Buttons:**
   - Two **touch-sensitive fields** are connected to specific GPIO pins (marked TOUCH_1 and TOUCH_2).
   - These buttons allow for interactive input, triggering various functions (e.g., illumination control or motor activation) via the UC2-ESP firmware.

5. **Motor Drivers:**
   - **Two DRV8837C H-bridge motor drivers** are included on the board, providing control for two DC motors or a peristaltic pump.
   - Each driver has connections for **IN1, IN2**, and **OUT1, OUT2**, with bulk capacitors (100uF, 16V) ensuring stable operation.
   - The motors are powered directly from the 5V system, with a maximum load current of 200mA per driver.

6. **Servo/PWM Ports:**
   - **Two servo headers** (3-pin 2.54mm pitch) for connecting servos or other PWM-driven devices.
   - Each header provides power, ground, and a PWM signal from the Xiao, supporting standard 9g servos or similar devices.
   - Dedicated **servo PWM pins** are used to send signals to the connected servos.

7. **I2C Interface:**
   - **I2C headers (J701, J702)** provide connections for the UC2 bus system, enabling the integration of additional peripherals (such as sensors or other cubes).
   - **I2C pull-up resistors (2.2kΩ)** are included onboard, with optional solder jumpers for enabling or disabling these pull-ups.

### **Key Connections:**

1. **Microcontroller:**
   - Pin PA4_A1_D1: Connects to motor driver IN1.
   - Pin PA5_A2_D2: Connects to motor driver IN2.
   - Pin PB08_TX: Connects to Neopixel DIN for LED control.
   - I2C_SDA (PA8_A4) and I2C_SCL (PA9_A5) pins are connected to the I2C bus for external communication.

2. **Peripherals:**
   - Neopixel connected to **TX/A6** of Xiao.
   - **Touch inputs** connected to dedicated pins on the Xiao.
   - **Motor drivers** controlled via IN1 and IN2 lines from the Xiao, providing forward/reverse motor control.
   - **Servo connectors** provide power and PWM signals to connected servos.

### **Power Management:**
   - **5V input** powers the Xiao and is distributed to the other components, with onboard voltage regulation.
   - Capacitance to handle high inrush current (max. 470uF).

### **Firmware Integration:**
   - The board runs on the UC2-ESP firmware, leveraging the ESP32S3's capabilities to control motors, Neopixel LEDs, and servos while communicating over I2C.
   - Firmware includes support for both **manual control** via touch inputs and **automated sequences** for driving motors and lighting.

### **Usage Notes:**
   - Ensure all components are connected before powering the system via USB.
   - The onboard Neopixel can be extended by attaching an external strip to the **Neopixel Extend** port.
   - For higher power requirements, ensure adequate power supply via the USB connection.

This PCB design provides a versatile platform for integrating the Seeed Xiao ESP32S3 into the UC2 modular system, enabling advanced control of motors, servos, and lighting, with seamless integration into the UC2 bus system.

## Mounting inside a cube

It gets as easy as placing the PCB inside a cube. Et voila:

![](./IMAGES/xiao-insert-with-illumination/IMG_20241016_152830.jpg)

## Schematics

![](./IMAGES/xiao-insert-with-illumination/xiao-insert-with-illumination-1.png)

![](./IMAGES/xiao-insert-with-illumination/xiao-insert-with-illumination-2.png)

![](./IMAGES/xiao-insert-with-illumination/xiao-insert-with-illumination-3.png)

![](./IMAGES/xiao-insert-with-illumination/xiao-insert-with-illumination-4.png)

![](./IMAGES/xiao-insert-with-illumination/xiao-insert-with-illumination-5.png)

![](./IMAGES/xiao-insert-with-illumination/xiao-insert-with-illumination-6.png)

![](./IMAGES/xiao-insert-with-illumination/xiao-insert-with-illumination-6.png)


## Pin Table


| **ESP32S3 Pin**        | **PCB Port/Component**                    | **Function**                              |
|------------------------|-------------------------------------------|-------------------------------------------|
| **D6 (TX)**             | Neopixel                                  | Neopixel data pin                         |
| **D0 (GPIO1)**          | Touch Button 1                            | Touch input 1 using `touchRead`           |
| **D1 (GPIO2)**          | Touch Button 2                            | Touch input 2 using `touchRead`           |
| **D3 (GPIO0)**          | Motor Driver 1 (IN1)                     | Motor 1 control                           |
| **D4 (GPIO9)**          | Motor Driver 1 (IN2)                     | Motor 1 control                           |
| **D9 (GPIO10)**         | Motor Driver 2 (IN1)                     | Motor 2 control                           |
| **D10 (GPIO3)**         | Motor Driver 2 (IN2)                     | Motor 2 control                           |
| **D4 (GPIO4)**          | I2C SDA                                  | I2C Data Line                             |
| **D5 (GPIO5)**          | I2C SCL                                  | I2C Clock Line                            |
| **D7 (GPIO8)**          | Servo Connector 1 (PWM)                  | Servo 1 PWM signal                        |
| **D8 (GPIO11)**         | Servo Connector 2 (PWM)                  | Servo 2 PWM signal                        |
| **3.3V**                | Power Supply                             | Powers Xiao and connected components      |
| **5V**                  | Power Supply (Neopixel and Motor Drivers)| Powers high-power components like motors  |
| **GND**                 | Ground                                   | Common ground for all components          |

## Sample Programm for the Arduino IDE

Here’s a simple Arduino sketch for the ESP32S3 on the Seeed Studio Xiao module. This sketch will test the Neopixel LED, motor drivers, touch buttons, servos, and I2C functionality on the PCB. You need the required libraries installed (`Adafruit_NeoPixel`, `Wire` for `I2C`, and `ESP_Servo` for servo control). The sketch assumes the UC2-ESP firmware isn't running.

```cpp
#include <Adafruit_NeoPixel.h>
#include <Wire.h>

// Pin definitions for Xiao ESP32S3 (using D1, D2, etc.)
#define NEOPIXEL_PIN D6         // Neopixel data pin (TX)
#define TOUCH_PIN_1 D0          // Touch Button 1 (Touch Pad 1)
#define TOUCH_PIN_2 D1          // Touch Button 2 (Touch Pad 2)
#define MOTOR_1_IN1 D3          // Motor 1 IN1 (GPIO0)
#define MOTOR_1_IN2 D4          // Motor 1 IN2 (GPIO9)
#define MOTOR_2_IN1 D9          // Motor 2 IN1 (GPIO10)
#define MOTOR_2_IN2 D10         // Motor 2 IN2 (GPIO3)
#define I2C_SDA D4              // I2C SDA (GPIO4)
#define I2C_SCL D5              // I2C SCL (GPIO5)
#define SERVO_PIN_1 D7          // Servo 1 PWM (GPIO8)
#define SERVO_PIN_2 D8          // Servo 2 PWM (GPIO11)

#define PWM_CHANNEL_SERVO_1 0
#define PWM_CHANNEL_SERVO_2 1
#define minPulseWidth 500      // Minimum pulse width for servos (in microseconds)
#define maxPulseWidth 2500     // Maximum pulse width for servos (in microseconds)

// Neopixel setup
#define NUMPIXELS 1
Adafruit_NeoPixel neopixel(NUMPIXELS, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);

// Servo control variables
int pwm_frequency = 50;
int pwm_resolution = 16;

// I2C test address
const int i2cAddress = 0x3C;

// Touch thresholds
int touchThreshold1 = 30;
int touchThreshold2 = 30;

void setup() {
  // Initialize Serial for debugging
  Serial.begin(115200);

  // Initialize Neopixel
  neopixel.begin();
  neopixel.setBrightness(50);  // Adjust brightness (0-255)

  // Initialize motor pins
  pinMode(MOTOR_1_IN1, OUTPUT);
  pinMode(MOTOR_1_IN2, OUTPUT);
  pinMode(MOTOR_2_IN1, OUTPUT);
  pinMode(MOTOR_2_IN2, OUTPUT);

  // Initialize I2C
  Wire.begin(I2C_SDA, I2C_SCL);

  // Configure PWM for servos
  configurePWM(SERVO_PIN_1, pwm_resolution, PWM_CHANNEL_SERVO_1, pwm_frequency);
  configurePWM(SERVO_PIN_2, pwm_resolution, PWM_CHANNEL_SERVO_2, pwm_frequency);
}

void loop() {
  // Test Neopixel LED
  neopixelTest();

  // Test Touch Buttons
  touchTest();

  // Test Motor Drivers
  motorTest();

  // Test Servo Motors
  moveServo(PWM_CHANNEL_SERVO_1, 90, pwm_frequency, pwm_resolution);  // Move servo to 90°
  moveServo(PWM_CHANNEL_SERVO_2, 90, pwm_frequency, pwm_resolution);  // Move servo to 90°

  // Test I2C Communication
  i2cTest();

  delay(2000);  // Wait 2 seconds before the next test cycle
}

// Neopixel Test: Cycles through colors
void neopixelTest() {
  Serial.println("Testing Neopixel...");
  neopixel.setPixelColor(0, neopixel.Color(255, 0, 0));  // Red
  neopixel.show();
  delay(500);
  neopixel.setPixelColor(0, neopixel.Color(0, 255, 0));  // Green
  neopixel.show();
  delay(500);
  neopixel.setPixelColor(0, neopixel.Color(0, 0, 255));  // Blue
  neopixel.show();
  delay(500);
}

// Touch Test: Reads touch inputs
void touchTest() {
  int touchValue1 = touchRead(TOUCH_PIN_1);
  int touchValue2 = touchRead(TOUCH_PIN_2);

  Serial.print("Touch Button 1: ");
  Serial.println(touchValue1);
  Serial.print("Touch Button 2: ");
  Serial.println(touchValue2);

  if (touchValue1 < touchThreshold1) {
    Serial.println("Touch Button 1 activated!");
  }
  if (touchValue2 < touchThreshold2) {
    Serial.println("Touch Button 2 activated!");
  }
}

// Motor Test: Drives both motors forward and backward
void motorTest() {
  Serial.println("Testing Motor 1...");
  digitalWrite(MOTOR_1_IN1, HIGH);
  digitalWrite(MOTOR_1_IN2, LOW);
  delay(1000);
  digitalWrite(MOTOR_1_IN1, LOW);
  digitalWrite(MOTOR_1_IN2, HIGH);
  delay(1000);

  Serial.println("Testing Motor 2...");
  digitalWrite(MOTOR_2_IN1, HIGH);
  digitalWrite(MOTOR_2_IN2, LOW);
  delay(1000);
  digitalWrite(MOTOR_2_IN1, LOW);
  digitalWrite(MOTOR_2_IN2, HIGH);
  delay(1000);

  digitalWrite(MOTOR_1_IN1, LOW);
  digitalWrite(MOTOR_1_IN2, LOW);
  digitalWrite(MOTOR_2_IN1, LOW);
  digitalWrite(MOTOR_2_IN2, LOW);
}

// I2C Test: Scans for I2C devices
void i2cTest() {
  Serial.println("Scanning for I2C devices...");
  Wire.beginTransmission(i2cAddress);
  if (Wire.endTransmission() == 0) {
    Serial.println("I2C device found.");
  } else {
    Serial.println("No I2C device found.");
  }
}

// Configure PWM for servo motor control
void configurePWM(int servoPin, int resolution, int ledChannel, int frequency) {
  ledcDetachPin(servoPin);
  setupLaser(servoPin, ledChannel, frequency, resolution);
}

// Move Servo using PWM
void moveServo(int ledChannel, int angle, int frequency, int resolution) {
  int pulseWidth = map(angle, 0, 180, minPulseWidth, maxPulseWidth);
  int dutyCycle = map(pulseWidth, 0, 1000000 / frequency, 0, (1 << resolution) - 1);
  ledcWrite(ledChannel, dutyCycle);
}

// Helper function to setup the servo PWM channel
void setupLaser(int pin, int channel, int frequency, int resolution) {
  ledcSetup(channel, frequency, resolution);
  ledcAttachPin(pin, channel);
}
```
## GPIO converter

| **Pin Label**  | **ESP32S3 GPIO**  | **PCB Port/Component**                    | **Function**                              |
|----------------|-------------------|-------------------------------------------|-------------------------------------------|
| **D0**         | **GPIO1**          | Touch Button 1                            | Touch input 1 using `touchRead`           |
| **D1**         | **GPIO2**          | Touch Button 2                            | Touch input 2 using `touchRead`           |
| **D2**         | **GPIO3**          | Motor Driver 2 (IN2)                      | Motor 2 control                           |
| **D3**         | **GPIO4**          | Motor Driver 1 (IN1)                      | Motor 1 control                           |
| **D4**         | **GPIO5**          | Motor Driver 1 (IN2)                      | Motor 1 control                           |
| **D5**         | **GPIO6**          | I2C SCL                                  | I2C Clock Line                            |
| **D6**         | **GPIO7**          | Neopixel                                  | Neopixel data pin                         |
| **D7**         | **GPIO8**          | Servo Connector 1 (PWM)                  | Servo 1 PWM signal                        |
| **D8**         | **GPIO9**          | Servo Connector 2 (PWM)                  | Servo 2 PWM signal                        |
| **D9**         | **GPIO10**         | Motor Driver 2 (IN1)                      | Motor 2 control                           |
| **D10**        | **GPIO11**         | I2C SDA                                  | I2C Data Line                             |

### Get Pin numbers from Macros

```cpp
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:

  Serial.print("D0: ");
  Serial.println(D0);
  Serial.print("D1: ");
  Serial.println(D2);
  Serial.print("D2: ");
  Serial.println(D2);    
  Serial.print("D3: ");
  Serial.println(D3);    
  Serial.print("D4: ");
  Serial.println(D4);    
  Serial.print("D5: ");
  Serial.println(D5);    
  Serial.print("D6: ");
  Serial.println(D6);    
  Serial.print("D7: ");
  Serial.println(D7);    
  Serial.print("D8: ");
  Serial.println(D8);    
  Serial.print("D9: ");
  Serial.println(D9);    
  Serial.print("D10: ");
  Serial.println(D10);   
  delay(1000);

}
```

## iBOM

<iframe width="100%" style={{"aspect-ratio": "16 / 9"}} src="https://docs.openuc2.com/kicad/ibom-led-xiao.html" title="iBOM" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>



## Tutorial for the new firmware


The firmware is available here https://github.com/youseetoo/openuc2-seeed-xiaos3-microscopy-board


<p><iframe width="560" height="315" src="https://www.youtube.com/embed/undefined" title="" frameBorder="0"   allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"  allowFullScreen><br>Powered by <a href="https://youtubeembedcode.com">how to get embed code from youtube</a> and <a href="https://xn--helgln-mua.com/">helglån.com</a></iframe></p>


![](./IMAGES/IMG_20260504_092458.jpg)


## Troubleshoot

If you have any questions, please feel free to reach out to us using the Forum: openuc2.discourse.group.
