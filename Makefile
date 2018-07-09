ENV=python3
PIP=pip3
CMD=cfltools

clean:
	rm ~/Desktop/BradEvans/testincident/unique* 

test-getunique:
	$(PIP) install -e .
	$(CMD) getuniqueips ~/Desktop/BradEvans/testincident/Activities.csv 
