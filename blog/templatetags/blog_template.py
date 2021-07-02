from django.template.defaultfilters import register

@register.filter(name='list_get')
def list_get(d, k):
    '''Returns the given key from a dictionary.'''
    if d is '':
     return None
    
    else:
      return d[k]
      
@register.filter(name='dict_key')
def dict_key(d, k):
    '''Returns the given key from a dictionary.'''
    if d is '':
     return None
    
    else:
      return d.get(k)