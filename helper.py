import re
import string
import os

DATA_FOLDER = './.your_vinyl_files/DO_NOT_EDIT_THESE_FILES/data/'
MASTER_FOLDER = './.your_vinyl_files/DO_NOT_EDIT_THESE_FILES/master_list/'
DEFAULT_PERMISSIONS = 0o640
TOKEN_FILE = DATA_FOLDER + '.token.dat'

def get_token():
	try:
		with open(TOKEN_FILE, 'r') as f:
			return f.readline()
	except IOError:
		return None

def write_json_to_data_folder(filename, the_dict):
	the_file = DATA_FOLDER+filename

	with open(DATA_FOLDER+filename, 'w') as f:
		f.write(get_dict_in_json_safe_format(the_dict))

	os.chmod(the_file, DEFAULT_PERMISSIONS)

def get_dict_in_json_safe_format(my_dict):
	my_dict = str(my_dict)
	my_dict = my_dict.replace('{\'', '{"')
	my_dict = my_dict.replace('\':', '":')
	my_dict = my_dict.replace(', \'', ', "')
	my_dict = my_dict.replace('\',', '",')
	my_dict = my_dict.replace('[\'', '["')
	my_dict = my_dict.replace('\']', '"]')
	return my_dict

def lower_and_strip_punctuation(my_string):
	return my_string.lower().replace(' ', '').translate(str.maketrans('', '', string.punctuation))

# To handle duplicate artists, Discogs appends a number to the end. ex: Disclosure (3)
def remove_trailing_number(artist):
	res = re.findall(r'\(\d+\)', artist)
	if len(res) == 0:
		return artist
	idx = artist.index(res[-1])
	return artist[:idx].strip()

def update_user_token(token):
	os.makedirs(os.path.dirname(DATA_FOLDER), exist_ok=True)
	os.makedirs(os.path.dirname(MASTER_FOLDER), exist_ok=True)

	with open(TOKEN_FILE, 'w') as f:
		f.write(token.strip())

	os.chmod(TOKEN_FILE, DEFAULT_PERMISSIONS)

	p = os.popen('attrib +h ' + TOKEN_FILE)
	t = p.read()
	p.close()
