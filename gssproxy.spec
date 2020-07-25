%global servicename gssproxy
%global pubconfpath %{_sysconfdir}/gssproxy
%global gpstatedir %{_localstatedir}/lib/gssproxy

Name:		gssproxy
Version:	0.8.3
Release:	1
Summary:	GSSAPI Proxy
License:	MIT
URL:		https://github.com/gssapi/gssproxy
Source0:	https://github.com/gssapi/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz


Requires: krb5 keyutils libverto-module-base libini_config
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Conflicts: selinux-policy < 3.13.1-283.5

BuildRequires: autoconf automake libtool m4 libxslt libxml2 docbook-style-xsl doxygen findutils systemd-units git popt-devel
BuildRequires: gettext-devel pkgconfig krb5-devel >= 1.12.0 libselinux-devel keyutils-libs-devel libini_config-devel >= 1.2.0 libverto-devel

%description
This is a proxy for GSSAPI which deals with credential handling

%package        help
Summary:        Help files for %{name}
%description    help
Help files for %{name}.

%prep
%autosetup -n  %{name}-%{version} -p1

%build
autoreconf -f -i
%configure \
    --with-pubconf-path=%{pubconfpath} \
    --with-initscript=systemd \
    --disable-static \
    --disable-rpath \
    --with-gpp-default-behavior=REMOTE_FIRST

make %{?_smp_mflags} all
make test_proxymech

%install
rm -rf %{buildroot}
%make_install
rm -f %{buildroot}%{_libdir}/gssproxy/proxymech.la
install -d -m755 %{buildroot}%{_sysconfdir}/gssproxy
install -m644 examples/gssproxy.conf %{buildroot}%{_sysconfdir}/gssproxy/gssproxy.conf
install -m644 examples/99-nfs-client.conf %{buildroot}%{_sysconfdir}/gssproxy/99-nfs-client.conf
install -D -m644 examples/mech %{buildroot}%{_sysconfdir}/gss/mech.d/gssproxy.conf
install -m644 examples/24-nfs-server.conf %{buildroot}%{_sysconfdir}/gssproxy/24-nfs-server.conf
mkdir -p %{buildroot}%{gpstatedir}/rcache

%post
%systemd_post gssproxy.service

%preun
%systemd_preun gssproxy.service

%postun
%systemd_postun_with_restart gssproxy.service

%files
%license COPYING
%{_unitdir}/gssproxy.service
%{_sbindir}/gssproxy
%attr(755,root,root) %dir %{pubconfpath}
%attr(755,root,root) %dir %{gpstatedir}
%attr(700,root,root) %dir %{gpstatedir}/clients
%attr(700,root,root) %dir %{gpstatedir}/rcache
%attr(0600,root,root) %config(noreplace) /%{_sysconfdir}/gssproxy/gssproxy.conf
%attr(0600,root,root) %config(noreplace) /%{_sysconfdir}/gssproxy/99-nfs-client.conf
%attr(0644,root,root) %config(noreplace) /%{_sysconfdir}/gss/mech.d/gssproxy.conf
%attr(0600,root,root) %config(noreplace) /%{_sysconfdir}/gssproxy/24-nfs-server.conf
%dir %{_libdir}/gssproxy
%{_libdir}/gssproxy/proxymech.so

%files help
%{_mandir}/man5/gssproxy.conf.5*
%{_mandir}/man8/gssproxy.8*
%{_mandir}/man8/gssproxy-mech.8*

%changelog
* Sat Jul 25 2020 zhangxingliang <zhangxingliang3@huawei.com> - 0.8.3-1
- Type:update
- ID:NA
- SUG:NA
- DESC:update to 0.8.3

* Fri Mar 27 2020 steven <steven_ygui@163.com> - 0.8.0-12
- Unlock cond_mutex before pthread exit in gp_worker_main()

* Sun Jan 12 2020 openEuler Buildteam <buildteam@openeuler.org> - 0.8.0-11
- revise the bogus date in changelog and instll the 24-nfs-server.conf file

* Sat Jan 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 0.8.0-10
- add the 24-nfs-server.conf file for nfs-server

* Fri Dec 20 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.8.0-9
- Modify requires

* Thu Sep 27 2018 openEuler Buildteam <buildteam@openeuler.org> 0.8.0-8
- Package init

* Mon Sep 10 2018 openEuler Buildteam <buildteam@openeuler.org> 0.8.0-7
- Package init
