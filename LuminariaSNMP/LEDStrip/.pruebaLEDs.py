
from LuminariaSNMP.LEDStrip.strip import LED_Strip
strip = LED_Strip(19,21,23)

strip.start_pwm(20000)

strip.change_duty(0,0,0)

while True:
    r,g,b = [int(x) for x in input().split()]
    strip.change_duty(r,g,b)
