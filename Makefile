.PHONY: bundle bundle-skill verify validate validate-doc-examples publish release skills-sh readme smoke upload-doc-examples-hf download-doc-examples-hf doc-examples-urls sync-doc-examples-hf

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

validate-doc-examples:
	python3 .maintainer/validate_doc_examples.py

doc-examples:
	python3 .maintainer/generate_doc_examples.py

upload-doc-examples-hf:
	python3 .maintainer/upload_doc_examples_hf.py

download-doc-examples-hf:
	python3 .maintainer/download_doc_examples_hf.py

doc-examples-urls:
	python3 .maintainer/rewrite_doc_examples_urls.py

format-examples-md:
	python3 .maintainer/format_examples_md.py

sync-doc-examples-hf: upload-doc-examples-hf doc-examples-urls
