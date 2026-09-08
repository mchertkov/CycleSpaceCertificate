.PHONY: install test static all reference-figures clean-generated

install:
	python -m pip install -r requirements.txt

test:
	pytest -q

static:
	python run_all.py --skip-transient

all:
	python run_all.py

reference-figures:
	python -c "from figures import make_figures; make_figures('figures/reference', reference_only=True)"

clean-generated:
	find results/generated -type f ! -name '.gitkeep' -delete
	find figures/generated -type f ! -name '.gitkeep' -delete
