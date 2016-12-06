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

from django.utils.translation import ugettext_lazy as _
from horizon import tables


class TenantMppdbsFilterAction(tables.FilterAction):
    name = "tenantmppdbsfilter"


class TenantMppdbsTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"))
    tenant_mppdb_name = tables.Column("tenant_mppdb_name", verbose_name=_("Name"))
    request_node_quantity = tables.Column("request_node_quantity", verbose_name=_("Node Quantity"))
    tenant_mppdb_group_id = tables.Column("tenant_mppdb_group_id", verbose_name=_("Tenant Group ID"))

    class Meta:
        name = "vault_admin"
        verbose_name = _("TenantMppdb")
        table_actions = (TenantMppdbsFilterAction,)
