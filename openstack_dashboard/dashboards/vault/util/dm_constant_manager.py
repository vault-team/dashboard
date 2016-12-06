# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests

import openstack_dashboard.dashboards.vault.conf


class replication_factor_manager():

    replication_factor_singleton = None
    replication_factor = None

    @staticmethod
    def get_replication_factor():
        if replication_factor_manager.replication_factor_singleton == None:
            replication_factor_manager.replication_factor_singleton = replication_factor_manager()
            replication_factor_manager.replication_factor_singleton.replication_factor = requests.get(
                openstack_dashboard.dashboards.vault.conf.VAULT_DM_REST_URL + '/v1.0/replication_factor').json()
            return replication_factor_manager.replication_factor_singleton.replication_factor
        else:
            return replication_factor_manager.replication_factor_singleton.replication_factor


class service_level_agreement_manager():

    service_level_agreement_singleton = None
    service_level_agreement = None

    @staticmethod
    def get_service_level_agreement():
        if service_level_agreement_manager.service_level_agreement_singleton == None:
            service_level_agreement_manager.service_level_agreement_singleton = service_level_agreement_manager()
            service_level_agreement_manager.service_level_agreement_singleton.service_level_agreement = requests.get(
                openstack_dashboard.dashboards.vault.conf.VAULT_DM_REST_URL + '/v1.0/service_level_agreement').json()
            return service_level_agreement_manager.service_level_agreement_singleton.service_level_agreement
        else:
            return service_level_agreement_manager.service_level_agreement_singleton.service_level_agreement

class queryrouter_uri_manager():

    queryrouter_uri_singleton = None
    queryrouter_uri = None

    @staticmethod
    def get_queryrouter_uri():
        if queryrouter_uri_manager.queryrouter_uri_singleton == None:
            queryrouter_uri_manager.queryrouter_uri_singleton = queryrouter_uri_manager()
            queryrouter_uri_manager.queryrouter_uri_singleton.queryrouter_uri = requests.get(
                openstack_dashboard.dashboards.vault.conf.VAULT_DM_REST_URL + '/v1.0/queryrouter_uri').json()
            return queryrouter_uri_manager.queryrouter_uri_singleton.queryrouter_uri
        else:
            return queryrouter_uri_manager.queryrouter_uri_singleton.queryrouter_uri
