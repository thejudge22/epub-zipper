#!/usr/bin/env python3
import os
import zipfile
import argparse
import shutil
from pathlib import Path

def convert_folder_to_epub(folder_path, output_dir, remove_original=False):
    """
    Convert a folder ending in .epub to an actual ePub file.
    Outputs to the specified output directory.
    """
    folder = Path(folder_path).resolve()

    if not folder.is_dir():
        print(f"❌ Skipping {folder.name}: Not a directory")
        return False

    if not folder.suffix == '.epub':
        print(f"❌ Skipping {folder.name}: Doesn't end with .epub")
        return False

    # Output filename (e.g., book1.epub)
    output_file = output_dir / folder.name

    try:
        print(f"📦 Processing: {folder.name}")

        # Create zip file directly in output location
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            file_count = 0

            # Walk the directory and add files
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = Path(root) / file
                    # Calculate archive name (relative path inside the zip)
                    arcname = file_path.relative_to(folder)
                    zf.write(file_path, arcname)
                    file_count += 1

            print(f"   Added {file_count} files -> converted/{folder.name}")

        if remove_original:
            shutil.rmtree(folder)
            print(f"✅ Created: converted/{folder.name} (original folder removed)")
        else:
            print(f"✅ Created: converted/{folder.name}")

        return True

    except Exception as e:
        print(f"❌ Error processing {folder.name}: {e}")
        if output_file.exists():
            output_file.unlink()
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Convert ePub folders (directories ending in .epub) to actual ePub files'
    )
    parser.add_argument(
        'directory',
        help='Directory containing the .epub folders (e.g., /path/to/books)'
    )
    parser.add_argument(
        '--remove-original',
        action='store_true',
        help='Remove original folders after successful conversion (WARNING: deletes source folders)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without creating files'
    )
    parser.add_argument(
        '--output-dir',
        default='converted',
        help='Name of the output subdirectory (default: converted)'
    )

    args = parser.parse_args()

    target_dir = Path(args.directory).expanduser().resolve()

    if not target_dir.exists():
        print(f"Error: Directory '{target_dir}' does not exist")
        return 1

    # Create output directory
    output_dir = target_dir / args.output_dir
    if not args.dry_run:
        output_dir.mkdir(exist_ok=True)

    # Find all .epub folders
    epub_folders = [d for d in target_dir.iterdir() if d.is_dir() and d.suffix == '.epub']

    if not epub_folders:
        print(f"No folders ending in .epub found in: {target_dir}")
        return 0

    print(f"Found {len(epub_folders)} folder(s) to process")
    print(f"Output directory: {output_dir}\n")

    success_count = 0
    for folder in epub_folders:
        if args.dry_run:
            print(f"Would process: {folder.name} -> {args.output_dir}/{folder.name}")
            continue

        if convert_folder_to_epub(folder, output_dir, args.remove_original):
            success_count += 1

    print(f"\nComplete: {success_count}/{len(epub_folders)} converted successfully")
    print(f"Files saved to: {output_dir}")

    if not args.remove_original and success_count > 0:
        print("\nNote: Original folders still exist in source directory.")
        print("Verify the ePubs work, then run with --remove-original to clean up.")

if __name__ == '__main__':
    exit(main() or 0)
