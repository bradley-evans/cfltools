ENV=python3
PIP=pip3
CMD=cfltools

test-getunique:
	rm ~/Desktop/BradEvans/testincident/unique* 
	$(PIP) install -e .
	$(CMD) --getuniqueips ~/Desktop/BradEvans/testincident/Activities.csv 
