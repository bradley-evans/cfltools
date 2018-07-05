ENV=python3
PIP=pip3
CMD=cfltools

test-getunique:
	$(PIP) install -e .
	$(CMD) --getuniqueips testfile.csv
