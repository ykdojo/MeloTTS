from melo.api import TTS
import time

# Speed is adjustable
speed = 1.5

# CPU is sufficient for real-time inference.
# You can set it manually to 'cpu' or 'cuda' or 'cuda:0' or 'mps'
device = 'cpu' # Will automatically use GPU if available

# English 
text = "Did you ever hear a folk tale about a giant turtle?"
model = TTS(language='EN', device=device)
speaker_ids = model.hps.data.spk2id

# British accent
output_path = 'en-br.wav'

# Measure execution time
start_time = time.time()
model.tts_to_file(text, speaker_ids['EN-BR'], output_path, speed=speed)
execution_time = time.time() - start_time

print(f"Audio generation took {execution_time:.2f} seconds")
