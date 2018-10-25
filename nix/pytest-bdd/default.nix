{ pkgs ? import <nixpkgs> {} }:
  
with pkgs;

python27.pkgs.buildPythonPackage rec {
  pname = "pytest-bdd";
  version = "3.0.0";

  src = python36.pkgs.fetchPypi {
    inherit pname version;
    sha256 = "1np2qvfnhz3amd02f2y4shp4pracnfdkcdxkhkigv997iwc4sih0";
  };

  glob2 = callPackage ../glob2 {};

  nativeBuildInputs = with pythonPackages; [ setuptools_scm ];
  propagatedBuildInputs = with pythonPackages; [ glob2 pytest pytest-forked mock pytest_xdist Mako parse-type ];

  doCheck = false;

  meta = {
    homepage = "https://github.com/pytest-dev/pytest-bdd";
    description = "BDD library for the py.test runner";
  };
}
