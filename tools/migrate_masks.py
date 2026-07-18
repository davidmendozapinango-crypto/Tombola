"""Codemod: replace mask_main/mask_complement calls with generator-derived masks.

This script performs an AST-based transformation on Python source files
in the repository. It replaces calls of the form:

    <expr>.mask_main(args...)
    <expr>.mask_complement(args...)

with the equivalent derived-mask expression using the numbered
generators, preserving semantics and making the migration explicit:

    (<expr>.generate_principal(args...) > 0).astype(int)
    (<expr>.generate_complementary(args...) > 0).astype(int)

Behavior and safety:
- The script parses each .py file into an AST, applies a NodeTransformer
  to rewrite calls, and writes back the transformed source if changes
  occurred. A backup file with suffix `.bak` is created for each
  modified file to allow easy rollback.
- Uses Python's `ast` module and `ast.unparse` for reliable code
  generation (Python 3.9+). The transformation preserves other code
  formatting minimally; run your formatter if desired.

Usage:
    python tools/migrate_masks.py [--dry-run]

If --dry-run is provided, the script will report files that would be
modified without changing them.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import Tuple


class MaskCallTransformer(ast.NodeTransformer):
    """Replace mask_main/mask_complement calls with generator-derived masks."""

    def visit_Call(self, node: ast.Call) -> ast.AST:  # type: ignore[override]
        # transform child nodes first
        self.generic_visit(node)

        # only handle attribute function calls like <expr>.mask_main(...)
        func = node.func
        if isinstance(func, ast.Attribute) and isinstance(func.attr, str):
            if func.attr == "mask_main":
                # replace with (<expr>.generate_principal(args...) > 0).astype(int)
                gen_attr = ast.copy_location(
                    ast.Attribute(
                        value=func.value, attr="generate_principal", ctx=ast.Load()
                    ),
                    func,
                )
                gen_call = ast.copy_location(
                    ast.Call(func=gen_attr, args=node.args, keywords=node.keywords),
                    node,
                )
                compare = ast.copy_location(
                    ast.Compare(
                        left=gen_call, ops=[ast.Gt()], comparators=[ast.Constant(0)]
                    ),
                    node,
                )
                ast_call = ast.copy_location(
                    ast.Call(
                        func=ast.Attribute(
                            value=compare, attr="astype", ctx=ast.Load()
                        ),
                        args=[ast.Name(id="int", ctx=ast.Load())],
                        keywords=[],
                    ),
                    node,
                )
                return ast_call
            if func.attr == "mask_complement":
                gen_attr = ast.copy_location(
                    ast.Attribute(
                        value=func.value, attr="generate_complementary", ctx=ast.Load()
                    ),
                    func,
                )
                gen_call = ast.copy_location(
                    ast.Call(func=gen_attr, args=node.args, keywords=node.keywords),
                    node,
                )
                compare = ast.copy_location(
                    ast.Compare(
                        left=gen_call, ops=[ast.Gt()], comparators=[ast.Constant(0)]
                    ),
                    node,
                )
                ast_call = ast.copy_location(
                    ast.Call(
                        func=ast.Attribute(
                            value=compare, attr="astype", ctx=ast.Load()
                        ),
                        args=[ast.Name(id="int", ctx=ast.Load())],
                        keywords=[],
                    ),
                    node,
                )
                return ast_call

        return node


def transform_file(path: Path, dry_run: bool = False) -> Tuple[bool, str]:
    """Transform a single Python file. Returns (changed, message)."""
    src = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return False, f"SKIP (syntax error): {path}: {e}"

    transformer = MaskCallTransformer()
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)

    new_src = ast.unparse(new_tree)
    if new_src != src:
        if dry_run:
            return True, f"WILL MODIFY: {path}"
        # create a backup and overwrite
        backup = path.with_suffix(path.suffix + ".bak")
        path.write_text(src, encoding="utf-8")
        backup.write_text(src, encoding="utf-8")
        path.write_text(new_src, encoding="utf-8")
        return True, f"MODIFIED: {path} (backup: {backup.name})"
    return False, f"UNCHANGED: {path}"


def main(argv: list[str]) -> int:
    dry_run = "--dry-run" in argv
    root = Path.cwd()
    py_files = list(root.glob("**/*.py"))

    changed_files = []
    for p in py_files:
        # skip virtual envs, .git, and tools folder itself
        if any(part.startswith(".") for part in p.parts):
            continue
        if "venv" in p.parts or "site-packages" in p.parts:
            continue
        if p.match("tools/migrate_masks.py"):
            continue
        changed, msg = transform_file(p, dry_run=dry_run)
        if changed:
            changed_files.append((p, msg))
        print(msg)

    print(f"\nSummary: {len(changed_files)} files changed")
    return 0 if not changed_files else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
