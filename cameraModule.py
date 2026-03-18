#cameraModule.py
from picamera import PiCamera
import time
import datetime
import os

class CameraModule:
    def __init__(self, directory_path):
        self.camera = PiCamera()
        self.directory_path = directory_path
        self.video_path = ""
        self.recording_time = 0
        self.recording_max = 30
        self.video_list = []

    def start_recording(self):
        self.video_path = f'{self.directory_path}{datetime.datetime.now().strftime("%Y%m%d-%H_%M_%S")}.h264'
        self.camera.start_recording(self.video_path)
        self.recording_time = time.time()

    def end_recording_and_save(self):
        time.sleep(10)
        self.camera.stop_recording()
        self.convert_and_trim_video()

    def end_recording_and_remove(self):
        self.camera.stop_recording()
        os.system(f'rm {self.video_path}')

    def convert_and_trim_video(self):
        mp4_path = f'{self.video_path[:-5]}.mp4'                  # .mp4 파일 경로 설정 
        self.video_list.append(mp4_path)                          # video list에 저장 
        os.system(f'MP4Box -add {self.video_path} {mp4_path}')    # .h264 파일을 .mp4 파일로 변환하여 생성.
        os.system(f'rm {self.video_path}')                        # .h264 파일 삭제

    def load_video_list(self):
        for filename in os.listdir(self.directory_path):
            if filename.endswith('.mp4'):
                self.video_list.append(f'{self.directory_path}{filename}')
        self.video_list.sort()

# # test
# c = CameraModule('/home/pi/Videos/')
# c.start_recording()
# c.end_recording_and_save()
