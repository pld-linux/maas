Summary:	Multicast address allocation server
Summary(pl):	Serwer przydzia³u adresów multicastowych
Name:		maas
Version:	0.1
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	http://prdownloads.sourceforge.net/malloc/%{name}-%{version}.tar.gz
Source1:	http://deimos.campus.luth.se/malloc/documentation/%{name}_manual.pdf
Source2:	%{name}d.init
Source3:	%{name}d.sysconfig
URL:		http://deimos.campus.luth.se/malloc/
Prereq:		rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MAAS is multicast address allocation server using MADCAP and AAP
protocols.

%description -l pl
MAAS to serwer przydzia³u adresów multicastowych wyko¿ystuj±cy
protoko³y MADCAP i AAP.

%prep
%setup  -q

%build
%configure 
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/%{name},/etc/rc.d/init.d,/etc/sysconfig}

install src/maasd $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} .
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/maasd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/maasd

gzip -9nf AUTHORS src/*.conf

%pre
GROUP=maasd; GID=69; %groupadd
USER=maasd; UID=69; HOMEDIR=/dev/null; COMMENT="MAAS server"; %useradd

%post
NAME=maasd; DESC="MAAS daemon"; %chkconfig_add

%preun
NAME=maasd; %chkconfig_del

%postun
USER=maasd; %userdel
GROUP=maasd; %groupdel

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS* %{name}_manual.pdf src/*.conf*
%attr(755,root,root) %{_sbindir}/*
%{_sysconfdir}/%{name}
%attr(755,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/*
