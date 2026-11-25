"""Database seed: learning paths, modules, lessons, quizzes, challenges, quests, achievements, projects."""
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.learning import (
    LearningPath, Module, Lesson, Quiz, Question, CodingChallenge
)
from app.models.gamification import Achievement, Quest
from app.models.project import Project


def seed_database(db: Session) -> None:
    if db.scalar(select(LearningPath)):
        return  # Already seeded

    # ── Learning Paths ────────────────────────────────────────────────────────
    paths_data = [
        {"slug": "python-foundations", "title": "Python Foundations", "subtitle": "Master Python from scratch",
         "description": "Build a solid Python programming foundation through hands-on exercises, interactive visualizations, and real coding challenges. From variables to OOP.", "difficulty": "beginner", "icon_name": "Code2", "accent_color": "blue", "estimated_hours": 20, "order_index": 1},
        {"slug": "data-science", "title": "Data Science", "subtitle": "Analyze data like a scientist",
         "description": "Learn NumPy, Pandas, statistics, data cleaning, EDA, and visualization to extract insights from real-world datasets.", "difficulty": "beginner", "icon_name": "BarChart3", "accent_color": "green", "estimated_hours": 25, "order_index": 2},
        {"slug": "machine-learning", "title": "Machine Learning", "subtitle": "Build predictive models",
         "description": "Master supervised and unsupervised learning algorithms, feature engineering, model evaluation, and ensemble methods with scikit-learn.", "difficulty": "intermediate", "icon_name": "Brain", "accent_color": "purple", "estimated_hours": 35, "order_index": 3},
        {"slug": "deep-learning", "title": "Deep Learning", "subtitle": "Neural networks from scratch",
         "description": "Understand neural networks mathematically and practically — from perceptrons to Transformers — using PyTorch.", "difficulty": "intermediate", "icon_name": "Network", "accent_color": "orange", "estimated_hours": 40, "order_index": 4},
        {"slug": "generative-ai", "title": "Generative AI", "subtitle": "Build with LLMs",
         "description": "Master large language models, prompt engineering, tokenization, embeddings, and fine-tuning to build AI-powered applications.", "difficulty": "advanced", "icon_name": "Sparkles", "accent_color": "violet", "estimated_hours": 30, "order_index": 5},
        {"slug": "ai-engineering", "title": "AI Engineering", "subtitle": "Deploy production AI systems",
         "description": "Build scalable AI systems with RAG pipelines, vector databases, LangChain, AI agents, and production deployment strategies.", "difficulty": "advanced", "icon_name": "Cpu", "accent_color": "indigo", "estimated_hours": 45, "order_index": 6},
    ]
    path_objs = {}
    for pd in paths_data:
        p = LearningPath(**pd)
        db.add(p)
        db.flush()
        path_objs[pd["slug"]] = p

    # ── Python Foundations Modules + Lessons ──────────────────────────────────
    py_modules = [
        {"slug": "intro-python", "title": "Introduction to Python", "description": "What Python is, why it's the #1 language for AI/ML, and how to run your first program.", "order_index": 1, "xp_reward": 80},
        {"slug": "variables-datatypes", "title": "Variables & Data Types", "description": "Integers, floats, strings, booleans — how Python stores and represents data.", "order_index": 2, "xp_reward": 80},
        {"slug": "control-flow", "title": "Control Flow", "description": "if/elif/else, for loops, while loops, break, continue — controlling program execution.", "order_index": 3, "xp_reward": 100},
        {"slug": "functions", "title": "Functions", "description": "Defining reusable code blocks, parameters, return values, scope, lambda, and *args/**kwargs.", "order_index": 4, "xp_reward": 100},
        {"slug": "data-structures", "title": "Data Structures", "description": "Lists, tuples, sets, dictionaries — Python's core collections for ML and data work.", "order_index": 5, "xp_reward": 120},
        {"slug": "oop", "title": "Object-Oriented Programming", "description": "Classes, objects, inheritance, encapsulation — structuring code the ML engineering way.", "order_index": 6, "xp_reward": 150},
        {"slug": "numpy-fundamentals", "title": "NumPy Fundamentals", "description": "Arrays, broadcasting, vectorized operations — the foundation of numerical computing in Python.", "order_index": 7, "xp_reward": 150},
        {"slug": "pandas-fundamentals", "title": "Pandas Fundamentals", "description": "DataFrames, Series, indexing, filtering, groupby — the essential toolkit for data manipulation.", "order_index": 8, "xp_reward": 150},
    ]

    py_lessons = {
        "intro-python": [
            {"slug": "what-is-python", "title": "What is Python?", "summary": "Python's history, philosophy, and why it dominates AI/ML", "order_index": 1, "xp_reward": 20, "estimated_minutes": 10,
             "learning_objectives": ["Understand Python's design philosophy", "Know why Python dominates AI/ML", "Run your first Python program"],
             "content_blocks": [
                 {"type": "text", "content": "Python is a high-level, interpreted programming language created by Guido van Rossum in 1991. Its philosophy is captured in the famous **Zen of Python**: *Beautiful is better than ugly. Explicit is better than implicit. Simple is better than complex.*"},
                 {"type": "code", "language": "python", "content": "# Your first Python program\nprint('Hello, AI World!')\n\n# Python reads like English\nname = 'Learnova'\nprint(f'Welcome to {name}!')\n\n# No semicolons, no curly braces\nfor i in range(5):\n    print(f'Count: {i}')"},
                 {"type": "callout", "variant": "info", "content": "Python is the #1 language for AI/ML because: (1) Clean readable syntax, (2) Massive ecosystem (NumPy, Pandas, TensorFlow, PyTorch), (3) Interactive development via Jupyter, (4) Huge community."},
                 {"type": "text", "content": "### Why Python for AI?\nEvery major ML framework — TensorFlow, PyTorch, scikit-learn, Hugging Face — has a Python API. Data scientists use Python to explore data, train models, and deploy predictions."},
             ],
             "key_terms": ["interpreter", "REPL", "variable", "statement", "expression"],
             "common_mistakes": ["Forgetting indentation (Python uses 4 spaces, not tabs)", "Using == instead of = for assignment", "Trying to run Python like C/Java with semicolons and braces"],
             "starter_code": "# Write your first Python program!\nprint('Hello, World!')\n\n# Try using variables\nmy_name = 'Your Name'\nprint(f'I am learning AI with {my_name}!')"},
            {"slug": "python-syntax", "title": "Python Syntax Essentials", "summary": "Comments, indentation, print, input — the building blocks", "order_index": 2, "xp_reward": 20, "estimated_minutes": 12,
             "learning_objectives": ["Write syntactically correct Python", "Use comments and docstrings", "Understand Python's indentation rules"],
             "content_blocks": [
                 {"type": "text", "content": "Python uses **indentation** (4 spaces) to define code blocks. This enforces readable code — a key reason Python became the language of science and AI."},
                 {"type": "code", "language": "python", "content": "# Single-line comment\n\n'''\nMulti-line comment / docstring\nUsed to document functions and classes\n'''\n\ndef greet(name):\n    \"\"\"Returns a greeting for the given name.\"\"\"\n    return f'Hello, {name}!'\n\nresult = greet('Ada Lovelace')\nprint(result)  # Hello, Ada Lovelace!"},
                 {"type": "callout", "variant": "warning", "content": "IndentationError is the most common beginner mistake. Always use 4 spaces — never mix tabs and spaces."},
             ],
             "key_terms": ["indentation", "comment", "docstring", "f-string", "whitespace"],
             "common_mistakes": ["Mixing tabs and spaces", "Forgetting the colon after if/for/def/class", "Incorrect indentation level"],
             "starter_code": "# Fix the indentation error:\ndef calculate_xp(lessons, challenges):\nxp = lessons * 20 + challenges * 40  # This line needs fixing!\nreturn xp\n\nprint(calculate_xp(5, 3))"},
        ],
        "variables-datatypes": [
            {"slug": "numbers-strings", "title": "Numbers & Strings", "summary": "int, float, str, bool — Python's primitive types", "order_index": 1, "xp_reward": 20, "estimated_minutes": 15,
             "learning_objectives": ["Use Python's numeric types", "Manipulate strings with methods", "Understand type coercion"],
             "content_blocks": [
                 {"type": "text", "content": "Python has 4 primitive data types: **int** (whole numbers), **float** (decimals), **str** (text), and **bool** (True/False). Unlike C/Java, Python is **dynamically typed** — you don't declare types."},
                 {"type": "code", "language": "python", "content": "# Integers\nlearner_xp = 1250\nlevel = 4\n\n# Floats — used constantly in ML (loss, accuracy, probabilities)\naccuracy = 0.9342\nlearning_rate = 0.001\n\n# Strings\npath_name = 'Machine Learning'\nmodel_name = \"GPT-4\"\n\n# Booleans — the result of comparisons\nis_trained = True\nhas_converged = False\n\n# Check types\nprint(type(learner_xp))   # <class 'int'>\nprint(type(accuracy))     # <class 'float'>\nprint(type(path_name))    # <class 'str'>"},
                 {"type": "code", "language": "python", "content": "# String operations — vital for NLP!\nsentence = 'Large Language Models are fascinating'\n\nprint(len(sentence))           # 38\nprint(sentence.upper())        # LARGE LANGUAGE MODELS...\nprint(sentence.split())        # ['Large', 'Language', ...]\nprint(sentence.startswith('L'))# True\nprint(sentence.replace('L', 'l'))  # lowercase L\n\n# String formatting\nxp = 1500\nprint(f'You have {xp} XP — Level {xp // 400}!')"},
                 {"type": "callout", "variant": "tip", "content": "In Machine Learning, floats are everywhere: loss = 0.0043, accuracy = 0.9876, probability = 0.73. Understanding float precision matters when comparing model outputs."},
             ],
             "key_terms": ["integer", "float", "string", "boolean", "dynamic typing", "f-string"],
             "common_mistakes": ["Dividing integers in Python 3 gives float by default (3/2 = 1.5, not 1)", "String immutability — strings cannot be modified in place", "Confusing = (assignment) with == (comparison)"],
             "starter_code": "# A data scientist's notebook\nmodel_name = 'Linear Regression'\ntrain_accuracy = 0.8734\ntest_accuracy = 0.8512\nn_features = 15\n\n# Print a formatted report\nprint(f'Model: {model_name}')\nprint(f'Train Accuracy: {train_accuracy:.2%}')\nprint(f'Test Accuracy: {test_accuracy:.2%}')\nprint(f'Features used: {n_features}')"},
        ],
        "control-flow": [
            {"slug": "if-elif-else", "title": "Conditionals: if / elif / else", "summary": "Make decisions in your programs", "order_index": 1, "xp_reward": 20, "estimated_minutes": 15,
             "learning_objectives": ["Write conditional logic", "Chain elif conditions", "Use nested conditionals"],
             "content_blocks": [
                 {"type": "text", "content": "Conditionals let programs **make decisions**. In ML, you use conditionals to check model performance, apply different preprocessing depending on data type, or implement early stopping."},
                 {"type": "code", "language": "python", "content": "# Classify model performance\ndef classify_model(accuracy):\n    if accuracy >= 0.95:\n        return 'Excellent'\n    elif accuracy >= 0.85:\n        return 'Good'\n    elif accuracy >= 0.70:\n        return 'Acceptable'\n    else:\n        return 'Needs improvement'\n\nfor acc in [0.97, 0.88, 0.72, 0.55]:\n    print(f'{acc:.0%} → {classify_model(acc)}')"},
                 {"type": "callout", "variant": "info", "content": "Ternary expression (one-liner): `label = 'spam' if score > 0.5 else 'ham'` — common in data preprocessing!"},
             ],
             "key_terms": ["conditional", "boolean expression", "comparison operator", "ternary", "truthy/falsy"],
             "common_mistakes": ["Using = instead of == in conditions", "Forgetting elif is one word (not 'else if')", "Comparing floats with == — use abs(a - b) < 1e-9 instead"],
             "starter_code": "# XP Level classifier\ndef get_level(xp):\n    # TODO: Return level 1-10 based on XP thresholds\n    # Level 1: 0+, Level 2: 150+, Level 3: 400+, Level 4: 800+\n    pass\n\nprint(get_level(0))    # 1\nprint(get_level(200))  # 2\nprint(get_level(900))  # 4"},
        ],
        "functions": [
            {"slug": "defining-functions", "title": "Defining Functions", "summary": "Reusable code blocks with parameters and return values", "order_index": 1, "xp_reward": 25, "estimated_minutes": 18,
             "learning_objectives": ["Define and call functions", "Use default parameters", "Understand *args and **kwargs"],
             "content_blocks": [
                 {"type": "text", "content": "Functions are the building blocks of ML pipelines. Every `sklearn` function, every PyTorch `forward()` method is a Python function. Mastering functions means mastering the language."},
                 {"type": "code", "language": "python", "content": "# Basic function\ndef euclidean_distance(p1, p2):\n    \"\"\"Compute Euclidean distance between two points.\"\"\"\n    return sum((a - b) ** 2 for a, b in zip(p1, p2)) ** 0.5\n\nd = euclidean_distance([1, 2], [4, 6])\nprint(f'Distance: {d:.2f}')  # 5.00\n\n# Default parameters\ndef normalize(values, method='minmax'):\n    if method == 'minmax':\n        mn, mx = min(values), max(values)\n        return [(v - mn) / (mx - mn) for v in values]\n    elif method == 'zscore':\n        mean = sum(values) / len(values)\n        std = (sum((v - mean)**2 for v in values) / len(values)) ** 0.5\n        return [(v - mean) / std for v in values]\n\ndata = [10, 20, 30, 40, 50]\nprint(normalize(data))             # minmax\nprint(normalize(data, 'zscore'))   # z-score"},
                 {"type": "code", "language": "python", "content": "# *args and **kwargs — used in PyTorch, sklearn, etc.\ndef train_model(*datasets, **hyperparams):\n    print(f'Training on {len(datasets)} datasets')\n    for key, val in hyperparams.items():\n        print(f'  {key} = {val}')\n\ntrain_model('train.csv', 'valid.csv',\n            lr=0.001, epochs=10, batch_size=32)"},
             ],
             "key_terms": ["function", "parameter", "argument", "return value", "default parameter", "*args", "**kwargs", "lambda"],
             "common_mistakes": ["Forgetting return (function returns None by default)", "Modifying mutable default arguments", "Confusing function definition vs function call"],
             "starter_code": "import math\n\ndef sigmoid(x):\n    \"\"\"Sigmoid activation function: 1 / (1 + e^-x)\"\"\"\n    # TODO: Implement sigmoid\n    pass\n\n# Test your implementation\nfor x in [-2, -1, 0, 1, 2]:\n    print(f'sigmoid({x}) = {sigmoid(x):.4f}')"},
        ],
        "data-structures": [
            {"slug": "lists-tuples", "title": "Lists & Tuples", "summary": "Python's ordered collections", "order_index": 1, "xp_reward": 25, "estimated_minutes": 18,
             "learning_objectives": ["Create and manipulate lists", "Understand list comprehensions", "Know when to use tuples vs lists"],
             "content_blocks": [
                 {"type": "text", "content": "Lists are Python's most versatile data structure. In ML, feature vectors, training batches, model predictions, and hyperparameter grids are all represented as lists or arrays."},
                 {"type": "code", "language": "python", "content": "# Lists in ML context\nfeatures = ['age', 'income', 'credit_score', 'employment_years']\npredictions = [0.82, 0.14, 0.95, 0.03, 0.67]\n\n# List comprehensions — elegant and fast\nhigh_confidence = [p for p in predictions if p > 0.5]\nprint(high_confidence)  # [0.82, 0.95, 0.67]\n\n# Enumerate — common in training loops\nfor idx, pred in enumerate(predictions):\n    label = 'positive' if pred > 0.5 else 'negative'\n    print(f'Sample {idx}: {label} ({pred:.2f})')\n\n# zip — pairing features with values\nsample = dict(zip(features, [35, 65000, 720, 8]))\nprint(sample)"},
                 {"type": "code", "language": "python", "content": "# Tuples — immutable, used for dimensions, coordinates, shapes\nimage_shape = (224, 224, 3)   # height, width, channels\ntrain_split = (0.7, 0.15, 0.15)  # train/val/test\n\nheight, width, channels = image_shape  # unpacking\nprint(f'Processing {height}x{width} RGB images')\n\n# Slicing — works on both lists and tuples\ndata = list(range(100))\ntrain = data[:70]\nval = data[70:85]\ntest = data[85:]"},
             ],
             "key_terms": ["list", "tuple", "index", "slice", "list comprehension", "enumerate", "zip", "unpacking"],
             "common_mistakes": ["Modifying a list while iterating over it", "Confusing list = [1,2] copy vs reference", "Using mutable default argument (def f(lst=[]) is a bug!)"],
             "starter_code": "# Count positives and negatives in a prediction array\npredictions = [0.82, 0.14, 0.95, 0.03, 0.67, 0.44, 0.91, 0.28]\n\n# Using list comprehension:\npositives = [p for p in predictions if p > 0.5]\nnegatives = [p for p in predictions if p <= 0.5]\n\nprint(f'Positive predictions: {len(positives)}')\nprint(f'Negative predictions: {len(negatives)}')\nprint(f'Class balance: {len(positives)/len(predictions):.0%} positive')"},
        ],
        "oop": [
            {"slug": "classes-objects", "title": "Classes & Objects", "summary": "Object-oriented programming fundamentals", "order_index": 1, "xp_reward": 30, "estimated_minutes": 25,
             "learning_objectives": ["Define classes with __init__", "Create objects and use methods", "Understand self and attributes"],
             "content_blocks": [
                 {"type": "text", "content": "Every scikit-learn model, every PyTorch `nn.Module`, every Pandas DataFrame is a **class**. Understanding OOP unlocks your ability to read and extend ML library source code."},
                 {"type": "code", "language": "python", "content": "class LinearRegressor:\n    \"\"\"A simple linear regression model: y = mx + b\"\"\"\n    \n    def __init__(self, learning_rate=0.01):\n        self.lr = learning_rate\n        self.weight = 0.0\n        self.bias = 0.0\n        self.history = []\n    \n    def predict(self, x):\n        return self.weight * x + self.bias\n    \n    def fit_step(self, x, y_true):\n        y_pred = self.predict(x)\n        error = y_pred - y_true\n        self.weight -= self.lr * error * x\n        self.bias -= self.lr * error\n        loss = error ** 2\n        self.history.append(loss)\n        return loss\n    \n    def __repr__(self):\n        return f'LinearRegressor(w={self.weight:.3f}, b={self.bias:.3f})'\n\n# Usage — same pattern as sklearn!\nmodel = LinearRegressor(learning_rate=0.1)\nfor _ in range(50):\n    model.fit_step(2.0, 5.0)\nprint(model)           # LinearRegressor(w=2.500, b=0.000)\nprint(model.predict(4))  # ~10.0"},
             ],
             "key_terms": ["class", "object", "instance", "__init__", "self", "method", "attribute", "encapsulation", "inheritance"],
             "common_mistakes": ["Forgetting self in method definition", "Calling method without parentheses", "Confusing class variables vs instance variables"],
             "starter_code": "class KNNClassifier:\n    def __init__(self, k=3):\n        self.k = k\n        self.X_train = []\n        self.y_train = []\n    \n    def fit(self, X, y):\n        self.X_train = X\n        self.y_train = y\n    \n    def _distance(self, a, b):\n        return sum((x - y)**2 for x, y in zip(a, b)) ** 0.5\n    \n    def predict(self, x):\n        # TODO: Find k nearest neighbors and return majority class\n        distances = [(self._distance(x, xi), yi) for xi, yi in zip(self.X_train, self.y_train)]\n        # Sort by distance and take k nearest\n        pass\n\n# Test\nclf = KNNClassifier(k=3)\nclf.fit([[1,1],[2,2],[3,3],[6,6],[7,7]], [0,0,0,1,1])\nprint(clf.predict([2.5, 2.5]))  # Should be 0"},
        ],
        "numpy-fundamentals": [
            {"slug": "numpy-arrays", "title": "NumPy Arrays", "summary": "The foundation of numerical computing in Python", "order_index": 1, "xp_reward": 30, "estimated_minutes": 20,
             "learning_objectives": ["Create NumPy arrays", "Understand broadcasting", "Perform vectorized operations"],
             "content_blocks": [
                 {"type": "text", "content": "NumPy is **the** library for numerical computing in Python. Every ML framework — PyTorch, TensorFlow, scikit-learn — builds on NumPy arrays. A NumPy operation runs in C, making it 100x faster than pure Python loops."},
                 {"type": "code", "language": "python", "content": "import numpy as np\n\n# Creating arrays\nfeatures = np.array([1.5, 2.3, 0.8, 4.1, 3.7])\nweights = np.zeros(5)\nbias = np.ones((3, 3))\nX = np.random.randn(100, 10)  # 100 samples, 10 features\n\nprint(f'Shape: {X.shape}')       # (100, 10)\nprint(f'Dtype: {X.dtype}')       # float64\nprint(f'Size: {X.size}')         # 1000\n\n# Vectorized operations — NO Python loops needed!\ny = features * 2 + 1\ndot = np.dot(features, weights)  # matrix multiply\nnorm = np.linalg.norm(features)  # vector magnitude\n\nprint(f'Normalized: {features / norm}')"},
                 {"type": "code", "language": "python", "content": "# Broadcasting — the magic of NumPy\nX = np.random.randn(100, 5)  # dataset: 100 rows, 5 features\nmean = X.mean(axis=0)        # mean per column: shape (5,)\nstd = X.std(axis=0)          # std per column:  shape (5,)\n\n# This is broadcasting! (100,5) - (5,) works automatically\nX_normalized = (X - mean) / std\nprint(f'Normalized mean: {X_normalized.mean(axis=0).round(10)}')  # ~zeros\nprint(f'Normalized std:  {X_normalized.std(axis=0).round(10)}')   # ~ones"},
                 {"type": "callout", "variant": "tip", "content": "Broadcasting rule: NumPy compares shapes element-wise from right to left. Dimensions must be equal or 1. This eliminates most explicit loops in ML code."},
             ],
             "key_terms": ["ndarray", "shape", "dtype", "broadcasting", "vectorization", "axis", "dot product"],
             "common_mistakes": ["Confusing shape (3,) vs (3,1) vs (1,3)", "Using Python loops instead of vectorized operations", "Forgetting axis parameter in mean/sum/std"],
             "starter_code": "import numpy as np\n\n# Implement softmax using NumPy (used in classification)\ndef softmax(logits):\n    \"\"\"\n    Softmax: e^x_i / sum(e^x_j) for all j\n    Numerically stable version subtracts max first.\n    \"\"\"\n    # TODO: Implement\n    pass\n\nlogits = np.array([2.0, 1.0, 0.1])\nprobs = softmax(logits)\nprint(probs)           # [0.659, 0.242, 0.099]\nprint(probs.sum())     # 1.0"},
        ],
        "pandas-fundamentals": [
            {"slug": "dataframes-series", "title": "DataFrames & Series", "summary": "Pandas: the Excel of Python", "order_index": 1, "xp_reward": 30, "estimated_minutes": 22,
             "learning_objectives": ["Create and load DataFrames", "Filter and select data", "Handle missing values"],
             "content_blocks": [
                 {"type": "text", "content": "Pandas is used in virtually every ML project to load, clean, and prepare tabular data. A `DataFrame` is a 2D table with labeled rows and columns — think of it as Excel inside Python, but infinitely more powerful."},
                 {"type": "code", "language": "python", "content": "import pandas as pd\nimport numpy as np\n\n# Create a sample ML dataset\nnp.random.seed(42)\nn = 100\ndf = pd.DataFrame({\n    'age': np.random.randint(22, 65, n),\n    'income': np.random.normal(60000, 20000, n).round(2),\n    'education_years': np.random.randint(10, 22, n),\n    'credit_score': np.random.randint(300, 850, n),\n    'default': np.random.choice([0, 1], n, p=[0.8, 0.2])\n})\n\nprint(df.head())\nprint('\\nDataset info:')\nprint(df.describe())"},
                 {"type": "code", "language": "python", "content": "# Filtering — selecting rows based on conditions\nhigh_risk = df[df['credit_score'] < 500]\nprint(f'High-risk customers: {len(high_risk)}')\n\n# Chained conditions\nprime_customers = df[(df['income'] > 80000) & (df['credit_score'] > 700)]\n\n# Handling missing data\ndf_missing = df.copy()\ndf_missing.loc[np.random.choice(n, 10), 'income'] = np.nan\nprint(f'\\nMissing income values: {df_missing[\"income\"].isna().sum()}')\ndf_missing['income'].fillna(df_missing['income'].median(), inplace=True)\n\n# GroupBy — aggregate statistics by category\ndefault_rate = df.groupby('default')['income'].mean()\nprint(f'\\nMean income by default status:\\n{default_rate}')"},
             ],
             "key_terms": ["DataFrame", "Series", "index", "loc/iloc", "boolean indexing", "groupby", "fillna", "dropna"],
             "common_mistakes": ["Using df[df.col == val] without parentheses in complex conditions", "SettingWithCopyWarning — always use .copy()", "Confusing loc (label-based) with iloc (position-based)"],
             "starter_code": "import pandas as pd\nimport numpy as np\n\n# Customer churn dataset\ndf = pd.DataFrame({\n    'customer_id': range(1, 11),\n    'tenure_months': [24, 3, 60, 1, 48, 12, 36, 6, 72, 18],\n    'monthly_charges': [65, 25, 95, 30, 85, 50, 70, 40, 90, 55],\n    'churned': [0, 1, 0, 1, 0, 0, 0, 1, 0, 0]\n})\n\n# 1. What's the average monthly charge for churned customers?\n# 2. Add a 'revenue_risk' column = monthly_charges for churned customers, 0 otherwise\n# 3. Sort by tenure_months descending\n\n# Your code here..."},
        ],
    }

    # Build Python path modules
    for mod_data in py_modules:
        lessons_for_mod = py_lessons.get(mod_data["slug"], [])
        mod = Module(path_id=path_objs["python-foundations"].id, **mod_data)
        db.add(mod)
        db.flush()
        for ld in lessons_for_mod:
            lesson = Lesson(module_id=mod.id, **ld)
            db.add(lesson)
            db.flush()
            # Attach a quiz to first lesson of each module
            if ld["order_index"] == 1:
                _add_python_quiz(db, lesson, mod_data["slug"])

    # ── ML Path (abbreviated modules) ─────────────────────────────────────────
    ml_modules_data = [
        {"slug": "intro-ml", "title": "Introduction to Machine Learning", "description": "What is ML, types of ML, the ML workflow, and when to use it.", "order_index": 1, "xp_reward": 100},
        {"slug": "linear-regression", "title": "Linear Regression", "description": "Fitting lines to data, cost functions, gradient descent, and OLS.", "order_index": 2, "xp_reward": 120},
        {"slug": "logistic-regression", "title": "Logistic Regression", "description": "Binary classification, sigmoid function, decision boundaries, cross-entropy.", "order_index": 3, "xp_reward": 120},
        {"slug": "decision-trees", "title": "Decision Trees", "description": "Information gain, Gini impurity, tree pruning, overfitting vs underfitting.", "order_index": 4, "xp_reward": 130},
        {"slug": "random-forest", "title": "Random Forest", "description": "Bagging, feature importance, hyperparameters, and comparing to single trees.", "order_index": 5, "xp_reward": 130},
        {"slug": "model-evaluation", "title": "Model Evaluation", "description": "Accuracy, precision, recall, F1, AUC-ROC, confusion matrix, cross-validation.", "order_index": 6, "xp_reward": 140},
        {"slug": "xgboost", "title": "XGBoost & Ensemble Methods", "description": "Gradient boosting, XGBoost, feature importance, hyperparameter tuning.", "order_index": 7, "xp_reward": 150},
    ]
    for mod_data in ml_modules_data:
        mod = Module(path_id=path_objs["machine-learning"].id, **mod_data)
        db.add(mod)
        db.flush()
        lesson = Lesson(
            module_id=mod.id, slug=f"{mod_data['slug']}-intro",
            title=f"{mod_data['title']}: Core Concepts",
            summary=mod_data["description"],
            learning_objectives=[f"Understand {mod_data['title']} fundamentals", "Apply the concept to real data", "Evaluate model performance"],
            content_blocks=_ml_content(mod_data["slug"]),
            key_terms=_ml_key_terms(mod_data["slug"]),
            common_mistakes=["Leaking test data into training", "Not normalizing features before gradient-based methods", "Ignoring class imbalance"],
            starter_code=_ml_starter(mod_data["slug"]),
            xp_reward=25, estimated_minutes=20, order_index=1,
        )
        db.add(lesson)

    # ── Generative AI Path (abbreviated) ─────────────────────────────────────
    genai_modules = [
        {"slug": "intro-genai", "title": "Introduction to Generative AI", "description": "What GenAI is, capabilities, risks, and the LLM revolution.", "order_index": 1},
        {"slug": "llms", "title": "Large Language Models", "description": "GPT, BERT, T5 — architectures, training data, emergent capabilities.", "order_index": 2},
        {"slug": "tokenization", "title": "Tokenization", "description": "BPE, WordPiece, SentencePiece — how text becomes numbers.", "order_index": 3},
        {"slug": "embeddings", "title": "Embeddings", "description": "Word2Vec, sentence embeddings, semantic similarity, vector spaces.", "order_index": 4},
        {"slug": "prompt-engineering", "title": "Prompt Engineering", "description": "Zero-shot, few-shot, chain-of-thought, structured output prompting.", "order_index": 5},
    ]
    for mod_data in genai_modules:
        mod = Module(path_id=path_objs["generative-ai"].id, xp_reward=120, estimated_minutes=40, is_published=True, **mod_data)
        db.add(mod)
        db.flush()
        lesson = Lesson(
            module_id=mod.id, slug=f"{mod_data['slug']}-core",
            title=mod_data["title"], summary=mod_data["description"],
            learning_objectives=[f"Master {mod_data['title']} concepts", "Apply to real AI applications"],
            content_blocks=[{"type": "text", "content": mod_data["description"]}],
            key_terms=[], common_mistakes=[], starter_code="# Explore " + mod_data['title'],
            xp_reward=25, estimated_minutes=20, order_index=1,
        )
        db.add(lesson)

    # ── AI Engineering Path (abbreviated) ────────────────────────────────────
    aieng_modules = [
        {"slug": "api-llm", "title": "API-based LLM Integration", "description": "Using OpenAI, Anthropic, and open-source model APIs in production.", "order_index": 1},
        {"slug": "vector-databases", "title": "Vector Databases", "description": "ChromaDB, Pinecone, Weaviate — storing and querying embeddings at scale.", "order_index": 2},
        {"slug": "rag-pipelines", "title": "RAG Pipelines", "description": "Build Retrieval-Augmented Generation: document ingestion, chunking, retrieval, generation.", "order_index": 3},
        {"slug": "ai-agents", "title": "AI Agents", "description": "ReAct agents, tool calling, memory, planning — building autonomous AI systems.", "order_index": 4},
    ]
    for mod_data in aieng_modules:
        mod = Module(path_id=path_objs["ai-engineering"].id, xp_reward=150, estimated_minutes=60, is_published=True, **mod_data)
        db.add(mod)
        db.flush()
        lesson = Lesson(
            module_id=mod.id, slug=f"{mod_data['slug']}-core",
            title=mod_data["title"], summary=mod_data["description"],
            learning_objectives=[f"Understand and implement {mod_data['title']}"],
            content_blocks=[{"type": "text", "content": mod_data["description"]}],
            key_terms=[], common_mistakes=[], starter_code=f"# {mod_data['title']} exercise",
            xp_reward=30, estimated_minutes=25, order_index=1,
        )
        db.add(lesson)

    # ── Coding Challenges ─────────────────────────────────────────────────────
    challenges = [
        {
            "slug": "hello-python",
            "title": "Hello, AI World!",
            "description": "Write a function called `greet` that takes a name string and returns `'Hello, {name}! Welcome to Learnova.'`",
            "path_slug": "python-foundations",
            "mode": "write_run",
            "difficulty": "easy",
            "starter_code": "def greet(name):\n    # Your code here\n    pass\n\nprint(greet('Ada'))",
            "solution_code": "def greet(name):\n    return f'Hello, {name}! Welcome to Learnova.'\n\nprint(greet('Ada'))",
            "hints": ["Use an f-string: f'Hello, {name}!'", "Don't forget to return the string"],
            "test_cases": [
                {"name": "Test greet('Ada')", "assert_expr": "greet('Ada') == 'Hello, Ada! Welcome to Learnova.'"},
                {"name": "Test greet('Turing')", "assert_expr": "greet('Turing') == 'Hello, Turing! Welcome to Learnova.'"},
            ],
            "xp_reward": 30,
        },
        {
            "slug": "fibonacci-sequence",
            "title": "Fibonacci Sequence",
            "description": "Write a function `fibonacci(n)` that returns the first `n` Fibonacci numbers as a list.",
            "path_slug": "python-foundations",
            "mode": "write_run",
            "difficulty": "easy",
            "starter_code": "def fibonacci(n):\n    # Return list of first n fibonacci numbers\n    # fibonacci(6) -> [0, 1, 1, 2, 3, 5]\n    pass\n\nprint(fibonacci(8))",
            "solution_code": "def fibonacci(n):\n    if n <= 0: return []\n    if n == 1: return [0]\n    result = [0, 1]\n    while len(result) < n:\n        result.append(result[-1] + result[-2])\n    return result[:n]\n\nprint(fibonacci(8))",
            "hints": ["Start with [0, 1]", "Each new number = previous two numbers", "Use a while loop or list comprehension"],
            "test_cases": [
                {"name": "fibonacci(6)", "assert_expr": "fibonacci(6) == [0, 1, 1, 2, 3, 5]"},
                {"name": "fibonacci(1)", "assert_expr": "fibonacci(1) == [0]"},
                {"name": "fibonacci(0)", "assert_expr": "fibonacci(0) == []"},
            ],
            "xp_reward": 40,
        },
        {
            "slug": "debug-list-average",
            "title": "Debug: Average Calculator",
            "description": "This function has 2 bugs. Find and fix them so `average([1,2,3,4,5])` returns `3.0`.",
            "path_slug": "python-foundations",
            "mode": "debug_code",
            "difficulty": "easy",
            "starter_code": "def average(numbers):\n    total = 0\n    for num in numbers:\n        total = total + num  \n    return total / len(numbers)  # Bug: what if numbers is empty?\n\n# Also fix this call:\nresult = average([1, 2, 3, 4, 5])\nprint(result)",
            "solution_code": "def average(numbers):\n    if not numbers:\n        return 0.0\n    return sum(numbers) / len(numbers)\n\nprint(average([1, 2, 3, 4, 5]))",
            "hints": ["What happens when you call average([])?", "Consider using Python's built-in sum() function"],
            "test_cases": [
                {"name": "average([1,2,3,4,5])", "assert_expr": "average([1,2,3,4,5]) == 3.0"},
                {"name": "average([10])", "assert_expr": "average([10]) == 10.0"},
            ],
            "xp_reward": 35,
        },
        {
            "slug": "numpy-dot-product",
            "title": "Vector Dot Product",
            "description": "Implement `dot_product(a, b)` using only NumPy. This is the core of linear regression predictions.",
            "path_slug": "python-foundations",
            "mode": "write_run",
            "difficulty": "medium",
            "starter_code": "import numpy as np\n\ndef dot_product(a, b):\n    \"\"\"Compute dot product of two 1D arrays.\"\"\"\n    # TODO: use np.dot or manual computation\n    pass\n\na = np.array([1.0, 2.0, 3.0])\nb = np.array([4.0, 5.0, 6.0])\nprint(dot_product(a, b))  # Expected: 32.0",
            "solution_code": "import numpy as np\n\ndef dot_product(a, b):\n    return np.dot(a, b)\n\na = np.array([1.0, 2.0, 3.0])\nb = np.array([4.0, 5.0, 6.0])\nprint(dot_product(a, b))",
            "hints": ["Use np.dot(a, b)", "Or compute: sum(a_i * b_i for all i)"],
            "test_cases": [
                {"name": "dot([1,2,3],[4,5,6])", "assert_expr": "abs(dot_product(np.array([1.0,2.0,3.0]), np.array([4.0,5.0,6.0])) - 32.0) < 1e-6"},
            ],
            "xp_reward": 50,
        },
        {
            "slug": "predict-output-loops",
            "title": "Predict the Output: Nested Loops",
            "description": "Before running the code, predict what it prints. Then run to verify your answer.",
            "path_slug": "python-foundations",
            "mode": "predict_output",
            "difficulty": "easy",
            "starter_code": "# Predict the output before running!\nmatrix = [[1,2,3],[4,5,6],[7,8,9]]\nfor row in matrix:\n    print(sum(row))",
            "solution_code": "matrix = [[1,2,3],[4,5,6],[7,8,9]]\nfor row in matrix:\n    print(sum(row))",
            "hints": ["Each row is a list", "sum([1,2,3]) = 6"],
            "test_cases": [],
            "expected_output": "6\n15\n24",
            "xp_reward": 25,
        },
        {
            "slug": "ml-accuracy-metric",
            "title": "Implement Accuracy Metric",
            "description": "Write `accuracy(y_true, y_pred)` — the fraction of correct predictions. This is used in every ML evaluation.",
            "path_slug": "machine-learning",
            "mode": "write_run",
            "difficulty": "medium",
            "starter_code": "def accuracy(y_true, y_pred):\n    \"\"\"Returns accuracy: correct / total\"\"\"\n    pass\n\ny_true = [0, 1, 1, 0, 1, 1, 0, 1]\ny_pred = [0, 1, 0, 0, 1, 1, 1, 1]\nprint(f'Accuracy: {accuracy(y_true, y_pred):.2%}')  # 75.00%",
            "solution_code": "def accuracy(y_true, y_pred):\n    correct = sum(t == p for t, p in zip(y_true, y_pred))\n    return correct / len(y_true)\n\ny_true = [0,1,1,0,1,1,0,1]\ny_pred = [0,1,0,0,1,1,1,1]\nprint(f'Accuracy: {accuracy(y_true, y_pred):.2%}')",
            "hints": ["Count how many y_pred[i] == y_true[i]", "Use zip() to iterate pairs", "Divide by len(y_true)"],
            "test_cases": [
                {"name": "75% accuracy", "assert_expr": "abs(accuracy([0,1,1,0,1,1,0,1],[0,1,0,0,1,1,1,1]) - 0.75) < 1e-6"},
                {"name": "100% accuracy", "assert_expr": "accuracy([1,0,1],[1,0,1]) == 1.0"},
            ],
            "xp_reward": 50,
        },
    ]
    for c in challenges:
        db.add(CodingChallenge(**c))

    # ── Quests ────────────────────────────────────────────────────────────────
    quests = [
        {"code": "daily_lessons_1", "title": "Quick Learner", "description": "Complete 1 lesson today", "quest_type": "daily", "metric_type": "lessons_completed", "target_count": 1, "xp_reward": 25, "difficulty": "easy"},
        {"code": "daily_lessons_3", "title": "Knowledge Sprint", "description": "Complete 3 lessons today", "quest_type": "daily", "metric_type": "lessons_completed", "target_count": 3, "xp_reward": 60, "difficulty": "normal"},
        {"code": "daily_challenge_1", "title": "Code Warrior", "description": "Solve 1 coding challenge", "quest_type": "daily", "metric_type": "challenges_solved", "target_count": 1, "xp_reward": 40, "difficulty": "normal"},
        {"code": "daily_quiz_1", "title": "Quiz Master", "description": "Pass 1 quiz with 80%+ score", "quest_type": "daily", "metric_type": "quizzes_passed", "target_count": 1, "xp_reward": 35, "difficulty": "normal"},
        {"code": "daily_mentor_2", "title": "Curious Mind", "description": "Ask your AI Mentor 2 questions", "quest_type": "daily", "metric_type": "mentor_questions", "target_count": 2, "xp_reward": 20, "difficulty": "easy"},
        {"code": "daily_no_hint_1", "title": "Independent Solver", "description": "Solve a challenge without hints", "quest_type": "daily", "metric_type": "challenges_no_hint", "target_count": 1, "xp_reward": 50, "difficulty": "hard"},
        {"code": "weekly_lessons_10", "title": "Weekly Learner", "description": "Complete 10 lessons this week", "quest_type": "weekly", "metric_type": "lessons_completed", "target_count": 10, "xp_reward": 150, "difficulty": "normal"},
        {"code": "weekly_challenges_5", "title": "Weekly Coder", "description": "Solve 5 coding challenges this week", "quest_type": "weekly", "metric_type": "challenges_solved", "target_count": 5, "xp_reward": 200, "difficulty": "hard"},
    ]
    for q in quests:
        db.add(Quest(**q))

    # ── Achievements ──────────────────────────────────────────────────────────
    achievements = [
        {"code": "first_steps", "title": "First Steps", "description": "Complete your very first lesson", "icon_name": "Footprints", "category": "milestones", "xp_reward": 50, "criteria_type": "lessons_completed", "criteria_value": 1},
        {"code": "python_pioneer", "title": "Python Pioneer", "description": "Complete 10 Python lessons", "icon_name": "Code2", "category": "paths", "xp_reward": 150, "criteria_type": "python_path", "criteria_value": 10},
        {"code": "consistency_king", "title": "Consistency King", "description": "Maintain a 7-day streak", "icon_name": "Flame", "category": "streaks", "xp_reward": 100, "criteria_type": "streak_days", "criteria_value": 7},
        {"code": "bug_hunter", "title": "Bug Hunter", "description": "Solve 5 coding challenges", "icon_name": "Bug", "category": "coding", "xp_reward": 100, "criteria_type": "challenges_solved", "criteria_value": 5},
        {"code": "perfect_score", "title": "Perfect Score", "description": "Achieve 100% on a quiz", "icon_name": "Trophy", "category": "quizzes", "xp_reward": 75, "criteria_type": "perfect_quiz", "criteria_value": 1},
        {"code": "ml_explorer", "title": "ML Explorer", "description": "Complete 5 Machine Learning lessons", "icon_name": "Brain", "category": "paths", "xp_reward": 100, "criteria_type": "ml_lessons", "criteria_value": 5},
        {"code": "century_club", "title": "Century Club", "description": "Earn 1,000 XP", "icon_name": "Star", "category": "milestones", "xp_reward": 100, "criteria_type": "total_xp", "criteria_value": 1000},
        {"code": "night_owl", "title": "Night Owl", "description": "Complete a lesson between 10 PM and 5 AM", "icon_name": "Moon", "category": "special", "xp_reward": 50, "criteria_type": "night_owl", "criteria_value": 1},
        {"code": "project_starter", "title": "Project Starter", "description": "Complete your first real-world project", "icon_name": "Rocket", "category": "projects", "xp_reward": 200, "criteria_type": "projects_completed", "criteria_value": 1},
        {"code": "marathon_learner", "title": "Marathon Learner", "description": "Complete 50 lessons total", "icon_name": "Zap", "category": "milestones", "xp_reward": 300, "criteria_type": "lessons_completed", "criteria_value": 50},
    ]
    for a in achievements:
        db.add(Achievement(**a))

    # ── Projects ──────────────────────────────────────────────────────────────
    projects = [
        {
            "slug": "customer-churn-prediction",
            "title": "Customer Churn Prediction",
            "summary": "Build an ML model to predict which customers will leave a subscription service",
            "problem_statement": "A telecom company wants to reduce customer churn. Using historical customer data, build a machine learning pipeline that predicts whether a customer will churn in the next month.",
            "difficulty": "intermediate",
            "technologies": ["Python", "Pandas", "Scikit-learn", "XGBoost"],
            "prerequisites": ["python-foundations", "data-science", "machine-learning"],
            "learning_objectives": ["Perform EDA on a business dataset", "Engineer features from raw data", "Train and compare multiple ML models", "Evaluate with precision, recall, and F1"],
            "milestones": [
                {"id": 1, "title": "Data Loading & EDA", "description": "Load dataset, explore distributions, identify missing values"},
                {"id": 2, "title": "Feature Engineering", "description": "Encode categoricals, handle missing data, create new features"},
                {"id": 3, "title": "Model Training", "description": "Train Logistic Regression, Random Forest, and XGBoost"},
                {"id": 4, "title": "Model Evaluation", "description": "Compare models using accuracy, precision, recall, F1, AUC-ROC"},
                {"id": 5, "title": "Predictions", "description": "Generate predictions on test set and interpret feature importance"},
            ],
            "evaluation_criteria": ["Achieves >75% accuracy on test set", "Uses at least 2 different models", "Includes confusion matrix analysis", "Demonstrates feature importance"],
            "dataset_name": "telecom_churn.csv",
            "sample_dataset": [
                {"customer_id": 1, "tenure": 24, "monthly_charges": 65.5, "total_charges": 1572.0, "contract": "Month-to-month", "tech_support": "No", "churn": 0},
                {"customer_id": 2, "tenure": 3, "monthly_charges": 25.0, "total_charges": 75.0, "contract": "Month-to-month", "tech_support": "Yes", "churn": 1},
                {"customer_id": 3, "tenure": 60, "monthly_charges": 95.0, "total_charges": 5700.0, "contract": "Two year", "tech_support": "Yes", "churn": 0},
            ],
            "starter_code": """import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Sample dataset
data = {
    'tenure': [24, 3, 60, 1, 48, 12, 36, 6, 72, 18, 5, 90, 15, 42, 8],
    'monthly_charges': [65.5, 25.0, 95.0, 30.0, 85.0, 50.0, 70.0, 40.0, 90.0, 55.0, 20.0, 100.0, 45.0, 75.0, 35.0],
    'contract_oneyear': [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
    'tech_support': [0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
    'churn': [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1]
}
df = pd.DataFrame(data)

# MILESTONE 1: Explore the data
print("Dataset shape:", df.shape)
print("\\nChurn distribution:")
print(df['churn'].value_counts())
print("\\nFeature statistics:")
print(df.describe())

# MILESTONE 2: Prepare features
X = df[['tenure', 'monthly_charges', 'contract_oneyear', 'tech_support']]
y = df['churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# MILESTONE 3: Train models (add your code here)
# TODO: Train LogisticRegression and RandomForestClassifier
# lr_model = LogisticRegression()
# lr_model.fit(X_train, y_train)

# MILESTONE 4: Evaluate (add your code here)
# TODO: Print accuracy and classification_report

print("\\nProject template ready! Add your ML code above.")
""",
            "required_keywords": ["train_test_split", "fit", "predict", "accuracy_score"],
            "xp_reward": 250,
            "badge_code": "data_detective",
        },
        {
            "slug": "enterprise-rag-assistant",
            "title": "Enterprise Policy RAG Assistant",
            "summary": "Build a Retrieval-Augmented Generation system that answers questions from company documents",
            "problem_statement": "Build a RAG pipeline that can answer questions about company policies from uploaded documents, using vector embeddings for semantic retrieval.",
            "difficulty": "advanced",
            "technologies": ["Python", "LangChain", "ChromaDB", "OpenAI Embeddings"],
            "prerequisites": ["ai-engineering", "generative-ai"],
            "learning_objectives": ["Implement document chunking strategies", "Generate and store embeddings in ChromaDB", "Build a retrieval pipeline", "Evaluate RAG quality"],
            "milestones": [
                {"id": 1, "title": "Document Processing", "description": "Load, parse, and chunk company policy documents"},
                {"id": 2, "title": "Embedding Generation", "description": "Generate embeddings using sentence-transformers"},
                {"id": 3, "title": "Vector Store", "description": "Store and index embeddings in ChromaDB"},
                {"id": 4, "title": "Retrieval Pipeline", "description": "Implement semantic search and context retrieval"},
                {"id": 5, "title": "RAG Response Generation", "description": "Generate grounded answers using retrieved context"},
            ],
            "evaluation_criteria": ["Correctly retrieves relevant chunks", "Generates contextually accurate answers", "Handles out-of-context questions gracefully"],
            "dataset_name": "company_policies.txt",
            "sample_dataset": [],
            "starter_code": """# Enterprise RAG Pipeline
# Note: This requires chromadb and sentence-transformers packages
# In the actual environment: pip install chromadb sentence-transformers

import json

# Simulated document chunks (in real project, load from files)
DOCUMENTS = [
    {'id': 'pol_001', 'text': 'Remote work policy: Employees may work remotely up to 3 days per week with manager approval. Home office equipment allowance is $500 annually.', 'source': 'remote_work_policy.pdf'},
    {'id': 'pol_002', 'text': 'Annual leave policy: Full-time employees receive 20 days paid leave per year, increasing by 1 day for each year of service up to 25 days.', 'source': 'leave_policy.pdf'},
    {'id': 'pol_003', 'text': 'Code of conduct: All employees must complete ethics training annually. Violations are subject to disciplinary action up to and including termination.', 'source': 'code_of_conduct.pdf'},
    {'id': 'pol_004', 'text': 'IT security policy: Passwords must be at least 12 characters. Multi-factor authentication is mandatory for all corporate systems.', 'source': 'it_security.pdf'},
]

def simple_retrieval(query, documents, top_k=2):
    '''Simple keyword-based retrieval (replace with embedding-based in real RAG)'''
    query_words = set(query.lower().split())
    scores = []
    for doc in documents:
        doc_words = set(doc['text'].lower().split())
        overlap = len(query_words & doc_words)
        scores.append((overlap, doc))
    scores.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scores[:top_k]]

def rag_answer(query):
    '''RAG pipeline: retrieve + generate'''
    retrieved = simple_retrieval(query, DOCUMENTS)
    context = '\\n\\n'.join([f"Source: {d['source']}\\n{d['text']}" for d in retrieved])
    
    # In production: send context + query to LLM
    # For now: return retrieved context as answer
    answer = f"Based on company policies:\\n\\nContext retrieved:\\n{context}\\n\\n[In production: LLM generates answer from this context]"
    return answer

# Test the pipeline
queries = [
    "How many days of remote work am I allowed?",
    "What is the annual leave policy?",
    "What are the password requirements?",
]
for q in queries:
    print(f"Q: {q}")
    print(f"A: {rag_answer(q)[:200]}...")
    print()
""",
            "required_keywords": ["retrieval", "context", "query"],
            "xp_reward": 350,
            "badge_code": "rag_builder",
        },
    ]
    for p in projects:
        db.add(Project(**p))

    db.commit()


