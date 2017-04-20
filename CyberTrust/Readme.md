# Cyber Trust

This repo contains some of the tools and scripts for HPE VAN SDN Controllers and HPE Network Protectors REST API I used during the research period in the Cyber Trust research project, under the work package 3, "Security in New Network Technologies".


Read more about Cyber Trust:
[Cyber Trust @ JAMK](https://cybertrust.labranet.jamk.fi/ct/public)
[CybertTrust.fi](http://cybertrust.fi)

> Please note, that these applications are far from finished, they are developed only enough to provide the functionality needed for the assignment. Therefore it might and probably will break at some point. No more development efforts are put to these applications.

## random_dns_lookup

This Bash script was run inside multiple [mininet](http://http://mininet.org) hosts to generate random DNS queries, using both malicious and clean URLs, during the first phase of blocking and logging malicious traffic with HPE Network Protector.

## Protector_ACL_and_Blacklist

These Python scripts add URLs to ACL as well as FQDNs to the custom blacklists and generating policies based on the profiles using the REST API. It contains also scripts to test how many individual list and entries can be added.
