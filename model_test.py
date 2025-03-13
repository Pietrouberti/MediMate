import transformers
import torch


def diagnosisVerify():
    model = "ContactDoctor/Bio-Medical-Llama-3-8B"
    pipeline = transformers.pipeline( "text-generation",
                                            model=model, 
                                            model_kwargs={"torch_dtype": torch.bfloat16}, 
                                            device_map = {"": "cuda"})
    messages = [{"role": "system",
                 "content": "You are a expert Medical AI agent trained on healthcare and biomedical domain, whos role is to verify a doctors diagnosis based of a patients symptoms and provide some potential alternative diagnosis"},
                {"role": "user",
                "content": "35-year-old male: For the past few months, experiencing fatigue, increased sensitivity to cold, and dry, itchy skin. Doctors Diagnosis: hypothyroidism"},
                ]
    prompt = pipeline.tokenizer.apply_chat_template( messages, tokenize=False, add_generation_prompt=True )
    terminators = [ pipeline.tokenizer.eos_token_id, pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>") ]
    outputs = pipeline( prompt, max_new_tokens=256, eos_token_id=terminators, do_sample=True, temperature=0.6, top_p=0.9, ) 
    print(outputs[0]["generated_text"][len(prompt):])
    

diagnosisVerify()