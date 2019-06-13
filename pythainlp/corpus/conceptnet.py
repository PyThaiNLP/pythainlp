# -*- coding: utf-8 -*-
"""
Get data from ConceptNet API at http://conceptnet.io
"""
import requests


def edges(word: str, lang: str = "th"):
    """
    Get edges from `ConceptNet <http://api.conceptnet.io/>`_ API.
    ConceptNet is a public semantic network, designed to help computers understand the meanings of words that people use.

    For example, the term "ConceptNet" is a "knowledge graph", and "knowledge graph" has "common sense knowledge" which is a  part of "artificial inteligence".
    Also, "ConcepNet" is used for "natural language understanding" which is a part of "artificial intelligence". 
 
        | "ConceptNet" --is a--> "knowledge graph" --has--> "common sense" --a part of--> "artificial intelligence" 
        | "ConceptNet" --used for--> "natural language understanding" --a part of--> "artificial intelligence" 
    
    With this illustration, it shows relationships (represented as *Edge*) between the terms (represented as *Node*)

   

    :param str word: word to be sent to ConceptNet API
    :param str lang: abbreviation of language (i.e. *th* for Thai, *en* for English, or *ja* for Japan). By default, it is *th* (Thai).

    :return: return edges of the given word according to the ConceptNet network. 
    :rtype: list[dict]
    """

    obj = requests.get(f"http://api.conceptnet.io/c/{lang}/{word}").json()
    return obj["edges"]
