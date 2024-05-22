from machine import Pin, ADC, PWM
import time

# Define GPIO pins for ESP32
led2_pin = 26
led3_pin = 25
led4_pin = 27
ldr_pin = 35
ir1_pin = 32
ir2_pin = 33
ir3_pin = 34

# Initialize GPIO pins
led2 = Pin(led2_pin, Pin.OUT)
led3 = Pin(led3_pin, Pin.OUT)
led4 = Pin(led4_pin, Pin.OUT)
ldr = ADC(Pin(ldr_pin))
ir1 = Pin(ir1_pin, Pin.IN)
ir2 = Pin(ir2_pin, Pin.IN)
ir3 = Pin(ir3_pin, Pin.IN)

# Initialize PWM for LED control
led2_pwm = PWM(led2, freq=5000, duty=0)
led3_pwm = PWM(led3, freq=5000, duty=0)
led4_pwm = PWM(led4, freq=5000, duty=0)

# Function to set LED PWM duty cycle
def set_led_intensity(led_pwm, intensity):
    duty = int((intensity / 255) * 1023)  # Convert 0-255 range to 0-1023 range for PWM
    led_pwm.duty(duty)

while True:
    ldr_value = ldr.read()
    print("LDR Value:", ldr_value)

    if ldr_value < 500:
        # Low light condition, turn on LEDs
        set_led_intensity(led2_pwm, 128)  # Initial medium intensity
        set_led_intensity(led3_pwm, 128)  # Initial medium intensity
        set_led_intensity(led4_pwm, 128)  # Initial medium intensity
        print("LEDs are ON at medium intensity due to low light condition.")

        # Read IR sensor values
        ir1_value = ir1.value()
        ir2_value = ir2.value()
        ir3_value = ir3.value()
        print("IR1 Value:", ir1_value)
        print("IR2 Value:", ir2_value)
        print("IR3 Value:", ir3_value)

        # Check IR sensors and adjust LED intensities
        if ir1_value == 0:
            set_led_intensity(led3_pwm, 255)  # Max intensity
            print("IR1 detected close object. LED3 at max intensity.")
        else:
            set_led_intensity(led3_pwm, 128)  # Medium intensity

        if ir2_value == 0:
            set_led_intensity(led4_pwm, 255)  # Max intensity
            print("IR2 detected close object. LED4 at max intensity.")
        else:
            set_led_intensity(led4_pwm, 128)  # Medium intensity

        if ir3_value == 0:
            set_led_intensity(led2_pwm, 255)  # Max intensity
            print("IR3 detected close object. LED2 at max intensity.")
        else:
            set_led_intensity(led2_pwm, 128)  # Medium intensity
    else:
        # Normal light condition, turn off LEDs
        led2_pwm.duty(0)
        led3_pwm.duty(0)
        led4_pwm.duty(0)
        print("LEDs are OFF due to normal light condition.")

    time.sleep(1)  # Delay for 1 second to avoid flooding the serial console

