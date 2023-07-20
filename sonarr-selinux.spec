%global selinuxtype targeted
%global moduletype contrib
%global modulename sonarr

Name:           %{modulename}-selinux
Version:        1.0.0
Release:        1%{?dist}
Summary:        Sonarr SELinux policy
License:        GPLv3
URL:            https://github.com/negativo17/%{name}
BuildArch:      noarch

Source0:        %{modulename}.te
Source1:        %{modulename}.if
Source2:        %{modulename}.fc
Source3:        LICENSE

Requires:       selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-%{selinuxtype}
BuildRequires:  selinux-policy-devel
%{?selinux_requires}

%description
Sonarr SELinux policy.

%prep
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} .

%build
make -f %{_datadir}/selinux/devel/Makefile %{modulename}.pp
bzip2 -9 %{modulename}.pp

%install
install -D -m 0644 %{modulename}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2

%pre
%selinux_relabel_pre -s %{selinuxtype}

%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2
if %{_sbindir}/selinuxenabled ; then
    %{_sbindir}/semanage port -a -t %{modulename}_port_t -p tcp 8989
fi

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
fi
if %{_sbindir}/selinuxenabled ; then
    %{_sbindir}/semanage port -d -t %{modulename}_port_t -p tcp 8989
fi

%posttrans
%selinux_relabel_post -s %{selinuxtype}

%files
%license LICENSE
%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.*
%ghost %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}

%changelog
* Thu Jul 20 2023 Simone Caronni <negativo17@gmail.com> - 1.0.0-1
- First build.
