from schema import Schema
import re


def validate_body(body):
	schema = Schema({
		"original_url": str,
		"short_name": str
	})
	return schema.is_valid(body)

def parse_and_check_range(range_query):
    range_query = range_query.replace(" ", "")
    pattern = r'^\[\d+,\d+\]$'
    if not re.match(pattern, range_query):
        return None, None
    only_numbers = range_query[1:-1]
    separator = ","
    (start_str, end_str) = only_numbers.split(separator)
    offset = int(start_str)
    end = int(end_str)
    if offset < 0 or end < 0:
        return None, None
    limit = end - offset
    if limit < 0:
        return None, None
    return offset, limit