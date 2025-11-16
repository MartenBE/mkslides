# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

{ pkgs, lib, config, inputs, ... }:

{
    languages.python = {
        enable = true;
        uv = {
            enable = true;
            sync = {
                enable = true;
            };
        };
    };

    cachix.enable = false;
}
