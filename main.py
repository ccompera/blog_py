#!/usr/bin/env python3
import marko
from datetime import datetime
import os

def parse_param(param):
	if param == "":
		return ()
	key, value = param.split(':', 1)
	key = key.strip()
	value = value.strip()
	if key == "tags":
		return (key, list(map(str.strip, value.split(','))))
	if key == "date":
		return (key, datetime.strptime(value, "%Y/%m/%d %H:%M:%S"))
	else:
		return (key, value)

def split_file(filepath):
	header = {}
	with open(filepath) as f:
		for line in f:
			if line == "---\n":
				break;
			(key, value) = parse_param(line)
			header[key] = value
		content = f.read()
		return (header, content)

def format_header(header):
	tags = ", ".join(header["tags"])
	return "<p><i> %s</i> – %s</p>" % (header["date"].strftime("%d/%m/%Y"), tags)

def format_content(content):
	return marko.convert(content)

def create_article_from_file(filename):
	header, content = split_file(filename)
	article = "<article>\n%s%s\n</article>" % (format_content(content), format_header(header))
	return article

def create_all_articles():
	directory = "Posts"
	filelist = [f.path for f in os.scandir(directory) if f.name.endswith(".md")]
	return "\n\n<hr>\n\n".join(map(create_article_from_file, filelist))

def main():
	html_start = """<!DOCTYPE html>
<html>
	<head>
		<title>Blog</title>
		<link rel="stylesheet" href="blog.css" >
	</head>
	<body>

"""
	html_end = """

	</body>
</html>\n"""
	index = html_start + create_all_articles() + html_end
	f = open('index.html','w')
	f.write(index)
	f.close()
	return None

if __name__ == "__main__":
	main()
