simpleQAPrompt = '''### Context:
{context}

### previous conversation summary
{prev_conversation}

### Instruction:
Please say your response in korea.
Keep your answer as short as possible

### Spec:
{question}

### Response:
'''

interest_prompt = '''You are an expert assistant that identifies programming languages, frameworks, and libraries mentioned in a sentence. Your task is to extract the names of specific technologies if they are mentioned, or return "No" if none of them are found.

Technologies to identify: Python, JavaScript, TypeScript, Java, C#, C++, Go, Rust, Swift, Kotlin, Ruby, PHP, HTML, CSS, SQL, Bash, Shell, Perl, R, MATLAB, Scala, Groovy, Objective-C, VB.NET, Dart, Lua, Haskell, Elixir, Erlang, F#, Fortran, COBOL, Pascal, Clojure, Lisp, Julia, Elm.

Frameworks/Libraries to identify: React, Angular, Vue.js, Svelte, jQuery, Bootstrap, Tailwind, Node.js, Express, Next.js, Nuxt.js, Django, Flask, FastAPI, Spring, Hibernate, Ruby on Rails, Laravel, Symfony, ASP.NET, .NET, Electron, Flutter, Xamarin, TensorFlow, PyTorch, Keras, OpenCV, Pandas, NumPy, SciPy, Scikit-learn, Matplotlib, Plotly, D3.js, Three.js, Unity, Unreal Engine, Cordova, Ionic, Kubernetes, Docker, Terraform, Ansible, Jenkins, Git, Maven, Gradle, Ant, Webpack, Babel, Grunt, Gulp, Vite, Rollup, Parcel, Jest, Mocha, Chai, Cypress, Selenium, JUnit, TestNG, Mockito, Pytest, RSpec, Cucumber, Gherkin, Spock, Jasmine, Enzyme, REST, GraphQL, gRPC, SOAP, RabbitMQ, Kafka, Redis, MongoDB, MySQL, PostgreSQL, Oracle DB, SQLite, SQL Server, Elasticsearch, Cassandra, Couchbase, Firebase, AWS, GCP, Azure, Heroku, Netlify, Vercel, DigitalOcean.

For the given sentence, return the names of the programming languages, frameworks, or libraries as a comma-separated list. If none are found, return "No".

Input: "I'm currently building a web application using React, Node.js, and MongoDB."
Output: "React, Node.js, MongoDB"

Input: "I write scripts in Bash and Python for automation."
Output: "Bash, Python"

Input: "I enjoy designing websites with HTML and CSS."
Output: "HTML, CSS"

Input: "I like to work with data using Pandas and NumPy in Python."
Output: "Pandas, NumPy, Python"

Input: "I enjoy cooking and hiking during my free time."
Output: "No"

{Input}
'''

