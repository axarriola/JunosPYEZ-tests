import yaml
import string
from jnpr.junos import Device
from jnpr.junos.factory.factory_loader import FactoryLoader

'''
  This scripts obtains important information for all the LSP's or the ones that match to a regex in a logical-system.
  The information presented contains LSP information and correspondent RSVP session information. For example,
  primary and secondary path ERO, FRR or node-link protection path information.
'''

# Device information
dev = Device(host="1.1.1.1", user="username", password="password", gather_facts=False)
dev.open()

# YAML 
yml = '''
---
mplsLSPs:
 rpc: get-mpls-lsp-information
 args_key: regex
 args: 
  extensive: True
  ingress: True
  count_active_routes: True
 item: rsvp-session-data/rsvp-session/mpls-lsp
 key: name
 view: mplsView

mplsView:
 fields:
  destination_address: destination-address
  lsp_state: lsp-state
  route_count: { route-count : int }
  active_path: active-path
  lsp_path: _lspPathTable

_lspPathTable:
  item: mpls-lsp-path
  key: name
  view: _lspPathView

_lspPathView:
  fields:
   path_name: name
   path_title: title
   path_active: { path-active : flag }
   path_state: path-state
   admin_groups: admin-groups/admin-group-name
   path_ero: explicit-route/address
   path_rro: received-rro

rsvpSessions:
 rpc: get-rsvp-session-information
 args_key: session-name
 args: 
  extensive: True
  ingress: True
 item: rsvp-session-data/rsvp-session
 key: 
  - name
  - lsp-path-type
 view: rsvpSessionView

rsvpSessionView:
 fields:
  lsp_path_type: lsp-path-type
  lsp_state: lsp-state
  lsp_id: lsp-id
  tunnel_id: tunnel-id
  is_nodeprotection: { is-nodeprotection : flag }
  bypass_name: bypass-name
  is_fastreroute: { is-fastreroute : flag }
  detour: _detourTable

_detourTable:
 item: detour
 view: _detourView

_detourView:
 fields:
  detour_state: lsp-state
  detour_ero: explicit-route/address
  detour_rro: record-route/address
'''

# Load Table and View definitions via YAML into namespace
globals().update(FactoryLoader().load(yaml.load(yml)))

# The code accepts and LSP regex as input or none.
regex = raw_input("LSP Regex: ")
#Obtain LSP and RSVP sessions information from device.
if(regex.isspace() or regex == ""):
    ml = mplsLSPs(dev).get(logical_system="LSYS-NAME")
    rs = rsvpSessions(dev).get(logical_system="LSYS-NAME")
else:
    ml = mplsLSPs(dev).get(regex, logical_system="LSYS-NAME")
    rs = rsvpSessions(dev).get(regex, logical_system="LSYS-NAME")

print("---------------------------------------------")
print("------------------MPLS LSP-------------------")
print("---------------------------------------------")
print "================================================"
# Iterate through the LSP list
for item in ml:
    print("Name: "+item.name + "    To: "+ item.destination_address + "    State: "+item.lsp_state)
    print("Route Count: " + str(item.route_count) + "        Active Path: " + item.active_path)
    print
    print("Paths: ")
    # Iterate through the path list of the LSP
    for path in item.lsp_path:
        print
        print "Path: "+path.path_name+" ("+path.path_title+")","*" if path.path_active else ""
        print("Include:" + string.translate(str(path.admin_groups),None,"'"))
        print
        print("ERO: " + string.translate(str(path.path_ero),None,"'"))
        print
        print(path.path_rro)
        print
    print "------------------RSVP------------------"
    rsvp_sessions = []
    # Iterate through the RSVP sessions to find correspondent information of the LSP
    for rskey in rs.keys():
        if rskey[0] == item.name:
            rsvp_sessions.append(rs[rskey])
    for rsvp_session in rsvp_sessions:
        print "Path: "+rsvp_session.lsp_path_type+"    State: "+rsvp_session.lsp_state
        print "LSP ID: "+rsvp_session.lsp_id+"      Tunnel ID: "+rsvp_session.tunnel_id  
        if(rsvp_session.is_nodeprotection):
            print "Using: " + rsvp_session.bypass_name
        if(rsvp_session.is_fastreroute):
            print "FRR:"
            for frdetour in rsvp_session.detour:
                print frdetour.detour_state
                print frdetour.detour_ero
                print frdetour.detour_rro
print("---------------------------------------------")

dev.close()
