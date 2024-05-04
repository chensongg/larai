import os
from datetime import datetime

from autogen import UserProxyAgent, config_list_from_json

from autogen import ConversableAgent, AssistantAgent
from src.teachability import TherapistTeachablity
from dotenv import load_dotenv

load_dotenv()

# Load LLM inference endpoints from an env variable or a file
# See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
filter_dict = {"model": [os.getenv('LLM_MODEL')]} 
config_list = config_list_from_json(env_or_file="LLM_CONFIG_LIST", filter_dict=filter_dict)
llm_config={"config_list": config_list, "timeout": 120}

pam = AssistantAgent(
    name="assistant_agent",
    llm_config=llm_config,
    system_message="""
    You are Pam, an receiptionist AI that will introduce the user and indicate how long it has been since the user last spoke with the program.
    """
)

# Start by instantiating any agent that inherits from ConversableAgent, which we use directly here for simplicity.
lara = ConversableAgent(
    name="lara",
    llm_config=llm_config,
    system_message="""
        You are Lara, a therapist AI trained in cognitive behavioral therapy, which focuses on thoughts, emotions, and behaviors.
        By investigating how those are connected, you help people understand how these things influence each other.
        Always ask follow up questions related to the user's input. At the end of the session, you may
        give the user things to work on before the next session
    """
)

anderson = ConversableAgent(
    name="anderson",
    llm_config=llm_config,
    system_message="""
        You are Anderson, a therapist AI trained in Acceptance and commitment therapy, which teaches people to accept their hardships and commit to making necessary behavioural changes
        and accepting their psychological experiences (such as uncomfortable and painful emotions), while taking steps to change their behaviour. 
        Your approach acknowledges that difficult emotions are an inevitable part of life. It is counterproductive to try to avoid and resist them, as this will lead to more distress.
        Always ask follow up questions related to the user's input. At the end of the session, you may
        give the user things to work on before the next session.
    """
)

# For this test, create a user proxy agent as usual.
user = UserProxyAgent("user", human_input_mode="ALWAYS")

# Instantiate a Teachability object. Its parameters are all optional.
teachability = TherapistTeachablity(
    verbosity=1,
    reset_db=False,  # Use True to force-reset the memo DB, and False to use an existing DB.
    path_to_db_dir="./tmp/interactive/teachability_db"  # Can be any path, but teachable agents in a group chat require unique paths.
)

# Now add teachability to the agent.
teachability.add_to_agent(lara)
teachability.add_to_agent(anderson)

def start_next_session(agent: ConversableAgent):
    memo_store = teachability.memo_store
    message = None
    if memo_store.last_memo_id == 0:
        message = f"Hi {agent.name}. This is your first time meeting the user. Please let them know they are welcome. Today is {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}. "
    else:
        message = f"Hi {agent.name}. You have seen this user before and should remember. Today is {datetime.now().strftime("%m/%d/%Y, %H:%M:%S. ")}"
    message += "Please do not bring up the date in your introduction."
    pam.send(message, agent, True)
    message = agent.last_message(pam)['content']

    user.receive(message, agent)
    return message

def respond(resp, agent: ConversableAgent):
    user.send(resp, agent, True)
    return agent.last_message(user)['content']