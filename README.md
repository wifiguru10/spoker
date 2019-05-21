# spoker
Spoker is a script that'll help configure Meraki Auto-VPN Spokes. The script will take a input of HUBS and will map appropriate HUB priorities based on network TAGS. So you can adjust spoke load-balancing across geographically tagged networks. This is also a good way to add or remove hubs from existing networks and/or change priority to load-balance.

# How to run
1. TAG all the networks in dashboard with "api_spoker" or customer tag (configurable in header of script)
2. Ensure the MX's site-to-site ruleset is configured in spoke mode (will bypass other modes)
3. Configure header of script with org-id, API-key, HUBs and tags.
4. Run script for it to fetch, query and configure all spoke networks.
5. when your done, remove the "api_spoker" tag from the networks.

# Use-Cases
1. You have alot of spokes deployed, and you add a new hub or add an additional one
    -note: you'll just need a single tag for all your locations
2. You want to load balance spokes geographically across multiple HUBS based on tags
    -assign priority orders(123,321,213) to the TAGs (east,west,central,asia, etc)
3. You want to migrate from FULL tunnel to Split or vice-versa


# Gotchas
1. Will not convert a network to a spoke network, the network must be in spoke mode with at least one network in VPN
2. Script is a little slow, will be adding action-batches soon
