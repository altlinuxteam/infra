{ pkgs ? import <nixpkgs> {}
, windowsSupport ? false
}:

with pkgs;

let
  myAnsible = pythonPackages.buildPythonPackage rec {
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
      maintainers = with maintainers; [
        jgeerds
        joamaki
      ];
      platforms = with platforms; linux ++ darwin;
    };
  };

  myProxmoxer = python27.pkgs.buildPythonPackage rec {
      pname = "proxmoxer";
      version = "1.0.2";

      src = python36.pkgs.fetchPypi {
        inherit pname version;
        sha256 = "0vpb3b1b8w4r4c28kfhyviw4q70s3vwwirkq6rywryl4wqc3fyra";
      };

      doCheck = false;

      meta = {
        homepage = "https://github.com/swayf/proxmoxer";
        description = "Proxmoxer is a wrapper around the Proxmox REST API v2";
      };
    };
  myPython = python27.withPackages (ps: with ps; [ myProxmoxer jmespath virtualenv pip hypothesis pytest_xdist pytest ]);
in
stdenv.mkDerivation {
  name = "alt-infra-ansible";

  buildInputs = [
    openssh
    myAnsible
    myPython
    pass
  ];
}
