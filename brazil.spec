%define gcj_support 1

Name:      brazil
Version:   2.3
Release:   %mkrel 2.3.3
Summary:   Extremely small footprint Java HTTP stack
Group:     Development/Java
License:   SPL
URL:       http://research.sun.com/brazil/

# source tarball and the script used to fetch it from Sun's Download Center
# script usage:
# $ sh get-brazil.sh
Source0:   %{name}-%{version}.tar.gz
Source1:   get-brazil.sh

# upsteam's build script doesn't build javadocs, so use our own, better script
Source2:   brazil-build.xml

# patch for removing sun proprietary signal handling api not in gcj
Patch0:    brazil-remove-proprietary-sun-api.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%else
BuildArch:        noarch
%endif
BuildRequires:    java-devel
BuildRequires:    jpackage-utils
BuildRequires:    java-rpmbuild
BuildRequires:    ant
Requires:         java
Requires:         jpackage-utils

%description
Brazil is as an extremely small footprint HTTP stack and flexible architecture 
for adding URL-based interfaces to arbitrary applications and devices from Sun 
Labs. This package contains the core set of classes that are not dependent on 
any other external Java libraries.

%package javadoc
Summary:   Javadocs for %{name}
Group:     Development/Java
Requires:  %{name} = %{version}-%{release}
Requires:  jpackage-utils

%description javadoc
API documentation for %{name}.

%package demo
Summary:   Demos for %{name}
Group:     Development/Java
Requires:  %{name} = %{version}-%{release}
Requires:  tcl

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q -n %{name}-%{version}

# apply patches
%patch0 -p0

# fix permissions and interpreter in sample scripts
grep -lR -e ^\#\!/usr/sfw/bin/tclsh8.3 samples | xargs sed --in-place "s|/usr/sfw/bin/tclsh8.3|/usr/bin/tclsh|"
grep -lR -e ^\#\!/usr/bin/tclsh        samples | xargs chmod 755
grep -lR -e ^\#\!/bin/sh               samples | xargs chmod 755

%build
cp -p %{SOURCE2} build.xml
%ant all

%install
rm -rf %{buildroot}

# jars
mkdir -p %{buildroot}%{_javadir}
cp -p build/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%create_jar_links

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr build/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 

# samples
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -pr samples %{buildroot}%{_datadir}/%{name}

%{gcj_compile}

%clean
rm -rf %{buildroot}

%if %{gcj_support}
%post 
%{update_gcjdb}

%postun 
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root,-)
%doc srcs/license.terms
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{gcj_files}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files demo
%defattr(-,root,root,-)
%doc %{_datadir}/%{name}/samples/README
%{_datadir}/%{name}
