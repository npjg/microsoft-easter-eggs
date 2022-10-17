#!/usr/bin/python3

## Exports the assets for the credits easter egg of a Windows 3.1x SHELL.DLL.
## Currently, only read-only support is planned. But eventually, modding
## will be possible!

import argparse
import credits
import os 
import json

# PARSE THE COMMAND-LINE ARGUMENTS.
argument_parser = argparse.ArgumentParser(
    formatter_class = argparse.RawTextHelpFormatter,
    description = """Extracts assets from the Windows 3.1 Credits easter egg.""")
# The input argument.
input_argument_help = """The filepath to SHELL.DLL (Windows 3.1x version)."""
argument_parser.add_argument('input', help = input_argument_help)
# The export argument.
export_argument_help = f"""Specify the directory location for exporting assets.
(If a directory that already exists is provided, a subdirectory with the name of the application will be created instead.)"""
argument_parser.add_argument('export', help = export_argument_help)
command_line_args = argument_parser.parse_args()

# EXTRACT THE ASSETS.
shell_dll = credits.Windows31Credits(command_line_args.input)
# First, the Windows flag animation.
shell_dll.windows_flag_animation.save_as_animated_gif(
    os.path.join(command_line_args.export, 'Windows Flag.gif'))
# Second the credit backgrounds (with emcees).
for emcee in shell_dll.emcees:
    emcee.image.save(os.path.join(command_line_args.export, f'{emcee.name}.bmp'))
# Finally, the decrypted and parsed credit text.
with open(os.path.join(command_line_args.export, 'credits.json'), 'w') as credits_file:
    json.dump(shell_dll.credits_text, credits_file)
