{
  description = "My Flake";
  inputs = { flake-utils.url = "github:numtide/flake-utils"; };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages."${system}";

        dev_packages = with pkgs.python3Packages; [ ipykernel jupyter ];
      in rec {
        packages = {
          library = pkgs.python3Packages.buildPythonPackage {
            build-system = with pkgs.python3Packages; [ setuptools wheel ];
            dependencies = with pkgs.python3Packages; [
              requests
              rich-click
              pandas
              matplotlib
              scipy
              tqdm
              rich
            ];
            name = "irmetafetch";
            src = ./src;
            pyproject = true;
            doCheck = false;

          };
          application =
            pkgs.python3Packages.toPythonApplication packages.library;

          default = packages.application;

        };
        devShells = {
          default = pkgs.mkShell {
            packages = with pkgs; [
              packages.default.dependencies
              csvlens
              dev_packages
            ];
            shellHook = ''
              export PYTHONPATH=''${PYTHONPATH}:$(realpath -s "./src")
            '';
          };
          aslibrary = pkgs.mkShell {
            packages = [
              (pkgs.python3.withPackages (python-pkgs: [ packages.library ]))
            ];
          };

        };
      });
}
