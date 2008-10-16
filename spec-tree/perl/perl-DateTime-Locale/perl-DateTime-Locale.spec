%{!?perlgen:%define perlgen 5.8}

Summary: DateTime-Locale Perl module
Name: perl-DateTime-Locale
Version: 0.09
Release: 9%{?dist}
Packager: Mike McCune
License: GPL or Artistic
Group: Development/Libraries
URL: http://search.cpan.org/dist/DateTime-Locale/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
BuildRequires: perl-Module-Build
%if "%{perlgen}" == "5.8"
BuildRequires: perl >= 2:5.8.0
%else
BuildRequires: perl >= 1:5.6.0
%endif

Requires: %(perl -MConfig -le 'if (defined $Config{useithreads}) { print "perl(:WITH_ITHREADS)" } else { print "perl(:WITHOUT_ITHREADS)" }')
Requires: %(perl -MConfig -le 'if (defined $Config{usethreads}) { print "perl(:WITH_THREADS)" } else { print "perl(:WITHOUT_THREADS)" }')
Requires: %(perl -MConfig -le 'if (defined $Config{uselargefiles}) { print "perl(:WITH_LARGEFILES)" } else { print "perl(:WITHOUT_LARGEFILES)" }')
Source0: DateTime-Locale-0.09.tar.gz

%description
%{summary}.

%prep
%setup -q -n DateTime-Locale-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL destdir=$RPM_BUILD_ROOT  < /dev/null
make OPTIMIZE="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

eval `perl '-V:installarchlib'`
mkdir -p $RPM_BUILD_ROOT$installarchlib
%makeinstall

find $RPM_BUILD_ROOT -type f -a \( -name perllocal.pod -o -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

[ -x /usr/lib/rpm/brp-compress ] && /usr/lib/rpm/brp-compress

find $RPM_BUILD_ROOT -type f \
| sed "s@^$RPM_BUILD_ROOT@@g" \
> %{name}-%{version}-%{release}-filelist

eval `perl -V:archname -V:installsitelib -V:installvendorlib -V:installprivlib`
for d in $installsitelib $installvendorlib $installprivlib; do
  [ -z "$d" -o "$d" = "UNKNOWN" -o ! -d "$RPM_BUILD_ROOT$d" ] && continue
  find $RPM_BUILD_ROOT$d/* -type d \
  | grep -v "/$archname\(/auto\)\?$" \
  | sed "s@^$RPM_BUILD_ROOT@%dir @g" \
  >> %{name}-%{version}-%{release}-filelist
done

if [ "$(cat %{name}-%{version}-%{release}-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit 1
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root,-)
%doc Changes LICENSE README

%changelog
* Thu Oct 16 2008 Milan Zazrivec 0.09-9
- bumped release for minor release tagging

* Wed Aug 27 2008 Mike McCune 0.09-8
- Cleanup spec file to work in fedora and our new Makefile structure
* Wed Sep 01 2004 Chip Turner <cturner@redhat.com> - 0.09-1
- Specfile autogenerated.

