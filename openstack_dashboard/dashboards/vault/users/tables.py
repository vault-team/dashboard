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
from openstack_dashboard.dashboards.vault.users import utils


class UserFilterAction(tables.FilterAction):
    name = "userfilter"


class AddTableData(tables.LinkAction):
    name = "add"
    verbose_name = _("Add User")
    url = "horizon:vault:users:create"
    classes = ("btn-launch", "ajax-modal")


class DeleteTableData(tables.DeleteAction):
    data_type_singular = _("User")
    data_type_plural = _("Users")

    def delete(self, request, obj_id):
        utils.deleteUser(self, request, obj_id)


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, post_id):
        pass


class UsersTable(tables.DataTable):
    user_id = tables.Column("id", verbose_name=_("ID"))
    user_name = tables.Column("user_name", verbose_name=_("Name"))
    tenant_mppdb_name = tables.Column("tenant_mppdb_name", verbose_name=_("Tenant Name"))

    class Meta:
        name = "vault"
        verbose_name = _("Users")
        row_class = UpdateRow
        table_actions = (AddTableData, UserFilterAction)
        row_actions = (DeleteTableData,)
