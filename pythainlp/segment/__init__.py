try:
	from pythainlp.segment.pyicu import segment
except ImportError:
	from pythainlp.segment.dict import segment