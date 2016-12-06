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

from openstack_dashboard.dashboards.vault.util.dm_constant_manager import replication_factor_manager, \
    service_level_agreement_manager, queryrouter_uri_manager


REPLICATION_FACTOR = replication_factor_manager.get_replication_factor()
SLA_THRESHOLD = service_level_agreement_manager.get_service_level_agreement()
QUERY_ROUTER_URI = queryrouter_uri_manager.get_queryrouter_uri()


