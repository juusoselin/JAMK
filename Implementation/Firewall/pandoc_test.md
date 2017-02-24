> **Implementing Basic Firewall Functionality in SDN Environment**
>
> Juuso Selin
>
> Personal Assignment
>
> YTCP0200 Cyber Security Implementation in Practice
>
> Firewalls
>
> Technology, ICT
>
> Degree Programme in Cyber Security

**Contents**

[1 Introduction 3](#introduction)

[2 Theory 3](#theory)

[2.1 Software-defined Networking 3](#software-defined-networking)

[2.1.1 OpenFlow 5](#openflow)

[2.2 Firewall 7](#firewall)

[2.3 Previous research papers 8](#previous-research-papers)

[3 Research question and methods 8](#research-question-and-methods)

[4 Research 8](#research)

[4.1 Hardware 8](#hardware)

[4.2 Topology (Two LANs, Controller, Internet, Web-server, Workstations
/ laptops)
9](#topology-two-lans-controller-internet-web-server-workstations-laptops)

[4.3 Software 9](#software)

[4.4 Use cases 10](#use-cases)

[4.4.1 Block traffic and / or devices 10](#block-traffic-and-or-devices)

[4.4.2 Allow only certain ports, ips, zones
10](#allow-only-certain-ports-ips-zones)

[4.4.3 Block websites ie. Facebook by IP -&gt; blacklist
10](#block-websites-ie.-facebook-by-ip---blacklist)

[4.4.4 Give priority to certain traffic
11](#give-priority-to-certain-traffic)

[4.4.5 Keep track of internet usage 11](#keep-track-of-internet-usage)

[4.4.6 Create alerts 11](#create-alerts)

[4.4.7 DDoS? 11](#ddos)

[4.4.8 TOR 11](#tor)

[5 Results and conclusions 11](#results-and-conclusions)

[5.1 Future development 12](#future-development)

[References 13](#references)

[Appendices 14](#appendices)

**Figures**

[Figure 1. Most viewed films in Finland in 2014 5](#_Toc457907732)

[Figure 2. Instructions of half time students 9](#_Toc457907733)

**Tables**

[Table 1. Required match fields 4](#_Toc475176033)

Introduction
============

In this assignment, I’ll implement some basic firewall functionality
using software-defined networking procedures and research what kind of
challenges and issues needs to be tackled during the implementation.
I’ll start by introducing SDN technology and clarifying terms and
phrases involved. I’ll also cover briefly some basic theory behind
firewalls. At the end of the theory section, I’ll make an introductory
review of the previous research of the topic.

Using the knowledge base gathered in theory section, I’ll present the
research question or questions and a research method suitable for the
constructive research on hand. I’ll clarify principles and theory behind
the chosen research method and make a research plan including also goals
of the research as well as the analyzing process of the results.

Third part is the practical research where I’ll introduce the hardware
and software used in the research as well as the multiple test cases.
I’ll also compare the results to the theory section.

I’ll conclude the assignment with analysis of the results, conclusions
and possible ideas for further development.

Theory
======

Software-defined Networking
---------------------------

Software-defined networking or SDN is an architecture where control
plane of the network is separated from the forwarding plane, hence one
controller can control several devices. Since the network control plane
becomes programmable, the underlying infrastructure can be abstracted
for applications and network services and the main principle is
basically the same than in any other virtualization solution like
software, storage or data virtualization. . Once the virtualization
technology became common in data centers, the state of data center
operations changed. Servers could be instantiated with a mouse click and
could be moved without significantly disrupting the operation of the
server being moved. Virtualization allows servers and storage to be
manipulated quickly and efficiently, but these advances in
virtualization has not been true in the networking domain. Even when the
tasks of creating, moving and removing networks are similar to those
same kinds of tasks performed for servers and storage. SDN holds the
promise that the time required for such network reconfiguration will be
reduced to the matter of minutes, such as is already the case for
reconfiguration of virtual machines. At the end, the aim of SDN is to
provide a dynamic and manageable network environment which is both
cost-effective and adaptable.

![](media/image3.png){width="5.536000656167979in"
height="5.1363156167979005in"}

Figure 1. SDN architecture

The SDN architecture is built from three layers as shown in Figure 1.
The infrastructure layer or data plane contains network elements such as
switches and routers. Since the data plane consists of various ports
that are used to receive and transmit packets, majority of packets
handled by a switch are only touched by the data plane. The Control
Plane in other hand is involved in multiple activities, although its
main role is to provide relevant information and instructions to the
forwarding plane so that data plane can handle traffic as much as
possible independently. Thus, the controller is responsible for
programming all the packet-matching and forwarding rules in the switch.
Controller also maintains a view of the entire network, utilizes path
computation, implements policy decisions, controls all the SDN devices
that comprise the network infrastructure and provides a northbound
interface for applications. The SDN Applications exists in the
Application Plane and communicate their network requirements and needs
toward the controller plane and get relevant information about the
network and resources from the controller via northbound interfaces.
Controller also translates applications requests and actions to the
network devices.

### OpenFlow

OpenFlow is a standards based protocol which allows a centralized
control plane in a separate device. Since the OpenFlow channel is the
interface that connects each OpenFlow switch to a controller and since
the controller configures and manages the switch, receives events from
the switch and sends packets out of the switch through this interface,
OpenFlow is the protocol of the southbound interface of SDN controller.
This protocol provides hardware abstraction where details of individual
ASICs (Application Specific Integrated Circuit) or individual networking
hardware are hidden from the controller using a standard API
(Application programming interface). The goal of SDN is interoperability
and openness and therefore OpenFlow provides the controller a method to
communicate with multiple vendor devices and multiple hardware types
(routers, switches, load balancers, and others) using a standard
interface. OpenFlow is currently developed and maintained by Open
Networking Foundation. Although Open Networking Foundation has already
released version 1.5 of OpenFlow Switch Specification, most of the
hardware and software using OpenFlow still utilizes version 1.3, so
that’s also the version focused on this research.

Flow tables are the fundamental data structures in an SDN device. These
flow tables allow the network device to evaluate incoming packets and
take the appropriate action based on the contents of the packet that has
just been received. Using the OpenFlow protocol, the controller can add,
update and delete flow entries in flow tables, both reactively (in
response to packets) and proactively (populating the flow tables ahead
of time for all traffic). Each flow table in the switch contains a set
of flow entries and each flow entry consists of match fields, counters,
and a set of instructions to apply to matching packets. When the first
matching entry is found, then the instructions associated with the
specific flow entry are executed. Actions are the instructions that the
network device should perform if an incoming packet matches the match
fields specified for that flow entry. All the required match fields,
according to OpenFlow Switch Specification version 1.3, are presented in
Table 1. There are many other match fields available in the OpenFlow
specification, but these mandatory fields are required from a switch
supporting OpenFlow version 1.3. .

[[[]{#_Toc475176033 .anchor}]{#_Ref475173779 .anchor}]{#_Ref475173719
.anchor}Table 1. Required match fields

  -------------------- ----------------------------------------------------------------------
  **Field**            **Description**
  OXM\_OF\_IN\_PORT    Ingress port. This may be a physical or switch-defined logical port.
  OXM\_OF\_ETH\_DST    Ethernet source address. Can use arbitrary bitmask
  OXM\_OF\_ETH\_SRC    Ethernet destination address. Can use arbitrary bitmask
  OXM\_OF\_ETH\_TYPE   Ethernet type of the OpenFlow packet payload, after VLAN tags.
  OXM\_OF\_IP\_PROTO   IPv4 or IPv6 protocol number
  OXM\_OF\_IPV4\_SRC   IPv4 source address. Can use subnet mask or arbitrary bitmask
  OXM\_OF\_IPV4\_DST   IPv4 destination address. Can use subnet mask or arbitrary bitmask
  OXM\_OF\_IPV6\_SRC   IPv6 source address. Can use subnet mask or arbitrary bitmask
  OXM\_OF\_IPV6\_DST   IPv6 destination address. Can use subnet mask or arbitrary bitmask
  OXM\_OF\_TCP\_SRC    TCP source port
  OXM\_OF\_TCP\_DST    TCP destination port
  OXM\_OF\_UDP\_SRC    UDP source port
  OXM\_OF\_UDP\_DST    UDP destination port
  -------------------- ----------------------------------------------------------------------

There are two mandatory Instructions in OpenFlow version 1.3:
Write-Actions tells which actions are executed when match is found and
Goto-Table, which indicates the next table in the processing pipeline.
Required Actions include Output, Drop and Group. Output defines a
specified port where packet is forwarded. This can be physical, logical
or reserved port such as ALL, CONTROLLER or ANY. Drop-action just drops
the packet, while Group-action processes packet through a specific
group. Like match fields, there are considerably more optional
instructions and actions switch may support.

OpenFlow-compliant switches come in two types: OpenFlow-only and
OpenFlow-hybrid. OpenFlow-only switches support only OpenFlow operation.
In these switches, all packets are processed by the OpenFlow pipeline
and cannot be processed otherwise. OpenFlow-hybrid switches support both
OpenFlow operation and normal Ethernet switching operation— that is,
traditional L2 Ethernet switching, VLAN isolation, L3 routing (IPv4
routing and IPv6 routing), access control list (ACL), and quality of
service (QoS) processing.

Firewall
--------

A firewall is a device, software or a combination of the two, running on
a device that inspects network traffic and allows or blocks traffic in
two or more networks based on a set of rules . A **network-based
firewall** inspects traffic as it flows between networks and are
typically dedicated hardware devices, while **host-based firewall**
inspects traffic received by a host and are usually software based
applications. Firewalls use filtering rules to identify allowed and
blocked traffic. Firewalls can manage this traffic based on source or
destination IP address, port number, the direction of the traffic
(inbound or outbound), service protocol, application or service type,
user account, and even traffic content.

A **packet filtering firewall** makes decisions about which network
traffic to allow by examining information in the IP packet header. Since
this type of firewall uses Access Control Lists (ACLs) or filter rules
to control traffic and it operates at OSI layer 3 (Network layer), it
can be implemented using features that are included in most routers. As
a result, packet filtering firewall offers high performance because it
only examines addressing information in the packet header, but is also
subject to DoS and buffer overflow attacks. A packet filtering firewall
is considered a **stateless** **firewall** because it examines each
packet and uses rules to accept or reject each packet without
considering whether the packet is part of a valid and active session.

The **stateful** **firewall** makes decisions about which traffic to
allow based on virtual circuits or sessions. The firewall is considered
stateful because it keeps track of the state of a session in a session
table. The stateful firewall operates up to OSI Layer 5 (Session layer)
and verifies that packets are properly sequenced.

An **application layer firewall** or **deep packet inspection firewall**
makes security decisions based on information contained within the data
portion of a packet. Application layer firewall operates up to OSI Layer
7 (Application layer) and stops each packet and inspects it and can
therefore filter based on user, group, and data such as URLs within an
HTTP request.

Previous research papers
------------------------

Research question and methods
=============================

Based on the theory of SDN and firewalls, this applied research will
focus on implementing a basic, stateless network firewall using only
tools provided in OpenFlow version 1.3. This research is conducted and
the primary data is collected by building a testbed for various use
cases, testing the configuration and setup against those test cases and
analyzing the results. Thus, the research question is what can be done
and what not with a OpenFlow protocol in a context of a firewall
application in SDN environment.

Applied research is a study that is designed to apply its research
findings to solve an existing problem and is therefore more pragmatic
and practical than pure or basic research, which tends to focus more on
the fundamental principles and testing of hypothesis for the development
of new or revised theories. . Constructive research is widely used
research method in computer science. It demands a form of validation
that doesn’t need to be quite as empirically based as in other type of
research. . Constructive research is often used to define and solve
problems, as well as improve an existing system or performance, with the
overall implication of adding to the existing body of knowledge. It can
be phenomenon or theory driven or combination of the two. The objective
is to identify and solve real practical problems. It both relies on
different research tools and is also associated with interpretive
epistemology, positivist epistemology and empiricism.

research plan including also goals of the research as well as the
analyzing process of the results

Kvantitatiivinen

Research
========

Hardware 
---------

The Openflow switch used in this research is a network development board
called Zodiac FX, manufactured by Australian company Northbound
Networks. Zodiac FX started as a Kickstarter project aiming to provide
affordable hardware switch for SDN prototyping. It has four 10/100 Fast
Ethernet ports; three of them are OpenFlow enabled while one is used for
traffic between controller and the switch. Zodiac FX supports OpenFlow
versions 1.0 and 1.3.

Configuration

Kuva Zodiacista!

Raspberry Pi is a small, yet high-performance computer in a single
board. Running Linux operating system, it will be used as a basic web
server in this research.

Laptops running vlans

Topology (Two LANs, Controller, Internet, Web-server, Workstations / laptops)
-----------------------------------------------------------------------------

Software 
---------

The SDN controller used in this research is a commercial controller by
Hewlett Packard Enterprise and is called HPE VAN SDN Controller; VAN is
an acronym from Virtual Application Networks. HPE provides free and
fully functional trial version of the controller. HPE has also created a
SDN ecosystem around their controller application and has a marketplace
called SDN App Store for distributing third-party SDN applications
running on top of HPE VAN SDN Controller. HPE VAN SDN Controller
supports OpenFlow versions 1.0 and 1.3.

Controller comes with several internal core module applications
preinstalled to perform tasks like link and node discovery, topology
management as well as path diagnostics. Furthermore, HPE provides two
methods for SDN applications to communicate with the controller; one can
use either custom Java programs or general-purpose RESTful control
interfaces.

External applications, such as firewall application created and used in
this research, are not installed on the controller, but can rather be
deployed on a platform of a choice outside of the controller platform
and are the northbound interface, which in this case is RESTful API, to
communicate with the controller.

Representational state transfer (REST) or RESTful is an architecture
style for stateless communications between web services and provides a
programmatic access to read and write web services or applications data.
It typically runs over HTTP. HPE VAN SDN Controller comes with an
interactive REST API Reference called RSDoc.

The firewall application used in this research is written in Python and
uses REST API to communicate with the controller. Moreover, a Python
library called HP SDN Client by a HP employee Dave Tucker, is used to
ease the REST API interaction with the controller.

Other software used in this research includes mininet, which is a
network emulator for creating realistic virtual networks for rapid and
interactive prototyping and development, virtualization software like
VMware Workstation and VirtualBox by Oracle as well as common
development tools for Python.

Use cases
---------

### Block traffic and / or devices

If one of the workstations has been infected with malware, it should be
possible to block all the traffic from the workstation in question,
since it’s generally preferable to block malicious traffic at the edge
of the network, where the users connect.

### Allow only certain ports, ips, zones 

Administrator needs access to the web server from his / her laptop using
SSH. This means that the firewall should allow traffic from \_\_ip\_\_
to \_\_ip\_\_ with TCP destination and source ports of 22. Workstations
as well as user from internet should be able to access the web server
using HTTP, so the TCP destination port 80 to the ip address of the
webserver should be open.

### Block websites ie. Facebook by IP -&gt; blacklist

In computer networking vernacular, a blacklist is a list of hostnames or
IP addresses that are known or suspected to be malicious or undesirable
in some other way.

In this use case, ip addresses of facebook.com, twitter.com and
Instagram.com are blocked, so no user should be able to access those web
services.

### Give priority to certain traffic

### Keep track of internet usage

While not firewall functionality per se, this use case describes how to
collect information about bandwidth usage. Since OpenFlow has counters
like bytes counter, it is relatively easy to monitor bandwidth usage.
With other tools, it would also be easy to track users internet usage
and store information about users, visited pages and time of day.

### Create alerts

### DDoS?

### TOR

Logging!

Results and conclusions
=======================

what can be done and what not

It’s important to note that currently the OpenFlow match fields are
limited to the packet header. Therefore, simple firewall functionality
can be implemented using OpenFlow fields such as destination IP address
or TCP/UDP port. But more sophisticated SDN firewall applications may
need to examine and act on fields that are not yet available or at least
not supported by the common hardware. Advanced firewalls in SDN
environment are usually using methods other than pure OpenFlow to
achieve the required functionality. Since the OpenFlow device examines
every packet independently and has no prior knowledge about the packets
received earlier, a stateful firewall or deep packet inspection are not
supported by the OpenFlow standard. Nonetheless, such stateful flow
awareness and application layer flow definitions may be possible in the
future version of OpenFlow using something like Experimenter modes.
Statefulness and other more advanced functions required by IPS/IDS
solutions can be accomplished using methods other than OpenFlow, such as
implementing these functions using tools available in i.e. Python, Java
or P4. On the other hand, deep packet inspection becomes more or less
obsolete if one can only allow verified traffic to the network at the
edge of the network.

ONF Security docs

Future development
------------------

Performance tests. Stateful firewall using Python (reference).

References

- - http://www.gartner.com/it-glossary/firewall

Default action is to drop if no flows are assigned.

[[[[]{#_Toc430768000 .anchor}]{#_Toc430675200 .anchor}]{#_Toc428799800
.anchor}]{#_Toc428542261 .anchor}

References {#references .LhteetOtsikko1}
==========

Add the references used in your thesis in alphabetical order here, all
in one list. Use markings in accordance with the reporting instructions.

Alasuutari, P. 1999. *Laadullinen tutkimus* *\[Qualitative research\]*.
3rd ed. Tampere: Vastapaino.

Hakala, J. T. 2004*. Opinnäyteopas ammattikorkeakouluille \[Thesis guide
for universities of applied sciences\]*. Helsinki: Gaudeamus.

Hendriks, R. 2013. *Perceptions of facility management in Europe: A
survey of Finland, Germany and the UK* (Bachelor’s thesis). JAMK
University of Applied Sciences, School of Business and Services
Management, Degree Programme in Facility Management.

Hirsjärvi, S., Remes, P., & Sajavaara, P. 2009. *Tutki ja kirjoita
\[Research and write\]*. 15th ed. Helsinki: Tammi.

X

Appendices {#appendices .LiitteetOtsikko1}
==========

1.  [[]{#_Toc430768002 .anchor}]{#_Toc430675202
    .anchor}Ammattikorkeakoulutuksen aloittaneiden läp
