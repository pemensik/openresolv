#
# spec file for package openresolv
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           openresolv
Version:        3.12.0
Release:        0
Summary:        DNS management framework
License:        BSD-2-Clause
URL:            https://roy.marples.name/projects/openresolv
Source:         https://roy.marples.name/downloads/openresolv/%{name}-%{version}.tar.xz
Requires:       bash
BuildArch:      noarch

%description
/etc/resolv.conf is a file that holds the configuration for the local resolution of domain names.
Normally this file is either static or maintained by a local daemon, normally a DHCP daemon.
openresolv will make sure, that multiple processes (eg. dhcpcd, NetworkManager, openvpn)
can write the resolv.conf without overwriting each others changes.

openresolv can generate a combined resolv.conf or a configuration file for a local nameserver
(like unbound, dnsmasq or bind) that will route the dns requests according to the search domain.

%prep
%autosetup
sed -i -e 's/^#!\/bin\/sh$//' named.in pdnsd.in dnsmasq.in unbound.in libc.in pdns_recursor.in

%build
# not GNU autoconf
./configure --bindir=%{_sbindir} --libexecdir=%{_libexecdir}/resolvconf
%make_build

%install
%make_install
mv %{buildroot}%{_sbindir}/resolvconf{,.%{name}}

%post
%{_sbindir}/update-alternatives --install %{_sbindir}/resolvconf \
  %{name} %{_sbindir}/resolvconf.%{name} 20

%postun
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_sbindir}/resolvconf.%{name}
fi

%files
%license LICENSE
%doc README.md
%config(noreplace) %{_sysconfdir}/resolvconf.conf
%dir %{_libexecdir}/resolvconf
%{_libexecdir}/resolvconf/*
%{_sbindir}/resolvconf.%{name}
%{_mandir}/man5/resolvconf.conf.5*
%{_mandir}/man8/resolvconf.8*

%changelog

