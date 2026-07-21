.PHONY: bundle bundle-skill verify validate validate-doc-examples publish release skills-sh readme smoke upload-doc-examples-hf download-doc-examples-hf doc-examples-urls sync-doc-examples-hf format-examples-md embed-examples-md doc-example-previews readme-example-embeds readme-quickstart-embeds

bundle:
	./.maintainer/bundle_all_skills.sh

bundle-skill:
	@test -n "$(SKILL)" || (echo "Usage: make bundle-skill SKILL=p-image" && exit 1)
	$(MAKE) bundle
	@python3 -c "from pathlib import Path; import sys; sys.path.insert(0,'.maintainer'); from skill_catalog import all_primary_skills; assert '$(SKILL)' in all_primary_skills() or any(Path(p).exists() for p in [f'skills/guides/$(SKILL)/SKILL.md',f'skills/image/$(SKILL)/SKILL.md',f'skills/video/$(SKILL)/SKILL.md',f'skills/audio/$(SKILL)/SKILL.md',f'skills/suite/$(SKILL)/SKILL.md',f'skills/workflows/$(SKILL)/SKILL.md'])"

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

doc-example-previews:
	python3 .maintainer/generate_example_previews.py

embed-examples-md:
	python3 .maintainer/embed_examples_md.py

format-examples-md-all: doc-example-previews embed-examples-md format-examples-md

QUICKSTART_WIDTH ?= 280
QUICKSTART_HEIGHT ?= 494
QUICKSTART_VF = scale=$(QUICKSTART_WIDTH):$(QUICKSTART_HEIGHT):force_original_aspect_ratio=increase,crop=$(QUICKSTART_WIDTH):$(QUICKSTART_HEIGHT)
# README thumbs write to readme-<stem>.* so full-res EXAMPLES assets stay intact
README_EMBED_STILLS = music-video-garage-drummer p-image-try-on-drummer quickstart-panda-01-open quickstart-panda-02-end illustrated-library-whale
README_EMBED_CLIPS = music-video-garage-drummer-clip quickstart-panda-clip illustrated-library-whale-reel
# GIF caps: short preview, tight palette (GitHub content-length)
README_GIF_SECS ?= 3.5
README_GIF_FPS ?= 8
README_GIF_COLORS ?= 48

readme-example-embeds:
	@mkdir -p docs/assets/examples
	@for s in $(README_EMBED_STILLS); do \
	  test -f docs/assets/examples/$$s.png || (echo "missing docs/assets/examples/$$s.png" && exit 1); \
	  ffmpeg -y -i docs/assets/examples/$$s.png -vf "$(QUICKSTART_VF)" -update 1 -frames:v 1 docs/assets/examples/readme-$$s.png; \
	done
	@for c in $(README_EMBED_CLIPS); do \
	  test -f docs/assets/examples/$$c.mp4 || (echo "missing docs/assets/examples/$$c.mp4" && exit 1); \
	  ffmpeg -y -t $(README_GIF_SECS) -i docs/assets/examples/$$c.mp4 \
	    -vf "fps=$(README_GIF_FPS),$(QUICKSTART_VF),split[s0][s1];[s0]palettegen=max_colors=$(README_GIF_COLORS)[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3" \
	    docs/assets/examples/readme-$$c.gif; \
	done

readme-quickstart-embeds: readme-example-embeds

sync-doc-examples-hf: doc-example-previews upload-doc-examples-hf doc-examples-urls embed-examples-md
