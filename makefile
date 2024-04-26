
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

test:
	# python setup.py test
	pytest
	@echo Warning: This test skip test_dispatcher because its long delay. Test it specifically if you need.

help:
	@echo " 	test"
	@echo " 		pytest the tests."
	@echo " 	clean-pyc"
	@echo " 		Remove python artifacts."
