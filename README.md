# echo

find (and remove) duplicate files by content hash.

```
echo ./photos ./downloads
```
```
  group 1  a3f8b2c1d4e5…  2.4 MB each
    keep  ./photos/IMG_1234.jpg
    dupe  ./downloads/IMG_1234.jpg

  group 2  9c7d3a1e8b2f…  14 KB each
    keep  ./photos/receipt.pdf
    dupe  ./photos/backup/receipt.pdf

  2 group(s) · 2.41 MB wasted
```

## usage

```
echo <paths...> [flags]

  --delete      delete duplicates, keeping the first copy found
  --dry-run     show what would be deleted without deleting anything
  --min-size    ignore files smaller than N bytes (default: 1)
```

## examples

```
echo .                              # find dupes in current dir
echo ~/Downloads ~/Documents        # search across directories
echo . --dry-run                    # preview what would be removed
echo . --delete                     # actually remove dupes
echo . --min-size 1048576           # only check files >= 1 MB
```

## install

```
pip install -e .
```

Python 3.11+.
