# spoker
Spoker is a script that'll help configure Meraki Auto-VPN Spokes. The script will take a input of HUBS and will map appropriate HUB priorities based on network TAGS. So you can adjust spoke load-balancing across geographically tagged networks. This is also a good way to add or remove hubs from existing networks and/or change priority to load-balance.


1. TAG all the networks in dashboard with "api_spoker" or customer tag (configurable in header of script)
2. Ensure the MX's site-to-site ruleset is configured in spoke mode (will bypass other modes)
3. Configure header of script with org-id, API-key, HUBs and tags.
4. Run script for it to fetch, query and configure all spoke networks.
5. when your done, remove the "api_spoker" tag from the networks.
