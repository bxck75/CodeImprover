'''Todos
# TODO: Try and learn
# TODO: Self-improve and make file write and read for yourself
# TODO: after acquiring that, speculate on the purpose of the stater.py file. If you think you know, read this file
# TODO: if you cannot succeed, let me know via a custom info log
# TODO: or in case of an error, try logging the actual error to the Logger by __call__ ing the Logger
# TODO: use this list of dicts to make your worker force and maybe make a worker for every dict using the values init
'''



roles = [
    {"class": "todogenerator", "starting Comment": "class handles research, movement of proposed features, keeps todo list per script filled, reads logs, splits them into Todo's, moves proposed features, manages comment blocks and doc strings."},
    {"class": "CommentsWriter", "starting Comment":
        "class handles the setup and preprocess, manages comment blocks and doc strings."},
    {"class": "Debugger", "starting Comment": "class reacts to logs and helps improver between code changes, tests and solve bugs."},
    {"class": "CodeAnalizer", "starting Comment": "class analyzes scripts, influences the code improver, issues logs for info, warnings, and errors to the data logger."},
    {"class": "CodeImprover", "starting Comment": "class that improves scripts, proposes extra features listed in bottom comment block, and is the provider of the high-level improvement plan"},
    {"class": "Controller", "starting Comment":
        "class to control the development process. executes most other classes"},
    {"class": "ScriptTemplate",
        "starting Comment": "class with a template to set up and structure all scripts."},
    {"class": "RequestHandler",
        "starting Comment": "class to handle requests between agents."},
    {"class": "AgentHandler",
        "starting Comment": "class to plan, fit, and execute expert agents"},
    {"class": "VectorStore", "starting Comment": "class that stores shared analyzer and improver history, also the knowledge and memory source for agents"},
    {"class": "Logger", "starting Comment": "class that centrally logs info, warnings, and errors of all other scripts callable)."},
    {"class": "Toolbox", "starting_Comment": "class that is the keeper and provider of all agent tools."},
    {"class": "Summerizer", "starting_Comment": "class that summarizes short descriptions, rules, templates, and Todos into more elaborate prompts for the agents"},
    {"class": "Splitter", "starting_Comment": "class that splits long logs into shorter prompts or long scripts into separate methods for improver or analyzer"},
    {"class": "Merger", "starting_Comment": "class that merges short text or keywords into prompts or separate scripts and methods into classes"}
]

# script rules and improvements order
settings = [
    {"scripting_rules": "Describe the rules of coding the templates, building the agent prompts helps tune agents and fit tools"},
    {"improvement_order": ["Todos", "debugging", "generic scripting",
                            "debugging", "reporting of description", "usage", "use cases"]}
]




