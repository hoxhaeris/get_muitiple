import asyncio
import concurrent.futures
from asyncio import Future
from typing import Tuple, Set, Generator
import aiohttp


class FetchMultiple:
    data_input: dict

    def __init__(self,
                 data_input: dict,
                 ):
        self.data_input = data_input

    @staticmethod
    async def fetch_page(url: str, session: aiohttp.client.ClientSession) -> str:
        """fetch the remote data, using the same session. Returns a string"""
        async with session.get(url) as res:
            return await res.text()

    async def dispatch(self) -> Tuple[Set[Future], Set[Future]]:
        """returns the asyncio task-list"""
        task_list = []
        async with aiohttp.ClientSession() as session:
            for task_name, details in self.data_input.items():
                task_list.append(asyncio.create_task(self.fetch_page(url=details["url"], session=session),
                                                     name=task_name))
            return await asyncio.wait(task_list)

    def get(self) -> Set[asyncio.Task]:
        """returns finished asyncio tasks"""
        finished, _ = asyncio.get_event_loop().run_until_complete(self.dispatch())
        return finished

    def get_mapped_result_generator(self) -> Generator:
        """returns a Generator key:value object. Key: task name, value: returned object"""
        for finished_task in self.get():
            yield {finished_task.get_name(): finished_task.result()}

    def get_key_value_result(self) -> dict:
        """returns the key:value result (dictionary), key: task name, value: returned object"""
        data_dict = {}
        for finished_task in self.get():
            data_dict.setdefault(finished_task.get_name())
            data_dict[finished_task.get_name()] = finished_task.result()
        return data_dict

    def get_and_process_data_key_value(self) -> dict:
        """In the input data, you can specify a function to processes the fetched data. The return is a key:value
        dictionary (key: task name, specified in the data_input dictionary, value: what is returned by the process
        function) """
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures_dict = {}
            result_dict = {}
            data = self.get()
            for finished_task in data:
                futures_dict.setdefault(finished_task.get_name())
                result_dict.setdefault(finished_task.get_name())
                futures_dict[finished_task.get_name()] = executor.submit(
                    self.data_input[finished_task.get_name()]['function'], finished_task.result())
            for task_name, future in futures_dict.items():
                result_dict[task_name] = future.result()
            return result_dict

    def get_and_only_process_data(self) -> None:
        """Process the fetched data, without returning anything (if you want to store this data to a file,
        database, or similar action). This expects I/O function types and is using ThreadPoolExecutor"""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            [futures.append(
                executor.submit(self.data_input[finished_task.get_name()]['function'], finished_task.result())) for
             finished_task in self.get()]
            [future.result() for future in futures]
