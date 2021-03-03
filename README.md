# Get Multiple
Fetch multipe web resources using asyncio.

This class is using asyncio (aiohttp lib) to fetch multiple resources from web. 
You can define a processing function for each resource, and get a key-value return (using multithreading for processing).

Example usage:

    >>> from get_multiple import FetchMultiple
    >>> import lxml.html
    >>> def process_page(html):
    ...     tree = lxml.html.fromstring(html)
    ...     return tree.find('.//title').text
    ...
    >>> fetch_objects = {
    ...     "google_task": {
    ...         "url": "https://google.com",
    ...         "function": process_page,
    ...     },
    ...     "yahoo_task": {
    ...         "url": "https://yahoo.com",
    ...         "function": process_page,
    ...     },
    ...     "stackoverflow_task": {
    ...         "url": "https://stackoverflow.com/",
    ...         "function": process_page,
    ...     }
    ... }
    >>>
    >>> fetch_data = FetchMultiple(data_input=fetch_objects)
    >>> fetch_data.get_and_process_data_key_value()
    {'google_task': 'Google', 'yahoo_task': 'Yahoo', 'stackoverflow_task': 'Stack Overflow - Where Developers Learn, Share, & Build Careers'}

The fetch_object is a dictionary of dictionares. 
The key is the task name, that contains this keys:
- url : the URL
- function: the processing function for the fetched data
