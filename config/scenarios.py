import re
from enum import Enum


class Scenario(str, Enum):
    # user service
    USER_SERVICE_USER_DETAILS_V1_0 = 'scenarios/user_service/user_details/v1.0.conf'
    USER_SERVICE_USER_DETAILS_V2_0 = 'scenarios/user_service/user_details/v2.0.conf'

    # account service
    ACCOUNT_SERVICE_ACCOUNT_DETAILS_V1_0 = 'scenarios/account_service/account_details/v1.0.conf'
    ACCOUNT_SERVICE_ACCOUNT_DETAILS_V2_0 = 'scenarios/account_service/account_details/v2.0.conf'

    # operations service
    OPERATIONS_SERVICE_OPERATIONS_LIST_V1_0 = 'scenarios/operations_service/operations_list/v1.0.conf'
    OPERATIONS_SERVICE_OPERATIONS_LIST_V2_0 = 'scenarios/operations_service/operations_list/v2.0.conf'

    @property
    def version(self) -> str:
        try:
            return "v%s" % re.findall(r'/v(\d+\.\d+)\.conf$', self.value)[0]
        except IndexError:
            raise IndexError(f'Unable to get version from scenario file "{self.value}"')

    @property
    def service(self) -> str:
        try:
            return self.split('/')[1]
        except IndexError:
            raise IndexError(f'Unable to get service from scenario file "{self.value}"')

    @property
    def scenario(self) -> str:
        try:
            return self.split('/')[2]
        except IndexError:
            raise IndexError(f'Unable to get scenario from scenario file "{self.value}"')

    @property
    def service_normalized(self) -> str:
        return self.service.replace('_', ' ')

    @property
    def scenario_normalized(self) -> str:
        return self.scenario.replace('_', ' ')
