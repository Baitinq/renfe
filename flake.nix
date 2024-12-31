{
  description = "Renfe flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-darwin" "aarch64-darwin" "x86_64-linux" ];
      createDevShell = system:
        let
          pkgs = import nixpkgs { system = "${system}"; config.allowUnfree = true; };
          my-python = pkgs.python3;
          python-with-my-packages = my-python.withPackages (p: with p; [
            selenium
            python-dotenv
          ]);
        in
        pkgs.mkShell {
          buildInputs = [
            python-with-my-packages

            # Chrome driver and google-chrome dependencies
            pkgs.chromedriver
            pkgs.google-chrome

            # Create a script to run google-chrome-stable
            (pkgs.writeShellScriptBin "google-chrome" "exec -a $0 ${pkgs.google-chrome}/bin/google-chrome-stable $@")
          ];
        };
    in
    {
      devShell = nixpkgs.lib.genAttrs systems createDevShell;
    };
}
