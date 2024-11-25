import concurrent.futures
import time
import heapq  # For optimized priority queue implementation
import re  # For cleaning up the content and splitting into words

# Document class to store information about each document
class Document:
    def __init__(self, doc_id, url, title, content_ref):
        """
        Initialize a document with a reference to the content (file path).
        
        :param doc_id: Document identifier
        :param url: URL of the document
        :param title: Title of the document
        :param content_ref: File path or reference to the document content
        """
        self.doc_id = doc_id
        self.url = url
        self.title = title
        self.content_ref = content_ref  # Store the file path as a reference to the content

    def read_content(self):
        """Read the content from the file referenced by content_ref."""
        try:
            with open(self.content_ref, 'r', encoding='utf-8') as file:
                return file.read()  # Return the content from the file
        except FileNotFoundError:
            print(f"Error: The file '{self.content_ref}' was not found.")
            return None
        except Exception as e:
            print(f"Error reading file '{self.content_ref}': {e}")
            return None

    def extract_keywords(self):
        """Extract unique keywords from the document's content."""
        content = self.read_content()  # Read content from the file
        if content is None:
            return set()  # Return an empty set if content could not be read

        content_lower = content.lower()  # Normalize content
        # Remove punctuation using regular expressions and split into words
        words = re.sub(r'[^\w\s]', '', content_lower).split()
        unique_keywords = set(words)  # Use a set to get unique keywords
        return unique_keywords

# InvertedIndex class to store and manage the inverted index
class InvertedIndex:
    def __init__(self):
        """Initialize an empty inverted index and cache for frequently searched terms."""
        self.index = {}
        self.cache = {}  # Cache for frequently searched terms

    def add_document(self, document):
        """Add a document to the inverted index."""
        keywords = document.extract_keywords()
        for keyword in keywords:
            if keyword not in self.index:
                self.index[keyword] = set()  # Use set to store unique document IDs
            self.index[keyword].add(document.doc_id)  # Add document ID to the set (avoid duplicates)

    def get_documents(self, keyword):
        """Retrieve document IDs for a given keyword, using the cache if possible."""
        if keyword in self.cache:
            print(f"Cache hit for keyword: {keyword}")
            return self.cache[keyword]  # Return cached result
        print(f"Cache miss for keyword: {keyword}")
        result = self.index.get(keyword.lower(), set())  # Return empty set if keyword not found
        self.cache[keyword] = result  # Cache the result
        return result

# PriorityQueue class to manage document rankings based on scores
class PriorityQueue:
    def __init__(self):
        """Initialize an empty priority queue."""
        self.heap = []  # Use a list to implement the heap

    def insert(self, item):
        """Insert an item into the priority queue."""
        heapq.heappush(self.heap, (-item[1], item[0]))  # Use negative scores to make the heap a max-heap

    def extract_max(self):
        """Remove and return the highest priority item."""
        if not self.heap:
            return None  # Return None if the heap is empty
        max_item = heapq.heappop(self.heap)  # Pop the highest priority item (max heap using negative scores)
        return (max_item[1], -max_item[0])  # Return as (doc_id, score), negate the score back

    def is_empty(self):
        """Check if the priority queue is empty."""
        return len(self.heap) == 0

# Function to add a document in parallel using ThreadPoolExecutor
def add_document_in_parallel(index, doc_id, url, title, content_ref):
    """Function to add a document in parallel using ThreadPoolExecutor."""
    doc = Document(doc_id, url, title, content_ref)
    index.add_document(doc)  # Add document to the index

# Main Usage Example
if __name__ == "__main__":
    # Create an inverted index
    index = InvertedIndex()

    # Documents to be added
    documents = [
        (1, "http://example.com/doc1", "SEO Basics", "doc1.txt"),
        (2, "http://example.com/doc2", "Advanced SEO", "doc2.txt"),
        (3, "http://example.com/doc3", "SEO Tips", "doc3.txt")
    ]

    # Timing the sequential insertion
    start_time = time.time()
    for doc_id, url, title, content_ref in documents:
        doc = Document(doc_id, url, title, content_ref)
        index.add_document(doc)  # Sequential document insertion
    print(f"Sequential Insertion Time: {time.time() - start_time} seconds")

    # Timing the parallel insertion
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for doc_id, url, title, content_ref in documents:
            # Submit the add_document_in_parallel for each document
            futures.append(executor.submit(add_document_in_parallel, index, doc_id, url, title, content_ref))

        # Wait for all tasks to complete
        for future in futures:
            future.result()  # This ensures we wait for the task to complete
    print(f"Parallel Insertion Time: {time.time() - start_time} seconds")
    
    # Search for a keyword and measure the search time
    keyword_to_search = "seo"
    start_time = time.time()  # Start the timer
    found_docs = index.get_documents(keyword_to_search)
    end_time = time.time()  # End the timer

    # Calculate and print the search time
    search_time = end_time - start_time
    print(f"Documents containing '{keyword_to_search}': {found_docs}")
    print(f"Search Time: {search_time:.6f} seconds")


    # Search for a keyword
    keyword_to_search = "seo"
    found_docs = index.get_documents(keyword_to_search)
    print(f"Documents containing '{keyword_to_search}': {found_docs}")

    # Create a priority queue and rank documents
    priority_queue = PriorityQueue()
    priority_queue.insert((1, 0.95))  # Document ID 1 with score
    priority_queue.insert((2, 0.85))  # Document ID 2 with score
    priority_queue.insert((3, 0.80))  # Document ID 3 with score

    # Retrieve documents based on scores
    while not priority_queue.is_empty():
        highest_scoring_doc = priority_queue.extract_max()
        print(f"Highest scoring document: {highest_scoring_doc}")