import os
import shutil
import uuid

from origami import constants, exceptions, utils


class OrigamiCache(object):
    """ Implements pipeline functions for Origami
    Handles various pipeline functions such as fetching and saving data from
    and to cache.

    This essentially is not cache since all the storage is done on the disk,
    and since IO are resource expensive this does not essentially increases speed
    in any sense. The main use of this here is for persistence, this can be also for large
    amount of data wherein it is not possible to store all of it in the memory.

    .. code-block:: python
        from origami import OrigamiCache

        cache = OrigamiCache()
        arr = ["Hello, ", "World!"]
        cache.save_text_array_to_cache(arr)
        arr = ''.join(arr)
        new_arr = cache.load_text_array_from_cache()
        print(new_arr)

    Attributes:
        global_cache_path: Path for all the file interaction for pipeline functions
        cache_id: ID for the current cache object
        cache_dir: Cache dir corresponding to global_cache_path and cache_id
    """

    def __init__(self, cache_path=constants.GLOBAL_CACHE_PATH):
        self.global_cache_path = utils.validate_cache_path(cache_path)
        self.cache_id = ""
        self.cache_dir = ""
        self.__create_cache()

    def __create_cache(self):
        """
        Create a cache space in global_cache_path and return the ID/directory to that.

        Returns:
            cache_id: Cache ID to reference the cache in future.

        Raises:
            FileHandlingException: Exception during creating directory for the cache.
        """
        self.cache_id = uuid.uuid4()
        self.cache_dir = os.path.join(self.global_cache_path, self.cache_id)
        try:
            if not os.path.exists(self.cache_dir):
                os.makedirs(self.cache_dir)
        except OSError:
            self.cache_dir = ""
            raise exceptions.FileHandlingException(
                "Error when creating directory for cache :: {}.".format(
                    self.cache_dir))

        return self.cache_id

    def delete_current_cache(self):
        """
        Delete the cache identifiers, cache_id and cache_dir
        """
        try:
            if self.cache_dir:
                shutil.rmtree(self.cache_dir)
                self.cache_dir = ""
            self.cache_id = ""
        except:
            pass

    def new_cache(self):
        """
        Create a cache space in global_cache_path and return the ID/directory to that.

        Returns:
            cache_id: Cache ID to reference the cache in future.
        """
        self.delete_current_cache()
        cache_id = self.__create_cache()
        return cache_id

    def save_text_array_to_cache(self, text_array):
        """
        Takes an array of string and saves it to cache file on the disk.

        Args:
            text_array: array of strings to be saved in the text file cache.
        """
        utils.strict_check_array_of_string(text_array)
        text_cache_path = os.path.join(self.cache_dir,
                                       constants.TEXT_CACHE_FILE)

        with open(text_cache_path, "w") as file:
            # Write it to the cache file as an array of string.
            text_array = ['"{}"'.format(x) for x in text_array]
            file.write('[' + ', '.join(text_array) + ']')

    def load_text_array_from_cache(self):
        """
        Load the text array from the cache file and return it.

        Returns:
            eval_ds: Evaluated data structure from the text cache file, in this
                case it corresponds to the text array.

        Raises:
            MalformedCacheException: Exception during parsing the data strcutre from
                text cache file.

            InvalidCachePathException: The path for cache we obtained is not present
                or there is nothing to load fro the cache path.
        """
        text_cache_path = os.path.join(self.cache_dir,
                                       constants.TEXT_CACHE_FILE)

        if os.path.exists(text_cache_path):
            with open(text_cache_path, "r") as cache_file:
                content = cache_file.read()
                try:
                    eval_ds = ast.literal_eval(content.strip())
                    return eval_ds
                except ValueError:
                    raise exceptions.MalformedCacheException(
                        "Text cache does not contain a valid string to be evaluated"
                    )
        else:
            raise exceptions.InvalidCachePathException(
                "No valid cache file found :: {}".format(text_cache_path))

    def cache_image_file_array(self, image_inputs):
        """
        Save an array of image to the global origami cache. The provided image inputs
        should be a list/tuple of images.

        Args:
            image_inputs: list/tuple of images to be saved.

        """
        if not isinstance(image_inputs, (list, tuple)):
            raise exceptions.MismatchTypeException(
                "send_text_array can only accept an array or a tuple")
        pass
