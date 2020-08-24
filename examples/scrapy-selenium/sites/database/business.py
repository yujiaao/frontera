# -*- coding: utf-8 -*-
import re
from urllib.parse import urlparse
from sqlalchemy.ext.declarative import declarative_base

import sqlalchemy
from sqlalchemy import Column, String, Integer, PickleType, SmallInteger, Float, DateTime, BigInteger, Text, ForeignKey
import json

from .__init__ import db
from ..utils import extract_domain_from_url

Base = declarative_base()


class BusinessModel(Base):
    __tablename__ = 'business'
    __table_args__ = (
        {
            'mysql_charset': 'utf8',
            'mysql_engine': 'InnoDB',
            'mysql_row_format': 'DYNAMIC',
        },
    )

    id = Column(Integer, primary_key=True)
    url = Column(String(700), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)
    fetched_at = Column(DateTime, nullable=True)
    make = Column(String(64), nullable=False, comment="品牌")
    model = Column(String(256), nullable=False, comment="型号")
    mileage = Column(String(16), comment="公里数")
    is_new = Column(String(16), comment="是否是新库存车 neufahrzeug")
    reg_date = Column(String(16), comment="ez注册时间")
    power = Column(String(16), comment="功率")
    fuel_consumption = Column(String(16), comment="综合油耗")
    emission = Column(String(16), comment="二氧化碳排放")
    gear_type = Column(String(16), comment="变速箱类型")
    image = Column(String(1024), comment="封面图")
    prise = Column(String(16), comment="含税价")
    month_rate = Column(String(16), comment="金融月费")
    energy_efficiency_class = Column(String(16), comment="能效等级")
    number_pic = Column(String(16), comment="图片数量")
    all_pic = Column(String(1024), comment="所有图片")
    tax_rate = Column(String(16), comment="增值税率")
    fuel_type = Column(String(16), comment="燃油类型")
    body_type = Column(String(16), comment="类别")
    site_num = Column(String(16), comment="座位数量")
    door_num = Column(String(16), comment="门数量")
    car_check = Column(String(16), comment="车检, hu")

    @classmethod
    def query(cls, session):
        return session.query(cls)

    def __repr__(self):
        return '<Business:%s (%s,%s)>' % (self.url, self.make, self.model)

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])


class SiteModel(db.Model):
    __tablename__ = 'site'
    __table_args__ = (
        {
            'mysql_charset': 'utf8',
            'mysql_engine': 'InnoDB',
            'mysql_row_format': 'DYNAMIC',
        },
    )

    id = Column(Integer, primary_key=True)
    domain = Column(String(256), nullable=False, unique=True)
    aliases = Column(String(256))
    entry_point = Column(String(512), nullable=False, unique=True)
    settings = Column(Text, nullable=True, comment="保存站点相关设置，json格式")
    site_name = Column(String(64))
    last_access = Column(DateTime)
    first_access = Column(DateTime)
    total_articles = Column(Integer)
    logo = Column(String(256))
    is_del = Column(Integer, default=0)

    def __init__(self, domain, site_name, entry_point, aliases):
        self.domain = domain
        self.site_name = site_name
        self.entry_point = entry_point
        self.aliases = aliases
        pass

    @classmethod
    def query(cls, session):
        return session.query(cls)

    def __repr__(self):
        return '<Site:%s (%s)>' % (self.domain, self.entry_point)


class TemplateModel(db.Model):
    __tablename__ = 'template'
    __table_args__ = (
        {
            'mysql_charset': 'utf8',
            'mysql_engine': 'InnoDB',
            'mysql_row_format': 'DYNAMIC',
        },
    )

    id = Column(Integer, primary_key=True)
    temp_type = Column(Integer, comment="模板类型，1-列表页，2-详情页")
    site_id = Column(Integer, ForeignKey('site.id'), nullable=False, comment="站点id")
    xpath_json = Column(Text)
    url_pattern = Column(String(512), nullable=False, default='.*', comment='Url匹配规则')

    def __init__(self, temp_type, site_id, xpath_json, url_pattern):
        self.temp_type = temp_type
        self.site_id = site_id
        self.xpath_json = xpath_json
        self.url_pattern = url_pattern
        pass


class TemplateModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TemplateModel):
            return {
                "temp_type": obj.temp_type,
                "site_id": obj.site_id,
                "xpath_json": obj.xpath_json,
                "url_pattern": obj.url_pattern
            }
        return json.JSONEncoder.default(self, obj)

    @classmethod
    def query(cls, session):
        return session.query(cls)

    def __repr__(self):
        return '<Site:%d (%s)>' % (self.id, self.xpath_json)


def find_site_by_url(url, create_if_not_found=False):
    domain = extract_domain_from_url(url)
    try:
        # return db.session.query(SiteModel).filter(SiteModel.domain.like("%" + domain + "%")).one()
        return db.session.query(SiteModel).filter(SiteModel.domain == domain).one()
    except sqlalchemy.orm.exc.NoResultFound:
        # url='http://user:pwd@domain:80/path;params?query=queryarg#fragment'
        # ParseResult(scheme='http', netloc='user:pwd@domain:80', path='/path', params='params', query='query=queryarg', fragment='fragment')
        parse_result = urlparse(url)
        return create_site({'domain': parse_result.netloc, 'site_name': parse_result.netloc, 'entry_point': url,
                            "aliases": parse_result.scheme + "://" + parse_result.netloc})


def create_site(data):
    domain = data.get('domain')
    site_name = data.get('site_name')
    entry_point = data.get('entry_point')
    aliases = data.get('aliases')
    site = SiteModel(domain, site_name, entry_point, aliases)
    db.session.add(site)
    db.session.commit()
    print(site.id)
    return site


def update_site(site_id, data):
    site = SiteModel.query.filter(SiteModel.id == site_id).one()
    site.domain = data.get('domain')
    site.site_name = data.get('site_name')
    site.entry_point = data.get('entry_point')
    db.session.add(site)
    db.session.commit()


def create_template(data):
    temp = TemplateModel(data.get('temp_type'), data.get('site_id'), data.get('xpath_json'), data.get('url_pattern'))
    db.session.add(temp)
    db.session.commit()
    pass


def create_template_by_url(data):
    url = json.loads(data['xpath_json'])['url']
    site = find_site_by_url(url, create_if_not_found=True)
    temp = TemplateModel(data.get('temp_type'), site.id, data.get('xpath_json'), data.get('url_pattern'))
    db.session.add(temp)
    db.session.commit()
    pass


def find_template_by_url(url):
    site = find_site_by_url(url, create_if_not_found=True)
    # print(site)
    temps = db.session.query(TemplateModel).filter(TemplateModel.site_id == site.id).all()
    for temp in temps:
        if re.match(temp.url_pattern, url):
            return temp
    return {"status": 1, "message": f"no template found for url: {url}"}


def update_template(template_id, data):
    template = db.session.query(TemplateModel).filter(TemplateModel.id == template_id).one()
    template.temp_type = data.get('temp_type')
    template.site_id = data.get('site_id')
    template.xpath_json = data.get('xpath_json')
    db.session.add(template)
    db.session.commit()


def update_business(id, data):
    b_id = id
    business = db.session.query(BusinessModel).filter(BusinessModel.id == b_id).one()
    business = BusinessModel()


def exists_business_by_url(url):
    return db.session.query(BusinessModel).filter(BusinessModel.url == url).count() > 0
