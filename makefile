run:
	python3 run.py

requirements:
	pip freeze > requirements.txt
	cp requirements.txt doc/requirements.txt
