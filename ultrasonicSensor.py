#ultrasonicSensor.py
import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    def __init__(self, trig_pin, echo_pin):
        self.TRIG = trig_pin
        self.ECHO = echo_pin
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        self.distance = 0.0

    def measure_distance(self):

        # TRIG 핀에서 10us 동안 펄스 발생
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

        # 상승/하강 시간값 초기화
        start = stop = 0.0

        # Echo핀 상승 시간값 저장
        while GPIO.input(self.ECHO) == 0:
            start = time.time()

        # Echo핀 하강 시간값 저장
        while GPIO.input(self.ECHO) == 1:
            stop = time.time()

        # 상승/하강 시간 차이를 이용하여 거리 계산
        self.distance = (stop - start) * 34300 / 2
        print(f"Distance: {self.distance:.1f} cm", end=" ")

        if self.distance <= 10:
            print("<= 10cm")
            return "ALERT"
        elif self.distance <= 100:
            print("<= 100cm")
        else:
            print("> 100cm")
        return "NORMAL"
