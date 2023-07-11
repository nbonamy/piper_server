
class Configuration:

  def __init__(self, config):
    self._config = config

  def has(self, key):
    default = '__key_not_found__'
    val = self.get(key, default, get_dict=False)
    return False if val == default else True

  def get(self, key, default=None, get_dict=True):
    tokens = key.split('.')
    entries = self._config
    for token in tokens:
      try:
        entries = entries[token]
      except:
        return default
    return entries if get_dict or type(entries) is not dict else default

  def __getitem__(self, key):
    return self.get(key, get_dict=False)
