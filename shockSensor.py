#shockSensor.py
import RPi.GPIO as GPIO
import time

class ShockSensor:
    def __init__(self, sensor_pin):
        self.sensor_pin = sensor_pin
        GPIO.setup(self.sensor_pin, GPIO.IN)
        self.duration = 0.0

    def measure_duration(self):
        
        MAX_DETECTION_TIME = 1  # 최대 진동 감지 시간 (초)
        start_time = time.time()
        detection_start = None
        detection_stop = None

        # 진동 감지
        while time.time() - start_time < MAX_DETECTION_TIME:
            if GPIO.input(self.sensor_pin) == GPIO.LOW:
                if detection_start is None:
                    detection_start = time.time()

            elif GPIO.input(self.sensor_pin) == GPIO.HIGH:
                if detection_start is not None:
                    detection_stop = time.time()
                    break

        # 진동 지속 시간 계산
        if detection_start is not None and detection_stop is not None:
            self.duration = (detection_stop - detection_start) * 1000  # ms(마이크로초)

            # 지속시간에 따라 level 출력
            if self.duration >= 0.7:
                print(f"level 3 - Vibration Duration: {self.duration:.2f}ms")
                return "ALERT"
            else:
                print(f"level 2 - Vibration Duration: {self.duration:.2f}ms")

        elif detection_start is None:
            print(f"level 1 - No vibration detected")

        return "NORMAL"

# # test
# GPIO.setmode(GPIO.BCM)
# s = ShockSensor(17)

# try:
#     while True:
#         s.measure_duration()
#         time.sleep(0.5)

# except KeyboardInterrupt:
#     print("Interrupted by user")

# finally:
#     GPIO.cleanup()
#     print("GPIO cleaned up")
