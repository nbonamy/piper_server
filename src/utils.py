
import yaml

def safe_delete(obj):
  if hasattr(obj, 'delete'):
    obj.delete()
    
def load_yaml(filename):
  with open(filename, 'r') as file:
    return yaml.safe_load(file)
