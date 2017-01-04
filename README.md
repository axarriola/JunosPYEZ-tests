# JunosPYEZ-tests
Scripts to test Junos eznc library functionality

#Libraries needed
You will need to download and install Junos eznc library, it will only take you a few minutes. Just follow the instructions in https://github.com/Juniper/py-junos-eznc

#MPLS-check
This script obtains MPLS LSPs and correspondent RSVP sessions information from a device, you may specify an LSP regex as input to show a subset of the LSPs or it will show all of them. For every LSP it will show its paths information and also the RSVP session information. Why did I need this? Well, when you want to check the LSP path ERO and also it's FRR ERO, you normally have to run a couple of commands for each LSP with extensive output. This script allows you to enter a regex and get all this information in seconds in an ordered smaller output.

#Route-check
The purpose of this was to implement it in a private web looking glass for the ISP I work, there was another version with GUI that I unfortunately can't share. The script gets the route information for the prefix input as seen in a cli, but it also obtains and displays the interface status/description and LSP status (if it is using any).

