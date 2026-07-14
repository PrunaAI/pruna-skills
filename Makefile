.PHONY: bundle verify validate publish release skills-sh readme

bundle:
	./scripts/bundle_all_skills.sh

verify:
	./scripts/verify_skill_bundles.sh

validate:
	python3 scripts/validate_all_skills.py

publish:
	./scripts/publish_all_skills.sh

release:
	@echo "Usage: ./scripts/release.sh <version> [--execute]"

skills-sh:
	python3 scripts/write_skills_sh_json.py

readme:
	python3 scripts/write_readme_skills_section.py
