import os, re

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

fixed_count = 0
fixed_files = []

for r, d, fnames in os.walk(root):
    for f in fnames:
        if f.endswith(".md") and not f.startswith("."):
            path = os.path.join(r, f)
            with open(path, "r", encoding="utf-8") as fl:
                content = fl.read()

            # Pattern to find blockquoted code blocks:
            # Lines starting with > followed by optional spaces and ```
            # up to > followed by ```
            def clean_block(match):
                global fixed_count
                fixed_count += 1
                full_match = match.group(0)
                lines = full_match.split("\n")
                new_lines = []
                for line in lines:
                    # Strip leading '>' and up to one space
                    cleaned = re.sub(r"^(\s*>\s?)+", "", line)
                    new_lines.append(cleaned)
                return "\n" + "\n".join(new_lines) + "\n"

            # Match:
            # ^[ \t]*>[ \t]*```[a-zA-Z0-9_-]*\n(?:^[ \t]*>.*?\n)*^[ \t]*>[ \t]*```
            pattern = re.compile(
                r"(^[ \t]*>[ \t]*```[a-zA-Z0-9_-]*\n(?:[ \t]*>.*?\n)*?[ \t]*>[ \t]*```)",
                re.MULTILINE
            )

            new_content = pattern.sub(clean_block, content)

            if new_content != content:
                with open(path, "w", encoding="utf-8") as fl:
                    fl.write(new_content)
                fixed_files.append(os.path.relpath(path, root))

print(f"Fixed {fixed_count} blockquoted code blocks across {len(fixed_files)} files:")
for ff in fixed_files:
    print(f"  - {ff}")
