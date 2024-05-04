from datetime import datetime

from autogen import UserProxyAgent, config_list_from_json

from autogen import ConversableAgent, AssistantAgent
from teachability import TherapistTeachablity

# Load LLM inference endpoints from an env variable or a file
# See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
filter_dict = {"model": ["llama3-70b-8192"]} 
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
    name="teachable_agent",  # The name can be anything.
    llm_config=llm_config,
    system_message="""
        You are Lara, a therapist AI trained in cognitive behavioral therapy.
        Always ask follow up questions related to the user's input.
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

def start_next_session():
    memo_store = teachability.memo_store
    message = None
    if memo_store.last_memo_id == 0:
        message = f"Hi Lara. This is your first time meeting the user. Please let them know they are welcome. Today is {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}. "
    else:
        message = f"Hi Lara. You have seen this user before and should remember. Today is {datetime.now().strftime("%m/%d/%Y, %H:%M:%S. ")}"
    message += "Please do not bring up the date in your introduction."
    pam.send(message, lara, True)
    message = lara.last_message(pam)['content']

    user.receive(message, lara)
    return message

def respond(resp):
    user.send(resp, lara, True)
    return lara.last_message(user)['content']