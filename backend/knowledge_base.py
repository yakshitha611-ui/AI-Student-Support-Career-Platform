"""
Knowledge Base System for AI Chatbot
RAG-ready architecture for storing and retrieving educational content
"""

from typing import Optional


class KnowledgeDocument:
    """Represents a knowledge base document"""

    def __init__(
        self,
        title: str,
        category: str,
        content: str,
        keywords: list[str],
        difficulty: str = "Beginner",
    ):
        self.title = title
        self.category = category
        self.content = content
        self.keywords = keywords
        self.difficulty = difficulty

    def to_dict(self):
        return {
            "title": self.title,
            "category": self.category,
            "content": self.content,
            "keywords": self.keywords,
            "difficulty": self.difficulty,
        }


class KnowledgeBase:
    """Manages and retrieves knowledge base documents"""

    def __init__(self):
        self.documents: list[KnowledgeDocument] = []
        self._initialize_documents()

    def _initialize_documents(self):
        """Initialize the knowledge base with educational content"""

        # Web Development Documents
        self.add_document(
            KnowledgeDocument(
                title="REST API Basics",
                category="Web Development",
                content="""
REST API Basics:
REST (Representational State Transfer) is an architectural style for designing networked applications.

Key Concepts:
1. Resources: Everything is a resource (user, product, order, etc.)
2. HTTP Methods:
   - GET: Retrieve a resource
   - POST: Create a new resource
   - PUT: Update an entire resource
   - PATCH: Update part of a resource
   - DELETE: Remove a resource
3. Status Codes:
   - 200 OK: Request successful
   - 201 Created: Resource created
   - 400 Bad Request: Invalid request
   - 404 Not Found: Resource not found
   - 500 Server Error: Internal server error

Example:
GET /api/users/123 - Fetch user with ID 123
POST /api/users - Create a new user
PUT /api/users/123 - Update user 123
DELETE /api/users/123 - Delete user 123

Best Practices:
- Use meaningful resource names
- Use HTTP methods correctly
- Return appropriate status codes
- Include proper error messages
- Version your API (/api/v1/)
- Document your endpoints
""",
                keywords=["REST", "API", "HTTP", "backend", "web development"],
                difficulty="Beginner",
            )
        )

        self.add_document(
            KnowledgeDocument(
                title="Database Fundamentals",
                category="Databases",
                content="""
Database Fundamentals:

1. Types of Databases:
   - Relational (SQL): MySQL, PostgreSQL, Oracle
   - NoSQL: MongoDB, Cassandra, Redis
   - Graph: Neo4j

2. Key Concepts:
   - Tables: Organized data structure
   - Rows: Individual records
   - Columns: Data fields
   - Primary Key: Unique identifier for a row
   - Foreign Key: References another table's primary key
   - Indexes: Speed up queries

3. SQL Basics:
   SELECT * FROM users WHERE age > 18;
   INSERT INTO users (name, email) VALUES ('John', 'john@example.com');
   UPDATE users SET age = 25 WHERE id = 1;
   DELETE FROM users WHERE id = 1;

4. Normal Forms:
   - 1NF: Eliminate duplicate columns
   - 2NF: Eliminate partial dependencies
   - 3NF: Eliminate transitive dependencies

5. Transactions:
   - ACID Properties: Atomicity, Consistency, Isolation, Durability
   - Ensure data integrity

Choosing a Database:
- Relational: Structured data, complex queries, ACID requirements
- NoSQL: Unstructured data, scalability, flexibility
""",
                keywords=["database", "SQL", "tables", "queries", "backend"],
                difficulty="Beginner",
            )
        )

        self.add_document(
            KnowledgeDocument(
                title="Python for Backend Development",
                category="Programming",
                content="""
Python for Backend Development:

1. Why Python for Backend?
   - Easy to learn and read
   - Rich ecosystem of frameworks
   - Great for rapid development
   - Excellent for data processing
   - Strong community support

2. Popular Frameworks:
   - FastAPI: Modern, fast, easy to learn
   - Django: Full-featured, batteries-included
   - Flask: Lightweight, flexible
   - Bottle: Minimal framework

3. Key Concepts:
   - Functions: Reusable code blocks
   - Classes: Object-oriented programming
   - Decorators: Modify function behavior
   - Context Managers: Resource management
   - Async/Await: Asynchronous programming

4. Virtual Environments:
   python -m venv venv
   source venv/bin/activate  (Linux/Mac)
   venv\\Scripts\\activate  (Windows)

5. Package Management:
   pip install package_name
   pip freeze > requirements.txt
   pip install -r requirements.txt

6. Best Practices:
   - Use type hints
   - Write unit tests
   - Follow PEP 8 style guide
   - Use proper error handling
   - Document your code
""",
                keywords=["Python", "backend", "FastAPI", "Django", "programming"],
                difficulty="Beginner",
            )
        )

        # Cyber Security Documents
        self.add_document(
            KnowledgeDocument(
                title="Cybersecurity Fundamentals",
                category="Cyber Security",
                content="""
Cybersecurity Fundamentals:

1. Core Concepts:
   - Confidentiality: Only authorized access
   - Integrity: Data accuracy and completeness
   - Availability: Systems accessible when needed

2. Common Threats:
   - Malware: Viruses, ransomware, spyware
   - Phishing: Social engineering attacks
   - SQL Injection: Database exploitation
   - Cross-Site Scripting (XSS): Web vulnerabilities
   - Denial of Service (DoS): Service disruption
   - Brute Force: Password guessing

3. Security Best Practices:
   - Use strong passwords (12+ characters, mixed case, numbers, symbols)
   - Enable two-factor authentication (2FA)
   - Keep software updated
   - Use firewalls
   - Implement encryption
   - Regular security audits
   - Principle of least privilege

4. Authentication Methods:
   - Single Sign-On (SSO)
   - Multi-Factor Authentication (MFA)
   - OAuth 2.0
   - JWT (JSON Web Tokens)

5. Data Protection:
   - Encryption at rest
   - Encryption in transit (HTTPS/TLS)
   - Secure backups
   - Disaster recovery

6. Cybersecurity Roles:
   - Security Analyst
   - Penetration Tester
   - Security Engineer
   - CISO (Chief Information Security Officer)
""",
                keywords=["cybersecurity", "security", "threats", "encryption", "authentication"],
                difficulty="Beginner",
            )
        )

        self.add_document(
            KnowledgeDocument(
                title="Linux Essential Commands",
                category="Cyber Security",
                content="""
Linux Essential Commands for Cybersecurity:

1. File System Navigation:
   ls - List files and directories
   cd - Change directory
   pwd - Print working directory
   mkdir - Create directory
   rm - Remove files
   cp - Copy files
   mv - Move/rename files

2. File Permissions:
   chmod 755 file.sh - Change permissions (owner: read/write/exec, others: read/exec)
   chown user:group file - Change owner
   chmod u+x file - Add execute permission for user

3. User Management:
   sudo su - Switch to root
   sudo apt-get install package - Install package
   useradd username - Create user
   passwd username - Change password
   whoami - Show current user

4. Network Commands:
   ifconfig - Show network interfaces
   ping hostname - Test connectivity
   netstat - Show network connections
   ssh user@host - Secure shell access
   scp file user@host:/path - Secure copy

5. Process Management:
   ps - Show running processes
   kill PID - Terminate process
   top - Display running processes
   bg/fg - Background/foreground processes

6. Text Processing:
   grep pattern file - Search for pattern
   sed - Stream editor
   awk - Text processing
   cat - Display file content
   find - Search files

7. Important Files:
   /etc/passwd - User information
   /etc/shadow - Password hashes (root only)
   /etc/sudoers - Sudo configuration
   /var/log - System logs
""",
                keywords=["Linux", "commands", "cybersecurity", "terminal", "file management"],
                difficulty="Beginner",
            )
        )

        # AI/ML Documents
        self.add_document(
            KnowledgeDocument(
                title="Machine Learning Basics",
                category="AI/ML",
                content="""
Machine Learning Basics:

1. Types of Machine Learning:
   - Supervised Learning: Learning from labeled data
     * Classification: Predict categories
     * Regression: Predict continuous values
   - Unsupervised Learning: Find patterns in unlabeled data
     * Clustering: Group similar items
     * Dimensionality Reduction: Reduce features
   - Reinforcement Learning: Learn through interactions

2. Key Concepts:
   - Training Data: Data used to train the model
   - Test Data: Data used to evaluate the model
   - Features: Input variables
   - Label: Output variable (in supervised learning)
   - Overfitting: Model too complex, poor generalization
   - Underfitting: Model too simple, poor accuracy

3. Common Algorithms:
   - Linear Regression: Predict continuous values
   - Logistic Regression: Binary classification
   - Decision Trees: Tree-based classification
   - Random Forest: Multiple decision trees
   - K-Means: Clustering algorithm
   - Neural Networks: Deep learning

4. Model Evaluation Metrics:
   - Accuracy: % of correct predictions
   - Precision: True positives / All predicted positives
   - Recall: True positives / All actual positives
   - F1-Score: Harmonic mean of precision and recall
   - Confusion Matrix: Shows prediction performance

5. Popular Libraries:
   - Scikit-learn: Machine learning
   - TensorFlow: Deep learning
   - Keras: Neural networks
   - Pandas: Data manipulation
   - NumPy: Numerical computing

6. Steps to Build ML Model:
   1. Data Collection
   2. Data Preprocessing
   3. Feature Engineering
   4. Model Selection
   5. Model Training
   6. Model Evaluation
   7. Hyperparameter Tuning
   8. Deployment
""",
                keywords=["machine learning", "AI", "algorithms", "neural networks", "data science"],
                difficulty="Intermediate",
            )
        )

        # Career Guidance Documents
        self.add_document(
            KnowledgeDocument(
                title="Backend Developer Career Path",
                category="Career Preparation",
                content="""
Backend Developer Career Path:

1. Core Skills Required:
   - Programming Language: Python, Java, Node.js, Go
   - Databases: SQL, NoSQL
   - APIs: REST, GraphQL
   - Frameworks: FastAPI, Django, Spring, Express
   - Version Control: Git
   - Containers: Docker
   - Databases: PostgreSQL, MongoDB, Redis

2. Learning Roadmap:
   Phase 1 (Beginner - 3 months):
   - Learn a programming language (Python/Java/JavaScript)
   - Understand databases and SQL
   - Build basic REST APIs
   
   Phase 2 (Intermediate - 3-6 months):
   - Master a web framework
   - Learn about authentication and security
   - Build full-stack projects
   
   Phase 3 (Advanced - 6+ months):
   - Docker and containerization
   - Cloud platforms (AWS, GCP, Azure)
   - Microservices architecture
   - Message queues and caching

3. Project Ideas:
   - Build a Todo API
   - Create a Blog Platform
   - Build an E-commerce Backend
   - Develop a Chat Application
   - Create a Task Management System

4. Job Requirements by Level:
   Junior (0-2 years):
   - Basic knowledge of one language and framework
   - Understand databases
   - Can build simple APIs
   
   Mid-level (2-5 years):
   - Strong in multiple technologies
   - System design knowledge
   - Production experience
   
   Senior (5+ years):
   - Architectural decisions
   - Team leadership
   - Mentoring junior developers

5. Internship Preparation:
   - Build 2-3 strong projects
   - Practice coding interviews
   - Understand data structures and algorithms
   - Learn about the company's tech stack
   - Prepare for system design questions

6. Salary Expectations (Entry Level):
   - US: $60,000 - $90,000/year
   - Europe: €30,000 - €50,000/year
   - India: ₹4,00,000 - ₹8,00,000/year
""",
                keywords=["career", "backend", "developer", "job", "skills"],
                difficulty="Beginner",
            )
        )

        self.add_document(
            KnowledgeDocument(
                title="Interview Preparation Guide",
                category="Interview Preparation",
                content="""
Interview Preparation Guide:

1. Types of Interviews:
   - Technical Screening: Coding problems, technical knowledge
   - System Design: Architecture, scalability
   - Behavioral: Teamwork, problem-solving
   - Case Study: Real-world scenarios

2. Coding Interview Tips:
   - Practice LeetCode, HackerRank problems
   - Understand data structures and algorithms
   - Practice problem-solving approach:
     1. Understand the problem
     2. Discuss approach with interviewer
     3. Code the solution
     4. Test with examples
     5. Optimize if needed
   - Communicate clearly while solving

3. System Design Interview:
   - Ask clarifying questions
   - Discuss trade-offs
   - Consider scalability
   - Design for failure
   - Think about databases
   - Consider caching and load balancing
   - Discuss monitoring and logging

4. Behavioral Interview:
   - Prepare STAR answers (Situation, Task, Action, Result)
   - Tell stories from past experiences
   - Show enthusiasm and learning ability
   - Ask thoughtful questions about the role

5. Common Questions:
   - "Tell me about yourself"
   - "Why do you want to join us?"
   - "Describe a challenging problem you solved"
   - "How do you handle conflicts with teammates?"
   - "Where do you see yourself in 5 years?"

6. Interview Day Tips:
   - Arrive 15 minutes early
   - Dress professionally
   - Make eye contact
   - Listen carefully
   - Ask questions
   - Follow up with thank you email

7. Popular Interview Platforms:
   - LeetCode: Coding problems
   - HackerRank: Competitive programming
   - System Design Primer: Design concepts
   - Glassdoor: Company reviews and questions
""",
                keywords=["interview", "preparation", "coding", "behavioral", "job"],
                difficulty="Intermediate",
            )
        )

        # Cloud Platform Documents
        self.add_document(
            KnowledgeDocument(
                title="Cloud Computing Basics",
                category="Cloud",
                content="""
Cloud Computing Basics:

1. Types of Cloud Services:
   - IaaS (Infrastructure as a Service): AWS EC2, Azure VM
   - PaaS (Platform as a Service): AWS RDS, Heroku
   - SaaS (Software as a Service): Google Workspace, Salesforce

2. Cloud Deployment Models:
   - Public Cloud: Available to the public (AWS, Azure, GCP)
   - Private Cloud: Organization-specific
   - Hybrid Cloud: Mix of public and private
   - Multi-Cloud: Multiple cloud providers

3. Major Cloud Providers:
   - AWS (Amazon Web Services)
   - Microsoft Azure
   - Google Cloud Platform (GCP)
   - IBM Cloud

4. AWS Essential Services:
   - EC2: Virtual servers
   - S3: Object storage
   - RDS: Managed databases
   - Lambda: Serverless computing
   - CloudFront: Content delivery network
   - DynamoDB: NoSQL database
   - SQS: Message queue

5. Key Concepts:
   - Scalability: Handle increased load
   - High Availability: System always operational
   - Durability: Data protection
   - Latency: Response time
   - Throughput: Data transfer rate

6. Security in Cloud:
   - IAM (Identity and Access Management)
   - Encryption
   - VPC (Virtual Private Cloud)
   - Security groups
   - Regular backups
   - Compliance standards

7. Cost Optimization:
   - Use spot instances
   - Auto-scaling
   - Reserved instances
   - Monitor usage
   - Clean up unused resources
""",
                keywords=["cloud", "AWS", "Azure", "GCP", "infrastructure", "deployment"],
                difficulty="Intermediate",
            )
        )

        # Data Structures & Algorithms
        self.add_document(
            KnowledgeDocument(
                title="Essential Data Structures",
                category="Data Structures",
                content="""
Essential Data Structures:

1. Arrays and Lists:
   - Order: O(1) access, O(n) insertion/deletion
   - Use cases: Store sequential data
   - Python: list, tuple
   - Java: ArrayList, Array

2. Linked Lists:
   - Single Linked List: Node -> Node -> Node
   - Doubly Linked List: Node <-> Node <-> Node
   - Operations: O(n) access, O(1) insertion/deletion
   - Use cases: Queue, Stack implementation

3. Stacks:
   - LIFO (Last In First Out)
   - Operations: Push, Pop, Peek
   - Applications: Browser history, undo/redo

4. Queues:
   - FIFO (First In First Out)
   - Operations: Enqueue, Dequeue
   - Applications: Task scheduling, BFS

5. Hash Tables / Hash Maps:
   - Average: O(1) operations
   - Worst case: O(n)
   - Use cases: Fast lookups, caching
   - Python: dict, Java: HashMap

6. Trees:
   - Binary Tree: At most 2 children per node
   - BST (Binary Search Tree): Left < Parent < Right
   - AVL Tree: Balanced BST
   - B-Tree: Multiple children per node
   - Applications: Databases, file systems

7. Graphs:
   - Nodes and edges
   - Directed and undirected
   - Weighted and unweighted
   - Applications: Social networks, GPS navigation

8. Complexity Analysis:
   - Time Complexity: How many operations
   - Space Complexity: How much memory
   - Big O Notation: O(1), O(log n), O(n), O(n²), O(2^n)
""",
                keywords=["data structures", "arrays", "trees", "graphs", "algorithms"],
                difficulty="Intermediate",
            )
        )

        # Internship Preparation
        self.add_document(
            KnowledgeDocument(
                title="Internship Preparation Checklist",
                category="Internship Preparation",
                content="""
Internship Preparation Checklist:

1. Before Applying:
   - ✓ Build 2-3 strong projects on GitHub
   - ✓ Create professional GitHub profile
   - ✓ Write a compelling resume
   - ✓ Research companies and roles
   - ✓ Practice coding problems (50+ problems)
   - ✓ Prepare elevator pitch

2. Resume Essentials:
   - ✓ Clear, concise format
   - ✓ Quantify achievements
   - ✓ Include relevant projects
   - ✓ List technical skills
   - ✓ Add links (GitHub, Portfolio, LinkedIn)
   - ✓ No grammar or spelling mistakes

3. Application Strategy:
   - ✓ Customize resume for each application
   - ✓ Write tailored cover letters
   - ✓ Apply to 10-20 positions per week
   - ✓ Track all applications
   - ✓ Follow up after 2 weeks

4. Technical Preparation:
   - ✓ Practice LeetCode Medium problems
   - ✓ Review data structures and algorithms
   - ✓ Study the company's tech stack
   - ✓ Understand system design basics
   - ✓ Practice explaining code to others

5. Interview Preparation:
   - ✓ Research the company
   - ✓ Prepare questions to ask
   - ✓ Practice mock interviews
   - ✓ Record yourself solving problems
   - ✓ Test your setup (webcam, mic, internet)

6. During Internship:
   - ✓ Build meaningful projects
   - ✓ Document your learning
   - ✓ Network with team members
   - ✓ Ask for feedback
   - ✓ Maintain professional conduct
   - ✓ Keep in touch with mentors

7. Resources:
   - LeetCode: Coding practice
   - GeeksforGeeks: Tutorials
   - GitHub: Portfolio projects
   - LinkedIn: Networking
   - YouTube: Interview prep videos
   - Glassdoor: Company insights

8. Timeline:
   - 6 months before: Build projects
   - 3 months before: Start applying
   - 1 month before: Interview prep
   - Interview phase: Mock interviews
   - After offer: Negotiate and prepare
""",
                keywords=["internship", "preparation", "checklist", "application", "interview"],
                difficulty="Beginner",
            )
        )

    def add_document(self, document: KnowledgeDocument):
        """Add a document to the knowledge base"""
        self.documents.append(document)

    def search_by_keywords(self, keywords: list[str], limit: int = 3) -> list[KnowledgeDocument]:
        """Search for documents by keywords"""
        matched_docs = []

        for doc in self.documents:
            doc_keywords_lower = [k.lower() for k in doc.keywords]
            for keyword in keywords:
                if keyword.lower() in doc_keywords_lower:
                    matched_docs.append(doc)
                    break

        return matched_docs[:limit]

    def search_by_category(self, category: str) -> list[KnowledgeDocument]:
        """Get all documents in a category"""
        return [doc for doc in self.documents if doc.category.lower() == category.lower()]

    def search_by_title(self, title: str) -> Optional[KnowledgeDocument]:
        """Find a document by title"""
        for doc in self.documents:
            if doc.title.lower() == title.lower():
                return doc
        return None

    def get_all_categories(self) -> list[str]:
        """Get all available categories"""
        categories = set()
        for doc in self.documents:
            categories.add(doc.category)
        return sorted(list(categories))

    def get_all_documents(self) -> list[KnowledgeDocument]:
        """Get all documents"""
        return self.documents

    def get_documents_by_difficulty(self, difficulty: str) -> list[KnowledgeDocument]:
        """Get documents by difficulty level"""
        return [doc for doc in self.documents if doc.difficulty.lower() == difficulty.lower()]


# Initialize global knowledge base instance
kb = KnowledgeBase()
