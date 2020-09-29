import microbit
while True:
    print(microbit.accelerometer.current_gesture())
    microbit.sleep(100)