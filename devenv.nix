{ pkgs, lib, config, inputs, ... }:

{
    languages.python = {
        enable = true;
        uv = {
            enable = true;
        };
    };

    cachix.enable = false;
}
