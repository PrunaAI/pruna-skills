.PHONY: bundle bundle-skill verify validate publish release skills-sh readme smoke

bundle:
	./.maintainer/bundle_all_skills.sh

bundle-skill:
	@test -n "$(SKILL)" || (echo "Usage: make bundle-skill SKILL=p-image" && exit 1)
	$(MAKE) bundle
	@test -f plugins/$(SKILL)/skills/$(SKILL)/SKILL.md

verify:
	./.maintainer/verify_skill_bundles.sh

validate:
	./.maintainer/validate_release.sh

smoke:
	./.maintainer/smoke_install.sh

publish:
	./.maintainer/release/publish_all_skills.sh

release:
	@echo "Usage: ./.maintainer/release/release.sh <version> [--execute]"

skills-sh:
	python3 .maintainer/write_skills_sh_json.py

readme:
	python3 .maintainer/write_readme_skills_section.py
	python3 .maintainer/write_readme_install.py
