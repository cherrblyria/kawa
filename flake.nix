{
  description = "Use less cute little CLI tool.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };

        pythonEnv = pkgs.python311.withPackages (
          ps: with ps; [
            pip
            setuptools
            wheel
          ]
        );

        kawa = pkgs.python311Packages.buildPythonApplication {
          pname = "kawa";
          version = "0.1.0";
          src = ./.;
          pyproject = true;
          build-system = [ pkgs.python311Packages.hatchling ];
        };
      in

      {
        packages.default = kawa;
        apps.default = {
          type = "app";
          program = "${kawa}/bin/kawa";
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonEnv
            pkgs.uv
            pkgs.git
          ];

          shellHook = ''
            if [ ! -d .venv ]; then
              echo "creating virtualenv with uv..."
              uv venv .venv
            fi

            export VIRTUAL_ENV="$PWD/.venv"
            export PATH="$VIRTUAL_ENV/bin:$PATH"
            export PIP_DISABLE_PIP_VERSION_CHECK=1

            echo "# Python $(python --version 2>&1 | cut -d' ' -f2) | uv $(uv --version | cut -d' ' -f2)"
          '';
        };
      }
    );
}
