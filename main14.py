from gpiozero import MotionSensor  # GPIO 입력을 위한 MotionSensor 라이브러리
import time                         # 시간 지연을 위한 라이브러리
from picamera2 import Picamera2     # 라즈베리파이 카메라 제어 라이브러리
import datetime                     # 현재 시간 정보를 가져오기 위한 라이브러리

# PIR 센서 설정 (GPIO 16번 핀 사용, 별도의 저항 없이 직접 연결)
pirPin = MotionSensor(16)

# 카메라 초기 설정 및 시작
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()

try:
    print("시스템 가동 중... 침입 감시를 시작합니다.")
    while True:
        # pirPin.value가 1이면 움직임이 감지된 상태
        if pirPin.value == 1:
            # 현재 날짜와 시간 정보를 가져옴
            now = datetime.datetime.now()
            print(f"침입 감지 시각: {now}")
            
            # 파일명을 '연-월-일 시:분:초.jpg' 형식으로 생성
            fileName = now.strftime('%y-%m-%d %H:%M:%S')
            
            # 설정한 파일명으로 사진 촬영 및 저장
            picam2.capture_file(fileName + '.jpg')
            
            # 센서의 중복 감지 및 연속 촬영 방지를 위해 0.5초간 대기
            time.sleep(0.5)
            
except KeyboardInterrupt:
    # Ctrl+C 입력 시 안전하게 프로그램 종료
    print("\n사용자에 의해 시스템이 종료되었습니다.")
