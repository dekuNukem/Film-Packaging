import sys

record_key_dict = {
	"film_speed":None,
	"item_type":["film_box_outside", "film_box_inside", "film_box_instruction_leaflet"],
	"expiry_date":None,
	"manufacturer":None,
	"model_name_full":None, # NOT including brand, including ISO, e.g. Retro 80s, Fujicolor Super HR 200
	"film_size":["120", "35mm", "APS"],
	"date_added":None, # unix ts,
	"item_id":None, # same ID for the same box, can have multiple entries, such as inside, outside, and leaflet
	"sort_order":None, # smallest number shows up first
}


