# Bar Prep Tools

This repository contains interactive bar exam study utilities built around the essay and MBE concept bank. The newest addition is a mini MEE game that automatically targets the two hardest essay subjects based on difficulty and exam frequency.

## MEE Hardest Subjects Game

The `mee_game.py` script ranks subjects from `essay_subjects.json`, surfaces the two hardest areas, and walks you through fast prompts so you can self-grade and drill high-yield doctrine.

```bash
# Preview the prompts without typing answers (helpful for quick demos)
python mee_game.py --preview --rounds 2

# Run the full interactive session
python mee_game.py --rounds 5
```

Use `--seed` to make the prompt order reproducible or `--data-path` to point at an alternate JSON dataset.
