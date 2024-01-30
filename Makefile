add_file_path_comment:
	@python utils.d/add_file_path_comment.py
	@echo "file path comment added"

format: add_file_path_comment
	# pip install isort black pylint bandit mypy flake8 pytest coverage safety pre-commit types-requests pydocstyle radon
	# pre-commit install

	# Code formatting
	python -m isort ./ --line-width 120 --quiet
	python -m black ./ --line-length 120 --quiet

f: format

prompt:
	@bash utils.d/generate_prompt.sh -i migrations -i test_permissions -i tests -p .
	@echo "prompt generated"
