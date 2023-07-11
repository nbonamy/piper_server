
import os
import subprocess
from piper import Piper
from string import punctuation

class Synthesizer:
    
  def __init__(self, config):
    self._config = config
    self._pipers = {}

  def synthesize(self, text, voice=None):

    # first select the voice
    if voice is None:
      voice = self._config.get('voice', 'ryan')
    onnx = f'voices/{voice}/en_US-{voice}-medium.onnx'

    # does text have punctuation?
    # piper-python doesn't like punctuation
    dotless = text.strip(punctuation)
    has_punctuation = any(p in dotless for p in punctuation)

    # is text not too long?
    # command line can stream so it's better for long texts
    is_long = len(text) > 1024

    # commamnd line?
    use_command_line = has_punctuation or is_long

    # check if command is available
    if use_command_line and os.path.exists('./bin/piper'):
      print('Synthesizing with command line...')
      return self._synthesize_cmd(text, onnx)
    else:
      print('Synthesizing with library')
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
    piper_process.stdin.close()

    # header
    yield self._wave_header(22050, 16, 1)

    # now bytes
    while piper_process.poll() is None:
      data = piper_process.stdout.read1()
      if len(data) != 0:
        yield data

  def _synthesize_lib(self, text, onnx):

    # do we have a piper instance
    if onnx in self._pipers:
      piper = self._pipers[onnx]
    else:
      piper = Piper(onnx)
      self._pipers[onnx] = piper

    # now synthesize  
    #synthesize = partial(piper.synthesize)
    wav_bytes = piper.synthesize(text)
    yield wav_bytes

  def _wave_header(self, sampleRate, bitsPerSample, channels):
    datasize = 10240000 # Some veeery big number here instead of: #samples * channels * bitsPerSample // 8
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o