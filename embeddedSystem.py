#embeddedSystem.py
import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from ultrasonicSensor import UltrasonicSensor
from shockSensor import ShockSensor
from cameraModule import CameraModule
from sendMail import SendMail

class EmbeddedSystem:

    def __init__(self):

        # GPIO set
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Initialize sensors
        self.ultrasonic_sensor = UltrasonicSensor(23, 24)
        self.shock_sensor = ShockSensor(17)
        self.camera_module = CameraModule('/home/pi/Videos/')
        self.send_mail = SendMail("sjpyo501@naver.com", "tjdwndrkt@13")

        # module active init
        self.active = False
        self.ultrasonic_active = True
        self.camera_active = False
        self.shock_active = False
        self.recording = False

        # Event callbacks
        self.shock_alert_callback = None
        self.video_list_update_callback = None

    def reset(self):
        self.ultrasonic_active = True
        self.camera_active = False
        self.shock_active = False
        self.recording = False
    
    def set_shock_alert_callback(self, callback):
        self.shock_alert_callback = callback

    def set_video_list_update_callback(self, callback):
        self.video_list_update_callback = callback

    def run(self):
        try:
            while True:

                if self.active:
                    self.reset()

                elif not self.active and self.recording:
                    self.camera_module.end_recording_and_remove()
                    self.reset()

                while self.active:

                    if self.ultrasonic_active:
                        status = self.ultrasonic_sensor.measure_distance()
                        if status == "ALERT":
                            self.ultrasonic_active = False
                            self.camera_active = True
                            self.shock_active = True

                    if self.camera_active:

                        if not self.recording:
                            self.camera_module.start_recording()
                            self.recording = True

                        elif self.recording and (time.time() - self.camera_module.recording_time >= self.camera_module.recording_max):
                                self.camera_module.end_recording_and_remove()
                                self.reset()

                    elif not self.camera_active and self.recording:
                        self.camera_module.end_recording_and_save()
                        self.video_list_update_callback({'video_list': self.camera_module.video_list})
                        self.send_mail.send_email()
                        self.reset()

                    if self.shock_active:
                        status = self.shock_sensor.measure_duration()
                        if status == "ALERT":
                            self.shock_alert_callback({'msg': 'Shock detected!'})
                            self.ultrasonic_active = False
                            self.camera_active = False
                            self.shock_active = False

                    time.sleep(0.5)

        except KeyboardInterrupt:
            print("Interrupted by user")

        finally:
            GPIO.cleanup()
            print("GPIO cleaned up")