def _add_python_quiz(db: Session, lesson: Lesson, module_slug: str) -> None:
    """Add a knowledge check quiz to a Python lesson."""
    quiz_data = {
        "intro-python": {
            "title": "Python Basics Knowledge Check",
            "questions": [
                {"prompt": "What does `print(type(42))` output?", "question_type": "multiple_choice",
                 "options": ["<class 'int'>", "<class 'float'>", "<class 'number'>", "<class 'str'>"],
                 "correct_answer": {"value": "<class 'int'>"}, "explanation": "42 is an integer literal. `type()` returns the class, displayed as `<class 'int'>`.", "topic_tag": "Data Types"},
                {"prompt": "Python uses _____ to define code blocks.", "question_type": "fill_blank",
                 "options": [], "correct_answer": {"value": "indentation"},
                 "explanation": "Python uses indentation (typically 4 spaces) to define code blocks, unlike C/Java which use curly braces.", "topic_tag": "Syntax"},
                {"prompt": "Which of these is a valid Python f-string?", "question_type": "multiple_choice",
                 "options": ['f"Hello, {name}!"', '"Hello, " + name + "!"', 'format("Hello, %s" % name)', '"Hello, " & name'],
                 "correct_answer": {"value": 'f"Hello, {name}!"'}, "explanation": "F-strings (f\"...\") are the modern way to embed variables in strings in Python 3.6+.", "topic_tag": "Strings"},
            ]
        },
        "variables-datatypes": {
            "title": "Data Types Knowledge Check",
            "questions": [
                {"prompt": "What is the result of `10 / 3` in Python 3?", "question_type": "multiple_choice",
                 "options": ["3", "3.3333333333333335", "3.33", "Error"],
                 "correct_answer": {"value": "3.3333333333333335"}, "explanation": "In Python 3, `/` always performs float division. Use `//` for integer division.", "topic_tag": "Numbers"},
                {"prompt": "Strings in Python are immutable.", "question_type": "true_false",
                 "options": ["True", "False"], "correct_answer": {"value": "True"},
                 "explanation": "Python strings cannot be modified after creation. Operations like .upper() return new strings.", "topic_tag": "Strings"},
            ]
        },
    }
    quiz_info = quiz_data.get(module_slug)
    if not quiz_info:
        return
    quiz = Quiz(lesson_id=lesson.id, title=quiz_info["title"], topic="Python Fundamentals",
                difficulty="easy", pass_percentage=70, xp_reward=30)
    db.add(quiz)
    db.flush()
    for idx, q in enumerate(quiz_info["questions"]):
        db.add(Question(quiz_id=quiz.id, order_index=idx, **q))


