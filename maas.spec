# TODO: standardize %pre (grep on group/passwd files is wrong!)
Summary:	Multicast address allocation server
Summary(pl):	Serwer przydzia³u adresów multicastowych
Name:		maas
Version:	0.1
Release:	3
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/malloc/%{name}-%{version}.tar.gz
Source1:	http://deimos.campus.luth.se/malloc/documentation/%{name}_manual.pdf
Source2:	%{name}d.init
Source3:	%{name}d.sysconfig
URL:		http://deimos.campus.luth.se/malloc/
BuildRequires:	autoconf
PreReq:		rc-scripts
Requires(pre): /usr/sbin/groupadd
Requires(pre): /usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MAAS is multicast address allocation server using MADCAP and AAP
protocols.

%description -l pl
MAAS to serwer przydzia³u adresów multicastowych wykorzystuj±cy
protoko³y MADCAP i AAP.

%prep
%setup  -q

%build
%{__autoconf}
%configure 
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/%{name},/etc/rc.d/init.d,/etc/sysconfig}

install src/maasd $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} .
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/maasd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/maasd

%clean
rm -rf $RPM_BUILD_ROOT

%pre
grep -q maasd %{_sysconfdir}/group || (
       /usr/sbin/groupadd -g 69 -r -f maasd 1>&2 || :
)
grep -q maasd %{_sysconfdir}/passwd || (
       /usr/sbin/useradd -M -o -r -u 69 \
        -g maasd -c "MAAS server" -d /dev/null maasd 1>&2 || :
)

%post
/sbin/chkconfig --add maasd
if [ -r /var/lock/subsys/maasd ]; then
       /etc/rc.d/init.d/maasd restart >&2
else
       echo "Run \"/etc/rc.d/init.d/maasd start\" to start MAAS daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/maasd ]; then
		/etc/rc.d/init.d/maasd stop >&2
	fi
	/sbin/chkconfig --del maasd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS %{name}_manual.pdf src/*.conf
%attr(755,root,root) %{_sbindir}/*
%{_sysconfdir}/%{name}
%attr(755,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/*
