# sci_scraping
trying to scraping data from [web of science](http://login.webofknowledge.com/error/Error?PathInfo=%2F&Alias=WOK5&Domain=.webofknowledge.com&Src=IP&RouterURL=http%3A%2F%2Fwww.webofknowledge.com%2F&Error=IPError)


In process...


**Target**: 

extracting all papers details *(title,authors, abstract, publication year,corresponding author and corresponding address)*, given journal names and a certain year period *(that is journal name, start year and end year)*

**Workflow**:
* First step: Collecting the link url of every paper, given a specific query/key words(*that is journal name, start year and end year*)
* Second step: Collecting the detailed data of each paper via looping through all the link urls derived in the first step

**Status**
* code for the second step is verified ok

**Todo**
* For query results with multiple pages, how to get the url links for page 2, 3, ...
