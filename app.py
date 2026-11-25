#!/usr/bin/env python3
import os
import sys
import asyncio
import inspect
import shutil
from pathlib import Path
from datetime import datetime

os.environ.setdefault(
    "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python"
)

try:
    from midx_guard import verify, ensure_requirements

    verify()
    ensure_requirements()

    import midx_app
    import br_engine

except Exception as exc:
    print("Startup error:", exc)
    raise SystemExit(1)


ROOT = Path(midx_app.ROOT)
ACCOUNT_FILE = ROOT / "accs.txt"


def banner():
    print("\n" + "=" * 65)
    print("                 BR RANK SQUAD CONTROL PANEL")
    print("=" * 65)
    print()
    print("                    CREATED BY MEGHA BHAI")
    print("                     DEVELOPER: MEGHA BHAI")
    print()
    print("-" * 65)
    print("  1  Generate guest accounts")
    print("  2  Join guild manually")
    print("  3  Start BR RANK matches")
    print("  4  Show saved accounts")
    print("  5  Remove saved IDs")
    print("  0  Exit")
    print("-" * 65)


async def run_action(function, *args, **kwargs):
    result = function(*args, **kwargs)

    if inspect.isawaitable(result):
        await result


def show_accounts():
    accounts = midx_app.load_accounts()

    print("\n========== SAVED ACCOUNTS ==========")
    print("Total saved accounts:", len(accounts))

    if not accounts:
        print("No saved accounts found.")
    else:
        for index, account in enumerate(accounts, 1):
            identifier = None

            if isinstance(account, dict):
                for key in ("uid", "account_id", "user_id", "id"):
                    if account.get(key):
                        identifier = str(account[key])
                        break

            if identifier:
                if len(identifier) > 4:
                    identifier = identifier[:2] + "***" + identifier[-2:]
                else:
                    identifier = "***"

                print(f"{index}. Account ID: {identifier}")
            else:
                print(f"{index}. Saved account")

    print("=" * 36)


def remove_saved_ids():
    if not ACCOUNT_FILE.exists():
        print("\nAccount file not found.")
        return

    lines = ACCOUNT_FILE.read_text(
        encoding="utf-8"
    ).splitlines(keepends=True)

    entries = [
        (index, line)
        for index, line in enumerate(lines)
        if line.strip()
    ]

    if not entries:
        print("\nNo saved IDs to remove.")
        return

    print("\n========== REMOVE SAVED IDs ==========")
    print("Total saved IDs:", len(entries))
    print("Enter numbers separated by commas.")
    print("Example: 1,3,5")
    print("Enter ALL to select every saved ID.")
    print("Enter 0 to cancel.")

    choice = input("\nYour selection: ").strip().lower()

    if choice == "0":
        print("Removal cancelled.")
        return

    try:
        if choice == "all":
            selected = set(range(1, len(entries) + 1))
        else:
            selected = {
                int(value.strip())
                for value in choice.split(",")
            }

        if not selected or any(
            number < 1 or number > len(entries)
            for number in selected
        ):
            raise ValueError

    except ValueError:
        print("Invalid selection.")
        return

    print("\nSelected IDs:", len(selected))
    confirm = input("Type YES to confirm removal: ").strip()

    if confirm != "YES":
        print("Removal cancelled.")
        return

    backup = ACCOUNT_FILE.with_name(
        "accs.txt.backup-" +
        datetime.now().strftime("%Y%m%d-%H%M%S")
    )

    try:
        shutil.copy2(ACCOUNT_FILE, backup)

        remove_indexes = {
            entries[number - 1][0]
            for number in selected
        }

        remaining = [
            line
            for index, line in enumerate(lines)
            if index not in remove_indexes
        ]

        ACCOUNT_FILE.write_text(
            "".join(remaining),
            encoding="utf-8"
        )

        print("\nRemoval successful!")
        print("Removed IDs:", len(selected))
        print("Remaining IDs:", len(entries) - len(selected))
        print("Backup:", backup.name)

    except Exception as exc:
        print("Removal error:", exc)
        print("Check your backup before retrying.")


async def main():
    while True:
        banner()

        choice = input("\nSelect command: ").strip()

        try:
            if choice == "1":
                print("\nStarting guest account generator...")
                await run_action(
                    br_engine.generate_accounts_interactive
                )

            elif choice == "2":
                print("\nOpening guild menu...")
                await run_action(midx_app.join_guild)

            elif choice == "3":
                print("\nStarting BR RANK mode...")
                await run_action(
                    midx_app.start_matches,
                    match_mode="BR"
                )

            elif choice == "4":
                show_accounts()

            elif choice == "5":
                remove_saved_ids()

            elif choice == "0":
                print("\nExiting BR RANK panel.")
                break

            else:
                print("\nInvalid command.")

        except KeyboardInterrupt:
            print("\nOperation interrupted.")

        except Exception as exc:
            print("\nOperation error:", exc)

        if choice != "0":
            input("\nPress ENTER to return to menu...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.")
