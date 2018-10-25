{ pkgs ? import <nixpkgs> {} 
, windowsSupport ? false
}:
  
with pkgs;

pythonPackages.buildPythonPackage rec {
  pname = "ansible";
  version = "devel";
  name = "${pname}-${version}";

  src = fetchFromGitHub {
    owner = "ansible";
    repo = "ansible";
    rev = "f0fd0f219de80a8f682b80e1ccdb83fd4988da64";
    sha256 = "128847r4bc650lcpc2z1wxjgdnh07zhxfd9m2bi3wfl069dvhjk9";
  };

  prePatch = ''
    sed -i "s,/usr/,$out," lib/ansible/constants.py
  '';

  doCheck = false;
  dontStrip = true;
  dontPatchELF = true;
  dontPatchShebangs = false;

  propagatedBuildInputs = with pythonPackages; [
    pycrypto paramiko jinja2 pyyaml httplib2 boto six netaddr dnspython
  ] ++ stdenv.lib.optional windowsSupport pywinrm;

  meta = with stdenv.lib; {
    homepage = http://www.ansible.com;
    description = "A simple automation tool";
    license = with licenses; [ gpl3 ];
    platforms = with platforms; linux ++ darwin;
  };
}
