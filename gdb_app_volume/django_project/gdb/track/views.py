from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from neomodel import db
from .models import Article, StructuredRel
import pytz


class Index(View):
    def get(self, request):

        nodes = self.get_all_nodes()
        rels = self.get_all_relationships()

        nodes = self.convert_node_to_dictlist(nodes)
        rels = self.convert_rel_to_dictlist(rels)

        graph_data = nodes + rels
        context = {
            'graph_data': graph_data
        }

        return render(request, 'track/index.html', context)

    # TODO: 一般化したい
    def get_all_nodes(self):

        # get all data from Neo4j database
        articles = db.cypher_query('MATCH (n:Article) RETURN n')

        # change the Neo4j objects to neomodel objects
        articles = [Article.inflate(node[0]) for node in articles[0]]

        return articles

    def get_all_relationships(self):

        # get all data from Neo4j database
        raw_rels = db.cypher_query('MATCH ()-[r]->() RETURN r, type(r)')

        # change the Neo4j objects to neomodel objects
        # the shape is like:
        # [[<neomodel object>, 'TYPE_OF_R'], [...], [...
        rels = []
        for rel in raw_rels[0]:
            tmp = StructuredRel.inflate(rel[0])
            rels.append([tmp, rel[1]])

        return rels

    def convert_node_to_dictlist(self, nodes):

        jst = pytz.timezone('Asia/Tokyo')

        dict_list = []

        for node in nodes:
            prop_dict = {
                'data': {
                    'id': node.id,
                    'author': node.author,
                    'creation_date': node.creation_date.astimezone(jst).strftime('%Y-%m-%d %H:%M:%S'),
                    'title': node.title,
                    'body': node.body
                }
            }
            dict_list.append(prop_dict)

        return dict_list

    def convert_rel_to_dictlist(self, rels):

        dict_list = []

        for rel in rels:
            prop_dict = {
                'data': {
                    'source': rel[0].start_node().id,
                    'target': rel[0].end_node().id,
                    'label': rel[1]
                }
            }
            dict_list.append(prop_dict)

        return dict_list
