# Created by pyp2rpm-2.0.0
%global pypi_name pydocstyle
%global with_python2 0
%define version 3.0.0

Name:           python-%{pypi_name}
Version:        %{version}
Release:        2
Group:          Development/Python
Summary:        pydocstyle is a static analysis tool for checking compliance with Python docstring conventions.

License:        MIT
URL:            https://github.com/PyCQA/pydocstyle
Source0:        https://github.com/PyCQA/pydocstyle/archive/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python-setuptools
 
%if %{?with_python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif # if with_python2


%description
pydocstyle is a static analysis tool for checking compliance with Python docstring conventions.
It supports most of PEP 257 out of the box, but should not be considered a reference implementation.

%if %{with_python2}
%package -n     python2-%{pypi_name}
Summary:        pydocstyle is a static analysis tool for checking compliance with Python docstring conventions.

%description -n python2-%{pypi_name}
pydocstyle is a static analysis tool for checking compliance with Python docstring conventions.
It supports most of PEP 257 out of the box, but should not be considered a reference implementation.
%endif # with_python2


%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# generate html docs 
#sphinx-build -C docs/source html
# remove the sphinx-build leftovers
#rm -rf html/.{doctrees,buildinfo}

%if %{with_python2}
rm -rf %{py2dir}
cp -a . %{py2dir}
find %{py2dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'
# generate html docs 
#sphinx-build2 docs/source html
# remove the sphinx-build leftovers
#rm -rf html/.{doctrees,buildinfo}

%endif # with_python2


%build
%{__python} setup.py build

%if 0%{?with_python2}
pushd %{py2dir}
%{__python2} setup.py build
popd
%endif # with_python2


%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if %{with_python2}
pushd %{py2dir}
%{__python2} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python2

%{__python} setup.py install --skip-build --root %{buildroot}


%files
%doc 
%{_bindir}/%{pypi_name}
%{python_sitelib}/%{pypi_name}
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%if %{with_python2}
%files -n python2-%{pypi_name}
%doc
%{_bindir}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with_python2

