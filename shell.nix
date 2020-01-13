{ pkgs ? import <nixpkgs> {}
, windowsSupport ? false
}:

with pkgs;

let
  myPytest-bdd = callPackage nix/pytest-bdd { pythonPackages = python37Packages; };
  myProxmoxer = callPackage nix/proxmoxer { pythonPackages = python37Packages; };
  myAnsible = callPackage nix/ansible { pythonPackages = python37Packages; };

  env = python37.withPackages (ps: with ps; [ myPytest-bdd myProxmoxer jmespath virtualenv pip hypothesis pytest_xdist pytest ]);
in
stdenv.mkDerivation {
  name = "alt-infra-ansible";

  buildInputs = [
    env
    openssh
    myAnsible
    pass
  ];
}
