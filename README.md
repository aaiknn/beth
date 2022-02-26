# BETH!
A tool that supports people busting some bottoms.

## Lookup
DNS data related lookup stuff.
Alias: `-L`

### DNS
`lookup --dns <DOMAINNAME>` retrieves DNS records for the name from your DNS server.

Example: `beth lookup --dns dontasktoask.com`

### Reverse IP
Note: This feature needs a SecurityTrails API key in order to work.

`lookup --reverse <IP>`

Example: `beth lookup --reverse 135.181.208.158`

## Query
Ask around the internet for advice.
Alias: `-Q`

### Urlscan
Note: This feature needs a urlscan.io API key in order to work.

`query --urlscan <QUERY_STRING> [RESULTS_AMOUNT]` finds entries on Urlscan.

For information on query string formatting, see [Urlscan Search API Docs](https://urlscan.io/docs/search/).

Example: `beth query --urlscan page.domain:dontasktoask.com`

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
Note: This feature needs a urlscan.io API key in order to work.

`investigate --scan <URL>` retrieves information on the target webpage from urlscan.io.

Example: `beth investigate --scan http://www.catb.org/~esr/faqs/smart-questions.html`
