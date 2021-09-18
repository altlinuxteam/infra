{ pkgs ? import <nixpkgs> {} }:
  
with pkgs;

python27.pkgs.buildPythonPackage rec {
  pname = "proxmoxer";
  version = "1.0.3";

  src = python36.pkgs.fetchPypi {
    inherit pname version;
    sha256 = "145hvphvlzvwq6sn31ldnin0ii50blsapxz0gv2zx3grzp6x9hvh";
  };

  patches = [ ./show_reason_on_exceptions.patch ];
  patches = [ ./added_timeout_settings_for_auth_request.diff ];
  patches = [ ./fix_pvesh_output_format_for_version_more_than_5.3.diff ];
  doCheck = false;

  meta = {
    homepage = "https://github.com/proxmoxer/proxmoxer";
    description = "Proxmoxer is a wrapper around the Proxmox REST API v2";
  };
}
