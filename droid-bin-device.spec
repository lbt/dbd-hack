%define android_root .
%define ha_device device

Name:           droid-bin-%{ha_device}
Summary:        Droid BIN package for %{ha_device}
License:        BSD-3-Clause
Version:        0.0.6
Release:        %{rel_date}
Provides:       droid-bin
Source0:        rpm.tar.bzip2
Source11:       package-section
Source12:       files-section
Source40:       repo.tar.bzip2

%description
The droid-bin package for %{ha_device}


%if 0%{?_obs_build_project:1}
# BuildRequires:  ubu-trusty # Skip the ubu root for hackery
BuildRequires:  sudo-for-abuild
%endif

%package out-of-image-files
Group:  System
BuildArch: noarch
Summary: Files that are used for flashing and are not needed on device.

%description out-of-image-files
Contains files that are used for flashing but are not needed inside image, e.g.,
flashing configurations or flashing scripts.

# %%include package-section
%package src-bionic
Provides: droid-bin-src-bionic
Group:  System
Summary: Syspart source for the bionic src tree to be used for droid-side code building

%description src-bionic
This is the src tree for the bionic subdirectory from the %device syspart manifest.
It is only meant for use in the OBS.



%prep
# No %%setup macro !!

%if 0%{?_obs_build_project:1}
# The OBS does not have access to 'repo' so a service does the repo init/sync
# and provides a (huge) tarball with the checked-out tree in it.
# So now drop to android_root and pretend to do a repo sync
tar xf %{SOURCE40} -C %android_root
# Clean up the repo tarball to save space
rm -f %{SOURCE40}
# Make a dummy tarball for rpm checks
mkdir dummy;(cd dummy; touch dummy; tar cvf - . | bzip2 > %{SOURCE40}); rm -rf dummy
# unpack the directories to SOURCES ... this needs to change
tar xf %{SOURCE0} -C ../SOURCES
# Clean up the rpm tarball too
rm -f %{SOURCE0}
cp %{SOURCE40} %{SOURCE0}

# In OBS the repo service leaves the rpm/* files for OBS and they just ^^
# got unpacked to ../SOURCES ... but we're used to having an rpm/ dir
# So if rpm/ is missing then we use ../SOURCES :
[ -d rpm ] || ln -s ../SOURCES rpm
%endif

%build

echo _target_cpu is %{_target_cpu}
echo _target_cpu is %{_target_cpu}

%if 0%{?_obs_build_project:1}
# Hadk style build of android on OBS
echo Running droid build in HABUILD_SDK
echo "run an ubu-chroot HADK build here in the OBS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
%endif
  
# Make a tmp location for built installables
rm -rf tmp
mkdir tmp

%install

#RPM_BUILD_ROOT is /home/abuild/rpmbuild/BUILDROOT/droid-bin-device-0.0.6-1.12.1.i386
# cwd is /home/abuild/rpmbuild/BUILD

echo home tree
find /home/abuild -type d

mkdir -p $RPM_BUILD_ROOT/home/abuild/src/droid
mv %android_root/bionic $RPM_BUILD_ROOT/home/abuild/src/droid

echo home tree
pwd
find /home/abuild -type d


# Create dir structure
#mkdir -p $RPM_BUILD_ROOT/boot

# Install
#mkdir -p tmp
#tar --list -vf %{android_root}/out/target/product/%{device}/system.tar.gz > tmp/system-files.txt
#tar -xf %{android_root}/out/target/product/%{device}/system.tar.gz -C $RPM_BUILD_ROOT/

# Get the uid and gid from the tar output and format lines so that those are ok for %files in rpm
#cat tmp/system-files.txt | awk '{ split($2,ids,"/"); print "%attr(-," ids[1] "," ids[2] ") /" $6 }' > tmp/system.files.tmp
# Add %dir macro in front of the directories
#cat tmp/system.files.tmp | awk '{ if (/\/$/) print "%dir "$0; else print $0}' > tmp/system.files

# HACK: This is a bit ugly, but gets the job done.
# As tar outputs numbers instead of names and rpm wants names, lets replace the id numbers
# with appropriate names here.
#sed -i 's/,0/,root/g' tmp/system.files
#sed -i 's/,2000/,shell/g' tmp/system.files

#cp -a %{android_root}/out/target/product/%{device}/{efilinux%{?device_variant}.efi,*.fv,*_EMMC.bin,droidboot.img,esp.img,partition.tbl} $RPM_BUILD_ROOT/boot/


#%%include files-section

%files src-bionic
%defattr(-,abuild,abuild,-)
/home/abuild/src/droid/bionic
