"""
Developer Notes & TIL Generator for GitHub Activity Bot.
Generates structured Markdown developer notes and tech snippets.
"""
import random
import os
from datetime import datetime

TEMPLATES = [
    {
        "topic": "python_dataclasses_vs_namedtuples.md",
        "commit": "docs: add TIL notes on Python dataclasses vs NamedTuples performance",
        "title": "TIL: Python Dataclasses vs NamedTuples",
        "content": """# TIL: Python Dataclasses vs NamedTuples

Comparing performance, immutability, and memory usage between `dataclasses` and `collections.namedtuple`.

## Quick Comparison

| Feature | `dataclass` | `namedtuple` |
|---|---|---|
| Mutability | Mutable by default (`frozen=True` supported) | Immutable |
| Memory Footprint | Slightly higher (unless `__slots__` used) | Very low (tuple subclass) |
| Inheritance | Supported | Limited |
| Dict conversion | `dataclasses.asdict()` | `._asdict()` |

## Code Example

```python
from dataclasses import dataclass
from collections import namedtuple

# NamedTuple
PointNT = namedtuple('PointNT', ['x', 'y'])
p1 = PointNT(10, 20)

# Dataclass with slots for low memory footprint
@dataclass(slots=True, frozen=True)
class PointDC:
    x: float
    y: float

p2 = PointDC(10.0, 20.0)
print(p1, p2)
```
"""
    },
    {
        "topic": "asyncio_concurrency_patterns.md",
        "commit": "docs: add notes on asyncio.gather vs asyncio.TaskGroup patterns",
        "title": "Asyncio Concurrency Patterns in Modern Python",
        "content": """# Modern Asyncio Patterns: TaskGroup vs gather

In Python 3.11+, `asyncio.TaskGroup` provides safer concurrency via structural async context managers compared to `asyncio.gather`.

## Why TaskGroup?

If one task in a `TaskGroup` fails, all other active tasks are cancelled immediately, avoiding leaked background coroutines.

```python
import asyncio

async def fetch_data(api_id: int):
    await asyncio.sleep(0.1)
    return f"Data from API {api_id}"

async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_data(1))
        task2 = tg.create_task(fetch_data(2))
    
    print(task1.result(), task2.result())

if __name__ == "__main__":
    asyncio.run(main())
```
"""
    },
    {
        "topic": "git_interactive_rebase_cheatsheet.md",
        "commit": "docs: add git interactive rebase and commit squashing cheatsheet",
        "title": "Git Interactive Rebase Cheatsheet",
        "content": """# Git Interactive Rebase Cheatsheet

Quick reference guide for cleaning up commit histories prior to opening PRs.

## Essential Commands

- `git rebase -i HEAD~N`: Start interactive rebase for last N commits.
- `pick (p)`: Use commit as-is.
- `reword (r)`: Use commit, but edit commit message.
- `squash (s)`: Meld commit into previous commit and combine messages.
- `fixup (f)`: Meld commit into previous commit and discard this commit's message.

## Useful Flags

```bash
# Auto-squash fixup commits
git commit --fixup <commit-hash>
git rebase -i --autosquash HEAD~5
```
"""
    }
]


def generate_dev_note(target_dir: str) -> tuple[str, str, str]:
    """Generates a markdown developer note in target_dir and returns (rel_filepath, content, commit_message)."""
    template = random.choice(TEMPLATES)
    dest_path = os.path.join(target_dir, template["topic"])
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    full_content = f"<!-- Generated on {date_str} by ActivityBot -->\n\n" + template["content"]
    
    return dest_path, full_content, template["commit"]
