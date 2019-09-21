# Netbox AWX inventory script
A simple inventory script to populate data from netbox to AWX inventory.  s script is tested with Netbox v2.6.2

## Grouping and Host vars
It groups hosts based on site, rack, platform, tenant, tag.
host vars are populated from hosts config_context.