def _ml_content(slug: str) -> list:
    contents = {
        "intro-ml": [
            {"type": "text", "content": "**Machine Learning** is a subset of AI where computers learn patterns from data without being explicitly programmed. Instead of writing rules, we provide examples and let the algorithm discover the patterns."},
            {"type": "text", "content": "### Three Types of ML\n\n**Supervised Learning**: Learn from labeled examples (input → known output). Used for regression and classification.\n\n**Unsupervised Learning**: Find structure in unlabeled data. Used for clustering and dimensionality reduction.\n\n**Reinforcement Learning**: Learn by trial and error with rewards/penalties."},
            {"type": "code", "language": "python", "content": "from sklearn.datasets import load_iris\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import StandardScaler\n\n# Load a classic ML dataset\niris = load_iris()\nX, y = iris.data, iris.target\n\nprint(f'Dataset shape: {X.shape}')  # (150, 4)\nprint(f'Classes: {iris.target_names}')  # setosa/versicolor/virginica\n\n# The golden rule: split before anything else!\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nprint(f'Train: {X_train.shape}, Test: {X_test.shape}')"},
            {"type": "callout", "variant": "warning", "content": "**Never use test data during training.** The test set simulates real-world unseen data. If you use it to make decisions during training, your model's performance estimate will be optimistically biased."},
        ],
        "linear-regression": [
            {"type": "text", "content": "**Linear Regression** finds the best-fit line through data points by minimizing the **Mean Squared Error**: $$MSE = \\frac{1}{n}\\sum_{i=1}^{n}(y_i - \\hat{y}_i)^2$$"},
            {"type": "code", "language": "python", "content": "from sklearn.linear_model import LinearRegression\nfrom sklearn.metrics import mean_squared_error, r2_score\nimport numpy as np\n\n# Generate synthetic data: y = 2x + noise\nX = np.random.randn(100, 1) * 10\ny = 2 * X.ravel() + np.random.randn(100) * 3\n\nmodel = LinearRegression()\nmodel.fit(X, y)\n\nprint(f'Coefficient (slope): {model.coef_[0]:.3f}')  # ~2.0\nprint(f'Intercept: {model.intercept_:.3f}')           # ~0.0\nprint(f'R² score: {model.score(X, y):.3f}')           # ~0.97"},
        ],
        "logistic-regression": [
            {"type": "text", "content": "**Logistic Regression** applies the sigmoid function to output probabilities between 0 and 1: $$\\sigma(z) = \\frac{1}{1 + e^{-z}}$$ where $z = w^Tx + b$."},
            {"type": "code", "language": "python", "content": "from sklearn.linear_model import LogisticRegression\nfrom sklearn.datasets import make_classification\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import classification_report\n\nX, y = make_classification(n_samples=1000, n_features=10, random_state=42)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\n\nmodel = LogisticRegression(max_iter=1000)\nmodel.fit(X_train, y_train)\npreds = model.predict(X_test)\nprint(classification_report(y_test, preds))"},
        ],
    }
    return contents.get(slug, [{"type": "text", "content": f"Content for {slug} coming soon. Use the AI Mentor to explore this topic!"}])


