# undump_io

A small script to take dump_io generated log entries and rebuild requests.

```
$ python undump_io.py /some/logfile --output output_file
Total of 4859 requests rebuilt.
$
```

## What

This small script aims to take the various log file entries created by dump_io and build them into the
requests. It allows for filtering and saving into files.

## How

1. Enable mod_dumpio on your Apache web server. (You're on your own with this!)
2. Capture some requests.
3. Rebuild the requests

## Options

To save the output to a file, use --output.
By default the requests will be streamed to stdout, use --no-list to prevent this.
To filter requests, use --filter "STRING". Normally the matched entries are printed to stdout, but using
  --filter-file you can specify a filename to save the requests into.

## Examples

```
$ python undump_io.py /some/logfile --no-list
```

This will simply recreate the requests and tell you how many were rebuilt.

```
$ python undump_io.py /some/logfile --filter "Hello World" --filter-file "hello.txt" --no-list
Total of 4859 requests rebuilt.

Filtering requests for 'Hello World'

Total of 10 matches for filter 'Hello World'
```

This processes the file, then saves any requests that contain 'Hello World' into hello.txt.

## Future

This was written to simplify some debugging and investigation, so may not get much more love. It was also
written with only input IO being captured, so if output IO is also captured it may not work. That said,
I'll happily look at suggestions and pull requests are welcome.