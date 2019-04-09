import logging
import requests
import os

import cfscrape
import internetarchive
import tubeup.TubeUp as tubeup
import internetarchive.config as iaconfig

from urllib.parse import quote_plus

from bears.general.MementoFetchBear import MementoFetchBear

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from dependency_management.requirements.PipRequirement import PipRequirement


def known_archive_method(archiver):
    archiver = str(archiver).lower()
    if archiver in LinkBackupBear.ARCHIVER_SAVE_URL_METHODS:
        return archiver
    else:
        msg = 'Invalid archive method option: %s' % archiver
        logging.error(msg)
        raise ValueError(msg)


def submit_to_archive_org(url):
    """
    Submit an url to archive.org to be archived.

    :param url: Url that will be submitted.
    :return:    Boolean, True means link successfully submitted to
                archive.org
    """
    try:
        resp = requests.head('https://web.archive.org/save/%s' % url)
    except requests.exceptions.RequestException as er:
        logging.error(er)
        return False
    else:
        if resp.status_code == 200:
            return True
        logging.error('web.archive.org responds with code %s while '
                      'submitting %s'
                      % (resp.status_code, url))
        return False


def submit_to_archive_is(url, scraper):
    """
    Submit an url to archive.is to be archived.

    :param url:      Url that will be submitted.
    :param scraper:  A `cfscrape.CloudflareScraper` instance.
    :return:         Boolean, True means link successfully submitted to
                     archive.is
    """
    try:
        # We use cfscrape post to overcome the CloudFlare IUAM challange
        # in archive.is
        resp = scraper.post('https://archive.is/submit/', data={'url': url})
    except requests.exceptions.RequestException as er:
        logging.error(er)
        return False
    else:
        if resp.status_code == 200:
            return True
        logging.error('archive.is responds with code %s while '
                      'submitting %s'
                      % (resp.status_code, url))
        return False


def submit_youtube_to_archive_org(url, tu):
    """
    Download video from a YouTube url and upload it to archive.org.

    :param url:      Url that will be submitted.
    :param tu:       A `tubeup.TubeUp` instance
    :return:         Boolean, True means link successfully downloaded
                     and uploaded to archive.org
    """
    logging.info('Archiving %s with tubeup.' % url)
    try:
        for identifier, meta in tu.archive_urls([url]):
            logging.info('Upload URL: https://archive.org/details/%s' %
                         identifier)
        return True
    except Exception as er:
        logging.error(er)
        return False


def check_is_content_already_in_archiveorg(url):
    """
    Check whether there's any file uploaded to archive.org that related
    to the url

    :param url: URL to be checked.
    :return:    Boolean, True means there's one or more file in archive.org
                that's related to the url.
    """
    try:
        query_str = quote_plus('originalurl:"%s"' % url)
        resp = requests.get(
            'https://archive.org/advancedsearch.php?q=%s'
            '&rows=50&page=1&output=json' % query_str)

        if resp.json()['response']['numFound'] > 0:
            logging.info('%s had already uploaded in archive.org' % url)
            return True

        logging.info('%s not found in archive.org' % url)
        return False

    except (requests.exceptions.RequestException, KeyError) as er:
        logging.error(er)
        raise er


