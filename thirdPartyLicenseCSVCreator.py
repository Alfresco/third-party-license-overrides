#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, csv, os, re

script_path = os.path.dirname(os.path.realpath(__file__))
# The default location for the  license information CSV files.
default_output_dir = script_path + '/target'

parser = argparse.ArgumentParser(description='A script to generate CSV files containing third-party license information.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-c', '--combined', action='store_true', help='Create a single output file containing all libraries.')
parser.add_argument('-o', '--output', default=default_output_dir, help='The output directory (will be created if necessary)')
parser.add_argument('-p', '--project', required=True, help='The path to the project containing THIRD-PARTY.txt files', default=argparse.SUPPRESS)
parser.add_argument('-v', '--version', required=True, help='The product version number being released', default=argparse.SUPPRESS)
args = parser.parse_args()

root_dir = args.project
# License information will be read from files in these target directories.
licenses_dirs = {}
target_dirs = set()
for path, dirs, files in os.walk(root_dir):
    if 'THIRD-PARTY.txt' in files and path.endswith('/target/generated-sources/license'):
        product = path.split('/')[-4]
        licenses_dirs[product] = path + '/'
    if 'target' in dirs:
        target_dirs.add(path.split('/')[-1])

if len(licenses_dirs) == 0:
    print('Failed to find any generated files matching "/target/generated-sources/license/THIRD-PARTY.txt".')
    exit(1)

skipped_target_dirs = target_dirs.difference(licenses_dirs.keys())
if len(skipped_target_dirs) > 0:
    print('No THIRD-PARTY.txt file found in the target directories of the following modules: {}'.format(', '.join(skipped_target_dirs)))

# Load license information for each application.
jars = {}
for product in licenses_dirs:
    jars[product] = {}
    with open(licenses_dirs[product] + '/THIRD-PARTY.txt') as f:
        text = f.read()
        for line in re.split(r'[\n\r]', text):
            if line.strip() == '' or re.match(r'Lists of [0-9]+ third-party dependencies.', line) or line == 'The project has no dependencies.':
                continue
            groups = re.search(r'^\W*(\(.*\)) .* \((.*)\)$', line)
            maven_coordinates, url = groups.group(2).split(' - ')
            group_id, artifact_id, version = maven_coordinates.split(':')
            jar = '{}-{}.jar'.format(artifact_id, version)
            licenses = groups.group(1)
            # Use the first license listed if there are more than one.
            if ') (' in licenses:
                license_name = licenses[1:-1].split(') (')[0]
            else:
                license_name = licenses[1:-1]
            jars[product][jar] = {'license': license_name, 'url': url, 'maven_coordinates': maven_coordinates}

def output_to_csv(project, version, license_information):
    """Create a CSV file containing the given license information."""
    output_file = '{}/{}-{}-3rd-Party-libraries.csv'.format(output_dir, project, version)
    with open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Library Info', 'File Name', 'Package', 'License', 'URL'])
        for jar in sorted(license_information.keys()):
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
    project_name = root_dir.strip('/').split('/')[-1]
    combined_information = {}
    for product in sorted(jars.keys()):
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
