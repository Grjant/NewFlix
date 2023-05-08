.PHONY: Collatz.log

FILES :=                              \
	models.html                      \
	models.log                       \
	models.py						\
	main.py                        \
	tests.py						\

models.html: models.py
	$(PYDOC) -w models

IDB3.log:
	git log > IDB3.log

Test.tmp: tests.py
	$(COVERAGE) run    --branch tests.py >  Test.tmp 2>&1
	$(COVERAGE) report -m                      >> Test.tmp
	cat Test.tmp
check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -rf __pycache__
	
docker:
	$(DOC)
	
config:
	git config -l

format:
	$(AUTOPEP8) -i main.py
	$(AUTOPEP8) -i tests.py

scrub:
	make clean
	rm -f  models.html
	rm -f  models.log

status:
	make clean
	@echo
	git branch
	git remote -v
	git status
	
versions:
	which       $(AUTOPEP8)
	$(AUTOPEP8) --version
	@echo
	which       $(COVERAGE)
	$(COVERAGE) --version
	@echo
	which       git
	git         --version
	@echo
	which       make
	make        --version
	@echo
	which       $(PIP)
	$(PIP)      --version
	@echo
	which       $(PYLINT)
	$(PYLINT)   --version
	@echo
	which        $(PYTHON)
	$(PYTHON)    --version

test: models.html models.log check
