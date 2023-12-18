.PHONY: htmlcov

htmlcov:
	cd htmlcov && python -m http.server 8000
