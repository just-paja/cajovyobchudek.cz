from django.conf import settings
from django.contrib.staticfiles.finders import FileSystemFinder


class CssFinder(FileSystemFinder):
    def find(self, path, all=False):  # pylint:disable=redefined-builtin
        # Assume the file already exists given we are running on AWS
        if settings.AWS_ACCESS_KEY_ID and (path.endswith('.css') or path.endswith('.css.map')):
            return path
        return None

    def list(self, ignore_patterns):
        return []
