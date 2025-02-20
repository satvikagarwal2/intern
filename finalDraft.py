from readEbayMail import readEbayMail
import openai
'''
    Things required from commonConfig
    apikey for openai
    temperature
    clientname
    companyname
    mailType List
    mailTone List
    engine model
'''

configurationDict_ = {}
configurationDict_['model'] = "gpt-3.5-turbo"
configurationDict_['temperature'] = 0.25
configurationDict_['clientName'] = "" # To be input accordingly
configurationDict_['companyName'] = "" # To be input accordingly
configurationDict_['apiKey'] = "" # To be input accordingly

configurationDict_['mailTypeList'] = ['Product Enquiry', 'Product Complaint',
                                      'Order placement', 'Order Detail Request', 'Order Return', 'Order Exchange', 'Order Refund',
                                      'Order Repair', 'Order Cancellation',
                                      'Delivery Address Change', 'Delivery Information Change', 'Delivery Status Request', 'Delivery Tracking Request',
                                      'Enquiry Cancellation Policy', 'Enquiry Refund Policy', 'Enquiry Return Policy', 'Enquiry Exchange Policy','Enquiry Delivery Options']

configurationDict_['mailToneList'] = ['Formal', 'Assertive', 'Persuasive', 'Apologetic', 'Assuring']

