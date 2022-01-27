{ pkgs ? import <nixpkgs> {} 
, windowsSupport ? false
, pythonPackages
}:
  
with pythonPackages;

buildPythonPackage rec {
  pname = "ansible";
  version = "devel";
  name = "${pname}-${version}";

  src = pkgs.fetchFromGitHub {
    owner = "ansible";
    repo = "ansible";
    rev = "1724b633f2fdc4c8d49e634d44864ef5e2e2d4c6";
    sha256 = "0lnql1ilcz174c0vy9hz8wa099x4z253izf55akji5b6ng31yqkv";
  };

  prePatch = ''
    sed -i "s,/usr/,$out," lib/ansible/constants.py
  '';

  patches = [ ./revert_path_check.patch ];

  doCheck = false;
  dontStrip = true;
  dontPatchELF = true;
  dontPatchShebangs = false;

  propagatedBuildInputs = with pythonPackages; [
    pycrypto paramiko jinja2 pyyaml httplib2 boto six netaddr dnspython cryptography
  ] ++ pkgs.stdenv.lib.optional windowsSupport pywinrm;

  meta = with pkgs.stdenv.lib; {
    homepage = http://www.ansible.com;
    description = "A simple automation tool";
    license = with licenses; [ gpl3 ];
    platforms = with platforms; linux ++ darwin;
  };
}
