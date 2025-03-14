{ lib, buildPythonPackage, fetchPypi }:

buildPythonPackage rec {
  pname = "presto";
  version = "0.7.2";

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-tPSzRBOvQgfrIFIxbTHXvCBnuGQoZJhHbYkBOtVCPdk=";
  };

}