class mailWizardConfig:

    def __init__(self, parent):
        self.mailReader = readEbayMail()
        self.parent = parent
        self.generatedMail = None
        self.mailIndex = None

    def readMail(self):
        currentURL = self.parent.getCurrentURL()

        # current URL format = https://mesg.ebay.com/mesgweb/ViewMessageDetail/0/m2m/175092920213
        mailIndex = self.getMailIndexFromURL(currentURL)

        if self.mailIndex and self.mailIndex == mailIndex:
            return

        # pageSource = self.parent.getPageSource()
        pageSourceInsideFrame = self.parent.getPageSourceInsideFrame()

        self.mailReader.readDetailsFromMail(pageSourceInsideFrame) # To be connected to GUI read mail button
        self.mailIndex = mailIndex

    def getMailIndexFromURL(self, currentURL):
        return currentURL.split('/')[-1]

    def sendMail(self):
        # send Mail function to be connected to the GUI
        currentURL = self.parent.getCurrentURL()

        if not self.validateMailIndex(currentURL):
            raise Exception("Mail is Not in Sync. Please do 'Read Mail' again")

        promptGenerated = self.generatePrompt()
        self.generateMailFromPrompt(promptGenerated)

    def validateMailIndex(self, currentURL):
        currentIndex = self.getMailIndexFromURL(currentURL)
        if self.mailIndex == currentIndex:
            return True
        return False

    def generateMailFromPrompt(self, prompt):
        # generate the mail from the prompt using gpt
        # include the api key here

        openai.api_key = configurationDict_['apiKey']
        completions = openai.ChatCompletion.create(
            model=configurationDict_['model'],
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant, who will help generate emails based on prompts, without including anything not explicitly mentioned to you"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            n=1,
            stop=None,
            temperature=configurationDict_['temperature']
            ,
        )

        generatedMail = (completions.choices[0].message.content).strip()
        self.generatedMail = generatedMail

    def readBuyerNameFromOrderTab(self):
        # reads buyer name from the order Tab
        return "Samantha"

    def generatePrompt(self, promptMessage, refundOption, returnOption, exchangeOption, deliveryStatus, coupon, couponCode, wordLength, mailTone, mailType):
        prompt = []

        if self.mailReader.productTitle:
            prompt.append(
                'I am a seller on ebay. One buyer send me a mail related to product : {}'.format(self.productTitle))
        else:
            prompt.append('I am a seller on ebay. One buyer send me a mail')

        prompt.append('Buyer Mail="{}"'.format(self.mailReader.mailBody))

        if promptMessage:
            prompt.append(
                'Generate a reply email to the customer, based on the following prompt : {}'.format(promptMessage))

        prompt.append('\nConsider Following extra information')
        if refundOption:
            if refundOption == 'No':
                prompt.append('We are unable to refund')
            elif refundOption == 'Partial':
                prompt.append('We are happy to to offer you partial refund')
            elif refundOption == 'Full':
                prompt.append('We are happy to refund you full.')

        if returnOption:
            if returnOption == 'No':
                prompt.append('We are unable to accept return')
            elif returnOption == 'Paid':
                prompt.append('We are happy to accept return but Shipment charges to be borne by customer')
            elif returnOption == 'Free':
                prompt.append('We are happy to accept return and we will bear the return shipping charges')

        if exchangeOption:
            if exchangeOption == 'No':
                prompt.append('We are unable to accept exchange')
            elif exchangeOption == 'Paid':
                prompt.append('We are happy to offer exchange but Shipment charges to be borne by customer')
            elif exchangeOption == 'Free':
                prompt.append('We are happy to offer exchange and we will bear the exchange shipping charges')

        if deliveryStatus:
            if deliveryStatus == 'Not Shipped':
                prompt.append('The product hsa not been shipped yet')
            elif deliveryStatus == 'Shipped':
                prompt.append('The product has been shipped')
            elif deliveryStatus == 'Delayed':
                prompt.append('The prodcut has been shipped, but has been delayed')
            elif deliveryStatus == 'Delivered':
                prompt.append('The product has been delivered')
            elif deliveryStatus == 'Rescheduled':
                prompt.append('Nobody recieved the product, so the delivery is rescheduled')

        if coupon == 'Yes' and couponCode:
            prompt.append('Also Send coupon code {}'.format(couponCode))

        buyerName = self.readBuyerNameFromOrderTab()

        if buyerName:
            prompt.append('Buyer Nanme = {}'.format(buyerName))
        else:
            prompt.append('Buyer Name is not available')

        if configurationDict_['companyName']:
            prompt.append('Store Name = {}'.format(configurationDict_['companyName']))

        if configurationDict_['clientName']:
            prompt.append('Customer Support Executive Name (My name) = {}'.format(configurationDict_['clientName']))

        prompt.append('Output should be in normal email format, without a subject line, and include line breaks')
        prompt.append('Do not assume any information which is not mentioned to you')
        prompt.append('Keep the message around {} word length'.format(wordLength))

        mailType, mailTone = self.obtainMailTypeAndTone(self.mailReader.mailBody, self.mailReader.productTitle)

        prompt.append('Mail Tone should be : {}'.format(mailTone))
        prompt.append('Mail Type is : {}'.format(mailType))

        promptToGenerateMail = '\n'.join(prompt)

        return promptToGenerateMail

    def obtainMailTypeAndTone(self, buyerMail, productTitle):
        prompt = []

        prompt.append('Following are my two list variables :')
        prompt.append("Mail Type = {}".format(configurationDict_['mailTypeList']))
        prompt.append("Mail Tone = {}".format(configurationDict_['mailToneList']))

        prompt.append('Following is mail received from Customer:')
        prompt.append("buyerMail = {}".format(buyerMail))

        if productTitle:
            prompt.append("Product Title : {}".format(productTitle))

        prompt.append('Now suggest me what Mail Type it is\nSuggest me the tone of the reply email I will generate')
        prompt.append('reply should only be in python list format [<Mail Type>, <Mail Tone>], nothing else is required')

        combinedPrompt = '\n'.join(prompt)

        openai.api_key = configurationDict_['apiKey']
        mailTT_response = openai.ChatCompletion.create(
            model=configurationDict_['model'],
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant, who answers in only list like [<Mail Type>, <Mail Tone>]"},
                {"role": "user", "content": combinedPrompt}
            ],
            max_tokens=2000,
            n=1,
            stop=None,
            temperature=configurationDict_['temperature']
        )

        response = mailTT_response.choices[0].message.content

        mailType = ''
        mailTone = ''

        for i in configurationDict_['mailTypeList']:
            if i in response:
                mailType = i
                break

        for i in configurationDict_['mailToneList']:
            if i in response:
                mailTone = i
                break

        return mailType, mailTone
