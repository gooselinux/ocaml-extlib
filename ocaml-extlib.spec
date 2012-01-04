%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global debug_package %{nil}

Name:           ocaml-extlib
Version:        1.5.1
Release:        8.2%{?dist}
Summary:        OCaml ExtLib additions to the standard library

Group:          Development/Libraries
License:        LGPLv2+ with exceptions
URL:            http://code.google.com/p/ocaml-extlib/
Source0:        http://ocaml-extlib.googlecode.com/files/extlib-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExcludeArch:    sparc64 s390 s390x

Patch0:         extlib-install.patch

BuildRequires:  ocaml >= 3.10.1
BuildRequires:  ocaml-findlib-devel, ocaml-ocamldoc
BuildRequires:  gawk


%description
ExtLib is a project aiming at providing a complete - yet small -
standard library for the OCaml programming language. The purpose of
this library is to add new functions to OCaml Standard Library
modules, to modify some functions in order to get better performances
or more safety (tail-recursive) but also to provide new modules which
should be useful for the average OCaml programmer.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n extlib-%{version}

# Files in the archive have spurious +x mode.
chmod 0644 *

# and DOS line endings.
for f in *.ml *.mli README.txt LICENSE; do \
  %{__sed} -i 's/\r//' $f;
done

%patch0 -p1


%build
# You can't just build extlib!


%install
rm -rf $RPM_BUILD_ROOT

extlibdir=$RPM_BUILD_ROOT%{_libdir}/ocaml/extlib
mkdir -p $extlibdir

# This does the build and install.
%if %opt
ocaml install.ml -d $extlibdir -b -n -doc
%else
ocaml install.ml -d $extlibdir -b -doc
%endif

# Copy the interface files, and extLib.ml which is really an interface.
cp extLib.ml *.mli $RPM_BUILD_ROOT%{_libdir}/ocaml/extlib

cp META.txt $RPM_BUILD_ROOT%{_libdir}/ocaml/extlib/META

# Move the HTML documentation - we'll install it using a %doc rule.
mv $extlibdir/extlib-doc .


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.txt LICENSE
%{_libdir}/ocaml/extlib
%if %opt
%exclude %{_libdir}/ocaml/extlib/*.a
%exclude %{_libdir}/ocaml/extlib/*.cmxa
%exclude %{_libdir}/ocaml/extlib/*.cmx
%endif
%exclude %{_libdir}/ocaml/extlib/*.mli
%exclude %{_libdir}/ocaml/extlib/*.ml


%files devel
%defattr(-,root,root,-)
%doc extlib-doc/*
%if %opt
%{_libdir}/ocaml/extlib/*.a
%{_libdir}/ocaml/extlib/*.cmxa
%{_libdir}/ocaml/extlib/*.cmx
%endif
%{_libdir}/ocaml/extlib/*.mli
%{_libdir}/ocaml/extlib/*.ml

%changelog
* Mon Jan 11 2010 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-8.2
- Replace %%define with %%global.
- Use upstream RPM 4.8 OCaml dependency generator.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.5.1-8.1
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-7
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-5
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-4
- Rebuild for OCaml 3.11.0

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-3
- Rebuild for OCaml 3.10.2

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-2
- License is LGPLv2+ with exceptions.
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-1
- New upstream version 1.5.1.
- New home page.
- Rebuild for OCaml 3.10.1.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-8
- Force rebuild because of updated requires/provides scripts in OCaml.

* Mon Sep  3 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-7
- Force rebuild because of base OCaml.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-6
- Force rebuild because of changed BRs in base OCaml.

* Wed Aug  1 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-5
- ExcludeArch ppc64
- Added BR on ocaml-ocamldoc
- Use %doc to install documentation.

* Mon Jun 11 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-4
- Updated to latest packaging guidelines.

* Sat Jun  2 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-3
- Support for bytecode-only architectures.
- *.cmx files are needed.

* Fri May 25 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-2
- Use OCaml find-requires and find-provides.

* Fri May 18 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-1
- Initial RPM release.

