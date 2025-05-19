from pathlib import Path
import argparse

def scan_txt_files(directory, min_size):
    directory = Path(directory)
    if not directory.exists():
        print("Directory does not exist.")
        return

    txt_files = list(directory.rglob("*.txt"))

    print(f"\nScanning: {directory.resolve()}")
    print(f"Found {len(txt_files)} text files:\n")

    print(f"{'File':<40} {'Size (KB)':>10}")
    print("-" * 52)

    total_size = 0
    displayed_files = 0
    for file in txt_files:
        size_kb = file.stat().st_size / 1024
        if size_kb >= min_size:
            total_size += size_kb
            displayed_files += 1
            print(f"{str(file.relative_to(directory)):<40} {size_kb:>10.1f}")

    print("-" * 52)
    print(f"Displayed files: {displayed_files}")
    print(f"Total size: {total_size:.1f} KB\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recursively scan directory for .txt files.")
    parser.add_argument("path", help="Path to directory to scan")
    parser.add_argument("--min-size", type=float, default=0, help="Minimum file size in kilobytes")
    args = parser.parse_args()
    scan_txt_files(args.path, args.min_size)
