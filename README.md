# BETH!
A tool that supports people busting some bottoms.

## Check Module
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

## Lookup Module
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

#### Options
```sh
-F      Instead of using one domain name from the command-line, read input from
        a file of domain names that are separated by new lines.
```

Example:

```sh
beth lookup --dns myfilename.txt -F
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

```sh
lookup --rwhois <SEARCH_TERM>
```

Default is querying current records.

Search terms are case insensitive.

Results output is capped after a default max amount of 50 entries. You can choose to either remove the cap or override the default value in your .env file.

Example:

```sh
beth lookup --rwhois test@test.com
```

#### Options
```sh
-H                Historic search
--after, -A       Query for records created after a given date
--before, -B      Query for records created before a given date
--between, -X     Query for records created between two given dates
--mode, -M        'preview' to retrieve only the amount of results. Will not consume
                    any Domain Research Suite (DRS) credits.
                  'default' to retrieve result entries. Consumes 1 DRS credit.
```

Examples:

```sh
beth lookup --rwhois test@test.com -H
beth lookup --rwhois Google --after 2022-03-20
beth lookup --rwhois Google --before 1990-01-01
beth lookup --rwhois Google -X 2022-01-01 2022-01-01
beth lookup --rwhois 'A very unique term that probably hardly finds any results whatsoever' -M 'preview'
```

#### Search Operators
Searches can be combined into bulk using AND.
Terms can be excluded from results using NOT.

Example:
```sh
beth lookup --rwhois "things AND stuff AND everything NOT desperation NOT exhaustion"
```

Note: Chaining terms with AND does not retrieve entries that match all of the terms. Instead, it retrieves a bulk of all entries that each match at least one of the terms.

WhoisXMLAPI accepts a maximum amount of 4 entries for each included and excluded search terms. Therefore, additional terms will be dropped from searches and thus from results.

## Query Module
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

## Investigate Module
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

#### Tags
You can choose to add one or more tags to your scan. These can be set in your .env file in the following format:

```txt
["tag1", "tag2", "tag3"]
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

## Test Module: HTTP Utilities
Some stuff about checking out the HTTP plumbing.

Alias: `-T`

### Up
Is a domain up?

```sh
test --up <URL>
```

Example:

```sh
beth test --up dontasktoask.com
```

#### Options
```sh
-F      Instead of using one domain name from the command-line, read input from
        a file of domain names that are separated by new lines.
```

Example:

```sh
beth test --up myfilename.txt -F
```

### Status
What's the response status from a request to a domain?

```sh
test --status <URL>
```

Example:

```sh
beth test --status dontasktoask.com
```

#### Options
```sh
-F      Instead of using one domain name from the command-line, read input from
        a file of domain names that are separated by new lines.
```

Example:

```sh
beth test --status myfilename.txt -F
```
