import argparse
import subprocess
import os


def normalize_package_name(name):
    """Normalize package names by replacing underscores with hyphens and lowercasing."""
    return name.replace("_", "-").lower()


def install_and_add_to_requirements(packages):
    """Install all the packages and store their names along with versions in requirements.txt file."""
    requirements_filename = "requirements.txt"
    open("requirements.txt", "a").close()

    # Install the packages
    for package in packages:
        subprocess.run(f"pip install {package}", shell=True, check=True)

    # Get the list of installed packages
    installed_packages = subprocess.run(
        "pip freeze", shell=True, capture_output=True, text=True, check=True
    ).stdout
    installed_packages_dict = {
        normalize_package_name(pkg.split("==")[0]): pkg
        for pkg in installed_packages.strip().split("\n")
    }

    # Read the existing requirements.txt
    with open(requirements_filename, "r") as file:
        existing_lines = file.readlines()

    # Prepare a dictionary of normalized package names to be installed with their versions
    package_dict_to_install = {
        normalize_package_name(pkg.split("==")[0]): pkg for pkg in packages
    }

    # Update requirements.txt
    with open(requirements_filename, "w") as file:
        for line in existing_lines:
            pkg_name = normalize_package_name(line.split("==")[0])
            if pkg_name not in package_dict_to_install:
                file.write(line)

        # Add or update the packages
        for pkg_name, pkg_full_name in package_dict_to_install.items():
            if pkg_name in installed_packages_dict:
                file.write(installed_packages_dict[pkg_name] + "\n")
            else:
                file.write(pkg_full_name + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Install packages and update requirements.txt"
    )
    parser.add_argument(
        "-p", "--package", nargs="+", required=True, help="Package name(s) to install"
    )
    args = parser.parse_args()

    install_and_add_to_requirements(args.package)

    # SAMPLE CMD:
    # python pkg_installer.py --package <pkg_name>