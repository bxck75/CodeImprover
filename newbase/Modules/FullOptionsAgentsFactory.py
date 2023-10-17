import os
from langchain_g4f import G4FLLM
from langchain.llms.base import LLM
from g4f import Provider, models
from llama_index import ServiceContext
from llama_index.llms import ChatMessage
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.tools import BaseTool, FunctionTool
from langchain.chains.summarize import load_summarize_chain
from inspect import signature
from llama_index.bridge.langchain import StructuredTool, Tool
from llama_index.bridge.pydantic import BaseModel
from llama_index.tools.types import AsyncBaseTool, ToolMetadata, ToolOutput
from llama_index.tools.utils import create_schema_from_function
from llama_index.memory import ConversationBufferMemory, DocumentMemory
from llama_index.agents import ReActAgent


class FullOptionsAgentsFactory:
    version: Optional[float] = 0.1
    def __init__(self, docu: str):
        self.document_memory = DocumentMemory()
        # Replace 'docu' with your document content.
        self.document = Document(page_content=docu)
        self.document_memory.add_document(self.document)
        self.memory = ConversationBufferMemory()
        self.memory.add_memory(self.document_memory)

        self.bash_curl_tool = FunctionTool.from_defaults(
            fn=self.bash_curl_shell)

        self.factory_tools = [self.bash_curl_tool]

        self.factory_llm: LLM = G4FLLM(model=models.gpt_35_turbo)

        self.factoryagent_turbo = ReActAgent.from_tools(
            self.factory_tools,
            memory=self.memory,
            llm=self.factory_llm,
            verbose=True
        )

    def bash_curl_shell(self, command: str) -> str:
        """Run a bash command and return its output"""
        return os.popen(command).read()

    def run(self):
        import langchain.utilities.opaqueprompts as op
        from langchain.schema.runnable import RunnablePassthrough
        from langchain.schema.output_parser import StrOutputParser

        prompt_template = """
            system: You are a FullOptionsFactory assistant.
            user: What can you do?
        """

        pg_chain = (
            op.sanitize
            | RunnablePassthrough.assign(
                response=(lambda x: x["sanitized_input"])
                | prompt_template
                | self.factoryagent_turbo
                | StrOutputParser(),
            )
            | (lambda x: op.desanitize(x["response"], x["secure_context"]))
        )

        result = pg_chain.invoke({"question": "", "history": ""})
        print(result)


if __name__ == "__main__":
    docu = "Your document content goes here."
    factory = FullOptionsAgentsFactory(docu)
    factory.run()
