==================================================
WezTerm & HPC Workflow Setup (Windows Edition)
==================================================

This guide documents the setup of a high-performance terminal environment using **WezTerm** on Windows, connected to an **HPC** running **Zsh** and **Powerlevel10k**.

.. contents:: Table of Contents
   :depth: 2

Prerequisites
=============

1. **WezTerm**: Installed via the Nightly setup (`WezTerm-nightly-setup.exe`).
2. **Font**: `MesloLGL Nerd Font` (essential for Powerlevel10k icons).
   
   * Download from `Nerd Fonts <https://www.nerdfonts.com>`_.
   * Install the ``.ttf`` files on Windows.

Local Configuration: `.wezterm.lua`
===================================

Create or edit your config at ``C:\Users\<YourUser>\.wezterm.lua``. This setup uses the **Acrylic** blur effect and includes a custom mapping for Windows Explorer.

.. code-block:: lua

   local wezterm = require("wezterm")
   local act = wezterm.action
   local config = wezterm.config_builder()

   -- Graphics & Performance
   config.front_end = "OpenGL"
   config.webgpu_power_preference = "HighPerformance"
   
   -- Visuals
   config.font = wezterm.font("MesloLGL Nerd Font Mono")
   config.font_size = 19
   config.window_background_opacity = 0.8
   config.win32_system_backdrop = 'Acrylic'

   -- Colorscheme (Coolnight Custom)
   config.colors = {
       foreground = "#CBE0F0",
       background = "#011423",
       cursor_bg = "#47FF9C",
       cursor_border = "#47FF9C",
       cursor_fg = "#011423",
       selection_bg = "#033259",
       selection_fg = "#CBE0F0",
       ansi = { "#214969", "#E52E2E", "#44FFB1", "#FFE073", "#0FC5ED", "#a277ff", "#24EAF7", "#24EAF7" },
       brights = { "#214969", "#E52E2E", "#44FFB1", "#FFE073", "#A277FF", "#a277ff", "#24EAF7", "#24EAF7" },
   }

   -- Keybindings
   config.keys = {
       -- CTRL+SHIFT+E: Sync HPC path to Windows Explorer
       {
           key = 'E',
           mods = 'CTRL|SHIFT',
           action = wezterm.action_callback(function(win, pane)
               local cwd = pane:get_current_working_dir()
               local default_home = 'Z:\\ResearchHome\\ClusterHome\\yli11'
               local path = default_home

               if cwd then
                   path = cwd.file_path
                   path = path:gsub("^/", "")
                   path = path:gsub("/", "\\")
               end

               win:perform_action(
                   act.SpawnCommandInNewWindow { args = { 'explorer.exe', path } },
                   pane
               )
           end),
       },
       { key = 'v', mods = 'CTRL|SHIFT', action = act.PasteFrom 'Clipboard' },
       { key = 'c', mods = 'CTRL|SHIFT', action = act.CopyTo 'Clipboard' },
   }

   return config

Remote Configuration: HPC Zsh
=============================

On the HPC, ensure you load Zsh and configure the environment to communicate with WezTerm.

Steps taken:
------------
1. **Load Zsh**: ``module load zsh``
2. **Oh My Zsh**: Installed for plugin management.
3. **Plugins**: 
   * ``zsh-autosuggestions``
   * ``zsh-syntax-highlighting``
4. **Theme**: ``Powerlevel10k``

The `.zshrc` File
-----------------

.. code-block:: zsh

   # Enable Powerlevel10k instant prompt
   if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
     source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
   fi

   export ZSH="$HOME/.oh-my-zsh"
   ZSH_THEME="powerlevel10k/powerlevel10k"
   plugins=(git zsh-autosuggestions zsh-syntax-highlighting)

   source $ZSH/oh-my-zsh.sh
   [[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

   # --- WezTerm Integration ---

   # Path Reporter: Maps Linux paths to Windows Network Drive (Z:)
   __wezterm_osc7() {
     local p=$(pwd)
     local win_path="Z:\\ResearchHome\\ClusterHome${p//\//\\}"
     printf "\033]7;file://localhost/%s\a" "$win_path"
   }

   autoload -Uz add-zsh-hook
   add-zsh-hook chpwd __wezterm_osc7
   __wezterm_osc7

   # Emulate bash while sourcing .bashrc
   if [ -f ~/.bashrc ]; then
      emulate bash -c "source ~/.bashrc"
   fi

Features
========

Inline Image Viewing
--------------------
To view PNG files (plots/graphs) directly in the terminal, use the ``imgcat`` script provided by WezTerm. This allows bioinformatics results to be previewed without downloading files.

Windows Explorer Sync
---------------------
By pressing **CTRL + SHIFT + E**, WezTerm will detect your current working directory on the HPC and open the corresponding folder on your mapped **Z: Drive** in Windows Explorer.


::

    module load zsh;zsh


Autocomplete failed
---------

::

    rm -f ~/.zcompdump; compinit
    source ~/.zshrc