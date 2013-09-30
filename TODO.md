Ideas:

Allow user to create 'parsers' regexes that crawl over any result set, 
optionally can be limited to type (exportable?). These 'parsers' should
be able to promote user defined IOCs that can then be automatically searched
by other plugins (splunk, sumo, etc)

Allow user to create 'whitelist' of uninterested or known sigs that can be 
avoided in order to not waste processing time

Allow user to create 'workflows'. These workflows should allow the user to 
specify the whole data collection chain. Including the extraction of IOCs
and retrieval of impact results.
