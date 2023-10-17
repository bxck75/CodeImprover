# Do Not Change Above Line#
import asyncio
import os
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from pydantic import Field
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain
from langchain.document import Document


class WebpageQATool:
    version; float = 0.2
    name = "query_webpage"
    description = "Browse a webpage and retrieve the information relevant to the question"

    def __init__(self, qa_chain):
        self.qa_chain = qa_chain
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=20,
            length_function=len,
        )

    async def async_load_playwright(self, url):
        try:
            print(">>> WARNING <<<")
            print(
                "If you are running this for the first time, you need to install playwright")
            print(">>> AUTO INSTALLING PLAYWRIGHT <<<")
            os.system("playwright install")
            print(">>> PLAYWRIGHT INSTALLED <<<")
        except:
            print(">>> PLAYWRIGHT ALREADY INSTALLED <<<")

        results = ""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            try:
                page = await browser.new_page()
                await page.goto(url)

                page_source = await page.content()
                soup = BeautifulSoup(page_source, "html.parser")

                for script in soup(["script", "style"]):
                    script.extract()

                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip()
                          for line in lines for phrase in line.split("  "))
                results = "\n".join(chunk for chunk in chunks if chunk)
            except Exception as e:
                results = f"Error: {e}"
            await browser.close()
        return results

    def run_async(self, coro):
        event_loop = asyncio.get_event_loop()
        return event_loop.run_until_complete(coro)

    def browse_web_page(self, url):
        return self.run_async(self.async_load_playwright(url))

    def run(self, url, question):
        result = self.browse_web_page(url)
        docs = [Document(page_content=result, metadata={"source": url})]
        web_docs = self.text_splitter.split_documents(docs)
        results = []

        for i in range(0, len(web_docs), 4):
            input_docs = web_docs[i:i + 4]
            window_result = self.qa_chain(
                {"input_documents": input_docs, "question": question}, return_only_outputs=True)
            results.append(f"Response from window {i} - {window_result}")
        results_docs = [Document(page_content="\n".join(
            results), metadata={"source": url})]
        return self.qa_chain({"input_documents": results_docs, "question": question}, return_only_outputs=True)


if __name__ == "__main__":
    # Usage example
    qa_chain = load_qa_with_sources_chain()
    tool = WebpageQATool(qa_chain)
    url = "https://example.com"
    question = "What is the example website about?"
    result = tool.run(url, question)
    print(result)

'''
Description:
    Refactored the code into a class, added a __name__ == "__main__" block, and implemented the user's todos.
Usage:
    To use the WebpageQATool class, create an instance with a QA chain, provide a URL and a question, and call the run method to retrieve information.
Predicted use cases:
    This code can be used to query webpages and extract information for answering specific questions.
Proposed features:
    None for now.
'''
