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

import traceback

from horizon import workflows, forms, exceptions
from django.utils.translation import ugettext_lazy as _

from openstack_dashboard.dashboards.vault.clusters import utils


class SetClusterDetailsAction(workflows.Action):
    tenant_mppdb_name = forms.CharField(
        label=_("Tenant Name"),
        required=True,
        max_length=80,
        help_text=_("Tenant Name"))

    node_quantity = forms.IntegerField(
        label=_("Node Quantity"),
        required=True,
        min_value=1,
        max_value=65535,
        help_text=_("Node Quantity"))

    flavor = forms.ChoiceField(
        label=_("Flavor"),
        help_text=_("Size of image to launch."),
        choices=[('m1.vertica', _('m1.vertica'))],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'}))

    class Meta:
        name = _("Details")

    def __init__(self, request, context, *args, **kwargs):
        self.request = request
        self.context = context
        super(SetClusterDetailsAction, self).__init__(
            request, context, *args, **kwargs)


class SetClusterDetails(workflows.Step):
    action_class = SetClusterDetailsAction
    contributes = ("tenant_mppdb_name", "node_quantity", "flavor")

    def contribute(self, data, context):
        if data:
            context['tenant_mppdb_name'] = data.get("tenant_mppdb_name", "")
            context['node_quantity'] = data.get("node_quantity", "")
            context['flavor'] = data.get("flavor", "")
        return context


class AddCluster(workflows.Workflow):
    slug = "add"
    name = _("Define Parallel Database setup")
    finalize_button_name = _("Submit")
    success_message = _('Added cluster "%s".')
    failure_message = _('Unable to add cluster "%s".')
    success_url = "horizon:vault:clusters:index"
    failure_url = "horizon:vault:clusters:index"
    default_steps = (SetClusterDetails,)

    def format_status_message(self, message):
        return message % self.context.get('node_quantity', 'unknown cluster')

    def handle(self, request, context):
        try:
            utils.addCluster(request, context)
            return True
        except Exception:
            print traceback.format_exc()
            exceptions.handle(request, _("Unable to add cluster"))
            return False