class LinkBackupBear(LocalBear):
    LANGUAGES = {'All'}
    REQUIREMENTS = {PipRequirement('requests', '2.12'),
                    PipRequirement('cfscrape', '1.9.0'),
                    PipRequirement('internetarchive', '1.7.2'),
                    PipRequirement('tubeup', '0.0.12'),
                    PipRequirement('mock', '2.0.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Documentation'}
    BEAR_DEPS = {MementoFetchBear}
    ARCHIVER_SAVE_URL_METHODS = {
        'archive.org': submit_to_archive_org,
        'archive.is': submit_to_archive_is,
        'youtube_to_archive.org': submit_youtube_to_archive_org
    }

    def run(self, filename, file, dependency_results=dict(),
            archiver: known_archive_method = 'archive.org',
            archiveorg_email: str = None,
            archiveorg_password: str = None):
        """
        Find unarchived links and submit them to an internet archive service.

        Link is considered valid if the link has been archived by any services
        in memento_client.

        This bear can automatically fix redirects.

        Warning: This bear will make HEAD requests to all URLs mentioned in
        your codebase, which can potentially be destructive. As an example,
        this bear would naively just visit the URL from a line that goes like
        `do_not_ever_open = 'https://api.acme.inc/delete-all-data'` wiping out
        all your data.

        :param dependency_results:
            Results given by URLBear.
        :param archiver:
            Archiving method to archive the url,
            default to "archive.org", available option:
            {"archive.org", "archive.is", "youtube_to_archive.org"}.
        :param archiveorg_email:
            Email of an archive.org account, just used when using
            `youtube_to_archive.org` archiving method. Can also be defined
            with `ARCHIVEORG_EMAIL` environment variable.
        :param archiveorg_password:
            Password of the archive.org account, just used when using
            `youtube_to_archive.org` archiving method. Can also be defined
            with `ARCHIVEORG_PASSWORD` environment variable.
        """
        # Parse the existing internetarchive configuration file (if any).
        parsed_ia_s3_config = iaconfig.parse_config_file()[1]['s3']
        s3_access_key = parsed_ia_s3_config['access']
        s3_secret_key = parsed_ia_s3_config['secret']

        if archiver == 'youtube_to_archive.org':
            # Configure the internetarchive library email and password.
            if archiveorg_email and archiveorg_password:
                internetarchive.configure(archiveorg_email,
                                          archiveorg_password)
            elif (os.environ.get('ARCHIVEORG_EMAIL') and
                    os.environ.get('ARCHIVEORG_PASSWORD')):
                internetarchive.configure(os.environ['ARCHIVEORG_EMAIL'],
                                          os.environ['ARCHIVEORG_PASSWORD'])
            elif s3_access_key and s3_secret_key:
                # If the `internetarchive` library has been configured before,
                # we just use the existing configuration from ia.
                logging.info('Using internetarchive configuration file')
            else:
                msg = (
                    'youtube_to_archive.org archiving method needs email and '
                    'password of an archive.org account to operate, '
                    'which can be set from `archiveorg_email` and '
                    '`archiveorg_password` settings, or by setting '
                    '`ARCHIVEORG_EMAIL` and `ARCHIVEORG_PASSWORD` in the '
                    'system environment variable.')
                logging.error(msg)
                raise Exception(msg)

        if archiver == 'archive.is':
            # We're using `cfscrape` to perform HTTP request to archive.is
            # to avoid CloudFlare IUA challange.
            self._scraper = cfscrape.create_scraper()

        if archiver == 'youtube_to_archive.org':
            self._tu = tubeup.TubeUp()

        for result in dependency_results.get(MementoFetchBear.name, []):
            if ((archiver == 'youtube_to_archive.org' and
                 check_is_content_already_in_archiveorg(result.link)) or
                    (archiver != 'youtube_to_archive.org' and
                        result.contents)):
                # For `youtube_to_archive.org` archiving method, we
                # don't use mementos to check whether the data has been
                # archived or not, since memento can't see YouTube links
                # that have been archived using `tubeup`, therefore
                # we use `check_is_content_already_in_archiveorg()`.
                #
                # If the YouTube link had been archived by someone else
                # to archive.org, we don't archive it because `tubeup`,
                # will just work with YouTube videos that's never uploaded
                # to archive.org.
                continue

            unarchived_url = result.link

            if archiver == 'archive.is':
                status = self.ARCHIVER_SAVE_URL_METHODS[archiver](
                    unarchived_url, self._scraper)
            elif archiver == 'youtube_to_archive.org':
                status = self.ARCHIVER_SAVE_URL_METHODS[archiver](
                    unarchived_url, self._tu)
            else:
                status = self.ARCHIVER_SAVE_URL_METHODS[archiver](
                    unarchived_url)

            if status:
                logging.info('This link (%s) successfully submitted with %s '
                             'method' % (unarchived_url, archiver))
            else:
                yield Result(
                    self,
                    'Failed to submit %s with %s method' % (
                        unarchived_url, archiver),
                    affected_code=result.affected_code,
                    severity=RESULT_SEVERITY.INFO
                    )
