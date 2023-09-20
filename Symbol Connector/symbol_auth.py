""" 
  Author: Samuel Fieldhouse
  Company: Thrive Networks 
  THRIVE CONFIDENTIAL & THRIVE PROPRIETARY SOURCE CODE
  add access token to info (& hide)
"""

import requests
from connectors.core.connector import ConnectorError, get_logger

CONFIG_SUPPORTS_TOKEN = True
try:
    from connectors.core.utils import update_connnector_config
except:
    CONFIG_SUPPORTS_TOKEN = False
    configfile = path.join(path.dirname(path.abspath(__file__)), 'config.conf')


def get_token(config):
    baseURL = config.get('url').strip()
    protocol = config.get('protocol').strip()
    api_key = config.get('api_key')
    if not any([baseURL.startswith('https://'), baseURL.startswith('http://')]):
      baseURL = protocol + '://' + baseURL
      baseURL = baseURL + '/auth/access'
      headers = {'Authorization':'{0} {1}'.format('Bearer', api_key)}
      response=requests.request("POST", baseURL, json=None,params=None, headers=headers)
      if response.status_code in [200, 204, 201]:
        #config.set() #set access token 
        return response.json().get('accessToken')
      else:
        if response.text != "":
          error_msg = ''
          err_resp = response.json()
          if err_resp and 'error' in err_resp:
            failure_msg = err_resp.get('error_description')
            error_msg = 'Response {0}: {1} \n Error Message: {2}'.format(response.status_code, response.reason, failure_msg if failure_msg else '')
          else:
            err_resp = response.text
        else:
          error_msg = '{0}:{1}'.format(response.status_code, response.reason)
          raise ConnectorError(error_msg)


