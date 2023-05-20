from hcsr04 import HCSR04

# ESP32
sensor1 = HCSR04(trigger_pin=13, echo_pin=32, echo_timeout_us=10000)
sensor2 = HCSR04(trigger_pin=13, echo_pin=33, echo_timeout_us=10000)
sensor1 = HCSR04(trigger_pin=13, echo_pin=34, echo_timeout_us=10000)
sensor2 = HCSR04(trigger_pin=13, echo_pin=35, echo_timeout_us=10000)

distance1 = sensor1.distance_cm()
distance2 = sensor2.distance_cm()
print('Distance:', distance1, 'cm')
print('Distance:', distance2, 'cm')