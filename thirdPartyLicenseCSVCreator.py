#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, csv, os, re

script_path = os.path.dirname(os.path.realpath(__file__))
# The default location for the  license information CSV files.
default_output_dir = script_path + '/target'

parser = argparse.ArgumentParser(description='A script to generate CSV files containing third-party license information.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-o', '--output', default=default_output_dir, help='The output directory (will be created if necessary)')
parser.add_argument('-p', '--project', required=True, help='The path to the project containing THIRD-PARTY.txt files', default=argparse.SUPPRESS)
parser.add_argument('-v', '--version', required=True, help='The product version number being released', default=argparse.SUPPRESS)
args = parser.parse_args()

root_dir = args.project
# License information will be read from files in these target directories.
licenses_dirs = {}
for path, dirs, files in os.walk(root_dir):
    if 'THIRD-PARTY.txt' in files and path.endswith('/generated-sources/license'):
        product = path.rsplit('/', 4)[1]
        licenses_dirs[product] = path + '/'

if len(licenses_dirs) == 0:
    print('Failed to find any generated files matching "/generated-sources/license/THIRD-PARTY.txt".')
    exit(1)

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
            jars[product][jar] = {'license': license_name, 'url': url}

# Write all license information
output_dir = args.output
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
for product, license_information in jars.items():
    output_file = '{}/{}-{}-3rd-Party-libraries.csv'.format(output_dir, product, args.version)
    with open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Library', 'License', 'URL'])
        for jar in sorted(license_information.keys()):
            lic = license_information[jar]['license']
            url = license_information[jar]['url']
            csv_writer.writerow([jar, lic, url])
    print('Created {}'.format(output_file))
