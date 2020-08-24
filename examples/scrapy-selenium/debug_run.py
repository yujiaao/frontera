from scrapy.cmdline import execute
from frontera.utils.add_seeds import run_add_seeds
from frontera.settings import Settings

settings = Settings(module='sites.frontera.settings')
run_add_seeds(settings, 'sites/seeds.txt')

execute(['scrapy', 'crawl', 'browser'])
