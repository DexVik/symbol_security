""" 
  Author: Samuel Fieldhouse
  Hours of Pain: 18
  Last Update: 5/12/23
  Company: Thrive Networks 
  THRIVE CONFIDENTIAL & THRIVE PROPRIETARY SOURCE CODE
"""
import validators, requests, json
from connectors.core.connector import ConnectorError, get_logger
from .symbol_auth import get_token

logger = get_logger('Symbol-SAT')

error_msgs = {
    400: 'Bad/Invalid Request',
    401: 'Unauthorized: Invalid credentials',
    403: 'Access Denied',
    404: 'Not Found',
    500: 'Unauthorized: Invalid credentials',
    503: 'Service Unavailable'
}

class symbol:
    def __init__(self, config):
      self.myconfig = config
      self.baseURL = config.get('url').strip()
      self.protocol = config.get('protocol').strip()
      self.api_key = config.get('api_key')
      self.accesstoken = config.get('access_token')
      if not any([self.baseURL.startswith('https://'), self.baseURL.startswith('http://')]):
        self.baseURL = self.protocol + '://' + self.baseURL
        self.headers = {'Authorization':'{0} {1}'.format('Bearer', self.accesstoken)} #additional token work and refresh tokens 

    def restCall(self, endpoint, headers=None, params=None, data=None, method='GET'):
      headers = headers if headers else self.headers
      url = '{base}{ep}'.format(base=self.baseURL, ep=endpoint)
      logger.info('Request URL {0}'.format(url))
      try:
        response=requests.request(method, url, json=data,params=params, headers=headers)
        if response:
          return json.loads(response.content.decode('utf-8'))
        else:
          if (response.json().get('message') == "Sorry, you are not authorized to access this resource"):
            auth = get_token(self.myconfig) # updates the API token to a new one 
            newHead = {'Authorization':'{0} {1}'.format('Bearer', auth)} #additional token work and refresh tokens
            response=requests.request(method, url, json=data,params=params, headers=newHead)
            if response.ok:
              return json.loads(response.content.decode('utf-8'))
            else:
              error_msg = response.json().get('message')
              error_reason = response.json().get('reason')
              logger.error(error_msg)
              raise ConnectorError(error_msg)
              raise
          else:
            error_msg = response.json().get('message')
            error_reason = response.json().get('reason')
            logger.error(error_msg)
            raise ConnectorError(error_msg)
            raise

      except Exception as e:
          logger.exception(e)
          raise ConnectorError(e)


# def _check_health(config): health check file 
def check_con(config):
    newCheck = symbol(config)
    try:
        response = newCheck.restCall('/msp/companies', method='GET')
        if response:
            logger.info('connector available')
            return True
    except Exception as e:
        raise ConnectorError('{0}'.format(e))

def get_companies(config, param):
    symbol_instance = symbol(config)
    return symbol_instance.restCall('/msp/companies')

def add_company(config, param):
    symbol_instance = symbol(config)
    return symbol_instance.restCall('/msp/companies/', params=param,method='POST')

def get_company_id(config, param):
    symbol_instance = symbol(config)
    return symbol_instance.restCall('/msp/companies/{}/'.format(param['company_id']))

def update_company(config, params):
    symbol_instance = symbol(config)
    company_data = params.get('company_data')
    return symbol_instance.restCall('/msp/companies/'+ params['company_id'] + '/', params=company_data, method='PUT')

def get_cyber_threat(config, param):
    symbol_instance = symbol(config)
    return symbol_instance.restCall('/msp/companies/{}/cyber-threats/results'.format(param['company_id']))

def get_email_threats(config, param):
    symbol_instance = symbol(config)
    return symbol_instance.restCall('/msp/companies/{}/email-threats/alerts'.format(param['company_id']))

def get_domain_threats(config, param):
    symbol_instance = symbol(config)
    domain = param.get('domain')
    if domain:
        return symbol_instance.restCall('/msp/companies/'+ param['company_id'] + '/domains/threats?domain=' + domain)
    else:
        return symbol_instance.restCall('/msp/companies/{}/domains/threats'.format(param['company_id']))


operations = {
    'get_companies': get_companies,
    'add_company': add_company,
    'get_company_id': get_company_id,
    'update_company': update_company,
    'get_cyber_threat': get_cyber_threat,
    'get_email_threats': get_email_threats,
    'get_domain_threats': get_domain_threats
}