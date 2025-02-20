#Import open AI OS and System Modules
import openai,os,sys
import json
from MailTypeAndTonePromptChat import returnMailTypeAndTone
from writeExcel import writeDataToExcel
from commonConfig import *


def generateMail():
    prompt2 = []

    if productTitle:
        prompt2.append('I am a seller on ebay. One buyer send me a mail related to product : {}'.format(productTitle))
    else:
        prompt2.append('I am a seller on ebay. One buyer send me a mail')

    prompt2.append('Buyer Mail="{}"'.format(buyerMail))

    if promptMessage:
        prompt2.append('Generate a reply email to the customer, based on the following prompt : {}'.format(promptMessage))

    prompt2.append('\nConsider Following extra information')
    if refundOption:
        if refundOption == 'No':
            prompt2.append('We are unable to refund')
        elif refundOption == 'Partial':
            prompt2.append('We are happy to to offer you partial refund')
        elif refundOption == 'Full':
            prompt2.append('We are happy to refund you full.')

    if returnOption:
        if returnOption == 'No':
            prompt2.append('We are unable to accept return')
        elif returnOption == 'Paid':
            prompt2.append('We are happy to accept return but Shipment charges to be borne by customer')
        elif returnOption == 'Free':
            prompt2.append('We are happy to accept return and we will bear the return shipping charges')

    if exchangeOption:
        if exchangeOption == 'No':
            prompt2.append('We are unable to accept exchange')
        elif exchangeOption == 'Paid':
            prompt2.append('We are happy to offer exchange but Shipment charges to be borne by customer')
        elif exchangeOption == 'Free':
            prompt2.append('We are happy to offer exchange and we will bear the exchange shipping charges')

    if deliveryStatus:
        if deliveryStatus == 'Not Shipped':
            prompt2.append('The product has not been shipped yet')
        elif deliveryStatus == 'Shipped':
            prompt2.append('The product has been shipped')
        elif deliveryStatus == 'Delayed':
            prompt2.append('The product has been shipped, but has been delayed')
        elif deliveryStatus == 'Delivered':
            prompt2.append('The product has been delivered')
        elif deliveryStatus == 'Rescheduled':
            prompt2.append('Nobody received the product, so the delivery is rescheduled')

    if coupon == 'Yes' and couponCode:
        prompt2.append('Also Send coupon code {}'.format(couponCode))

    if buyerName:
        prompt2.append('Buyer Name = {}'.format(buyerName))
    else:
        prompt2.append('Buyer Name is not available')

    if compnayName:
        prompt2.append('Store Name = {}'.format(compnayName))

    if clientName:
        prompt2.append('Customer Support Executive Name (My name) = {}'.format(clientName))

    prompt2.append('Output should be in normal email format, without a subject line, and include line breaks')
    prompt2.append('Do not assume any information which is not mentioned to you')
    prompt2.append('Keep the message around {} word length'.format(wordLength))

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
    completions = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant, who will help generate emails based on prompts, without including anything not explicitly mentioned to you"},
            {"role": "user", "content": prompt_generateMail}
        ],
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=temperature
        ,
    )
    #
    message = (completions.choices[0].message.content).strip()
    pToken = completions.usage.prompt_tokens
    cToken = completions.usage.completion_tokens
    tToken = completions.usage.total_tokens
    return message, prompt_generateMail, pToken, cToken, tToken


if __name__ == '__main__':
    mailType, mailTone, generatedPrompt1, promptToken, completionToken, totalToken = returnMailTypeAndTone(buyerMail, productTitle)

    repliedMail, generatedPrompt2, prompt2Token, completion2Token, total2Token = generateMail()

    writeDataToExcel([temperature, model,  buyerMail, buyerName, productTitle, compnayName, clientName, mailType, mailTone, generatedPrompt1, promptToken, completionToken, totalToken, returnOption, refundOption, exchangeOption, deliveryStatus,coupon, couponCode, promptMessage, generatedPrompt2, prompt2Token, completion2Token, total2Token, repliedMail])

