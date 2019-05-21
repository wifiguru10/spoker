#!/usr/bin/python3 -i

"""spoker.py: Spoker is a script that'll help configure Meraki Auto-VPN Spokes. The script will take a input of HUBS and will map appropriate HUB priorities based on network TAGS. So you can adjust spoke load-balancing across geographically tagged networks. This is also a good way to add or remove hubs from existing networks."""


from datetime import datetime
from convert_library import MS_inv, MS, port
import time
import re
import os
import sys
import getopt
from meraki.meraki import Meraki

#***********************************************
#*****ONLY MODIFY HERE**************************

orgid = "1234567890" #organization ID

x_cisco_meraki_api_key = "<INSERT YOUR API KEY HERE>" #make sure your org has API enabled 

API_RW_TAG = "api_spoker" #what TAG should be the Read/Write flag for this script?

HUBS = [ '<HUB1 NETID>', '<HUB2 NETID>', '<HUB3 NETID>'] #Configure these with your hub's networkID's.
SITE_TAGS = { 1 : 'western', 2 : 'central', 3 : 'eastern'} #tags to track
SITE_ORDER = { 1:'123', 2:'231', 3:'321' } # number of entries should match tags
FULL_TUNNEL = True # <True> or <False>


#***********************************************
#***********************************************

SCOPE={} #used for testing, keeps from having to recall API queries

api_client = Meraki(x_cisco_meraki_api_key)

collect = {}
collect['organization_id'] = orgid
networks = api_client.networks.get_organization_networks(collect)
#print(networks)

inventory = api_client.organizations.get_organization_inventory(orgid)
#print(inventory)

    

#returns list of networks that have the tag <tag_value>
#Only tagged networks with  <API_RW_TAG> will be returned
def getNetByTag(tag_value):
    nets = []
    for n in networks:
        tags=str(n['tags']).lower()
        if tag_value in tags:
            if API_RW_TAG in tags:
                nets.append(n)

    return nets

#returns s2s settings for network based on netId
def get_s2s_by_netID(netid):
    collect={}
    collect['networkId'] = netid
    result = api_client.networks.get_network_site_to_site_vpn(netid)
    return result

#returns list of hubs, based on NetworkIds in the HUBS[] 
def getHubs():
    t_inv = api_client.organizations.get_organization_inventory(orgid)
    result = []
    for t in t_inv:
        m = t['model']
        nid = t['networkId']
        if "MX" in m and nid in HUBS or "Z" in m and nid in HUBS:
            result.append(t)
    return result


#this function inserts the correct HUBs based on SITE_ORDER + HUBS
def insertS2S(s2s_in, scope_id, netid_target):
    collect={}
    collect['network_id'] = netid_target

    payload={'hubs': []}

    #next line makes sure it only configures a spoke
    if not s2s_in['mode'] == 'spoke':
        print("NOT A SPOKE!")
        return False

    print("")
    print("Updating Site:")
    order = SITE_ORDER[scope_id]
    for o in order:
        tmp={}
        tmp['hubId'] = HUBS[int(o)-1]
        tmp['useDefaultRoute'] = FULL_TUNNEL #based on boolean in header config
        payload['hubs'].append(tmp)
        print("#"+str(o)+" nid:"+ HUBS[int(o)-1])

    #need to insert old subnets and mode
    payload['mode'] = s2s_in['mode']
    payload['subnets'] = s2s_in['subnets']
    
    collect['update_network_site_to_site_vpn'] = payload


    print()
    print("Payload:")
    print(collect)

    result = api_client.networks.update_network_site_to_site_vpn(collect)
    print(result)
    return True

#this interates through the SCOPE targets with "scope_id" = <int>
def updateScope(scope_id):
    collect={'hubs': []}
    print("Updating SCOPE["+str(scope_id)+"]")
    print("TAG ID["+SITE_TAGS[scope_id]+"]")
    for s in SCOPE[scope_id]:
#       print(s['name'])        
        t_net = get_s2s_by_netID(s['id'])
#       print(t_net)
        if insertS2S(t_net,scope_id, s['id']):
            print("Success on "+s['id'])
    
    return True


def main(argv):
    print("")
    print("Cisco Meraki - spoker.py")
    print("")

    hubs = getHubs()
    

    #print(hubs)
    count = 0
    for h in hubs:
        print("HUB"+str(count)+" ["+str(hubs[count]['name']+"]"))
        count+=1

    print("")

    #This puts all the networks that are in SCOPE into SCOPE['tag']
    print("NETWORK COUNT BY TAG (TARGETED SCOPE)")
    for c in range(1,len(SITE_TAGS)+1):
        st=SITE_TAGS[c]
        nets = getNetByTag(st)
        print("["+st+"] Count["+str(len(nets))+"]")
        SCOPE[c] = nets

    print("")

    #by this line you should have SCOPE[X] maps to SITE_TAGS[X] where X = index
    
    #so time to make some changes...
    for i in range(1,len(SITE_TAGS)+1):
        updateScope(i)

    print("DONE")


#AAAAARRRRRGGGGHHHVVVV
if __name__ == '__main__':
    print("Starting")
    main(sys.argv[1:])




