from bs4 import BeautifulSoup

class readEbayMail:

    def __init__(self):
        # make into property
        self._productTitle = None
        self._mailBody = None
        self._itemID = None
        self._buyerID = None
        # till here

        ''' declaring the above attributes as properties '''

        @property
        def productTitle(self):
            return self._productTitle

        @productTitle.setter
        def productTitle(self, value):
            self._productTitle = value

        @property
        def mailBody(self):
            return self._mailBody

        @mailBody.setter
        def mailBody(self, value):
            self._mailBody = value

        @property
        def itemID(self):
            return self._itemID

        @itemID.setter
        def itemID(self, value):
            self._itemID = value

        @property
        def buyerID(self):
            return self._buyerID

        @buyerID.setter
        def buyerID(self, value):
            self._buyerID = value

        '''Declaration complete'''

    def readDetailsFromMail(self, pageSourceInsideFrame):
        # BeautifulSoup with the pageSource

        '''
            Beginning the webscrapping script
        '''

        pageSourceInsideFrameSoup = BeautifulSoup(pageSourceInsideFrame, 'html.parser')

        '''
        Can be used to find the iframe with the specific page code
        productIDmailBodyTag = mainTag.find(id="email-body")
        '''

        # finds buyerMail and buyerID

        tableWithNameAndMail = pageSourceInsideFrameSoup.find(id="PrimaryMessage")
        buyerID = tableWithNameAndMail.find(class_="secondary-headline").find('a').text

        customerMailTagText = tableWithNameAndMail.find(id="UserInputtedText").text
        customerMail = re.sub(r'\s+', ' ', customerMailTagText.strip())

        # finds productTitle and itemID

        tableContainer = pageSourceInsideFrameSoup.find(id="area7Container")
        tableWithTitles = tableContainer.findAll('table', class_="device-width")

        anchorWithTitle = tableWithTitles[0].find('a').text
        productTitle = re.sub(r'\s+', ' ', anchorWithTitle.strip())

        '''Following Line of code will try to extract the product title, or assign it NULL in case of an error'''

        try:
            tableWithID = tableWithTitles[1].find('table', class_="twoColumnSixty")
            tdWithProductID = tableWithID.find('td', class_="product-bids")

            for item in tdWithProductID.contents:
                if item.name == 'br':
                    break
                if isinstance(item, str):
                    itemID = item.strip().split()[2]

        # mention specific error

        except:
            itemID = None

        '''
            End of webscrapping script
        '''

        self._buyerID = buyerID
        self._mailBody = customerMail
        self._itemID = itemID
        self._productTitle = productTitle