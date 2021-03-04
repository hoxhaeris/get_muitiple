import lxml.html
import json

from get_multiple import FetchMultiple


def process_page(input_data):
    tree = lxml.html.fromstring(input_data)
    return tree.find('.//title').text


def another_processing_function(input_data):
    return "I just return a string"


def parse_json(json_data):
    try:
        return json.loads(str(json_data))
    except json.decoder.JSONDecodeError:
        return None


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

fetch_data = FetchMultiple(data_input=fetch_objects, enable_ssl=False)

"""this method returns the key:value processed data"""
print(json.dumps(fetch_data.get_and_process_data_key_value(), indent=4))
"""
Returned data:
{
    "stackoverflow_task": "Stack Overflow - Where Developers Learn, Share, & Build Careers",
    "nomad_task": null,
    "google_task": "Google",
    "github_task": {
        "message": "Bad credentials",
        "documentation_url": "https://docs.github.com/rest"
    },
    "yahoo_task": "I just return a string"
}
"""

"""the get() method returns the finished asyncio tasks. Each task is named, to have a key:value mapping with the 
input. You can process this data according to your needs then"""
data = (fetch_data.get())
for resource in data:
    print(resource.get_name())  # the name of the task
    print(resource.result())  # the result of the task(data fetched)

"""the get_and_only_process_data method will not return any value. This method will run a function defined in the 
input dictionary. This is designed for I/O bound tasks, like writing the output in a file, or database. If no 
processing function is defined in the input, that task will be skipped """
process_only_data = fetch_data.get_and_only_process_data()

"""the get_key_value_result method will return a key:value result, with key being the task name defined in the input, 
and the value is the unprocessed data returned from the http call """
key_value_result = fetch_data.get_key_value_result()

"""the get_mapped_result_generator method will return a generator, with key:value; the key is the task name, 
the value is the unprocessed data returned from the http call """
key_value_generator = fetch_data.get_mapped_result_generator()