def _ml_key_terms(slug: str) -> list:
    terms = {
        "intro-ml": ["supervised learning", "unsupervised learning", "features", "labels", "training set", "test set", "overfitting"],
        "linear-regression": ["coefficient", "intercept", "MSE", "R²", "gradient descent", "ordinary least squares"],
        "logistic-regression": ["sigmoid", "log-loss", "decision boundary", "threshold", "binary classification"],
        "decision-trees": ["Gini impurity", "information gain", "depth", "leaf node", "pruning"],
        "random-forest": ["ensemble", "bagging", "feature importance", "out-of-bag error"],
        "model-evaluation": ["accuracy", "precision", "recall", "F1-score", "AUC-ROC", "confusion matrix", "cross-validation"],
        "xgboost": ["gradient boosting", "weak learner", "learning rate", "regularization", "tree depth"],
    }
    return terms.get(slug, ["machine learning", "model", "features", "predictions"])


def _ml_starter(slug: str) -> str:
    starters = {
        "intro-ml": "from sklearn.datasets import load_iris\nfrom sklearn.model_selection import train_test_split\n\niris = load_iris()\nX, y = iris.data, iris.target\n\n# Split the data (80% train, 20% test)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nprint(f'Training samples: {X_train.shape[0]}')\nprint(f'Test samples: {X_test.shape[0]}')\nprint(f'Features: {X.shape[1]}')\nprint(f'Classes: {list(iris.target_names)}')",
        "linear-regression": "from sklearn.linear_model import LinearRegression\nfrom sklearn.metrics import mean_squared_error\nimport numpy as np\n\n# Boston-style housing data (simplified)\nX = np.array([[1400, 3], [1600, 4], [1700, 4], [1875, 4], [1100, 3], [1550, 3]])\ny = np.array([245000, 312000, 279000, 308000, 199000, 219000])\n\n# Train linear regression\nmodel = LinearRegression()\nmodel.fit(X, y)\n\nprint(f'Coefficients: {model.coef_}')\nprint(f'R² score: {model.score(X, y):.3f}')\n\n# Predict for 1800 sq ft, 4 bedrooms\npred = model.predict([[1800, 4]])\nprint(f'Predicted price: ${pred[0]:,.0f}')",
    }
    return starters.get(slug, f"# {slug} exercise\n# Implement the concept from this lesson\npass")
