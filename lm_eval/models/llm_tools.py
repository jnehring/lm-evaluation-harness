from lm_eval.base import LM
import traceback
import requests
import json 

class LLMToolsModel(LM):

    def __init__(self, api_url="http://localhost:5000"):
        super().__init__()
        self.api_url = api_url
        self.error_file = "error.log"

        # subclass must implement properties vocab_size, eot_token_id, max_gen_toks, batch_size, device, max_length.

    # generate text
    def greedy_until(
            self, _requests
    ):
        inputs = [x[0] for x in _requests]
        until = [x[1] for x in _requests]

        responses = []
        for i in range(len(inputs)):

            try:
                if i%50==0:
                    print(f"generate text {i}/{len(inputs)}")
                
                url = self.api_url + "/api/generate"
                data = {
                    "doc": inputs[i] 
                }
                r = requests.post(url, json=data).json()
                responses.append(r["response"])
            except Exception as e:
                e = traceback.format_exc(limit=None, chain=True)
                msg = "Exception from /api/generate\n"
                msg += traceback.format_exc(limit=None, chain=True) + "\n"
                msg += inputs[i] + "\n"
                msg += "----------------"
                print(msg)
                with open(self.error_file, "a") as f:
                    f.write(msg)

        return responses

    # token probabilities
    def loglikelihood(self, _requests):

        inputs = [x[0] for x in _requests]
        targets = [x[1] for x in _requests]

        scores = []
        for i in range(len(inputs)):
            try:
                if i%50==0:
                    print(f"cond_log_prob {i}/{len(inputs)}")
                url = self.api_url + "/api/cond_log_prob"
                data = {
                    "doc": inputs[i],
                    "targets": targets[i]
                }
                r = requests.post(url, json=data).json()
                scores.append(r["cond_log_prob"])
            except Exception as e:
                e = traceback.format_exc(limit=None, chain=True)
                msg = "Exception from /api/cond_log_prob\n"
                msg += traceback.format_exc(limit=None, chain=True) + "\n"
                msg += json.dumps(data) + "\n"
                msg += str(targets[i]) + "\n"
                msg += "----------------"
                with open(self.error_file, "a") as f:
                    f.write(msg)
        return scores

    
    def loglikelihood_rolling(self, requests):
        raise NotImplementedError("loglikelihood_rolling is not implemented")
    
    