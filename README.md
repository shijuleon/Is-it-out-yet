Checks if a particular torrent is out from kat.cr.

Uses kat-console for scraping.
Bash script is a wrapper for *nix. Can be used with a cronjob.

katf.py is standlone checker, can be used with a scheduler in Windows.

```python
$ ./katf.py -s 'silicon valley'
Is it out yet? v0.1
* Sending request to: https://kat.cr/usearch/silicon%20valley/ with headers Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36 at 2016-05-29 11:53:03
* Getting latest silicon valley S03E05 torrents
[snip]
Update latest episode details? (y/n): y
Enter latest episode details: S03E06
Done
```