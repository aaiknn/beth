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

## Investigate
More in-depth investigation.
Alias: `-I`

Note: This feature needs a urlscan.io API key in order to work.

`investigate --scan <URL>` retrieves information on the target webpage from urlscan.io.
Example: `beth investigate --scan http://www.catb.org/~esr/faqs/smart-questions.html`
