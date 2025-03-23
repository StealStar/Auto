import PyInstaller.__main__
import os

# 현재 디렉토리의 game_images 폴더를 포함하도록 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, 'game_images')

PyInstaller.__main__.run([
    'auto_game_ui.py',
    '--onefile',
    '--windowed',
    '--name=LimbusCompany_Auto',
    f'--add-data={images_dir};game_images',
]) 