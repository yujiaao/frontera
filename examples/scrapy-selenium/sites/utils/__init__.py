from sqlalchemy.orm import class_mapper


def extract_domain_from_url(url):
    """Get domain name from url"""
    from urllib.parse import urlparse
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return domain


def serialize(model):
    """Transforms a model into a dictionary which can be dumped to JSON."""
    # first we get the names of all the columns on your model
    columns = [c.key for c in class_mapper(model.__class__).columns]
    # then we return their values in a dict
    return dict((c, getattr(model, c)) for c in columns)


def to_json(model):
    """ Returns a JSON representation of an SQLAlchemy-backed object. """
    if type(model) is dict:
        return  model
    json = {}
    # json['fields'] = {}
    # json['pk'] = getattr(model, 'id')
    for col in model._sa_class_manager.mapper.mapped_table.columns:
        # json['fields'][col.name] = getattr(model, col.name)
        json[col.name] = getattr(model, col.name)
    # return dumps([json])
    return json


def to_json_list(model_list):
    json_list = []
    for model in model_list:
        json_list.append(to_json(model))
    return json_list


'''
import os
common = os.path.commonprefix(['apple pie available', 'apple pies'])
assert common == 'apple pie'
'''
