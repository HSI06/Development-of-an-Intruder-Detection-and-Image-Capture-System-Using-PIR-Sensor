from gpiozero import MotionSensor  # PIR 센서 제어를 위한 라이브러리
import time                         # 시간 지연(sleep)을 위한 라이브러리
from picamera2 import Picamera2     # 라즈베리파이 카메라 제어 라이브러리
import datetime                     # 현재 시간을 가져오기 위한 라이브러리

# PIR 센서 설정 (GPIO 16번 핀 사용)
pirPin = MotionSensor(16)

# 카메라 객체 생성 및 초기화
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start() # 카메라 시작

try:
    print("시스템 가동 중... 침입 감시 및 자동 촬영 모드입니다.")
    while True:
        # 인체 감지 센서값이 1(움직임 감지)인 경우
        if pirPin.value == 1:
            # 현재 시스템 시간을 가져옴
            now = datetime.datetime.now()
            print(f"침입 감지! 시각: {now}")
            
            # 파일명을 '26-04-13 23:15:30.jpg'와 같은 형식으로 생성
            # %y(년), %m(월), %d(일), %H(시), %M(분), %S(초)
            fileName = now.strftime('%y-%m-%d %H:%M:%S')
            
            # 생성된 파일 이름으로 사진 촬영 및 저장
            picam2.capture_file(fileName + '.jpg')
            
            # 연속 촬영을 방지하고 시스템 안정을 위해 0.5초 대기
            time.sleep(0.5)
            
except KeyboardInterrupt:
    # Ctrl + C 클릭 시 종료 메시지 출력
    print("\n보안 프로그램을 종료합니다.")
