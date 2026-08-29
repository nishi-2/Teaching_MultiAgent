Phase 1 -

- Create a virtual environment and .gitignore file. Place all the file names in .gitignore that we dont want to push to github. Add the obvious ones to the latter - which can be expanded later as well.

- Create the requirements file now with the necessary libraries. We can add more on the go.

- Create an .env file with the following details -
OPENAI_API_KEY=<give your key here>
OPENAI_MODEL=gpt-5-mini <or model of your choice>
OPENAI_REASONING_EFFORT=minimal  <look out for reasoning availability with the model>
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=ai_tutor_documents
DOCUMENTS_DIR=data/documents
LOG_LEVEL=INFO