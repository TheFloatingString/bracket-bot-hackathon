import simpleaudio as sa

wave_obj = sa.WaveObject.from_wave_file("static/rick-roll.wav")
play_obj = wave_obj.play()
play_obj.wait_done()
