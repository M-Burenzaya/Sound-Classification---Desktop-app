convert:
	find UI -name "*.ui" | cut -d/ -f2 | cut -d. -f1 | xargs -I {} pyside6-uic "UI/{}.ui" -o "Custom_UIs/{}.py"

convert_fix:
	find Custom_UIs -name "*.py" | xargs -I {} misc/Fix-pyside-conversion-types.sh {}

convert_black:
	find Custom_UIs -name "*.py" | xargs -I {} black {}

convert_removal_imports:
	find Custom_UIs -name "*.py" | xargs -I {} autoflake --in-place --remove-all-unused-imports {}

convert_all:
	make clean_convert
	make convert
	make convert_fix
	make convert_black
	make convert_removal_imports

release:
	pyinstaller -F main.py

clean_convert:
	find Custom_UIs ! -name '__init__.py' -type f -exec rm -f {} +

run:
	python3 main.py

run_from_nix:
	nixGL python3 main.py
