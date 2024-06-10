from __future__ import print_function
from cement.core import controller
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from datetime import datetime
from dscan.common.exceptions import CannotResumeException
from dscan.common.functions import template
from dscan.common import template
from dscan import common
from dscan.plugins.internal.base_plugin import BasePlugin
from dscan.plugins.internal.base_plugin_internal import BasePluginInternal
import dscan
import dscan.common.functions as f
import dscan.common.plugins_util as pu
import dscan.common.versions as v
import gc

class Scan(BasePlugin):
    class Meta:
        label = 'scan'
        description = 'cms scanning functionality.'
        stacked_on = 'base'
        stacked_type = 'nested'

        epilog = "\n"

        argument_formatter = common.SmartFormatter
        epilog = template("help_epilog.mustache")

    def default(self):
        url = input("Enter URL: ")
        url_file = None
        enumerate = "a"
        method = "a"
        verb = input("Enter HTTP verb (head/get/post/put/delete/patch/options): ")
        number = 1000
        plugins_base_url = None
        themes_base_url = None
        timeout = 45
        timeout_host = 1800
        follow_redirects = "y"
        host = None
        user_agent = BasePluginInternal.DEFAULT_UA
        massscan_override = "y"
        threads = 4
        threads_identify = None
        threads_scan = None
        threads_enumerate = None
        output = input("Enter output format (standard/json/xml/csv/html): ")
        hide_progressbar = "y"
        debug_requests = "n"
        error_log = None
        resume = "n"

        opts = {
            'url': url,
            'url_file': None,
            'enumerate': enumerate,
            'method': method,
            'verb': verb,
            'number': number,
            'plugins_base_url': None,
            'themes_base_url': None,
            'timeout': int(timeout),
            'timeout_host': int(timeout_host),
            'follow_redirects': follow_redirects.lower(),
            'host': host,
            'user_agent': user_agent,
            'massscan_override': massscan_override.lower(),
            'threads': int(threads) if threads else 4,
            'threads_identify': int(threads_identify) if threads_identify else None,
            'threads_scan': int(threads_scan) if threads_scan else None,
            'threads_enumerate': int(threads_enumerate) if threads_enumerate else None,
            'output': output,
            'headers': None,
            'hide_progressbar': hide_progressbar.lower(),
            'debug_requests': debug_requests.lower(),
            'error_log': "error_log.log",
            'resume': resume.lower()
        }

        self._general_init(opts)
        follow_redirects = opts['follow_redirects']
        opts['follow_redirects'] = False

        if url_file:
            self.out.debug('scan.default -> url_file')
            self._process_scan_url_file(opts, follow_redirects)
        else:
            plugins = pu.plugins_base_get()
            instances = self._instances_get(opts, plugins, False, self.out)
            self.out.debug('scan.default -> url')

            if not url:
                self.out.fatal("--url parameter is blank.")
                return

            cms_name, scan_out = self._process_cms_identify(url, opts, instances, follow_redirects)
            if not cms_name:
                no_cms = "'%s' not identified as a supported CMS. If you disagree, please specify a CMS manually." % url
                self.out.fatal(no_cms)
            else:
                self.out.echo("[+] Site identified as %s." % cms_name)
            url, host_header = scan_out
            inst_dict = instances[cms_name]
            inst = inst_dict['inst']
            opts['url'] = url
            opts['headers'] = self._generate_headers(host_header)
            inst.process_url(opts, **inst_dict['kwargs'])

        self.out.close()

    def _process_scan_url_file(self, opts, follow_redirects):
        self.out.debug('scan._process_scan_url_file')
        file_location = opts['url_file']

        with open(file_location) as url_file:
            self.check_file_empty(file_location)
            self.resume_forward(url_file, opts['resume'], file_location,
                    opts['error_log'])

            i = 0
            urls = []
            for url in url_file:
                urls.append(url)
                if i % 2500 == 0 and i != 0:
                    plugins, opts, executor, instances = self._recreate_all()
                    self._process_generate_futures(urls, executor, opts,
                            instances, follow_redirects)
                    executor.shutdown()
                    gc.collect()
                    urls = []

                i += 1

            if len(urls) > 0:
                plugins, opts, executor, instances = self._recreate_all()
                self._process_generate_futures(urls, executor, opts, instances,
                        follow_redirects)
                executor.shutdown()

    def _process_generate_futures(self, urls, executor, opts, instances, follow_redirects):
        self.out.debug('scan._process_generate_futures')

        futures = []
        for url in urls:
            url = url.strip()
            future = executor.submit(self._process_cms_identify, url,
                    opts, instances, follow_redirects)
            future.url = url

            futures.append(future)

        if futures:
            self._process_identify_futures(futures, opts, instances)

    def _process_identify_futures(self, futures, opts, instances):
        self.out.debug('scan._process_identify_futures')
        checkpoint = datetime.now()

        i = 0
        to_scan = {}
        cancelled = False
        for future in as_completed(futures):

            if common.shutdown:
                if not cancelled:
                    map(lambda x: x.cancel(), futures)
                    cancelled = True

                continue

            url = future.url
            try:
                cms_name, result_tuple = future.result(timeout=opts['timeout_host'])

                if cms_name != None:
                    if cms_name not in to_scan:
                        to_scan[cms_name] = []

                    to_scan[cms_name].append(result_tuple)
            except:
                f.exc_handle(url, self.out, self.app.testing)

            i += 1

        if to_scan:
            self._process_scan(opts, instances, to_scan)
            to_scan = {}

    def _process_cms_identify(self, url, opts, instances, follow_redirects):
        self.out.debug('scan._process_cms_identify -> %s' % url)
        try:
            url, host_header = url, opts['headers']['Host']
        except:
            url, host_header = self._process_host_line(url)

        url = f.repair_url(url)

        if follow_redirects:
            url, host_header = self.determine_redirect(url, host_header, opts)

        found = False
        for cms_name in instances:
            inst_dict = instances[cms_name]
            inst = inst_dict['inst']

            if inst.cms_identify(url, opts['timeout'], self._generate_headers(host_header)) == True:
                found = True
                break

        if not found:
            return None, None
        else:
            return cms_name, (url, host_header)

    def _process_scan(self, opts, instances, to_scan):
        self.out.debug('scan._process_scan')
        for cms_name in to_scan:
            inst_dict = instances[cms_name]
            cms_urls = to_scan[cms_name]

            if len(cms_urls) > 0:
                inst_dict['inst'].process_url_iterable(cms_urls, opts, **inst_dict['kwargs'])

    def _instances_get(self, *args, **kwargs):
        return f.instances_get(*args, **kwargs)

    def _recreate_all(self):
        plugins = pu.plugins_base_get()
        opts = self._options(self.app.pargs)
        executor = ThreadPoolExecutor(max_workers=opts['threads_identify'])
        instances = self._instances_get(opts, plugins, True, self.out)

        return plugins, opts, executor, instances
