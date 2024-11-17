class Document:
    def __init__(self, doc_id, url, title, content):
        self.doc_id = doc_id
        self.url = url
        self.title = title
        self.content = content

    def __str__(self):
        return f"Document(ID: {self.doc_id}, Title: {self.title}, URL: {self.url})"
class InvertedIndex:
    def __init__(self):
        self.index = {}

    def add_document(self, doc):
        # Tokenize content and add words to the inverted index
        for word in doc.content.split():
            word = word.lower()  # Normalize to lowercase for uniform indexing
            if word not in self.index:
                self.index[word] = []
            self.index[word].append(doc.doc_id)

    def get_documents(self, keyword):
        return self.index.get(keyword.lower(), [])

    def __str__(self):
        return str(self.index)

# Main Usage Example
if __name__ == "__main__":
    # Create documents
    doc1 = Document(1, "http://example.com/doc1", "SEO Basics", "SEO is important for websites.")
    doc2 = Document(2, "http://example.com/doc2", "Advanced SEO", "Advanced SEO techniques improve visibility.")
    doc3 = Document(3, "http://example.com/doc3", "SEO Tips", "SEO tips help in optimizing content.")

    # Create an inverted index and add documents
    index = InvertedIndex()
    index.add_document(doc1)
    index.add_document(doc2)
    index.add_document(doc3)
    
    #Searching for the keyword "SEO"
    print("SEO Found in Documets: " + str(index.get_documents("seo")))
    
    #Serching for optimization
    print(index.get_documents("optimizing"))
    
    #Searching for Ranking
    print(index.get_documents("ranking"))

    #Search with Empty Keyword
    print(index.get_documents(""))




