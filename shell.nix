{ pkgs ? import <nixpkgs> {}
, windowsSupport ? false
}:

with pkgs;

let
  pytest-bdd = callPackage nix/pytest-bdd {};
  proxmoxer = callPackage nix/proxmoxer {};
  ansible = callPackage nix/ansible {};

  myPython = python27.withPackages (ps: with ps; [ pytest-bdd proxmoxer jmespath virtualenv pip hypothesis pytest_xdist pytest ]);
in
stdenv.mkDerivation {
  name = "alt-infra-ansible";

  buildInputs = [
    openssh
    ansible
    myPython
    pass
  ];
}
