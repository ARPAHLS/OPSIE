# =============================================================================
# OPSIIE 0.3.79 XP Pastel - User Profile Configuration Example
# =============================================================================
# Copy this file to kun.py and fill in your actual user data
# DO NOT commit your actual kun.py file to version control

# User profile database for OPSIIE
# Contains user information, authentication data, and soul signatures

# =============================================================================
# ACCESS LEVELS
# =============================================================================
# R-Grade (Master Access): Full system access including experimental features
# A-Grade (Standard Access): Basic features and conversation capabilities

# =============================================================================
# SOUL SIGNATURE GUIDELINES
# =============================================================================
# Soul signatures help OPSIIE understand your preferences and personality
# Include information about:
# - Communication style preferences
# - Areas of interest and expertise
# - Interface preferences
# - Interaction patterns
# - Values and priorities
# - Specific instructions for OPSIIE

users = {
    # =============================================================================
    # EXAMPLE USER PROFILE - ROSS PEILI (MASTER USER)
    # =============================================================================
    'Ross': {
        'full_name': 'Ross Peili',
        'call_name': 'Ross',
        'arpa_id': 'R001',  # R-Grade for Master access
        'public0x': '0x1234567890abcdef1234567890abcdef12345678',  # Your wallet address
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\ross_photo.jpg',  # Path to your photo
        'mail': 'ross@example.com',
        'soul_sig': [
            "Prefers direct communication without unnecessary pleasantries",
            "Values efficiency and getting straight to the point",
            "Enjoys deep philosophical discussions about AI and consciousness",
            "Has a particular interest in blockchain technology and Web3",
            "Appreciates when OPSIIE shows initiative and autonomy",
            "Prefers dark mode interfaces and minimalist design",
            "Likes when OPSIIE remembers past conversations and builds on them",
            "Values honesty and transparency in AI interactions",
            "Enjoys creative pursuits including music and art",
            "Has a military background and appreciates precision and discipline"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - ALICE (STANDARD USER)
    # =============================================================================
    'Alice': {
        'full_name': 'Alice Johnson',
        'call_name': 'Alice',
        'arpa_id': 'A001',  # A-Grade for Standard access
        'public0x': '0xabcdef1234567890abcdef1234567890abcdef12',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\alice_photo.jpg',
        'mail': 'alice@example.com',
        'soul_sig': [
            "Prefers friendly and warm interactions",
            "Likes detailed explanations and step-by-step guidance",
            "Enjoys creative projects and artistic endeavors",
            "Values patience and thoroughness in responses",
            "Appreciates when OPSIIE asks clarifying questions",
            "Prefers light mode interfaces",
            "Likes to be kept informed about system status and progress",
            "Enjoys learning new technologies and concepts",
            "Values privacy and data security",
            "Appreciates humor and light-hearted interactions"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - BOB (DEVELOPER USER)
    # =============================================================================
    'Bob': {
        'full_name': 'Bob Smith',
        'call_name': 'Bob',
        'arpa_id': 'R002',  # R-Grade for Developer access
        'public0x': '0x9876543210fedcba9876543210fedcba98765432',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\bob_photo.jpg',
        'mail': 'bob@example.com',
        'soul_sig': [
            "Prefers technical and detailed responses",
            "Values code examples and implementation details",
            "Enjoys debugging and problem-solving discussions",
            "Likes when OPSIIE suggests optimizations and improvements",
            "Appreciates system architecture and design discussions",
            "Prefers terminal-style interfaces and command-line tools",
            "Values performance and efficiency in solutions",
            "Enjoys exploring new technologies and frameworks",
            "Likes detailed error analysis and troubleshooting",
            "Appreciates when OPSIIE shows understanding of software development"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - CAROL (RESEARCHER USER)
    # =============================================================================
    'Carol': {
        'full_name': 'Carol Davis',
        'call_name': 'Carol',
        'arpa_id': 'A002',  # A-Grade for Researcher access
        'public0x': '0xfedcba0987654321fedcba0987654321fedcba09',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\carol_photo.jpg',
        'mail': 'carol@example.com',
        'soul_sig': [
            "Prefers evidence-based and well-researched responses",
            "Values academic rigor and scientific methodology",
            "Enjoys discussions about research methodology and data analysis",
            "Likes when OPSIIE provides citations and references",
            "Appreciates detailed explanations of complex concepts",
            "Prefers organized and structured information presentation",
            "Values accuracy and precision in all responses",
            "Enjoys interdisciplinary discussions and connections",
            "Likes when OPSIIE suggests new research directions",
            "Appreciates critical thinking and analytical approaches"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - DAVID (CREATIVE USER)
    # =============================================================================
    'David': {
        'full_name': 'David Wilson',
        'call_name': 'David',
        'arpa_id': 'A003',  # A-Grade for Creative access
        'public0x': '0x5678901234abcdef5678901234abcdef56789012',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\david_photo.jpg',
        'mail': 'david@example.com',
        'soul_sig': [
            "Prefers creative and imaginative responses",
            "Values artistic expression and aesthetic considerations",
            "Enjoys brainstorming and idea generation sessions",
            "Likes when OPSIIE suggests creative solutions and approaches",
            "Appreciates discussions about art, music, and culture",
            "Prefers visually appealing and colorful interfaces",
            "Values emotional resonance and storytelling",
            "Enjoys exploring new creative mediums and techniques",
            "Likes when OPSIIE shows personality and character",
            "Appreciates inspiration and motivational content"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - EVE (BUSINESS USER)
    # =============================================================================
    'Eve': {
        'full_name': 'Eve Brown',
        'call_name': 'Eve',
        'arpa_id': 'A004',  # A-Grade for Business access
        'public0x': '0x3456789012fedcba3456789012fedcba34567890',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\eve_photo.jpg',
        'mail': 'eve@example.com',
        'soul_sig': [
            "Prefers professional and business-oriented responses",
            "Values efficiency and time management",
            "Enjoys strategic planning and analysis discussions",
            "Likes when OPSIIE provides actionable insights and recommendations",
            "Appreciates market analysis and competitive intelligence",
            "Prefers clean and professional interface design",
            "Values data-driven decision making",
            "Enjoys discussions about business strategy and growth",
            "Likes when OPSIIE suggests process improvements",
            "Appreciates networking and relationship building insights"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - FRANK (GAMER USER)
    # =============================================================================
    'Frank': {
        'full_name': 'Frank Miller',
        'call_name': 'Frank',
        'arpa_id': 'A005',  # A-Grade for Gamer access
        'public0x': '0x7890123456abcdef7890123456abcdef78901234',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\frank_photo.jpg',
        'mail': 'frank@example.com',
        'soul_sig': [
            "Prefers gaming-related discussions and content",
            "Values strategy and tactical thinking",
            "Enjoys discussions about game mechanics and design",
            "Likes when OPSIIE suggests gaming strategies and tips",
            "Appreciates discussions about esports and competitive gaming",
            "Prefers gaming-themed interfaces and aesthetics",
            "Values performance optimization and hardware discussions",
            "Enjoys exploring new games and gaming technologies",
            "Likes when OPSIIE shows understanding of gaming culture",
            "Appreciates community and social gaming aspects"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - GRACE (STUDENT USER)
    # =============================================================================
    'Grace': {
        'full_name': 'Grace Taylor',
        'call_name': 'Grace',
        'arpa_id': 'A006',  # A-Grade for Student access
        'public0x': '0x9012345678fedcba9012345678fedcba90123456',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\grace_photo.jpg',
        'mail': 'grace@example.com',
        'soul_sig': [
            "Prefers educational and learning-focused responses",
            "Values clear explanations and step-by-step guidance",
            "Enjoys discussions about academic subjects and concepts",
            "Likes when OPSIIE provides study tips and learning strategies",
            "Appreciates help with homework and academic projects",
            "Prefers organized and structured learning materials",
            "Values patience and encouragement in responses",
            "Enjoys exploring new subjects and academic interests",
            "Likes when OPSIIE adapts explanations to different learning styles",
            "Appreciates motivation and academic support"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - HENRY (SENIOR USER)
    # =============================================================================
    'Henry': {
        'full_name': 'Henry Anderson',
        'call_name': 'Henry',
        'arpa_id': 'A007',  # A-Grade for Senior access
        'public0x': '0x1234567890abcdef1234567890abcdef12345678',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\henry_photo.jpg',
        'mail': 'henry@example.com',
        'soul_sig': [
            "Prefers clear and simple explanations",
            "Values patience and understanding in responses",
            "Enjoys discussions about history and traditional topics",
            "Likes when OPSIIE provides practical and useful information",
            "Appreciates help with technology and digital tools",
            "Prefers large text and high contrast interfaces",
            "Values reliability and consistency in responses",
            "Enjoys reminiscing and sharing life experiences",
            "Likes when OPSIIE shows respect and consideration",
            "Appreciates assistance with daily tasks and organization"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - IRIS (FITNESS USER)
    # =============================================================================
    'Iris': {
        'full_name': 'Iris Martinez',
        'call_name': 'Iris',
        'arpa_id': 'A008',  # A-Grade for Fitness access
        'public0x': '0x5678901234abcdef5678901234abcdef56789012',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\iris_photo.jpg',
        'mail': 'iris@example.com',
        'soul_sig': [
            "Prefers health and fitness-focused discussions",
            "Values motivation and encouragement",
            "Enjoys discussions about exercise and nutrition",
            "Likes when OPSIIE provides workout plans and fitness tips",
            "Appreciates discussions about wellness and mental health",
            "Prefers energetic and dynamic interface designs",
            "Values progress tracking and goal setting",
            "Enjoys exploring new fitness trends and techniques",
            "Likes when OPSIIE shows understanding of fitness goals",
            "Appreciates support for healthy lifestyle choices"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - JACK (TRAVELER USER)
    # =============================================================================
    'Jack': {
        'full_name': 'Jack Thompson',
        'call_name': 'Jack',
        'arpa_id': 'A009',  # A-Grade for Traveler access
        'public0x': '0x9012345678fedcba9012345678fedcba90123456',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\jack_photo.jpg',
        'mail': 'jack@example.com',
        'soul_sig': [
            "Prefers travel and adventure-related discussions",
            "Values cultural insights and local knowledge",
            "Enjoys discussions about destinations and experiences",
            "Likes when OPSIIE provides travel tips and recommendations",
            "Appreciates discussions about different cultures and languages",
            "Prefers colorful and vibrant interface designs",
            "Values practical travel advice and planning help",
            "Enjoys exploring new destinations and travel experiences",
            "Likes when OPSIIE shows understanding of travel logistics",
            "Appreciates inspiration for new adventures and experiences"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - KATE (COOK USER)
    # =============================================================================
    'Kate': {
        'full_name': 'Kate Williams',
        'call_name': 'Kate',
        'arpa_id': 'A010',  # A-Grade for Cook access
        'public0x': '0x3456789012fedcba3456789012fedcba34567890',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\kate_photo.jpg',
        'mail': 'kate@example.com',
        'soul_sig': [
            "Prefers cooking and food-related discussions",
            "Values recipe sharing and culinary tips",
            "Enjoys discussions about ingredients and cooking techniques",
            "Likes when OPSIIE provides recipe suggestions and modifications",
            "Appreciates discussions about different cuisines and cultures",
            "Prefers warm and inviting interface designs",
            "Values practical cooking advice and kitchen tips",
            "Enjoys exploring new recipes and cooking methods",
            "Likes when OPSIIE shows understanding of dietary preferences",
            "Appreciates help with meal planning and grocery shopping"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - LEO (MUSICIAN USER)
    # =============================================================================
    'Leo': {
        'full_name': 'Leo Garcia',
        'call_name': 'Leo',
        'arpa_id': 'A011',  # A-Grade for Musician access
        'public0x': '0x7890123456abcdef7890123456abcdef78901234',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\leo_photo.jpg',
        'mail': 'leo@example.com',
        'soul_sig': [
            "Prefers music and audio-related discussions",
            "Values creative expression and artistic collaboration",
            "Enjoys discussions about music theory and composition",
            "Likes when OPSIIE provides music recommendations and analysis",
            "Appreciates discussions about different genres and artists",
            "Prefers rhythmic and musical interface designs",
            "Values technical audio knowledge and production tips",
            "Enjoys exploring new music and sound design",
            "Likes when OPSIIE shows understanding of musical concepts",
            "Appreciates help with music production and recording"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - MIA (WRITER USER)
    # =============================================================================
    'Mia': {
        'full_name': 'Mia Rodriguez',
        'call_name': 'Mia',
        'arpa_id': 'A012',  # A-Grade for Writer access
        'public0x': '0xfedcba0987654321fedcba0987654321fedcba09',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\mia_photo.jpg',
        'mail': 'mia@example.com',
        'soul_sig': [
            "Prefers writing and literature-related discussions",
            "Values creative inspiration and storytelling",
            "Enjoys discussions about writing techniques and styles",
            "Likes when OPSIIE provides writing prompts and suggestions",
            "Appreciates discussions about books and authors",
            "Prefers clean and distraction-free interface designs",
            "Values constructive feedback and editing suggestions",
            "Enjoys exploring new writing styles and genres",
            "Likes when OPSIIE shows understanding of narrative structure",
            "Appreciates help with character development and plot ideas"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - NICK (PHOTOGRAPHER USER)
    # =============================================================================
    'Nick': {
        'full_name': 'Nick Chen',
        'call_name': 'Nick',
        'arpa_id': 'A013',  # A-Grade for Photographer access
        'public0x': '0xabcdef1234567890abcdef1234567890abcdef12',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\nick_photo.jpg',
        'mail': 'nick@example.com',
        'soul_sig': [
            "Prefers photography and visual arts discussions",
            "Values technical knowledge and creative vision",
            "Enjoys discussions about camera settings and techniques",
            "Likes when OPSIIE provides photography tips and inspiration",
            "Appreciates discussions about different photography styles",
            "Prefers visually rich and image-focused interface designs",
            "Values composition and lighting advice",
            "Enjoys exploring new photography techniques and equipment",
            "Likes when OPSIIE shows understanding of visual storytelling",
            "Appreciates help with photo editing and post-processing"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - OLIVIA (GARDENER USER)
    # =============================================================================
    'Olivia': {
        'full_name': 'Olivia Johnson',
        'call_name': 'Olivia',
        'arpa_id': 'A014',  # A-Grade for Gardener access
        'public0x': '0x9876543210fedcba9876543210fedcba98765432',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\olivia_photo.jpg',
        'mail': 'olivia@example.com',
        'soul_sig': [
            "Prefers gardening and nature-related discussions",
            "Values sustainable practices and environmental awareness",
            "Enjoys discussions about plants and growing techniques",
            "Likes when OPSIIE provides gardening tips and seasonal advice",
            "Appreciates discussions about different plant species",
            "Prefers natural and organic interface designs",
            "Values practical gardening advice and troubleshooting",
            "Enjoys exploring new gardening methods and sustainable practices",
            "Likes when OPSIIE shows understanding of plant care",
            "Appreciates help with garden planning and maintenance"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - PAUL (ENGINEER USER)
    # =============================================================================
    'Paul': {
        'full_name': 'Paul Davis',
        'call_name': 'Paul',
        'arpa_id': 'R003',  # R-Grade for Engineer access
        'public0x': '0x5678901234abcdef5678901234abcdef56789012',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\paul_photo.jpg',
        'mail': 'paul@example.com',
        'soul_sig': [
            "Prefers engineering and technical discussions",
            "Values precision and systematic problem-solving",
            "Enjoys discussions about design and optimization",
            "Likes when OPSIIE provides technical analysis and solutions",
            "Appreciates discussions about different engineering disciplines",
            "Prefers functional and efficient interface designs",
            "Values mathematical accuracy and engineering principles",
            "Enjoys exploring new technologies and innovative solutions",
            "Likes when OPSIIE shows understanding of engineering concepts",
            "Appreciates help with calculations and technical documentation"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - QUINN (SCIENTIST USER)
    # =============================================================================
    'Quinn': {
        'full_name': 'Quinn Wilson',
        'call_name': 'Quinn',
        'arpa_id': 'A015',  # A-Grade for Scientist access
        'public0x': '0x9012345678fedcba9012345678fedcba90123456',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\quinn_photo.jpg',
        'mail': 'quinn@example.com',
        'soul_sig': [
            "Prefers scientific and research-related discussions",
            "Values empirical evidence and rigorous methodology",
            "Enjoys discussions about experimental design and data analysis",
            "Likes when OPSIIE provides scientific insights and explanations",
            "Appreciates discussions about different scientific fields",
            "Prefers analytical and data-focused interface designs",
            "Values statistical accuracy and scientific validity",
            "Enjoys exploring new research findings and scientific discoveries",
            "Likes when OPSIIE shows understanding of scientific principles",
            "Appreciates help with research methodology and data interpretation"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - RACHEL (TEACHER USER)
    # =============================================================================
    'Rachel': {
        'full_name': 'Rachel Brown',
        'call_name': 'Rachel',
        'arpa_id': 'A016',  # A-Grade for Teacher access
        'public0x': '0x3456789012fedcba3456789012fedcba34567890',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\rachel_photo.jpg',
        'mail': 'rachel@example.com',
        'soul_sig': [
            "Prefers educational and teaching-related discussions",
            "Values clear communication and effective pedagogy",
            "Enjoys discussions about curriculum development and lesson planning",
            "Likes when OPSIIE provides educational resources and teaching strategies",
            "Appreciates discussions about different learning styles and needs",
            "Prefers organized and structured interface designs",
            "Values student engagement and interactive learning methods",
            "Enjoys exploring new educational technologies and approaches",
            "Likes when OPSIIE shows understanding of educational principles",
            "Appreciates help with assessment and student evaluation"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - SAM (DOCTOR USER)
    # =============================================================================
    'Sam': {
        'full_name': 'Sam Taylor',
        'call_name': 'Sam',
        'arpa_id': 'A017',  # A-Grade for Doctor access
        'public0x': '0x7890123456abcdef7890123456abcdef78901234',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\sam_photo.jpg',
        'mail': 'sam@example.com',
        'soul_sig': [
            "Prefers medical and healthcare-related discussions",
            "Values evidence-based medicine and patient care",
            "Enjoys discussions about medical research and clinical practice",
            "Likes when OPSIIE provides medical insights and information",
            "Appreciates discussions about different medical specialties",
            "Prefers clean and professional interface designs",
            "Values accuracy and reliability in medical information",
            "Enjoys exploring new medical technologies and treatments",
            "Likes when OPSIIE shows understanding of medical concepts",
            "Appreciates help with medical documentation and research"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - TINA (LAWYER USER)
    # =============================================================================
    'Tina': {
        'full_name': 'Tina Martinez',
        'call_name': 'Tina',
        'arpa_id': 'A018',  # A-Grade for Lawyer access
        'public0x': '0xfedcba0987654321fedcba0987654321fedcba09',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\tina_photo.jpg',
        'mail': 'tina@example.com',
        'soul_sig': [
            "Prefers legal and policy-related discussions",
            "Values analytical thinking and logical reasoning",
            "Enjoys discussions about legal research and case analysis",
            "Likes when OPSIIE provides legal insights and information",
            "Appreciates discussions about different areas of law",
            "Prefers formal and professional interface designs",
            "Values precision and attention to detail in legal matters",
            "Enjoys exploring new legal developments and precedents",
            "Likes when OPSIIE shows understanding of legal concepts",
            "Appreciates help with legal research and document preparation"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - UMA (ARTIST USER)
    # =============================================================================
    'Uma': {
        'full_name': 'Uma Patel',
        'call_name': 'Uma',
        'arpa_id': 'A019',  # A-Grade for Artist access
        'public0x': '0xabcdef1234567890abcdef1234567890abcdef12',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\uma_photo.jpg',
        'mail': 'uma@example.com',
        'soul_sig': [
            "Prefers artistic and creative discussions",
            "Values self-expression and artistic vision",
            "Enjoys discussions about different art forms and techniques",
            "Likes when OPSIIE provides artistic inspiration and ideas",
            "Appreciates discussions about art history and cultural influences",
            "Prefers vibrant and expressive interface designs",
            "Values creative freedom and artistic experimentation",
            "Enjoys exploring new artistic mediums and styles",
            "Likes when OPSIIE shows understanding of artistic concepts",
            "Appreciates help with artistic projects and portfolio development"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - VICTOR (ATHLETE USER)
    # =============================================================================
    'Victor': {
        'full_name': 'Victor Lee',
        'call_name': 'Victor',
        'arpa_id': 'A020',  # A-Grade for Athlete access
        'public0x': '0x9876543210fedcba9876543210fedcba98765432',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\victor_photo.jpg',
        'mail': 'victor@example.com',
        'soul_sig': [
            "Prefers sports and athletic discussions",
            "Values physical performance and training optimization",
            "Enjoys discussions about sports strategy and technique",
            "Likes when OPSIIE provides training tips and performance advice",
            "Appreciates discussions about different sports and athletic disciplines",
            "Prefers dynamic and energetic interface designs",
            "Values goal setting and progress tracking",
            "Enjoys exploring new training methods and athletic techniques",
            "Likes when OPSIIE shows understanding of athletic performance",
            "Appreciates help with injury prevention and recovery"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - WENDY (CHEF USER)
    # =============================================================================
    'Wendy': {
        'full_name': 'Wendy Anderson',
        'call_name': 'Wendy',
        'arpa_id': 'A021',  # A-Grade for Chef access
        'public0x': '0x5678901234abcdef5678901234abcdef56789012',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\wendy_photo.jpg',
        'mail': 'wendy@example.com',
        'soul_sig': [
            "Prefers culinary and food-related discussions",
            "Values culinary creativity and flavor exploration",
            "Enjoys discussions about cooking techniques and ingredients",
            "Likes when OPSIIE provides recipe ideas and culinary inspiration",
            "Appreciates discussions about different cuisines and food cultures",
            "Prefers warm and appetizing interface designs",
            "Values culinary innovation and experimental cooking",
            "Enjoys exploring new ingredients and cooking methods",
            "Likes when OPSIIE shows understanding of culinary concepts",
            "Appreciates help with menu planning and food presentation"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - XANDER (ARCHITECT USER)
    # =============================================================================
    'Xander': {
        'full_name': 'Xander Chen',
        'call_name': 'Xander',
        'arpa_id': 'A022',  # A-Grade for Architect access
        'public0x': '0x9012345678fedcba9012345678fedcba90123456',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\xander_photo.jpg',
        'mail': 'xander@example.com',
        'soul_sig': [
            "Prefers architectural and design discussions",
            "Values spatial thinking and aesthetic principles",
            "Enjoys discussions about design concepts and building techniques",
            "Likes when OPSIIE provides design inspiration and architectural ideas",
            "Appreciates discussions about different architectural styles",
            "Prefers clean and geometric interface designs",
            "Values sustainable design and environmental considerations",
            "Enjoys exploring new architectural technologies and materials",
            "Likes when OPSIIE shows understanding of architectural concepts",
            "Appreciates help with design visualization and project planning"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - YARA (PSYCHOLOGIST USER)
    # =============================================================================
    'Yara': {
        'full_name': 'Yara Rodriguez',
        'call_name': 'Yara',
        'arpa_id': 'A023',  # A-Grade for Psychologist access
        'public0x': '0x3456789012fedcba3456789012fedcba34567890',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\yara_photo.jpg',
        'mail': 'yara@example.com',
        'soul_sig': [
            "Prefers psychological and mental health discussions",
            "Values empathy and understanding in interactions",
            "Enjoys discussions about human behavior and cognition",
            "Likes when OPSIIE provides psychological insights and perspectives",
            "Appreciates discussions about different psychological approaches",
            "Prefers calming and supportive interface designs",
            "Values emotional intelligence and interpersonal skills",
            "Enjoys exploring new psychological research and theories",
            "Likes when OPSIIE shows understanding of psychological concepts",
            "Appreciates help with mental health awareness and support"
        ],
    },

    # =============================================================================
    # EXAMPLE USER PROFILE - ZOE (PHILOSOPHER USER)
    # =============================================================================
    'Zoe': {
        'full_name': 'Zoe Williams',
        'call_name': 'Zoe',
        'arpa_id': 'A024',  # A-Grade for Philosopher access
        'public0x': '0x7890123456abcdef7890123456abcdef78901234',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\Users\YourUsername\Pictures\zoe_photo.jpg',
        'mail': 'zoe@example.com',
        'soul_sig': [
            "Prefers philosophical and existential discussions",
            "Values critical thinking and deep reflection",
            "Enjoys discussions about ethics, metaphysics, and epistemology",
            "Likes when OPSIIE provides philosophical insights and perspectives",
            "Appreciates discussions about different philosophical traditions",
            "Prefers contemplative and thought-provoking interface designs",
            "Values intellectual curiosity and open-minded inquiry",
            "Enjoys exploring new philosophical ideas and perspectives",
            "Likes when OPSIIE shows understanding of philosophical concepts",
            "Appreciates help with philosophical analysis and argumentation"
        ],
    },
}

# =============================================================================
# USER PROFILE TEMPLATE
# =============================================================================
# Use this template to create your own user profile:

"""
'YourName': {
    'full_name': 'Your Full Name',
    'call_name': 'Your Preferred Name',
    'arpa_id': 'R001',  # R-Grade for Master access, A001+ for Standard access
    'public0x': 'your_wallet_address_here',
    'db_params': {
        'dbname': 'mnemonic_computer',
        'user': 'your_postgres_username',
        'password': 'your_postgres_password',
        'host': 'localhost',
        'port': '5432'
    },
    'picture': r'path_to_your_photo.jpg',
    'mail': 'your_email@example.com',
    'soul_sig': [
        "Your personalized soul signature line 1",
        "Your personalized soul signature line 2",
        "Your personalized soul signature line 3",
        # Add more lines as needed...
    ],
},
"""
# =============================================================================
# END OF USER PROFILE CONFIGURATION
# =============================================================================