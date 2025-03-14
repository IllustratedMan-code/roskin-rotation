{ lib, buildPythonPackage, fetchPypi }:

buildPythonPackage rec {
  pname = "airr";
  version = "1.5.1";

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-cfierwwvtP4Dim6KrZxY4XEssGuSAh5z2X0IxZt7cUk=";
  };

}
