SITE_NAME = 'Čaje z celého světa'


def get_page_title(page_title=None):
    if not page_title:
        return SITE_NAME
    return '%s - %s' % (page_title, SITE_NAME)
