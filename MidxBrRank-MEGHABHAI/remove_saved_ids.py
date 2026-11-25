from pathlib import Path
import shutil

FILE = Path("accs.txt")

if not FILE.exists():
    print("Account file not found.")
    raise SystemExit(1)

lines = FILE.read_text().splitlines(keepends=True)

print(f"\nSaved account entries: {len(lines)}")
print("\nEnter entry numbers to remove.")
print("Example: 2,5,8")
print("Enter 0 to cancel.")

choice = input("\nSelect entries: ").strip()

if choice == "0":
    print("Cancelled.")
    raise SystemExit

try:
    selected = {int(x.strip()) for x in choice.split(",")}
    if not selected or any(x < 1 or x > len(lines) for x in selected):
        raise ValueError
except ValueError:
    print("Invalid selection.")
    raise SystemExit(1)

print(f"\nEntries selected: {len(selected)}")
confirm = input("Confirm removal? (yes/no): ").strip().lower()

if confirm != "yes":
    print("Cancelled.")
    raise SystemExit

backup = Path("accs.txt.backup")
shutil.copy2(FILE, backup)

remaining = [
    line for i, line in enumerate(lines, 1)
    if i not in selected
]

FILE.write_text("".join(remaining))

print(f"\nRemoved: {len(selected)} entries")
print(f"Remaining: {len(remaining)} entries")
print(f"Backup: {backup}")
