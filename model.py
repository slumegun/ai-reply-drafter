from unsloth import FastLanguageModel
import re

from prompt import system_prompt


class Generating:
    def __init__(self):
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name="./my_model1",
            load_in_4bit=True
        )
        FastLanguageModel.for_inference(self.model)

    def generate_answer(self, msgs: str, chat_history: list) -> str:
        msgs = self.formatting_history(chat_history=chat_history)

        inputs = self.tokenizer.apply_chat_template(
                msgs,
                tokenize=True,
                add_generation_prompt=True,
                return_tensors="pt",
            ).to(self.model.device)
        
        outputs = self.model.generate(
            input_ids=inputs,
            max_new_tokens=150,
            temperature=0.8,
            top_p=0.9,
            do_sample=True,
        )
    
        response = self.tokenizer.decode(
            outputs[0][inputs.shape[-1]:],
            skip_special_tokens=True,
        )
        response = re.sub(r"<.*?>", "", response)
        response = response.strip()

        return response

    def formatting_history(self, chat_history: list) -> list:
        new_history = [{"role": "system", "content": system_prompt}]
        for i in chat_history:
            new_history.append({"role": i[0], "content": i[1]})

        return new_history
