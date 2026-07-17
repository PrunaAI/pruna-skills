.PHONY: bundle bundle-skill verify validate validate-doc-examples publish release skills-sh readme smoke upload-doc-examples-hf download-doc-examples-hf doc-examples-urls sync-doc-examples-hf format-examples-md readme-quickstart-gif quickstart-gif

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

QUICKSTART_WIDTH ?= 280
README_CLIP ?= chain-monarch-clip

readme-quickstart-gif:
	@test -f docs/assets/examples/$(README_CLIP).mp4 || (echo "missing docs/assets/examples/$(README_CLIP).mp4" && exit 1)
	ffmpeg -y -i docs/assets/examples/$(README_CLIP).mp4 -vf "fps=12,scale=$(QUICKSTART_WIDTH):-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3" docs/assets/examples/$(README_CLIP).gif

quickstart-gif: readme-quickstart-gif

sync-doc-examples-hf: upload-doc-examples-hf doc-examples-urls
