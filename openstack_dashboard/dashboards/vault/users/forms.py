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
import collections
import django
from django.core.exceptions import ValidationError
from horizon import workflows, forms, exceptions
from django.utils.translation import ugettext_lazy as _
from horizon.utils import validators
from openstack_dashboard.dashboards.vault.clusters.utils import get_clusters_by_tenant_id

from openstack_dashboard.dashboards.vault.users import utils


class PasswordMixin(forms.SelfHandlingForm):
    password = forms.RegexField(
        label=_("Password"),
        widget=forms.PasswordInput(render_value=False),
        regex=validators.password_validator(),
        error_messages={'invalid': validators.password_validator_msg()})
    confirm_password = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(render_value=False))
    no_autocomplete = True

    def clean(self):
        '''Check to make sure password fields match.'''
        data = super(forms.Form, self).clean()
        if 'password' in data:
            if data['password'] != data.get('confirm_password', None):
                raise ValidationError(_('Passwords do not match.'))
        return data


class CreateUserForm(PasswordMixin, forms.SelfHandlingForm):
    tenant_mppdb_id = forms.ChoiceField(
        label=_("Tenant Name"),
        required=True)

    user_name = forms.CharField(
        label=_("User Name"),
        required=True,
        max_length=80,
        help_text=_("User Name"))

    def create_tenant_list(self, tenant_id):
        clusters = get_clusters_by_tenant_id(tenant_id)
        self.fields['tenant_mppdb_id'].choices = [(cluster.id, cluster.tenant_mppdb_name) for cluster in clusters]

    def __init__(self, request, *args, **kwargs):
        super(CreateUserForm, self).__init__(request, *args, **kwargs)

        ordering = ["tenant_mppdb_id", "user_name", "password", "confirm_password"]
        # Starting from 1.7 Django uses OrderedDict for fields and keyOrder
        # no longer works for it
        if django.VERSION >= (1, 7):
            self.fields = collections.OrderedDict(
                (key, self.fields[key]) for key in ordering)
        else:
            self.fields.keyOrder = ordering

        # Construct MPPDB list
        self.create_tenant_list(request.user.id)

    def handle(self, request, context):
        try:
            new_user_name = context['user_name']
            new_password = context['password']
            tenant_id = request.user.id
            tenant_mppdb_id = context['tenant_mppdb_id']
            utils.add_user(new_user_name, new_password, tenant_id, tenant_mppdb_id)
            return True
        except Exception:
            logging.exception("Unable to add user")
            exceptions.handle(request, _("Unable to add user"))
            return False


