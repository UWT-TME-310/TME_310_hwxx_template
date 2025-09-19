#!/usr/bin/env python3
"""
Alternative script: Add visual read-only indicators to notebook cells.
Since VS Code doesn't fully respect editable/deletable metadata,
this adds clear visual warnings to cells with 'read_only' tags.
"""

import json
import sys


def add_readonly_warnings(notebook_path):
    """Add visual read-only warnings to tagged cells."""

    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    modified_count = 0
    for cell in notebook.get("cells", []):
        tags = cell.get("metadata", {}).get("tags", [])
        if "read_only" in tags:
            # Add metadata
            if "metadata" not in cell:
                cell["metadata"] = {}
            cell["metadata"]["editable"] = False
            cell["metadata"]["deletable"] = False

            # Add visual warning to cell content
            if cell["cell_type"] == "markdown":
                source = "".join(cell.get("source", []))
                if not source.startswith("⚠️ **READ-ONLY"):
                    cell["source"] = ["⚠️ **READ-ONLY CELL** ⚠️\n\n"] + cell.get(
                        "source", []
                    )
            elif cell["cell_type"] == "code":
                source = "".join(cell.get("source", []))
                if not source.startswith("# ⚠️ READ-ONLY"):
                    cell["source"] = [
                        "# ⚠️ READ-ONLY CELL - DO NOT EDIT ⚠️\n"
                    ] + cell.get("source", [])

            modified_count += 1

    with open(notebook_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)

    print(f"Added read-only warnings to {modified_count} cells")
    print(
        "Cells now have visual warnings since VS Code doesn't enforce metadata restrictions"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python add_readonly_warnings.py <notebook_file.ipynb>")
        sys.exit(1)

    add_readonly_warnings(sys.argv[1])
