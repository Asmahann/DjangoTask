#!/usr/bin/env python3
"""
GitHub Activity Bot Core Orchestrator.
Generates code modules, updates repositories, and pushes commits to keep GitHub contribution graphs active.
"""

import argparse
import sys
import os
import random
import subprocess
from datetime import datetime

# Add script directory to python path for imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from generators.python_utils import generate_python_util
from generators.algorithms import generate_algorithm
from generators.dev_notes import generate_dev_note
from generators.web_snippets import generate_web_snippet


def run_command(cmd, cwd=None, exit_on_error=True):
    """Executes a shell command and prints output."""
    print(f"-> Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error executing command: {result.stderr}")
        if exit_on_error:
            sys.exit(result.returncode)
    return result.stdout.strip()


def pick_generator(gen_type: str):
    """Selects generator function based on choice."""
    generators = {
        "utils": (generate_python_util, "projects/python_utils"),
        "algo": (generate_algorithm, "projects/algorithms"),
        "notes": (generate_dev_note, "notes"),
        "web": (generate_web_snippet, "projects/web_snippets"),
    }

    if gen_type in ("random", "python"):
        # Select exclusively Python code generators
        chosen_key = random.choice(["utils", "algo"])
        return generators[chosen_key]

    if gen_type in generators:
        return generators[gen_type]

    raise ValueError(f"Unknown generator type: {gen_type}")


def main():
    parser = argparse.ArgumentParser(description="GitHub Activity & Mini-Project Bot")
    parser.add_argument("--type", choices=["utils", "algo", "notes", "web", "random", "python"], default="random",
                        help="Type of mini-project/snippet to generate")
    parser.add_argument("--dry-run", action="store_true", help="Generate files without making git commits")
    parser.add_argument("--push", action="store_true", help="Automatically push commit to remote git repository")
    parser.add_argument("--repo-root", default=os.path.abspath(os.path.join(SCRIPT_DIR, "..")),
                        help="Root path of git repository")
    args = parser.parse_args()

    repo_root = os.path.abspath(args.repo_root)
    print(f"==================================================")
    print(f"🤖 GitHub Activity Bot starting at {datetime.now().isoformat()}")
    print(f"Repository Root: {repo_root}")
    print(f"==================================================")

    # Pick generator function and relative directory
    generator_func, rel_subfolder = pick_generator(args.type)
    target_dir = os.path.join(repo_root, rel_subfolder)
    os.makedirs(target_dir, exist_ok=True)

    # Generate content
    file_path, content, commit_message = generator_func(target_dir)

    print(f"Generated File: {file_path}")
    print(f"Commit Message: {commit_message}")

    # Write file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    rel_file_path = os.path.relpath(file_path, repo_root)

    if args.dry_run:
        print("\n[DRY RUN] Skipping git commit and push steps.")
        print("Generated Content Snippet:")
        print("--------------------------------------------------")
        print(content[:300] + ("\n..." if len(content) > 300 else ""))
        print("--------------------------------------------------")
        print("Dry run completed successfully!")
        return

    # Perform Git Actions
    run_command(["git", "add", rel_file_path], cwd=repo_root)
    
    # Check if there are changes to commit
    status_out = run_command(["git", "status", "--porcelain"], cwd=repo_root)
    if not status_out:
        print("No new changes detected in git status.")
        return

    run_command(["git", "commit", "-m", commit_message], cwd=repo_root)
    print(f"Successfully committed: {commit_message}")

    if args.push:
        run_command(["git", "push"], cwd=repo_root)
        print("Successfully pushed commit to remote repository!")

    print("==================================================")
    print("✨ GitHub Activity Bot completed successfully.")
    print("==================================================")


if __name__ == "__main__":
    main()
