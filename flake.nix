{
  description = "My Flake";
  inputs = { flake-utils.url = "github:numtide/flake-utils"; };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages."${system}";
        immcantation = (with pkgs.python3Packages; [
          (pkgs.callPackage ./nix/presto.nix {
            buildPythonPackage = pkgs.python3Packages.buildPythonPackage;
          })
          (pkgs.callPackage ./nix/changeo.nix {
            buildPythonPackage = pkgs.python3Packages.buildPythonPackage;
          })
          (pkgs.callPackage ./nix/airr.nix {
            buildPythonPackage = pkgs.python3Packages.buildPythonPackage;
          })
        ]) ++ (with pkgs.rPackages; [ alakazam shazam trigger scoper dowser ]);
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
              biopython
              pyyaml
              numpy
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
              immcantation
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
