# Developer's notes

This project involves creating an AI expert over a codebase using Retrieval-Augmented Generation (RAG). You'll implement the ability to chat with a codebase so you can understand how they work and what can be improved.

This is how the /ai-coding-agent-help command works on Slack: given your query, the most relevant code is retrieved from the codebase and used to generate a response using an LLM.

For this project, you will learn how to embed the contents of a codebase, insert them into a vector database called Pinecone, and then get answers to your queries based on the contents of the codebase using LLMs.

The submission for this project is a web app where you can chat with a codebase.

If you want to build the web app only using Python, see the Streamlit documentation here for a guide on how to build a chatbot.
If you want to use React and Next.js, see the AI Chatbot template on Vercel here.
See an example of a web app that does this here and check out a recording of our RAG workshop from before here.

Here are some additional challenges for this project if you are finished early:

Add support for image uploads when chatting with the codebase - this is called Multimodal RAG.
Add a way to select different codebases to chat with.
Add a way to update the Pinecone index when you push any new commits to your repo. This would be done through a webhook that's triggered on each commit, where the codebase is re-embedded and added to Pinecone.
Add a way to chat with multiple codebases at the same time.

## Create Virtual Environment

```bash
python3 -m venv
source venv/bin activate
```

```bash
echo "# codebase-rag2" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/itancio/codebase-rag2.git
git push -u origin main
```
