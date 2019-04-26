# pydns
_A fully python 3 implementation of a DNS server_


## Notes
+ At the moment the only records supported are IPV4 A records (however the main codebase is there to support others)
+ TTL will be set to 0 as not to corrupt cache with bad records, in the future this can be changed

## Hosts
You can setup hosts in a `hosts.txt` file in the format

`DOMAIN IP`

_Example_
```
test.com 127.0.0.1
google.com 216.58.212.110
```

## Run
**Must** use python 3
```bash
python main.py
```
```
usage: main.py [-h] [-f HOSTS] [-a ADDRESS] [-p PORT] [-d]

A python DNS server

optional arguments:
  -h, --help            show this help message and exit
  -f HOSTS, --hosts HOSTS
                        The file to load hosts from
  -a ADDRESS, --address ADDRESS
                        Address to bind
  -p PORT, --port PORT  Port to bind
  -d, --debug           Print debug messages
```

## Testing _(Windows)_

1. Open `nslookup`
2. Enter `SET debug`
3. Optional enter `SET TYPE=ALL`
4. Enter `server 127.0.0.1` or whatever IP you bound to (must be using port 53)
5. Query a domain name you have in your `hosts.txt` configuration

## License
[MIT license](LICENSE)
