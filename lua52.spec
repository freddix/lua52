Summary:	A simple lightweight powerful embeddable programming language
Name:		lua52
Version:	5.2.2
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://www.lua.org/ftp/lua-%{version}.tar.gz
# Source0-md5:	efbb645e897eae37cad4344ce8b0a614
Patch0:		%{name}-link.patch
URL:		http://www.lua.org/
BuildRequires:	readline-devel
BuildRequires:	sed
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lua is a powerful, light-weight programming language designed for
extending applications. It is also frequently used as a
general-purpose, stand-alone language. It combines simple procedural
syntax (similar to Pascal) with powerful data description constructs
based on associative arrays and extensible semantics. Lua is
dynamically typed, interpreted from bytecodes, and has automatic
memory management with garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.

%package libs
Summary:	lua 5.2.x libraries
Group:		Libraries

%description libs
lua 5.2.x libraries.

%package devel
Summary:	Header files for Lua
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files needed to embed Lua in C/C++ programs and docs for the
language.

%prep
%setup -qn lua-%{version}
%patch0 -p1

%{__sed} -i '/#define LUA_ROOT/s,/usr/local/,%{_prefix}/,' src/luaconf.h
%{__sed} -i '/#define LUA_CDIR/s,lib/lua/,%{_lib}/lua/,' src/luaconf.h

%build
%{__make} -j1 all \
	PLAT=linux \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -fPIC -DPIC -D_GNU_SOURCE -DLUA_USE_LINUX"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/lua}

%{__make} install \
	INSTALL_TOP=$RPM_BUILD_ROOT%{_prefix} \
	INSTALL_INC=$RPM_BUILD_ROOT%{_includedir}/lua5.2 \
	INSTALL_LIB=$RPM_BUILD_ROOT%{_libdir} \
	INSTALL_MAN=$RPM_BUILD_ROOT%{_mandir}/man1 \
	INSTALL_CMOD=$RPM_BUILD_ROOT%{_libdir}/lua/5.2

# change name from lua to lua5.2
for f in lua luac ; do
	mv -f $RPM_BUILD_ROOT%{_bindir}/${f} $RPM_BUILD_ROOT%{_bindir}/${f}5.2
	mv -f $RPM_BUILD_ROOT%{_mandir}/man1/${f}.1 $RPM_BUILD_ROOT%{_mandir}/man1/${f}5.2.1
done

# install shared library
install src/liblua.so.5.2 $RPM_BUILD_ROOT%{_libdir}
ln -s liblua.so.5.2 $RPM_BUILD_ROOT%{_libdir}/liblua5.2.so

# create pkgconfig file
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
cat > $RPM_BUILD_ROOT%{_pkgconfigdir}/lua5.2.pc <<'EOF'
prefix=%{_prefix}
exec_prefix=%{_exec_prefix}
includedir=%{_includedir}/lua5.2
libdir=%{_libdir}
interpreter=%{_bindir}/lua5.2
compiler=%{_bindir}/luac5.2

Name: Lua
Description: An extension programming language
Version: %{version}
Cflags: -I${includedir}
Libs: -L${libdir} -llua5.2 -ldl -lm
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /usr/sbin/ldconfig
%postun libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lua5.2
%attr(755,root,root) %{_bindir}/luac5.2
%{_mandir}/man1/lua5.2.1*
%{_mandir}/man1/luac5.2.1*

%files libs
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/liblua.so.5.2
%dir %{_datadir}/lua
%dir %{_libdir}/lua
%{_datadir}/lua/5.2
%{_libdir}/lua/5.2

%files devel
%defattr(644,root,root,755)
%doc doc/*.{html,css,gif,png}
%attr(755,root,root) %{_libdir}/liblua5.2.so
%{_includedir}/lua5.2
%{_pkgconfigdir}/lua5.2.pc

