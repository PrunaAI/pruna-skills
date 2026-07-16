.PHONY: bundle verify validate publish release skills-sh readme smoke

bundle:
	./scripts/bundle_all_skills.sh

verify:
	./scripts/verify_skill_bundles.sh

validate:
	./scripts/validate_release.sh

smoke:
	./scripts/smoke_install.sh

publish:
	./scripts/publish_all_skills.sh

release:
	@echo "Usage: ./scripts/release.sh <version> [--execute]"

skills-sh:
	python3 scripts/write_skills_sh_json.py

readme:
	python3 scripts/write_readme_skills_section.py
	python3 scripts/write_readme_install.py
