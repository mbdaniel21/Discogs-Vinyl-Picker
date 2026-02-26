# TODO import discogs_client via pip
import discogs_client
import helper as v
import string
import sys
import webbrowser
from getpass import getpass

#TODO functionanlity is broken if vinyl is not updated

d = discogs_client.Client('MyVinylPickerHelper/1.0', user_token=v.get_token())
DEBUG = True

def artists():
	artists = dict()
	me = d.identity()

	for it in me.collection_folders[0].releases:
		release_artist = it.release.artists
		artist = v.lower_and_strip_punctuation(release_artist[0].name)
		title = it.release.title
		if DEBUG:
			print("Scanning '" + title + "' by " + v.remove_trailing_number(release_artist[0].name))

		if artist in artists:
			artists[artist].append(title)
		else:
			artists[artist] = [title]

	v.write_json_to_data_folder('artists.json', artists)
	print('Artists from your collection updated')

def genres():
	# TODO use d
	genres = '{'
	current_genre = ''

	with open(v.MASTER_FOLDER+'genre_master.txt', 'r') as f:
		for line in f:
			if not line.strip():
				genres = genres[:-2] + '], '
				continue

			if line[0] == '#':
				current_genre = v.lower_and_strip_punctuation(line.strip()[1:])
				genres = genres + '"' + current_genre + '": ['
				continue
			
			pair = line.split('-', 1)
			_, song = pair[0].strip(), pair[1].strip()

			genres = genres + '"' + song + '", ' 

		# Need to strip incorrect '],' from beginning of string and
		# add bracket for last artist
		genres = genres[:-2] + ']}'

	with open(v.DATA_FOLDER+'genres.json', 'w') as f:
		f.write(genres)

	print('genres.txt updated')
				

def vinyl():
	#TODO use d
	vinyl = ''

	with open(v.MASTER_FOLDER+'vinyl_master.txt', 'r') as f:
		for line in f:
			pair = line.split('-', 1)
			_, album = pair[0].strip(), pair[1].strip().replace(',', '')
			print(album)
			vinyl = vinyl + album + ', '

	# Strip the unnecessary trailing ', '
	vinyl = vinyl[:-2]

	with open(v.DATA_FOLDER+'vinyl.txt', 'w') as f:
		f.write(vinyl)

	print('vinyl.txt updated')

def _setup_user_token():
	input("You will be taken to Discogs. Please generate and copy your user token to the console. Enter to continue...")
	webbrowser.open_new_tab("https://www.discogs.com/settings/developers")
	token = getpass("Enter token here: ")
	v.update_user_token(token)
	return discogs_client.Client('MyVinylPickerHelper/1.0', user_token=token)


# TODO --help message
def main():	
	if len(sys.argv) < 2:
		print('\n====== Please run the setup with a flag. --help for options. ======\n')
		return

	global DEBUG
	if '--debug' in sys.argv:
		DEBUG = True
	
	global d
	try:
		d.identity()
	except discogs_client.exceptions.HTTPError:
		print("Your user token is either empty or invalid, let's get it one setup for you.")
		d = _setup_user_token()		
	
	if '--all' in sys.argv:
		vinyl()
		artists()
		genres()
		return

	if '-a' in sys.argv:
		artists()

	if '-g' in sys.argv:
		genres()

	if '-v' in sys.argv:
		vinyl()

if __name__ == '__main__':
	main()
