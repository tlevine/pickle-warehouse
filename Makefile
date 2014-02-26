test:
	nosetests-3.3
	nosetests-2.7
	sh -c 'if rst2html.py README | grep "(ERROR|WARNING)"; then echo "Error parsing README" && exit 1; fi'
