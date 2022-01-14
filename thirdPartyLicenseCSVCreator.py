#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, csv, io, os, re, zipfile

LICENSE_SEPARATOR = '|'
LICENSE_PREFERENCE_ORDER = ['Apache-2.0', 'BSD-2-Clause', 'BSD-3-Clause', 'MIT', 'Zlib', 'BSD-3-Clause-No-Nuclear-Warranty',
'CC0-1.0', 'CDDL-1.0', 'CDDL-1.1', 'CPL-1.0', 'EDL-1.0', 'EPL-1.0', 'EPL-2.0', 'ANTLR-PD', 'PostgreSQL', 'JSON']
GENERATED_SOURCES_FILE = os.sep + os.path.join('target', 'generated-sources', 'license')

script_path = os.path.dirname(os.path.realpath(__file__))
# This should be the name of the directory "third-party-license-overrides".
script_dir = os.path.basename(script_path)
# The default location for the  license information CSV files.
default_output_dir = os.path.join(script_path, 'target')

parser = argparse.ArgumentParser(description='A script to generate CSV files containing third-party license information.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-c', '--combined', action='store_true', help='Create a single output file containing all libraries.')
parser.add_argument('-d', '--desired', required=False, help='An ordered list of desired licenses delimited by |',
        default=LICENSE_SEPARATOR.join(LICENSE_PREFERENCE_ORDER))
parser.add_argument('-o', '--output', default=default_output_dir, help='The output directory (will be created if necessary)')
parser.add_argument('-p', '--project', required=False, help='The path to the project containing THIRD-PARTY.txt files', default=argparse.SUPPRESS)
parser.add_argument('-v', '--version', required=True, help='The product version number being released', default=argparse.SUPPRESS)
parser.add_argument('-z', '--zippath', required=False, help='A path to a zip file (or jar, war, etc.) to search for a THIRD-PARTY.txt file.', default=argparse.SUPPRESS)
args = parser.parse_args()

class MavenThirdPartyWalker:
    """A third party walker that can load THIRD-PARTY.txt files from a maven project."""
    def __init__(self, root_dir):
        self.root_dir = root_dir
        # License information will be read from files in these target directories.
        self.licenses_dirs = {}
        target_dirs = set()
        # Always ignore THIRD-PARTY.txt files that are within clones of this project.
        ignore_dirs = set()
        if os.path.commonprefix([script_path, root_dir]) != script_path:
            for path, dirs, files in os.walk(root_dir):
                if script_dir in dirs:
                    ignore_dirs.add(os.path.join(path, script_dir))
        # Search for any THIRD-PARTY.txt files.
        for path, dirs, files in os.walk(root_dir):
            if any([path.startswith(ignore_dir) for ignore_dir in ignore_dirs]):
                continue
            if 'THIRD-PARTY.txt' in files and path.endswith(GENERATED_SOURCES_FILE):
                product = path.split(os.sep)[-4]
                self.licenses_dirs[product] = path + os.sep
            if 'target' in dirs:
                target_dirs.add(os.path.basename(path))

        if len(self.licenses_dirs) == 0:
            print('Failed to find any generated files matching "{}".'.format(GENERATED_SOURCES_FILE))
            exit(1)

        skipped_target_dirs = target_dirs.difference(self.licenses_dirs.keys())
        if len(skipped_target_dirs) > 0:
            print('No THIRD-PARTY.txt file found in the target directories of the following modules: {}'.format(', '.join(skipped_target_dirs)))
    
    def get_project(self):
        return os.path.basename(self.root_dir.strip(os.sep))

    def get_products(self):
        return self.licenses_dirs.keys()
    
    def get_third_party_license_file(self, product):
        return open(os.path.join(self.licenses_dirs[product], 'THIRD-PARTY.txt'))


