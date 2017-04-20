# Cyber Trust

This repo contains some of the tools and scripts I wrote and used during the research period in the Cyber Trust research project. Since our work package was called "Security in New Network Technologies", this research focused on software-defined-networks (SDN), hence these tools are mostly created for HPEs commercial SDN products.


Read more about Cyber Trust:

- [Cyber Trust @ JAMK](https://cybertrust.labranet.jamk.fi/ct/public)
- [CybertTrust.fi](http://cybertrust.fi)


> Please note, that these applications are far from finished applications, they are developed only enough to provide the functionality needed for the task at hand. Therefore it might and probably will break at some point. No more development efforts are put to these applications.


## random_dns_lookup

This Bash script was run inside multiple [mininet](http://mininet.org) hosts to generate random DNS queries, both malicious and legit, during the first phase of blocking and logging malicious traffic with the HPE Network Protector.

## Protector_ACL_and_Blacklist

These Python scripts add URLs to ACL as well as FQDNs to the custom blacklists and generates also policy based on the profile using the REST API. It contains also scripts to test how many individual list and entries can be added.
