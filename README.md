# BETH!
A tool that supports people busting some bottoms.

## Check
Verify things.

Alias: `-C`

### Email
Finds a verdict on the legitimacy of a given email address, and provides details about on what grounds the verdict is decided.

```sh
check --email <EMAIL_ADDRESS>
```

Example:

```sh
beth check --email test@test.com
```

## Lookup
DNS data related lookup stuff.

Alias: `-L`

### DNS
Retrieves DNS records for the name from your DNS server.

```sh
lookup --dns <DOMAINNAME>
```

Example:

```sh
beth lookup --dns dontasktoask.com
```

### Reverse IP
Note: This feature needs a SecurityTrails API key in order to work.

Note: Result output is currently capped after listing a max amount of 20 entries. While that isn't a great solution, it saves your terminal from certain spam for the time being. Reverse IP output is soon going to be more detailed, and options are going to be added to the command.

```sh
lookup --reverse <IP>
```

Example:

```sh
beth lookup --reverse 8.8.8.8
```

### Whois
Retrieves Whois entries for a given domain.

Note: This feature needs a WhoisXMLAPI API key in order to work.

```sh
lookup --whois <DOMAIN_NAME>
```

Example:

```sh
beth lookup --whois test.com
```

### Reverse Whois
Retrieves current and historic domain name entries for a given target.

Note: This feature needs a WhoisXMLAPI API key in order to work.

Note: Result output is currently capped after listing a max amount of 50 entries. While that isn't a great solution, it saves your terminal from certain spam for the time being. There's going to be a more suitable solution in the near future where you can pick your own cap amount or choose to not cap it at all, similar to Urlscan querying. Promise.

```sh
lookup --rwhois <SEARCH_STRING> | <ARRAY_OF_SEARCH_STRINGS>
```

Default is querying current records.

Example:

```sh
beth lookup --rwhois test@test.com
```

#### Options
```sh
-H      Historic search
```

Example:

```sh
beth lookup --rwhois test@test.com -H
```

## Query
Ask around the internet for advice.
Alias: `-Q`

### Urlscan
Finds scan result entries on Urlscan.
Note: This feature needs a urlscan.io API key in order to work.

```sh
query --urlscan <QUERY_STRING> [RESULTS_AMOUNT]
```

For information on query string formatting, see [Urlscan Search API Docs](https://urlscan.io/docs/search/).

Example:

```sh
beth query --urlscan page.domain:dontasktoask.com
```

Note: A default value of the amount of results that are retrieved can be set in your .env file.

#### Options
```sh
-R      Repeatedly run the specified query without ever stopping.
```

Note: The amount of seconds that pass before the next query is sent can be set in your .env file.

## Investigate
More in-depth investigation.
Alias: `-I`

### Scan
Retrieves information on the target webpage from urlscan.io.

Note: This feature needs a urlscan.io API key in order to work.

```sh
investigate --scan <URL>
```

Example:

```sh
beth investigate --scan http://www.catb.org/~esr/faqs/smart-questions.html
```

### Shodan
Retrieves information on the target IP from Shodan.

```sh
investigate --shodan <IP>
```

Example:

```sh
beth investigate --shodan 4.4.4.4
```

## HTTP Utilities
### Test: Is a domain up?

```sh
test --up <URL>
```

Example:

```sh
beth test --up dontasktoask.com
```

#### Options
```sh
-F      Instead of using one domain name from the command-line, read input from a file of domain names
        that are separated by new lines.
```

Example:

```sh
beth test --up myfilename.txt -F
```

### Test: What's the response status from a request to a domain?

```sh
test --status <URL>
```

#### Options
```sh
-F      Instead of using one domain name from the command-line, read input from a file of domain names
        that are separated by new lines.
```

Example:

```sh
beth test --status dontasktoask.com
```

Example:

```sh
beth test --status myfilename.txt -F
```
