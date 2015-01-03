import re
  
def _add_to_header(response, key, value):
     if response.has_header(key):
         values = re.split(r'\s*,\s*', response[key])
         if not value in values:
             response[key] = ', '.join(values + [value])
     else:
         response[key] = value
  
def _nocache(request, response):
     _add_to_header(response, 'Cache-Control', 'no-store')
     _add_to_header(response, 'Cache-Control', 'no-cache')
     _add_to_header(response, 'Pragma', 'no-cache')
     return response
  
class NoCachePages(object):
     def process_response(self, request, response):
         return _nocache(request, response)
