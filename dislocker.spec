#
# Conditional build:
%bcond_without	ruby	# Ruby binding in library, dislocker-find utility

Summary:	Read BitLocker encrypted volumes under Linux
Summary(pl.UTF-8):	Odczyt wolumenów szyfrowanych BitLockerem spod Linuksa
Name:		dislocker
Version:	0.7.3
Release:	3
License:	GPL v2+
Group:		Applications/File
#Source0Download: https://github.com/Aorimn/dislocker/releases
Source0:	https://github.com/Aorimn/dislocker/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ff1a5a0120cedf04c6146da91dfbd27c
Patch0:		mbedtls.patch
URL:		https://github.com/Aorimn/dislocker
BuildRequires:	cmake >= 2.6
BuildRequires:	libfuse-devel
BuildRequires:	mbedtls-devel
%{?with_ruby:BuildRequires:	ruby-devel >= 1:1.8}
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This software has been designed to read BitLocker encrypted partitions
under a Linux system. The driver has the capability to read/write on:
- Windows Vista, 7, 8, 8.1 and 10 encrypted partitions - that's
  AES-CBC, AES-XTS, 128 or 256 bits, with or without the Elephant
  diffuser, encrypted partitions;
- BitLocker-To-Go encrypted partitions - that's USB/FAT32 partitions.

%description -l pl.UTF-8
To oprogramowanie powstało w celu odczytu spod systemu Linux partycji
zaszyfrowanych BitLockerem. Sterownik potrafi czytać i zapisywać na
partycjach szyfrowanych:
- Windows Vista, 7, 8, 8.1 oraz 10 - czyli AES-CBC, AES-XTS, 128 lub 256
  bitów, z lub bez dyfuzora Elephant
- BitLocker-To-Go, czyli USB/FAT32

%package fuse
Summary:	Read/write BitLocker encrypted volumes under Linux
Summary(pl.UTF-8):	Odczyt/zapis wolumenów szyfrowanych BitLockerem spod Linuksa
Group:		Applications/File
Requires:	%{name} = %{version}-%{release}

%description fuse
FUSE driver to mount BitLocker volume and create a virtual NTFS
partition, which can be mounted as any other NTFS partition.

%description fuse -l pl.UTF-8
Sterownik FUSE do montowania wolumenów BitLockera i tworzenia
wirtualnych partycji NTFS, które można zamontować tak, jak inne
partycje NTFS.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e '1s,/usr/bin/env ruby,/usr/bin/ruby,' src/dislocker-find.rb.in

%build
install -d build
cd build
%cmake .. \
	-DLIB_INSTALL_DIR=%{_libdir} \
	%{!?with_ruby:-DRUBY_OLD_VERSION=ON}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# workaround race during recompression/symlink conversion
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/dislocker.1.gz
echo '.so dislocker-fuse.1' > $RPM_BUILD_ROOT%{_mandir}/man1/dislocker.1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md
%attr(755,root,root) %{_bindir}/dislocker-bek
%attr(755,root,root) %{_bindir}/dislocker-file
%attr(755,root,root) %{_bindir}/dislocker-metadata
%attr(755,root,root) %{_libdir}/libdislocker.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdislocker.so.0.7
# symlink required for ruby
%attr(755,root,root) %{_libdir}/libdislocker.so
%{_mandir}/man1/dislocker-file.1*
%if %{with ruby}
%attr(755,root,root) %{_bindir}/dislocker-find
%{_mandir}/man1/dislocker-find.1*
%endif

%files fuse
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dislocker
%attr(755,root,root) %{_bindir}/dislocker-fuse
%{_mandir}/man1/dislocker.1*
%{_mandir}/man1/dislocker-fuse.1*
