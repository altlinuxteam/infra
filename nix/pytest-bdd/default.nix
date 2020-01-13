{ pkgs ? import <nixpkgs> {}
, pythonPackages
}:
  
with pythonPackages;

buildPythonPackage rec {
  pname = "pytest-bdd";
  version = "3.1.1";

  src = fetchPypi {
    inherit pname version;
    sha256 = "0r5p9i0viqfm8l5336fpjjwad4z98077fgi3652qym75mmhirb2w";
  };

  glob2 = callPackage ../glob2 { inherit pythonPackages; };

  nativeBuildInputs = with pythonPackages; [ setuptools_scm ];
  propagatedBuildInputs = with pythonPackages; [ glob2 pytest pytest-forked mock pytest_xdist Mako parse-type ];

  doCheck = false;

  meta = {
    homepage = "https://github.com/pytest-dev/pytest-bdd";
    description = "BDD library for the py.test runner";
  };
}
