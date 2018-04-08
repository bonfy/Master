# -*- coding:utf-8 -*-
###
# Author: bonfy
# Email: foreverbonfy@163.com
# Created Date: 2018-04-08
###
import json


class Media:

    def __init__(self, username, platform, url):
        self.username = username
        self.platform = platform
        self.url = url
        if self.platform == 'Twitter' and not self.username.startswith('@'):
            self.username = f'@{self.username}'

    @classmethod
    def from_json(cls, js):
        username = js.get('username')
        platform = js.get('platform')
        url = js.get('url')
        return cls(username=username, platform=platform, url=url)

    @property
    def md(self):
        return f'{self.platform}: [{self.username}]({self.url})'


class Talk:

    def __init__(self, title, url, star=5):
        self.title = title
        self.url = url
        self.star = star

    @classmethod
    def from_json(cls, js):
        title = js.get('title')
        url = js.get('url')
        star = js.get('star', 5)
        return cls(title=title, url=url, star=star)

    @property
    def stars(self):
        return self.star * '\u2b51' + (5-self.star) * '\u2b52'

    @property
    def md(self):
        return f'[{self.stars}] [{self.title}]({self.url})'


class Course:

    def __init__(self, title, url, platform):
        self.title = title
        self.url = url
        self.platform = platform

    @classmethod
    def from_json(cls, js):
        title = js.get('title')
        url = js.get('url')
        platform = js.get('platform')
        return cls(title=title, url=url, platform=platform)

    @property
    def md(self):
        return f'[{self.title}]({self.url})({self.platform})'


class Book:

    def __init__(self, title, url):
        self.title = title
        self.url = url

    @classmethod
    def from_json(cls, js):
        title = js.get('title')
        url = js.get('url')
        return cls(title=title, url=url)

    @property
    def md(self):
        return f'[{self.title}]({self.url})'


class Master:

    def __init__(
        self,
        name,
        language,
        wiki=None,
        website=None,
        medias=[],
        talks=[],
        courses=[],
        books=[],
    ):
        self.name = name
        self.language = language
        self.wiki = wiki
        self.website = website
        self.medias = medias
        self.talks = talks
        self.courses = courses
        self.books = books

    @classmethod
    def from_json(cls, js):
        name = js.get('name')
        language = js.get('language')
        wiki = js.get('wiki')
        website = js.get('website')
        medias = [Media.from_json(i) for i in js.get('medias', [])]
        talks = [Talk.from_json(i) for i in js.get('talks', [])]
        courses = [Course.from_json(i) for i in js.get('courses', [])]
        books = [Book.from_json(i) for i in js.get('books', [])]
        return cls(
            name=name,
            language=language,
            wiki=wiki,
            website=website,
            medias=medias,
            talks=talks,
            courses=courses,
            books=books,
        )

    @property
    def homepage(self):
        if self.website:
            return self.website

        return self.wiki if self.wiki else ''

    @property
    def md(self):
        md_medias = ''
        md_talks = ''
        md_courses = ''
        md_books = ''
        if self.medias:
            md_medias = 'Medias: '
            md_medias += ', '.join([m.md for m in self.medias])
            md_medias += '\n\n'
        if self.talks:
            md_talks = 'Talks:\n'
            for i in self.talks:
                md_talks += f'- {i.md}\n'
            md_talks += '\n\n'
        if self.courses:
            md_courses = 'Courses:\n'
            for i in self.courses:
                md_courses += f'- {i.md}\n'
            md_courses += '\n\n'
        if self.books:
            md_books = 'Books:\n'
            for i in self.books:
                md_books += f'- {i.md}\n'
            md_books += '\n\n'
        md = f'[{self.name}]({self.homepage})\n\n{md_medias}{md_talks}{md_courses}{md_books}'
        return md

    def __repr__(self):
        return f'<Master: {self.name}({self.language})>'


class Masters:

    def __init__(self, masters=[]):
        self.masters = masters

    @classmethod
    def from_json_file(cls, filename='data.json'):
        masters = []
        with open(filename, 'r') as f:
            items = json.load(f)
        for item in items:
            masters.append(Master.from_json(item))
        return cls(masters=masters)

    def __getitem__(self, idx):
        return self.masters[idx]

    @property
    def languages(self):
        lans = [i.language for i in self.masters]
        return set(lans)

    @property
    def md(self):
        md = ''
        for language in self.languages:
            md += f'## {language} \n\n'
            masters_lan = filter(
                lambda x: x.language == language, self.masters
            )
            for m in masters_lan:
                md += f'### {m.md}'
        return md

    def write_md(self):
        with open('readme.md', 'w') as f:
            f.write('# Masters\n> List Great Programmers\n\n')
            f.write(self.md)


if __name__ == '__main__':
    masters = Masters.from_json_file()
    masters.write_md()
