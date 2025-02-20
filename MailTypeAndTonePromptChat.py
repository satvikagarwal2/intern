# Import open AI OS and System Modules
import openai, os, sys
import json
from commonConfig import *

def returnMailTypeAndTone(buyerMail, productTitle):
    prompt1 = []
    prompt1.append('Following are my two list variables :')
    prompt1.append("Mail Type = {}".format(mailTypeList))
    prompt1.append("Mail Tone = {}".format(mailToneList))
    prompt1.append('Following is mail received from Customer:')
    prompt1.append("buyerMail = {}".format(buyerMail))
    if productTitle:
        prompt1.append("Product Title : {}".format(productTitle))
    prompt1.append('Now suggest me what Mail Type it is\nSuggest me the tone of the reply email I will generate')
    prompt1.append(
        'reply should only be in python list format [<Mail Type>, <Mail Tone>], nothing else is required')
    # prompt1.append('reply should be in python json format, so that i will directly typecast this output string object to python dict object')
    # prompt1.append('reply output string should be typecast to python dict object i.e. {"Mail Type" : "Product Enquiry"; "Mail Tone" : "Formal"}')

    prompt_mailTT = '\n'.join(prompt1)

    openai.api_key = apiKey
    mailTT_response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant, who answers in only list like [<Mail Type>, <Mail Tone>]"},
            {"role": "user", "content": prompt_mailTT}
        ],
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=temperature
    )

    response = mailTT_response.choices[0].message.content
    mailType = ''
    mailTone = ''
    for i in mailTypeList:
        if i in response:
            mailType = i
            break

    for i in mailToneList:
        if i in response:
            mailTone = i
            break

    promptToken = mailTT_response.usage.prompt_tokens
    completionToken = mailTT_response.usage.completion_tokens
    totalToken = mailTT_response.usage.total_tokens

    return mailType, mailTone, prompt_mailTT, promptToken, completionToken, totalToken


if __name__ == '__main__':
    print(returnMailTypeAndTone(buyerMail, productTitle))