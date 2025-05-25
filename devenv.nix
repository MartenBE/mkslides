{ pkgs, lib, config, inputs, ... }:

{
    languages.python = {
        enable = true;
        poetry = {
            enable = true;
            install = {
                enable = true;
                installRootPackage = true;
            };
            activate.enable = true;
            package = pkgs.poetry;
        };
    };

    cachix.enable = false;
}
