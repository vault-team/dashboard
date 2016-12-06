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

import logging

from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from horizon import tables
from horizon.tables.base import Cell, Row


class CustomCell(Cell):

    def render(self):

        # control progress bar width
        self.progress_bar_width = 100 if self.value > 100 else self.value
        return render_to_string(
            "vault_admin/tenant_mppdb_groups/_data_table_cell.html",
            {"cell": self})

class CustomRow(Row):
    def render(self):
        return render_to_string(
            "vault_admin/tenant_mppdb_groups/_data_table_row.html",
            {"row": self})


class TenantMppdbGroupFilterAction(tables.FilterAction):
    name = "tenantmppdbgroupfilter"


class TenantMppdbGroupsTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("# Group"))
    node_quantity = tables.Column("node_quantity", verbose_name=_("Nodes Quantity"))
    sla_ok = tables.Column("sla_ok", verbose_name=_("SLA"))
    consolidation_effectiveness = tables.Column("consolidation_effectiveness", verbose_name=_("Consolidation Effectiveness"))
    tenant_members = tables.Column("tenant_mppdb_members", verbose_name=_("Composition"))

    class Meta:
        name = "vault_admin"
        verbose_name = ("TenantMppdbGroup",)
        table_actions = (TenantMppdbGroupFilterAction,)
        cell_class = CustomCell
        row_class = CustomRow