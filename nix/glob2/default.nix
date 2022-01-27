{ pkgs ? import <nixpkgs> {}
, pythonPackages
}:

with pythonPackages;

buildPythonPackage rec {
  pname = "glob2";
  version = "0.6";

  src = fetchPypi {
    inherit pname version;
    sha256 = "1miyz0pjyji4gqrzl04xsxcylk3h2v9fvi7hsg221y11zy3adc7m";
  };

  nativeBuildInputs = with pythonPackages; [ setuptools_scm ];
  buildInputs = with pythonPackages; [ ];
  doCheck = false;

  meta = {
    homepage = "https://github.com/miracle2k/python-glob2";
    description = "extended version of Python's builtin glob module";
  };
}
