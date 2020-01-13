{ pkgs ? import <nixpkgs> {}
, pythonPackages
}:

with pythonPackages;

buildPythonPackage rec {
  pname = "proxmoxer";
  version = "1.0.3";

  src = fetchPypi {
    inherit pname version;
    sha256 = "145hvphvlzvwq6sn31ldnin0ii50blsapxz0gv2zx3grzp6x9hvh";
  };

  patches = [ ./show_reason_on_exceptions.patch ];
  doCheck = false;

  meta = {
    homepage = "https://github.com/swayf/proxmoxer";
    description = "Proxmoxer is a wrapper around the Proxmox REST API v2";
  };
}
