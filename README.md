# Get Multiple
Fetch multipe web resources using asyncio.

This class (FetchMultiple) is using asyncio (aiohttp lib) to fetch multiple resources from web. 
You can define a processing function for each resource, and get a key-value return (using multithreading for processing).
The result can be obtained processed, unprocessed (raw response), or mapped (key:value).

Example usage:

    >>> from get_multiple import FetchMultiple
    >>> import lxml.html
    >>>
    >>>
    >>> def process_page(input_data):
    ...     tree = lxml.html.fromstring(input_data)
    ...     return tree.find('.//title').text
    ...
    >>> def another_processing_function(input_data):
    ...     return "I just return a string"
    ...
    >>>
    >>>
    >>> fetch_objects = {
    ...     "google_task": {
    ...         "url": "https://google.com",
    ...         "function": process_page,
    ...     },
    ...     "yahoo_task": {
    ...         "url": "https://yahoo.com",
    ...         "function": another_processing_function,
    ...     },
    ...     "stackoverflow_task": {
    ...         "url": "https://stackoverflow.com/",
    ...         "function": process_page,
    ...     },
    ...     "some_other_task": {
    ...         "url": "https://jsonplaceholder.typicode.com/todos/1",
    ...     }
    ... }
    >>>
    >>>
    >>> fetch_data = FetchMultiple(data_input=fetch_objects)
    >>>
    >>> fetch_data.get_and_process_data_key_value()
    some_other_task': '{\n  "userId": 1,\n  "id": 1,\n  "title": "delectus aut autem",\n  "completed": false\n}', 'yahoo_task': 'I just return a string', 'stackoverflow_task': 'Stack Overflow - Where Developers Learn, Share, & Build Careers', 'google_task': 'Google'}
    >>>

Result:

    {
        "stackoverflow_task": "Stack Overflow - Where Developers Learn, Share, & Build Careers",
        "some_other_task": "{\n  \"userId\": 1,\n  \"id\": 1,\n  \"title\": \"delectus aut autem\",\n  \"completed\": false\n}",
        "google_task": "Google",
        "yahoo_task": "I just return a string"
    }

The fetch_object is a dictionary of dictionares. 
The key is the task name, that contains this keys:
- url : the URL
- function: the processing function for the fetched data (optional)
- headers (optional)

Input example:

    fetch_objects = {
        "google_task": {
            "url": "https://google.com",
            "function": process_page,
        },
        "yahoo_task": {
            "url": "https://yahoo.com",
            "function": another_processing_function,
        },
        "stackoverflow_task": {
            "url": "https://stackoverflow.com/",
            "function": process_page,
        },
        "nomad_task": {
            "url": "https://nomad.testing/v1/job/some_job/allocations/url_does_not_exist",
            "headers": {"X-Nomad-Token": "45648-fake-token-5457869-57997"}
        },
        "github_task": {
            "url": "https://api.github.com/users/octocat/orgs",
            "function": parse_json,
            "headers": {"Authorization": f'token OAUTH-TOKEN'}
        }
    }

If no function is defined, the unprocessed data is returned. If no headers are provided, no headers are used for that connection
