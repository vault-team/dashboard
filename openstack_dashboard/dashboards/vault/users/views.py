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

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions, tables, workflows, forms, tabs
from forms import CreateUserForm
from openstack_dashboard.dashboards.vault.users.tables import UsersTable
from openstack_dashboard.dashboards.vault.users import utils


class UserIndexView(tables.DataTableView):
    table_class = UsersTable
    template_name = 'vault/users/index.html'

    def get_data(self):
        return utils.getUsers(self)


class CreateView(forms.ModalFormView):
    template_name = 'vault/users/create.html'
    modal_header = _("Create User")
    form_id = "create_user_form"
    form_class = CreateUserForm
    submit_label = _("Create User")
    submit_url = reverse_lazy("horizon:vault:users:create")
    success_url = reverse_lazy("horizon:vault:users:index")
    page_title = _("Create User")
    success_message = _('Added user "%s".')
    failure_message = _('Unable to add user "%s".')
