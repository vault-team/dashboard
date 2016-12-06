# Vault Dashboard on OpenStack Horizon
## Installation instruction
### 1.Change the host ip of urls in the following files to the current host ip.
* openstack_dashboard/dashboards/vault_admin/tenant_mppdb_group_status/templates/tenant_mppdb_group_status/index.html
* openstack_dashboard/dashboards/vault_admin/tenant_mppdb_status/templates/tenant_mppdb_status/index.html
* vault/constant.py

### 2.Copy files to corresponding directories.

openstack_dashboard/dashboards/*:  /usr/share/openstack-dashboard/openstack_dashboard/dashboards/

_50_vault.py:  /usr/share/openstack-dashboard/openstack_dashboard/enabled/_50_vault.py

_55_vault_admin.py:  /usr/share/openstack-dashboard/openstack_dashboard/enabled/_55_vault_admin.py

### 3. Restart Horizon.

`service apache2 restart`