""" 
  Author: Samuel Fieldhouse
  Company: Thrive Networks 
  THRIVE CONFIDENTIAL & THRIVE PROPRIETARY SOURCE CODE
"""

from .operations import operations, check_con
from connectors.core.connector import get_logger, ConnectorError, Connector

logger = get_logger('ipstack')


class symbol(Connector):

    def execute(self, config, operation, params, **kwargs):
        try:
            action = operations.get(operation)
            logger.debug('Action name {0}'.format(action))
            return action(config, params)
        except Exception as e:
            raise ConnectorError(e)

    def check_health(self, config):
        check_con(config)
