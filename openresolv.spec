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

%global manext .gz

Name:           openresolv
Version:        3.12.0
Release:        1
Summary:        DNS management framework
License:        BSD
URL:            https://roy.marples.name/projects/openresolv
Source:         https://roy.marples.name/downloads/openresolv/%{name}-%{version}.tar.xz
Requires:       bash
BuildArch:      noarch
Provides:       resolvconf = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description
/etc/resolv.conf is a file that holds the configuration for the local resolution of domain names.
Normally this file is either static or maintained by a local daemon, normally a DHCP daemon.
openresolv will make sure, that multiple processes (eg. dhcpcd, NetworkManager, openvpn)
can write the resolv.conf without overwriting each others changes.

openresolv can generate a combined resolv.conf or a configuration file for a local nameserver
(like unbound, dnsmasq or bind) that will route the dns requests according to the search domain.

%prep
%autosetup
sed -i -e '1 s,^#!/bin/sh$,,' *.in

%build
# not GNU autoconf
./configure --bindir=%{_sbindir} --libexecdir=%{_libexecdir}/resolvconf
%make_build

%install
%make_install
mv %{buildroot}%{_sbindir}/resolvconf{,.%{name}}
mv %{buildroot}%{_mandir}/man8/resolvconf{,.%{name}}.8
touch %{buildroot}%{_sbindir}/resolvconf %{buildroot}%{_mandir}/man8/resolvconf.8%{?manext}

%post
%{_sbindir}/update-alternatives \
  --install %{_sbindir}/resolvconf resolvconf %{_sbindir}/resolvconf.%{name} 30 \
  --slave %{_mandir}/man8/resolvconf.8%{?manext} resolvconf.8%{?manext} %{_mandir}/man8/resolvconf.%{name}.8%{?manext}

%postun
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove resolvconf %{_sbindir}/resolvconf.%{name}
  %{_sbindir}/update-alternatives --remove-slave resolvconf %{_sbindir}/resolvconf.%{name} resolvconf.8%{?manext}
fi

%files
%license LICENSE
%doc README.md
%config(noreplace) %{_sysconfdir}/resolvconf.conf
%dir %{_libexecdir}/resolvconf
%{_libexecdir}/resolvconf/*
%{_sbindir}/resolvconf.%{name}
%{_mandir}/man5/resolvconf.conf.5*
%{_mandir}/man8/resolvconf.%{name}.8*

%changelog
* Mon Feb 01 2021 Petr Menšík <pemensik@redhat.com> - 3.12.0-1
- Initial build


