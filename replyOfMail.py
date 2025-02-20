#Import open AI OS and System Modules
import openai,os,sys
import json
from MailTypeAndTonePrompt import returnMailTypeAndTone
from writeExcel import writeDataToExcel
from commonConfig import *


def generateMail():
    prompt2 = []

    if productTitle:
        prompt2.append('I am a seller on ebay. One buyer send me a mail related to product : {}'.format(productTitle))
    else:
        prompt2.append('I am a seller on ebay. One buyer send me a mail')

    prompt2.append('Buyer Mail="{}"'.format(buyerMail))
    prompt2.append('Generate a reply email to the customer, based on the following prompt : {}'.format(promptMessage))
    prompt2.append('Consider Following extra information')
    if refundOption != 'Choose Option':
        if refundOption == 'No':
            prompt2.append('We are unable to refund')
        elif refundOption == 'Partial':
            prompt2.append('We are happy to to offer you partial refund')
        elif refundOption == 'Full':
            prompt2.append('We are happy to refund you full.')

    if returnOption != 'Choose Option':
        if returnOption == 'No':
            prompt2.append('We are unable to accept return')
        elif returnOption == 'Paid':
            prompt2.append('We are happy to accept return but Shipment charges to be borne by customer')
        elif returnOption == 'Free':
            prompt2.append('We are happy to accept return and we will bear the return shipping charges')

    if coupon == 'Yes' and couponCode:
        prompt2.append('Also Send coupon code {}'.format(couponCode))

    if buyerName:
        prompt2.append('Buyer Nanme = {}'.format(buyerName))
    else:
        prompt2.append('Buyer Name is not available')

    if compnayName:
        prompt2.append('Store Nanme = {}'.format(compnayName))

    if clientName:
        prompt2.append('Customer Support Executive Nanme = {}'.format(clientName))

    prompt2.append('Output should be in normal email format (Not json), without a subject line, and include line breaks, Do not include any information which is not provided to you')

    prompt2.append('Mail Tone should be : {}'.format(mailTone))
    prompt2.append('Mail Type is : {}'.format(mailType))

    prompt_generateMail = '\n'.join(prompt2)

    # prompt2 = 'customerMail="I placed an order for my colgate toothbrush 2 days ago, but it hastn been delivered yet"' \
    #           '' \
    #           'Generate a reply email to the customer from my company, based on the following prompt:' \
    #           '"The product has been shipped, but due to the cyclone, we are not able to deliver on time. Please wait"' \
    #           'Output should have normal email format (Not json), without a subject line, and include line breaks' \
    #           'Do not include any information not provided to you' \
    #           'Mail Tone = Apologetic' \
    #           'My Company Name = Jasonelectroniceaass' \
    #           'My Name = ramesh' \
    #           'Customer Name = suta'

    openai.api_key = apiKey
    completions = openai.Completion.create(
        engine=model,
        prompt=prompt_generateMail,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=temperature
        ,
    )
    #
    message = (completions.choices[0].text).strip()
    pToken = completions.usage.prompt_tokens
    cToken = completions.usage.completion_tokens
    tToken = completions.usage.total_tokens
    return message, prompt_generateMail, pToken, cToken, tToken


if __name__ == '__main__':
    mailType, mailTone, generatedPrompt1, promptToken, completeionToken, totalToken = returnMailTypeAndTone(buyerMail, productTitle)

    repliedMail, generatedPrompt2, prompt2Token, completion2Token, total2Token = generateMail()

    writeDataToExcel([temperature, model,  buyerMail, buyerName, productTitle, compnayName, clientName, mailType, mailTone, generatedPrompt1, promptToken, completeionToken, totalToken, returnOption, refundOption, coupon, couponCode, promptMessage, generatedPrompt2, prompt2Token, completion2Token, total2Token, repliedMail])

