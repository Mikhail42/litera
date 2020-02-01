#! /usr/bin/python3

import argparse
import json
from os import path
from time import sleep
import requests
from bs4 import BeautifulSoup


class NoDataException(Exception):
    pass


MAX_PAGES_PER_CHAPTER = 10000
WAIT_BETWEEN = 10


class LitEraParser(object):

    csrf_token = ''
    _session = None
    _chapter_id_list = None

    def __init__(self, book_slug):
        self.book_url = path.join('https://litnet.com/reader', book_slug).replace("\\", '/')
        self._init_book()

    @property
    def session(self):
        if self._session is None:
            self._session = requests.Session()
            self._session.headers.update({
                'user-agent': 'Browser 2.1',
                'accept-language': 'en-US, en; q = 0.8',
                'x-requested-with': 'XMLHttpRequest'
            })
        return self._session

    def _init_book(self):

        html_response = self.session.get(self.book_url)
        html_parser = BeautifulSoup(html_response.text, 'html.parser')

        chapters = html_parser.find('select', {'name': 'chapter'})
        self._chapter_id_list = [
            option_element.attrs['value']
            for option_element in chapters.find_all('option')
        ]

        token_meta = html_parser.find('meta', {'name': 'csrf-token'})
        self.csrf_token = token_meta.attrs['content']

        self.session.headers.update({
            'origin': 'https://litnet.com',
            'referer': self.book_url,
            'x-csrf-token': self.csrf_token
        })

    def _get_page(self, chapter_id, page):

        post_params = {
            'chapterId': chapter_id,
            'page': page,
            '_csrf': self.csrf_token
        }

        response_data = self.session.post('https://litnet.com/reader/get-page', post_params)
        response_json = json.loads(response_data.text)

        if not response_json['status']:
            raise NoDataException(response_json['data'])

        page_parser = BeautifulSoup(response_json['data'], 'html.parser')

        # Filter from so-called "protection" tags
        for bad_span in page_parser.find_all('span'):
            bad_span.replace_with('')
        [x.extract() for x in page_parser.findAll('i')]

        return page_parser.text, response_json['isLastPage']

    def _get_chapter(self, chapter_id):

        self.session.headers['referer'] = '{}?c={}'.format(self.book_url, chapter_id)
        total_chapter_text = ''
        try:
            for page in range(1, MAX_PAGES_PER_CHAPTER):
                chapter_text, is_last_page = self._get_page(chapter_id, page)
                total_chapter_text += chapter_text
                if is_last_page:
                    break
                sleep(WAIT_BETWEEN)
        except NoDataException as ex:
            print('Error! ', ex)

        total_chapter_text += '\n\n'

        return total_chapter_text

    def parse_to_file(self, book_file_name):
        with open(book_file_name, 'w', encoding='utf-8') as text_file:
            print('Progress: ')
            for index, chapter_id in enumerate(self._chapter_id_list):
                progress = int(index * 100 / len(self._chapter_id_list))
                print(progress)
                text_file.write(self._get_chapter(chapter_id))
            print('100..OK')


def main(book_slug, book_file_name):
    LitEraParser(book_slug).parse_to_file(book_file_name)


if __name__ == '__main__':

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        '-s', '--slug', required=True,
        help='Book slug from browser, example: "volchya-tropa-b34046".'
    )
    argument_parser.add_argument(
        '-o', '--output', required=True,
        help='File name to save book.'
    )
    arguments = argument_parser.parse_args()

    main(arguments.slug, arguments.output)

