# Prompt Builder

Build structured prompts from templates and variables.

## Requirements

- Python 3 (standard library only — no extra packages)

## Usage

```bash
python3 main.py --list
python3 main.py explain --var topic="list comprehensions" --var level=beginner
python3 main.py --template-file my.txt --var name=World
```

Options:

- `template` — name of a built-in template (see `--list`)
- `--template-file FILE` — custom template file with `{placeholders}`
- `--var KEY=VALUE` — set a template variable (repeatable)
- `--list` — list built-in templates and their variables, then exit
- `--output, -o FILE` — write the prompt to a file instead of stdout

Built-in templates: `explain`, `summarize`, `debug`, `code-review`,
`write`. Defaults are applied for `level` (beginner), `length` (200),
`tone` (friendly), `format` (blog post), and `audience` (general).

## Example

```bash
$ python3 main.py explain --var topic="list comprehensions"
Explain list comprehensions to a beginner audience.
Use clear, simple language and give one concrete example.
Keep the answer under 200 words.
```

Missing variables are reported as an `ERROR` naming the variable
instead of producing a broken prompt.
