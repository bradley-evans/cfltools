ENV=python3
PIP=pip3
CMD=cfltools
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))

clean:
	rm ~/Desktop/BradEvans/testincident/unique* 

test-getunique:
	$(PIP) install -e .
	$(CMD) getuniqueips ~/Desktop/BradEvans/testincident/Activities.csv 

test:
	$(PIP) install -e .
	flake8 $(current_dir) > flake8_output
