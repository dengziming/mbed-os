"""
mbed SDK
Copyright (c) 2011-2013 ARM Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from json import load
from os.path import join, dirname
from argparse import ArgumentParser
from tools.toolchains import TOOLCHAINS
from tools.targets import TARGET_NAMES
from tools.utils import argparse_force_uppercase_type, \
    argparse_lowercase_hyphen_type, argparse_many, \
    argparse_filestring_type, args_error

def get_default_options_parser(add_clean=True, add_options=True,
                               add_app_config=False):
    """Create a new options parser with the default compiler options added

    Keyword arguments:
    add_clean - add the clean argument?
    add_options - add the options argument?
    """
    parser = ArgumentParser()

    targetnames = TARGET_NAMES
    targetnames.sort()
    toolchainlist = list(TOOLCHAINS)
    toolchainlist.sort()

    parser.add_argument("-m", "--mcu",
                        help=("build for the given MCU (%s)" %
                              ', '.join(targetnames)),
                        metavar="MCU",
                        type=argparse_many(
                            argparse_force_uppercase_type(
                                targetnames, "MCU")))

    parser.add_argument("-t", "--tool",
                        help=("build using the given TOOLCHAIN (%s)" %
                              ', '.join(toolchainlist)),
                        metavar="TOOLCHAIN",
                        type=argparse_many(
                            argparse_force_uppercase_type(
                                toolchainlist, "toolchain")))

    parser.add_argument("--color",
                        help="print Warnings, and Errors in color",
                        action="store_true", default=False)

    parser.add_argument("--cflags", default=[], action="append",
                        help="Extra flags to provide to the C compiler")

    parser.add_argument("--asmflags", default=[], action="append",
                        help="Extra flags to provide to the assembler")

    parser.add_argument("--ldflags", default=[], action="append",
                        help="Extra flags to provide to the linker")

    if add_clean:
        parser.add_argument("-c", "--clean", action="store_true", default=False,
                            help="clean the build directory")

    if add_options:
        parser.add_argument("--profile", dest="profile", action="append",
                            type=argparse_filestring_type,
                            default=[])
    if add_app_config:
        parser.add_argument("--app-config", default=None, dest="app_config",
                            type=argparse_filestring_type,
                            help="Path of an app configuration file (Default is to look for 'mbed_app.json')")

    return parser


def extract_profile(parser, options, toolchain):
    profile = { 'c': [], 'cxx': [], 'ld': [], 'common': [], 'asm': []}
    filenames = options.profile or [join(dirname(__file__), "profiles",
                                         "default.json")]
    for filename in filenames:
        contents = load(open(filename))
        try:
            for key in profile.iterkeys():
                profile[key] += contents[toolchain][key]
        except KeyError:
            args_error(parser, ("argument --profile: toolchain {} is not"
                                " supported by profile {}").format(toolchain,
                                                                   filename))
    return profile
