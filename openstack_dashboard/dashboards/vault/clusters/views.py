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

from django.views import generic
from horizon import exceptions, tables, workflows, forms, tabs
from openstack_dashboard.dashboards.vault.clusters.tables import ClustersTable
from openstack_dashboard.dashboards.vault.clusters import utils
from openstack_dashboard.dashboards.vault.clusters.workflows.add_cluster import AddCluster


class ClusterIndexView(tables.DataTableView):
    table_class = ClustersTable
    template_name = 'vault/clusters/index.html'

    def get_data(self):
        tenant_name = self.request.user.username
        return utils.getClusters(tenant_name)


class AddClusterView(workflows.WorkflowView):
    workflow_class = AddCluster

    def get_initial(self):
        initial = super(AddClusterView, self).get_initial()
        return initial


class ClusterDetailView(generic.TemplateView):
    template_name = 'vault/clusters/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ClusterDetailView, self).get_context_data(**kwargs)
        cluster = self.get_data()
        context["cluster"] = cluster
        context["page_title"] = "Parallel database details: %s" % cluster.tenant_mppdb_name
        return context

    def get_data(self):
        id = self.kwargs['id']
        return utils.getCluster(id)

