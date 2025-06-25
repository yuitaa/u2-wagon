from pathlib import Path
base_dir = Path("images")

for file in base_dir.rglob("debug*.png"):
    if file.is_file():
        file.unlink()
        print(f"Deleted: {file}")