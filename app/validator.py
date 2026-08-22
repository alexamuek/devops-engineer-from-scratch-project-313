from schema import Schema

def validate(data):
	schema = Schema({
	        "original_url": str,
	        "short_name": str
	})
	return schema.is_valid(data)