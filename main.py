#!/usr/bin/env python3
"""Build structured prompts from templates and variables.

Built-in templates use {placeholders}; pass values with --var key=value.
Custom templates can be loaded from a file with the same placeholders.

Usage:
    python3 main.py --list
    python3 main.py explain --var topic="list comprehensions" --var level=beginner
    python3 main.py --template-file my.txt --var name=World
"""
import argparse
import string
import sys

TEMPLATES = {
    "explain": (
        "Explain {topic} to a {level} audience.\n"
        "Use clear, simple language and give one concrete example.\n"
        "Keep the answer under {length} words."),
    "summarize": (
        "Summarize the following text in {length} words or fewer, "
        "keeping the key points:\n\n{text}"),
    "debug": (
        "I have a bug in my {language} code. The error is:\n{error}\n\n"
        "Here is the code:\n{code}\n\n"
        "Explain the cause and suggest a fix."),
    "code-review": (
        "Review this {language} code as a senior engineer. "
        "Check correctness, readability, and performance, "
        "then list concrete improvements:\n\n{code}"),
    "write": (
        "Write a {tone} {format} about {topic} for a {audience} audience. "
        "Keep it around {length} words."),
}

DEFAULTS = {"level": "beginner", "length": "200", "tone": "friendly",
            "format": "blog post", "audience": "general"}


def build(template_text, variables):
    """Fill placeholders; error on any that are still missing."""
    fields = [name for _, name, _, _ in string.Formatter().parse(template_text)
              if name]
    missing = [f for f in fields if f not in variables]
    if missing:
        return None, missing
    return template_text.format(**variables), None


def parse_vars(pairs):
    variables = dict(DEFAULTS)
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"--var needs key=value, got: {pair!r}")
        key, value = pair.split("=", 1)
        variables[key.strip()] = value
    return variables


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Build structured prompts from templates and variables.")
    parser.add_argument("template", nargs="?",
                        help="built-in template name (see --list)")
    parser.add_argument("--template-file",
                        help="custom template file with {placeholders}")
    parser.add_argument("--var", action="append", default=[],
                        metavar="KEY=VALUE",
                        help="set a template variable (repeatable)")
    parser.add_argument("--list", action="store_true",
                        help="list built-in templates and exit")
    parser.add_argument("--output", "-o",
                        help="write the prompt to FILE instead of stdout")
    args = parser.parse_args(argv)

    if args.list:
        for name, text in TEMPLATES.items():
            fields = sorted({f for _, f, _, _ in
                             string.Formatter().parse(text) if f})
            print(f"{name}: {{{', '.join(fields)}}}")
            print(f"    {text.splitlines()[0]}")
        return 0
    if args.template_file:
        with open(args.template_file, encoding="utf-8") as handle:
            template_text = handle.read()
    elif args.template:
        if args.template not in TEMPLATES:
            print(f"ERROR: unknown template {args.template!r}; "
                  f"use --list to see them.", file=sys.stderr)
            return 1
        template_text = TEMPLATES[args.template]
    else:
        parser.error("give a template name, --template-file, or --list")

    try:
        variables = parse_vars(args.var)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    prompt, missing = build(template_text, variables)
    if missing:
        print(f"ERROR: missing variable(s): {', '.join(missing)}; "
              f"pass them with --var key=value.", file=sys.stderr)
        return 1
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(prompt + "\n")
        print(f"Wrote prompt to {args.output}")
    else:
        print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
