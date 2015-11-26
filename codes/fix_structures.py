#!/usr/bin/env python3
import glob
import json
import sys
import random
import re


def strip_tags(value):
	while '<' in value and '>' in value:
		new_value = _strip_once(value)
		if len(new_value) >= len(value):
			break
		value = new_value
	return value

def filter_structure (obj1, obj2):
	if type(obj1) == type(obj2):
		if isinstance(obj1, dict):
			struct = {}
			for k in obj1:
				if k in obj2:
					struct[k] = filter_structure(obj1[k], obj2[k])
		elif isinstance(obj1, list):
			copy = list(obj1)
			struct = copy.pop()
			for k in copy:
				struct = filter_structure(struct, k)
			for k in obj2:
				struct = filter_structure(struct, k)
			struct = [struct]
		else:
			struct = obj1
		return struct
	return None

def copy_structure (obj):
	if isinstance(obj, dict):
		struct = {}
		for k in obj:
			struct[k] = copy_structure(obj[k])
	elif isinstance(obj, list):
		struct = filter_structure(obj, obj)
	else:
		struct = obj
	return struct

def fix_structure (struct, dlcs, publishers, developers):
	del struct['package_groups']
	if 'dlc' in struct:
		for dlc in struct['dlc']:
			dlcs[dlc] = struct['steam_appid']
		del struct['dlc']
	if 'price_overview' in struct:
		struct['price'] = struct['price_overview']['initial']
		del struct['price_overview']
	else:
		struct['price'] = 0
	if not isinstance(struct['required_age'], int):
		struct['required_age'] = int(struct['required_age'])
	for reqs in ['pc_requirements', 'mac_requirements', 'linux_requirements']:
		if not isinstance(struct[reqs], dict) or (not 'minimum' in struct[reqs] and not 'recommended' in struct[reqs]):
			if (isinstance(struct[reqs], list)):
				struct[reqs] = ''
		else:
			if 'minimum' in struct[reqs]:
				struct[reqs] = re.sub('<[^<]+?>', '', struct[reqs]['minimum'].strip())
			else:
				struct[reqs] = re.sub('<[^<]+?>', '', struct[reqs]['recommended'].strip())
	if not 'supported_languages' in struct:
		struct['supported_languages'] = 'English'
	struct['linux_support'] = struct['platforms']['linux']
	struct['mac_support'] = struct['platforms']['mac']
	struct['windows_support'] = struct['platforms']['windows']
	del struct['platforms']
	struct['coming_soon'] = struct['release_date']['coming_soon']
	struct['release_date'] = struct['release_date']['date']
	struct['support_email'] = struct['support_info']['email']
	struct['support_url'] = struct['support_info']['url']
	if 'developers' in struct:
		for dev in struct['developers']:
			if dev != '':
				if not dev in developers:
					developers[dev] = set()
				developers[dev].add(struct['steam_appid'])
		del struct['developers']
	for pub in struct['publishers']:
		if pub != '':
			if not pub in publishers:
				publishers[pub] = set()
			publishers[pub].add(struct['steam_appid'])
	del struct['publishers']
	del struct['support_info']
	if not isinstance(struct['website'], str):
		struct['website'] = ""

files = {}
first = None
dlcs = {}
publishers = {}
developers = {}

for f in glob.glob('*.json'):
	if random.random():
		with open(f, 'r') as fo:
			js = json.load(fo)
			uid = f[:-5]
			if 'data' in js[uid] and js[uid]['success']:
				if first is None:
					first = f
				files[f] = js[uid]['data']
			fo.close()

for k in files:
	fix_structure(files[k], dlcs, publishers, developers)

dlc = int(first[:-5])
files[first]['dlc_from'] = dlcs[dlc] if dlc in dlcs else 0
structure = copy_structure(files[first])
del files[first]

for k in files:
	dlc = int(k[:-5])
	files[k]['dlc_from'] = dlcs[dlc] if dlc in dlcs else 0
	structure = filter_structure(structure, files[k])

for k in files:
	with open('details/' + k, 'w') as fo:
		json.dump({ i: files[k][i] for i in structure }, fo, indent = 4, sort_keys = True)
		fo.close()

for i, pub in enumerate(publishers):
	with open('publishers/{0}.json'.format(i + 1), 'w') as fo:
		json.dump({pub: list(publishers[pub])}, fo, indent = 4, sort_keys = True)

for i, dev in enumerate(developers):
	with open('developers/{0}.json'.format(i + 1), 'w') as fo:
		json.dump({dev: list(developers[dev])}, fo, indent = 4, sort_keys = True)
