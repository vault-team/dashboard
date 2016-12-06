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

from django.shortcuts import render

from openstack_dashboard.dashboards.vault.conf import VAULT_PROJECT_ID, VAULT_ROLE_ID
from utils import OpenstackUtil
from django.http import JsonResponse

def register_openstack_user(request):

    if request.method == 'POST':
        newUser = OpenstackUtil.get_keystone_client().users.create(name=request.POST.get('tenant_name'),
                                                                   password=request.POST.get('tenant_password'),
                                                                   tenant_id=VAULT_PROJECT_ID)

        OpenstackUtil.get_keystone_client().roles.add_user_role(newUser.id, VAULT_ROLE_ID, VAULT_PROJECT_ID)

        return JsonResponse({"status":"OK"})

    else:
        return render(request, 'vault/register.html')


