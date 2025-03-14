{ buildPythonPackage, fetchPypi }:

buildPythonPackage rec {
  pname = "changeo";
  version = "1.3.0";
  src = fetchPypi {
    inherit pname version;
    hash = "sha256-/r7CUDCGtNdqF31g+by3QmRdJEF3UOl2QJeQ6baCiK0=";
  };
}
