import pyautogui
import cv2
import numpy as np
import keyboard
import time
from PIL import ImageGrab
import os

class GameBot:
    def __init__(self):
        # 프로그램 실행 상태
        self.running = True
        # 기본 대기 시간 설정
        self.delay = 1.5  # 대기 시간을 1.5초로 증가
        # 이미지 매칭 신뢰도 임계값
        self.confidence = 0.7  # 신뢰도 임계값을 0.7로 낮춤
        
        # 이미지 경로 설정
        self.image_dir = "game_images"
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
            
        # 이미지 파일 경로
        self.module_icon = os.path.join(self.image_dir, "module_icon.png")  # 모듈 아이콘
        self.right_arrow = os.path.join(self.image_dir, "right_arrow.png")  # 오른쪽 화살표
        self.confirm_button = os.path.join(self.image_dir, "confirm_button.png")  # 확인 버튼
        self.driver_seat = os.path.join(self.image_dir, "driver_seat.png")  # 운전석 버튼
        self.mining = os.path.join(self.image_dir, "mining.png")  # 채광 버튼
        self.enter_button = os.path.join(self.image_dir, "enter_button.png")  # 입장 버튼
        
        # 레벨 설정
        self.target_level = 48
        
        # 레벨 UI 관련 설정
        self.level_region = None  # 레벨 텍스트가 표시되는 영역

    def set_target_level(self, level):
        """
        목표 레벨을 설정하는 메서드
        """
        self.target_level = level
        print(f"목표 레벨이 {level}로 설정되었습니다.")

    def check_level(self):
        """
        현재 선택된 레벨이 목표 레벨과 일치하는지 확인하는 메서드
        """
        try:
            # 현재는 레벨 확인 없이 바로 True를 반환
            # 추후 OCR 구현 시 실제 레벨 확인 로직 추가 예정
            return True
            
        except Exception as e:
            print(f"레벨 확인 실패: {e}")
            return False

    def start_mining(self):
        """
        채광 작업을 시작하는 메서드
        """
        print("작업을 시작합니다...")
        print("ESC 키를 누르면 프로그램이 종료됩니다.")
        try:
            while self.running:
                if keyboard.is_pressed('esc'):
                    print("ESC 키가 눌렸습니다. 프로그램을 종료합니다.")
                    self.stop()
                    break

                # 1. 모듈 제작 수행
                print("\n=== 모듈 제작 시작 ===")
                self.module_loop()
                time.sleep(self.delay * 2)  # 모듈 제작 후 잠시 대기

                # 2. 채광 작업 수행
                print("\n=== 채광 작업 시작 ===")
                self.mining_loop()
                time.sleep(self.delay)

        except Exception as e:
            print(f"오류 발생: {e}")
            self.stop()

    def start_module(self):
        """
        모듈 제작 작업을 시작하는 메서드
        """
        print("모듈 제작 작업을 시작합니다...")
        print("ESC 키를 누르면 프로그램이 종료됩니다.")
        try:
            while self.running:
                if keyboard.is_pressed('esc'):
                    print("ESC 키가 눌렸습니다. 프로그램을 종료합니다.")
                    self.stop()
                    break

                self.module_loop()
                time.sleep(self.delay)

        except Exception as e:
            print(f"오류 발생: {e}")
            self.stop()

    def mining_loop(self):
        """
        채광 작업의 주요 로직을 구현하는 메서드
        """
        try:
            # 1. 운전석 클릭
            print("\n운전석을 찾는 중...")
            if self.click_image(self.driver_seat, confidence=0.6):
                time.sleep(self.delay)
                
                # 2. 채광 클릭
                print("채광을 찾는 중...")
                if self.click_image(self.mining):
                    time.sleep(self.delay)
                    
                    # 3. 레벨 확인
                    print(f"레벨 {self.target_level} 확인 중...")
                    if self.check_level():
                        # 4. 입장 버튼 클릭
                        print("입장 버튼을 찾는 중...")
                        if self.click_image(self.enter_button):
                            print("채광 입장 완료!")
                            time.sleep(self.delay * 2)
                            return
                        else:
                            print("입장 버튼을 찾을 수 없습니다.")
                    else:
                        print("레벨이 일치하지 않습니다.")
                else:
                    print("채광을 찾을 수 없습니다.")
            else:
                print("운전석을 찾을 수 없습니다.")
                
        except Exception as e:
            print(f"채광 작업 중 오류 발생: {e}")

    def module_loop(self):
        """
        모듈 제작의 주요 로직을 구현하는 메서드
        """
        try:
            # 1. 모듈 아이콘 클릭
            print("\n모듈 아이콘을 찾는 중...")
            if self.click_image(self.module_icon, confidence=0.6):
                time.sleep(self.delay)
                
                # 2. 오른쪽 화살표 클릭
                print("오른쪽 화살표를 찾는 중...")
                if self.click_image(self.right_arrow):
                    time.sleep(self.delay)
                    
                    # 3. 확인 버튼 클릭
                    print("확인 버튼을 찾는 중...")
                    if self.click_image(self.confirm_button):
                        print("모듈 제작 완료!")
                        time.sleep(self.delay)
                        return
                    else:
                        print("확인 버튼을 찾을 수 없습니다.")
                else:
                    print("오른쪽 화살표를 찾을 수 없습니다.")
            else:
                print("모듈 아이콘을 찾을 수 없습니다.")
                
        except Exception as e:
            print(f"모듈 제작 중 오류 발생: {e}")

    def find_image(self, template_path, confidence=None):
        """
        화면에서 특정 이미지를 찾는 메서드
        """
        if confidence is None:
            confidence = self.confidence
        
        try:
            # 이미지 파일 존재 확인
            if not os.path.exists(template_path):
                print(f"이미지 파일을 찾을 수 없습니다: {template_path}")
                return None
                
            location = pyautogui.locateOnScreen(template_path, 
                                              confidence=confidence,
                                              grayscale=True)  # 흑백 이미지로 검색하여 속도 향상
            return location
        except Exception as e:
            print(f"이미지 찾기 실패: {e}")
            return None

    def click_image(self, template_path, confidence=None):
        """
        찾은 이미지 위치를 클릭하는 메서드
        """
        location = self.find_image(template_path, confidence)
        if location:
            try:
                center = pyautogui.center(location)
                pyautogui.click(center)
                print(f"클릭 성공: {template_path}")
                return True
            except Exception as e:
                print(f"클릭 실패: {e}")
                return False
        return False

    def stop(self):
        """
        프로그램 종료
        """
        self.running = False
        print("프로그램을 종료합니다.")

if __name__ == "__main__":
    # 안전 장치: 마우스가 화면 모서리로 가면 프로그램 중지
    pyautogui.FAILSAFE = True
    
    # 봇 인스턴스 생성
    bot = GameBot()
    
    # 목표 레벨 설정
    bot.set_target_level(48)
    
    # 봇 실행
    bot.start_mining() 