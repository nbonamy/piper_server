
import io
import os
import wave
import subprocess
from piper import Piper

class Synthesizer:
    
  def __init__(self, config):
    self._config = config
    self._pipers = {}

  def synthesize(self, text, voice=None):

    # first select the voice
    if voice is None:
      voice = self._config.get('voice', 'ryan')
    onnx = f'voices/{voice}/en_US-{voice}-medium.onnx'

    # check if command is available
    if os.path.exists('./bin/piper'):
      return self._synthesize_cmd(text, onnx)
    else:
      return self._synthesize_lib(text, onnx)

  def _synthesize_cmd(self, text, onnx):

    # open the process
    piper_process = subprocess.Popen(
      f'./bin/piper --model {onnx} --output_raw'.split(),
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.DEVNULL,
    )

    # write text
    piper_process.stdin.write(text.encode('utf-8'))
    piper_process.stdin.flush()

    # read stdout
    audio = piper_process.communicate()[0]

    # Convert to WAV
    with io.BytesIO() as wav_io:
      wav_file: wave.Wave_write = wave.open(wav_io, "wb")
      with wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(22050)
        wav_file.writeframes(audio)

      return wav_io.getvalue()
    
  def _synthesize_lib(self, text, voice):

    # do we have a piper instance
    if voice in self._pipers:
      piper = self._pipers[voice]
    else:
      piper = Piper(f'./voices/{voice}')
      self._pipers[voice] = piper

    # now synthesize  
    #synthesize = partial(piper.synthesize)
    wav_bytes = piper.synthesize(text)
    return wav_bytes
