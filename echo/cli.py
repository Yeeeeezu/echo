import click
from pathlib import Path
from rich.console import Console
from .finder import find

console = Console()


@click.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--delete", is_flag=True, help="delete duplicates, keeping the first copy")
@click.option("--dry-run", is_flag=True, help="show what would be deleted")
@click.option("--min-size", default=1, metavar="BYTES", show_default=True,
              help="ignore files smaller than this")
def main(paths: tuple[Path, ...], delete: bool, dry_run: bool, min_size: int) -> None:
    """find (and optionally remove) duplicate files by content hash."""
    dupes = find(list(paths), min_size=min_size)

    if not dupes:
        console.print("[green]no duplicates found[/green]")
        return

    wasted = 0
    for i, (digest, files) in enumerate(dupes.items(), 1):
        size = files[0].stat().st_size
        wasted += size * (len(files) - 1)

        console.print(f"\n[bold]group {i}[/bold]  [dim]{digest[:16]}…  {size:,} B[/dim]")
        for j, f in enumerate(files):
            tag = "[green]keep[/green]" if j == 0 else "[red]dupe[/red]"
            console.print(f"  {tag}  {f}")
            if j > 0:
                if dry_run:
                    console.print(f"       [dim]→ would delete[/dim]")
                elif delete:
                    f.unlink()
                    console.print(f"       [red]deleted[/red]")

    mb = wasted / 1_048_576
    console.print(f"\n[dim]{len(dupes)} group(s) · {mb:.2f} MB wasted[/dim]")
