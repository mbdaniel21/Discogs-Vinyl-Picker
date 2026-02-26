import copy
import helper as v
import json
import random
import sys

def get_dict_from_json_file(flag):
	to_ret = None
	if flag == '-g':
		with open(v.DATA_FOLDER+'genres.json', 'r') as json_file:
			return json.loads(json_file.read())
	if flag == '-a':
		with open(v.DATA_FOLDER+'artists.json', 'r') as json_file:
			return json.loads(json_file.read())

def filter_by_user_want(params_tuple):
	albums_with_desired_parameters = []
	potential_albums, desired_music, flag = params_tuple[0], params_tuple[1], params_tuple[2]
	music_set = get_dict_from_json_file(flag)

	for param in desired_music:
		key = v.lower_and_strip_punctuation(param)
		print(key)
		print(music_set["kendricklamar"])
		try:
			albums_with_desired_parameters.extend(music_set[key])
		except KeyError:
			print('Given parameter ' + param + ' not present in database.')

	print(albums_with_desired_parameters)
	print(potential_albums)
	print(list(filter(lambda a: a in albums_with_desired_parameters, potential_albums)))
	return list(filter(lambda a: a in albums_with_desired_parameters, potential_albums))

def setup(flag, potential_albums):
	start = sys.argv.index(flag)+1
	end = start+1

	while  end < len(sys.argv) and not '-' in sys.argv[end]:
		end += 1

	args = ''.join(sys.argv[start:end]).split(',')

	return (potential_albums, args, flag)

def main():
	if '--help' in sys.argv:
		print('TODO')
		return

	potential_albums = None
	with open(v.DATA_FOLDER+'vinyl.txt','r') as f:
		potential_albums = f.readline().split(', ')

	if '-a' in sys.argv:
		potential_albums = filter_by_user_want(setup('-a', potential_albums))
		print('Found ' + str(len(potential_albums)) + ' albums by desired artists.')

	if '-g' in sys.argv:
		potential_albums = filter_by_user_want(setup('-g', potential_albums))
		print('Found ' + str(len(potential_albums)) + ' albums in desired genre.')

	try:
		print('\n\nGiven your parameters, your suggested album is ' + random.choice(potential_albums) + '!\n')
	except IndexError:
		print('No album found with given parameters, please try again.')

if __name__ == '__main__':
	main()