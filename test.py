import microbit, radio
radio.on()
while True:
    gesture = microbit.accelerometer.current_gesture()
    if gesture != '':
        print(gesture)
    microbit.sleep(100)