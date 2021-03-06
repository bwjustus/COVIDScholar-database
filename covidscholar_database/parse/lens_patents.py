from base import Parser, VespaDocument, indexes
import json
import re
from datetime import datetime
import requests
from utils import clean_title, find_cited_by, find_references
from mongoengine import DynamicDocument, ReferenceField, DateTimeField

latest_version = 1

class LensPatentDocument(VespaDocument):

    meta = {"collection": "Lens_Patents_parsed_vespa",
            "indexes": indexes
    }

    latest_version = latest_version
    unparsed_document = ReferenceField('UnparsedLensDocument', required=True)

class LensPatentParser(Parser):
    """
    Parser for documents from The Lens Human Coronaviruses Data Initiative.
    """

    def _parse_doi(self, doc):
        """ Returns the DOI of a document as a <class 'str'>"""
        return None

    def _parse_title(self, doc):
        """ Returns the title of a document as a <class 'str'>"""
        return doc['Title']

    def _parse_authors(self, doc):
        """ Returns the authors of a document as a <class 'list'> of <class 'dict'>.
        Each element in the authors list should have a "name" field with the author's
        full name (e.g. John Smith or J. Smith) as a <class 'str'>.
        """
        return None

    def _parse_journal(self, doc):
        """ Returns the journal of a document as a <class 'str'>. """
        return None

    def _parse_issn(self, doc):
        """ Returns the ISSN and (or) EISSN of a document as a <class 'list'> of <class 'str'> """
        return None

    def _parse_journal_short(self, doc):
        """ Returns the shortend journal name of a document as a <class 'str'>, if available.
         e.g. 'Comp. Mat. Sci.' """
        return None

    def _parse_publication_date(self, doc):
        """ Returns the publication_date of a document as a <class 'datetime.datetime'>"""
        return doc['Published_Date']

    def _parse_has_year(self, doc):
        """ Returns a <class 'bool'> specifying whether a document's year can be trusted."""
        return self._parse_publication_date(doc) != None

    def _parse_has_month(self, doc):
        """ Returns a <class 'bool'> specifying whether a document's month can be trusted."""
        return self._parse_publication_date(doc) != None

    def _parse_has_day(self, doc):
        """ Returns a <class 'bool'> specifying whether a document's day can be trusted."""
        return self._parse_publication_date(doc) != None

    def _parse_abstract(self, doc):
        """ Returns the abstract of a document as a <class 'str'>"""
        return doc['Abstract']

    def _parse_origin(self, doc):
        """ Returns the origin of the document as a <class 'str'>. Use the mongodb collection
        name for this."""
        return "Scraper_lens_patents"

    def _parse_source_display(self, doc):
        """ Returns the source of the document as a <class 'str'>. This is what will be
        displayed on the website, so use something people will recognize properly and
        use proper capitalization."""
        return 'Lens Patents'

    def _parse_last_updated(self, doc):
        """ Returns when the entry was last_updated as a <class 'datetime.datetime'>. Note
        this should probably not be the _bt field in a Parser."""
        return datetime.now()

    def _parse_has_full_text(self, doc):
        """ Returns a <class 'bool'> specifying if we have the full text."""
        return False

    def _parse_body_text(self, doc):
        """ Returns the body_text of a document as a <class 'list'> of <class 'dict'>.
        This should be a list of objects of some kind. Seems to be usually something like
        {'section_heading':  <class 'str'>,
         'text': <class 'str'>
         }
         """
        return None

    def _parse_references(self, doc):
        """ Returns the references of a document as a <class 'list'> of <class 'dict'>.
        This is a list of documents cited by the current document.
        """
        return None

    def _parse_cited_by(self, doc):
        """ Returns the citations of a document as a <class 'list'> of <class 'str'>.
        A list of DOIs of documents that cite this document.
        """
        return None

    def _parse_link(self, doc):
        """ Returns the url of a document as a <class 'str'>"""
        return doc['Link']

    def _parse_category_human(self, doc):
        """ Returns the category_human of a document as a <class 'list'> of <class 'str'>"""
        return None

    def _parse_keywords(self, doc):
        """ Returns the keywords for a document from original source as a a <class 'list'> of <class 'str'>"""
        return None

    def _parse_summary_human(self, doc):
        """ Returns the human-written summary of a document as a <class 'list'> of <class 'str'>"""
        return None

    def _parse_is_preprint(self, doc):
        """ Returns a <class 'bool'> specifying whether the document is a preprint.
        If it's not immediately clear from the source it's coming from, return None."""
        return None

    def _parse_is_covid19(self, doc):
        """ Returns a <class 'bool'> if we know for sure a document is specifically about COVID-19.
        If it's not immediately clear from the source it's coming from, return None."""
        return None

    def _parse_license(self, doc):
        """ Returns the license of a document as a <class 'str'> if it is specified in the original doc."""
        return None

    def _parse_pmcid(self, doc):
        """ Returns the pmcid of a document as a <class 'str'>."""
        return None

    def _parse_pubmed_id(self, doc):
        """ Returns the PubMed ID of a document as a <class 'str'>."""
        return None

    def _parse_who_covidence(self, doc):
        """ Returns the who_covidence of a document as a <class 'str'>."""
        return None

    def _parse_version(self, doc):
        """ Returns the version of a document as a <class 'int'>."""
        return latest_version

    def _parse_copyright(self, doc):
        """ Returns the copyright notice of a document as a <class 'str'>."""
        return None

    def _parse_document_type(self, doc):
        """ Returns the document type of a document as a <class 'str'>.
        e.g. 'paper', 'clinical_trial', 'patent', 'news'. """
        return 'patent'

    def _preprocess(self, doc):
        """
        Preprocesses an entry from the Elsevier_corona_meta collection into a flattened
        metadata document.
        Args:
            doc:
        Returns:
        """
        return doc

    def _postprocess(self, doc, parsed_doc):
        """
        Post-process an entry to add any last-minute fields required. Gets called right before parsed doc is
        returned. Return parsed_doc if you don't want to make any changes.
        """
        return parsed_doc

class UnparsedLensDocument(DynamicDocument):
    meta = {"collection": "Scraper_lens_patents"
    }

    parser = LensPatentParser()

    parsed_class = LensPatentDocument

    parsed_document = ReferenceField(LensPatentDocument, required=False)

    last_updated = DateTimeField(db_field="Last_Updated")

    def parse(self):
        parsed_document = self.parser.parse(self.to_mongo())
        parsed_document['_bt'] = datetime.now()
        parsed_document['unparsed_document'] = self
        return LensPatentDocument(**parsed_document)
