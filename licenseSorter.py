#!/usr/bin/env python3
# -*- coding: utf-8 -*-

includes = 'includedLicenses.txt'
merges = 'licenseMerges.txt'
overrides = 'override-THIRD-PARTY.properties'

# Sort the includes file.
with open(includes) as f:
	lines = f.readlines()
with open(includes, 'w') as f:
	lines = sorted(lines, key=str.casefold)
	for line in lines:
		line = line.strip()
		if line:
			f.write(line + '\n')

# Sort the merges file.
with open(merges) as f:
	lines = f.readlines()
with open(merges, 'w') as f:
	lines = sorted(lines, key=str.casefold)
	for line in lines:
		line = line.strip()
		if line:
			licenses = line.split('|')
			licenses = licenses[:1] + sorted(licenses[1:], key=str.casefold)
			f.write('|'.join(licenses) + '\n')

# Sort the overrides file.
with open(overrides) as f:
	lines = f.readlines()
lines = list(filter(lambda line: line.strip(), lines))
pairs = zip(lines[::2], lines[1::2])
with open(overrides, 'w') as f:
	pairs = sorted(pairs, key=lambda pair: str.casefold(pair[1]))
	for pair in pairs:
		for line in pair:
			f.write(line.strip() + '\n')
