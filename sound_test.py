import pygame

# Initialize mixer
pygame.mixer.init()

# Load a sound file (WAV/MP3/OGG)
pygame.mixer.music.load("PowerUp.wav")

# Play it
pygame.mixer.music.play()

# Keep the script alive until sound finishes
while pygame.mixer.music.get_busy():
    pass