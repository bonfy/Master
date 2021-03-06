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


class Star:

    def __init__(self, star):
        self.star = star

    @property
    def stars(self):
        return self.star * '\u2605' + (5 - self.star) * '\u2606'


class Talk(Star):

    def __init__(self, title, url, star=5):
        super().__init__(star=star)
        self.title = title
        self.url = url

    @classmethod
    def from_json(cls, js):
        title = js.get('title')
        url = js.get('url')
        star = js.get('star', 5)
        return cls(title=title, url=url, star=star)

    @property
    def md(self):
        return f'{self.stars} [{self.title}]({self.url})'


class Course(Star):

    def __init__(self, title, url, platform, star=5):
        super().__init__(star=star)
        self.title = title
        self.url = url
        self.platform = platform

    @classmethod
    def from_json(cls, js):
        title = js.get('title')
        url = js.get('url')
        platform = js.get('platform')
        star = js.get('star', 5)
        return cls(title=title, url=url, platform=platform, star=star)

    @property
    def md(self):
        return f'{self.stars} [{self.title}]({self.url})({self.platform})'


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
        avatar,
        wiki=None,
        website=None,
        medias=[],
        talks=[],
        courses=[],
        books=[],
    ):
        self.name = name
        self.language = language
        self.avatar = avatar
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
        avatar = js.get('avatar')
        wiki = js.get('wiki')
        website = js.get('website')
        medias = [Media.from_json(i) for i in js.get('medias', [])]
        talks = [Talk.from_json(i) for i in js.get('talks', [])]
        courses = [Course.from_json(i) for i in js.get('courses', [])]
        books = [Book.from_json(i) for i in js.get('books', [])]
        return cls(
            name=name,
            language=language,
            avatar=avatar,
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
        md_avatar = f'<img align="left" width="30" height="30" src="{self.avatar}"> '
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
        md = f'{md_avatar}[{self.name}]({self.homepage})\n\n{md_medias}{md_talks}{md_courses}{md_books}'
        return md

    def __repr__(self):
        return f'<Master: {self.name}({self.language})>'


class Masters:

    def __init__(self, masters=[]):
        self.masters = masters

    @classmethod
    def from_json_file(cls, filename='data.json'):
        self = cls()
        with open(filename, 'r') as f:
            items = json.load(f)
        for item in items:
            self.masters.append(Master.from_json(item))
        return self

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
            f.write(
                '# Master\n> "Do you want to know the difference between a master and a beginner?"\n\n'
            )
            f.write(
                '> "The master has failed more times than the beginner has tried."\n\n'
            )
            f.write(self.md)
            f.write('## Contributing\n')
            f.write('Your contributions are always welcome!\n\n')
            f.write('Please add the programmer you appreciate in `data.json`.')

    def write_html(self):
        import jinja2

        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "template.html"
        template = templateEnv.get_template(TEMPLATE_FILE)
        output = template.render(masters=self.masters)
        with open('index.html', 'w') as f:
            f.write(output)


if __name__ == '__main__':
    masters = Masters.from_json_file()
    masters.write_md()
    masters.write_html()