class ZipThirdPartyWalker:
    """A third party walker that can load THIRD-PARTY.txt files from a zip, jar, war or amp file."""
    def __init__(self, zip_path):
        self.zip = zipfile.ZipFile(zip_path)
        paths = [path for path in self.zip.namelist() if path.endswith('THIRD-PARTY.txt')]
        if len(paths) == 0:
            print('Failed to find any files in zip {} matching THIRD-PARTY.txt'.format(zip_path))
            exit(1)
        if len(paths) > 1:
            print('Multiple THIRD-PARTY.txt files found in zip - only using first: ' + paths)
        self.path = paths[0]
    
    def get_project(self):
        zip_name = os.path.basename(self.zip.filename)
        return zip_name.split('.')[0] if '.' in zip_name else zip_name

    def get_products(self):
        return [os.path.basename(self.zip.filename)]
    
    def get_third_party_license_file(self, product):
        return io.TextIOWrapper(self.zip.open(self.path, 'r'))


if 'project' in dir(args) and 'zippath' in dir(args):
    print('Only one project or zippath may be specified as the source.')
    exit(1)
elif 'project' in dir(args):
    third_party_walker = MavenThirdPartyWalker(args.project)
elif 'zippath' in dir(args):
    third_party_walker = ZipThirdPartyWalker(args.zippath)
else:
    print('A project or zippath must be specified.')
    exit(1)

def pick_license(licenses, desired_str):
    """Return the first applicable desired license, otherwise one from includedLicenses.txt, or fall back on the first license provided."""
    # Look for a matching license in the supplied list of desired licenses.
    desired = map(str.strip, desired_str.split(LICENSE_SEPARATOR))
    for desired_license in desired:
        if desired_license in licenses:
            return desired_license
    # If no desired license matches then look for a license in the includedLicenses.txt file.
    with open(os.path.join(script_path, 'includedLicenses.txt')) as included_licenses:
        approved_licenses = included_licenses.read().strip().split('\n')
        for approved_license in approved_licenses:
            if approved_license in licenses:
                return approved_license
    # Fall back on the first license in the list.
    return licenses[0]

# Load license information for each application.
jars = {}
for product in third_party_walker.get_products():
    jars[product] = {}
    with third_party_walker.get_third_party_license_file(product) as f:
        text = f.read()
        for line in re.split(r'[\n\r]', text):
            if line.strip() == '' or re.match(r'Lists of [0-9]+ third-party dependencies.', line) or line == 'The project has no dependencies.':
                continue
            groups = re.search(r'^\W*(\(.*\)) .* \((.*)\)$', line)
            maven_coordinates, url = groups.group(2).split(' - ')
            group_id, artifact_id, version = maven_coordinates.split(':')
            jar = '{}-{}.jar'.format(artifact_id, version)
            licenses = groups.group(1)
            license_name = pick_license(licenses[1:-1].split(') ('), args.desired)
            jars[product][jar] = {'license': license_name, 'url': url, 'maven_coordinates': maven_coordinates}

def output_to_csv(project, version, license_information):
    """Create a CSV file containing the given license information."""
    output_file = os.path.join(output_dir, '{}-{}-3rd-Party-libraries.csv'.format(project, version))
    with open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Library Info', 'File Name', 'Package', 'License', 'URL'])
        for jar in sorted(license_information.keys(), key=str.lower):
            lib_info = license_information[jar]['maven_coordinates']
            product = project if 'product' not in license_information[jar] else license_information[jar]['product']
            lic = license_information[jar]['license']
            url = license_information[jar]['url']
            csv_writer.writerow([lib_info, jar, product, lic, url])
    print('Created {}'.format(output_file))

# Write all license information
output_dir = args.output
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
if args.combined:
    project_name = third_party_walker.get_project()
    combined_information = {}
    for product in sorted(jars.keys(), key=str.lower):
        license_information = jars[product]
        for jar, metadata in license_information.items():
            if jar not in combined_information:
                combined_information[jar] = metadata
                combined_information[jar]['product'] = product
            else:
                combined_information[jar]['product'] += '|' + product
    output_to_csv(project_name, args.version, combined_information)
else:
    for product, license_information in jars.items():
        output_to_csv(product, args.version, license_information)
