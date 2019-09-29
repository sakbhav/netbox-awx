# Netbox AWX inventory script
A simple inventory script to populate data from netbox to AWX inventory.  This script is tested with Netbox v2.6.2

## Grouping and Host vars
It groups hosts based on site, rack, platform, tenant, tag.
host vars are populated from hosts config_context.

## Filtering hosts
You might not want to import all devices from netbox to AWX inventory.  For such cases, a list of tags to filter the hosts may be added to FILTER_TAGS variable.  If FILTER_TAGS list is empty, all devices will be imported
