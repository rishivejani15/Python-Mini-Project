import pygame

def play_music():
    
    pygame.mixer.init()
    music_file = "Noise-Long-Version-chosic.com_.mp3"  # Replace with your file path
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(loops=-1)  # -1 for infinite loop
    
def stop_music():
    pygame.mixer.music.stop()