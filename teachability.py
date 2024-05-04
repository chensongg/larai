from typing import Dict
from typing import Dict, Union
from autogen.agentchat.contrib.capabilities.teachability import Teachability

class TherapistTeachablity(Teachability):
    def _consider_memo_storage(self, comment: Union[Dict, str]):
        """Decides whether to store something from one user comment in the DB."""
        memo_added = False

        # Check for information to be learned.
        response = self._analyze(
            comment,
            "Does the TEXT contain information that tells you about the logistics of the session, including date of visit, or would help you determine how many visits the user has had?",
        )

        if "yes" in response.lower():
            question = self._analyze(
                comment,
                "Imagine that the user forgot this information in the TEXT. How would they ask you for this information? Include no other text in your response."
            )
            # Extract the information.
            answer = self._analyze(
                comment, "Copy the information from the TEXT that should be committed to memory. Add no explanation."
            )

            # Add the question-answer pair to the vector DB.
            if self.verbosity >= 1:
                print("\nREMEMBER THIS QUESTION-ANSWER PAIR", "light_yellow")
            self.memo_store.add_input_output_pair(question, answer)
            memo_added = True
        # Check for information to be learned.
        response = self._analyze(
            comment,
            "Does the TEXT contain information that would help you understand their personality or experiences that could be committed to memory? Answer with just one word, yes or no.",
        )
        if "yes" in response.lower():
            # Yes. What question would this information answer?
            question = self._analyze(
                comment,
                "Imagine that the user forgot this information in the TEXT. How would they ask you for this information? Include no other text in your response.",
            )
            # Extract the information.
            answer = self._analyze(
                comment, "Copy the information from the TEXT that should be committed to memory. Add no explanation."
            )
            # Add the question-answer pair to the vector DB.
            if self.verbosity >= 1:
                print("\nREMEMBER THIS QUESTION-ANSWER PAIR", "light_yellow")
            self.memo_store.add_input_output_pair(question, answer)
            memo_added = True

        # Were any memos added?
        if memo_added:
            # Yes. Save them to disk.
            self.memo_store._save_memos()