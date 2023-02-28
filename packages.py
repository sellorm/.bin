#!/usr/bin/env python3
"""
A little package management tool for my private binaries.

It uses a json file to specify a repo and a command.
The repo is cloned into ~/.bin_packages and the command inside the repo is
symlinked back to the ~/.bin_packages directory.

Remember that we need to use something like `EXPORT PATH=~/.bin:~/.bin_projects:${PATH}`
"""

import argparse
import json
import os
import re
import subprocess
import sys


def package_paths_handler(packages_entry):
    """
    parse a package entry from packages.json and return useful paths etc.
    """
    pkg = {}
    pkg["repo"] = packages_entry["repo"]
    pkg["command"] = packages_entry["command"]
    pkg["clean_dir"] = clean_url(packages_entry["repo"])
    pkg["pkg_path"] = os.path.join(
        os.path.expanduser("~/.bin_packages/packages"), pkg["clean_dir"]
    )
    pkg["cmd_path"] = os.path.join(pkg["pkg_path"], pkg["command"])
    pkg["link_path"] = os.path.join(
        os.path.expanduser("~/.bin_packages"), pkg["command"]
    )
    return pkg


def clean_url(url):
    """
    Strips 'http://', 'https://' and '.git' from URLs
    """
    pattern_html = r"^http[s]?:\/\/"
    pattern_git = r"\.git$"
    url_no_http = re.sub(pattern_html, "", url)
    url_no_git = re.sub(pattern_git, "", url_no_http)
    return url_no_git


def has_git():
    """
    checks for the existance of the git cli tool
    """
    try:
        _result = subprocess.run(["git", "--version"], capture_output=True, check=True)
    except ChildProcessError:
        return False
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError:
        return False
    return True


def validate_packages_install_path():
    """
    Checks for the existance of the packages installation path ~/.bin_packages/packages
    """
    packages_path = os.path.expanduser("~/.bin_packages/packages")
    if not os.path.isdir(packages_path):
        os.makedirs(packages_path)


def get_packages_json():
    """
    returns parsed packages.json
    """
    with open("packages.json", "r", encoding="utf8") as file:
        package_data = json.load(file)
    return package_data


def install_packages():
    """
    installs packages from packages.json
    """
    packages_data = get_packages_json()
    for package_data in packages_data:
        package = package_paths_handler(package_data)
        if os.path.exists(package["pkg_path"]):
            print(f"Error: package already installed {package['repo']}")
        else:
            os.makedirs(package["pkg_path"])
            git_cmd = ["git", "clone", package["repo"], package["pkg_path"]]
            _result = subprocess.run(git_cmd, capture_output=True, check=True)
            os.symlink(package["cmd_path"], package["link_path"])


def upgrade_packages():
    """
    upgrades installed packages
    """
    packages_data = get_packages_json()
    for package_data in packages_data:
        package = package_paths_handler(package_data)
        git_cmd = ["git", "-C", package["pkg_path"], "pull"]
        _result = subprocess.run(git_cmd, capture_output=True, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="packager.py",
        description="a simple package manager for my private bin directory",
        epilog="Another sellorm rough cut",
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-i",
        "--install",
        help="install packages",
        action="store_true",
    )

    group.add_argument(
        "-u",
        "--upgrade",
        help="upgrade packages",
        action="store_true",
    )

    args = parser.parse_args()

    validate_packages_install_path()

    if not has_git():
        print("Error: no installation of git command line tool on $PATH")
        sys.exit(1)

    if args.install:
        install_packages()

    if args.upgrade:
        upgrade_packages()
