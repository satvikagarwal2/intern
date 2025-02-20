#import os, sys, datetime, queue, subprocess, glob, traceback, time, psutil, win32serviceutil, win32service, shutil, ctypes, win32com.client, pandas
import os, sys, datetime, queue, subprocess, glob, traceback, time, shutil, ctypes, pandas

from winreg import *
from threading import Thread, active_count
from PyQt5 import uic
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication


fullpath = "mainwindowNew.ui"
appBase, appForm = uic.loadUiType(fullpath)


class mainWindowNew(appBase, appForm):

    def __init__(self, userID ,app = None, parent = None):
        super(appBase,self).__init__(parent)
        self._bucket = queue.Queue()
        self.app =app
        self.parent = parent
        self._userID = userID
        # self._chromeVersion = chromeVersion_
        self._disabledTabs = []
        self.setupUi(self)
        # self.icon = QIcon(resource_path("windowICON.png"))
        # self.setWindowIcon(self.icon)
        self.setWindowTitle('eBay BOTs')
        # self._enableFeatures()
        # self.setListingTabConfigurations()
        # self.setMailingTabConfigurations()
        # self.setHealthTabConfigurations()
        # self.setSetupTabConfigurations()
        # self.setConfigTabConfigurations()
        # self.setEditTabConfigurations()
        self.tabWidget.setCurrentIndex(0)
        # quit = QAction("Quit", self)
        # quit.triggered.connect(self.closeEvent)
        # MergeAllMastersInToOne()
        self.wizrdConfig()
        self.show()

    def wizrdConfig(self):
        self.readMailButton.clicked.connect(self.readMailButtonFunction)
        self.sendMailButton.clicked.connect(self.sendMailButtonFunction)
        self.mailCategory.activated.connect(self.subcategoryUpdate)
        self.wordLengthOptions.setCurrentIndex(2)

    def subcategoryUpdate(self):
        self.mailSubCategory.clear()
        category = self.mailCategory.currentText()

        subcategories = {
            "Product": ['Enquiry', 'Complaint'],
            "Order": ['Placement', 'Detail Request', 'Return', 'Exchange', 'Refund', 'Repair', 'Cancellation'],
            "Delivery": ['Address Change', 'Information Change', 'Status Request', 'Tracking Request'],
            "Enquiry": ['Cancellation Policy', 'Refund Policy', 'Return Policy', 'Exchange Policy', 'Delivery Options']
        }

        self.mailSubCategory.addItems(subcategories[category])

    def sendMailButtonFunction(self):
        self.disableWidgets()

        refundOption, returnOption, exchangeOption, deliveryStatusOption, sendCoupon, couponValue, prompt, mType, mSubType, mTone, wordLength = self.getParameters()
        time.sleep(2)
        self.enableWidgets()

        return refundOption, returnOption, exchangeOption, deliveryStatusOption, sendCoupon, couponValue, prompt, mType, mSubType, mTone, wordLength



    def readMailButtonFunction(self):
        self.disableWidgets()
        time.sleep(2)

        print('read mail done')

        # Sample Category extracted from Mail
        _mailCategory = "Product"
        _mailSubCategory = "Complaint"

        indexCategory = self.readMailButton.findText(_mailCategory)
        self.mailCategory.setCurrentIndex(indexCategory)
        self.subcategoryUpdate()
        indexSubCategory = self.mailSubCategory.findText(_mailSubCategory)
        self.mailSubCategory.setCurrentIndex(indexSubCategory)

        self.enableWidgets()

    def getParameters(self):

        _refund = self.refundOptions.currentText()
        _return = self.returnOptions.currentText()
        _exchange = self.exchangeOptions.currentText()
        _deliveryStatus = self.deliveryStatusOptions.currentText()

        if self.couponCheckBox.isChecked():
            _sendCoupon = 'Yes'
            _couponValue = self.couponValueInput.text()
        else:
            _sendCoupon = ''
            _couponValue = ''

        _prompt = self.promptText.toPlainText()

        _mType = self.mailCategory.currentText()
        _mSubType = self.mailSubCategory.currentText()
        _mTone = self.mailTone.currentText()
        _wordLength  = self.wordLengthOptions.currentText()

        return _refund, _return, _exchange, _deliveryStatus, _sendCoupon, _couponValue, _prompt, _mType, _mSubType, _mTone, _wordLength

    def enableWidgets(self):
        self.correctionWidget.setEnabled(True)
        self.fileWidget.setEnabled(True)
        self.countryWidget.setEnabled(True)
        self.createListings.setEnabled(True)
        self.manualUpload.setEnabled(True)
        self.openChromeListing.setEnabled(True)
        self.openChromeForLogin.setEnabled(True)
        self.addToMasterDB.setEnabled(True)
        self.getFromMaster.setEnabled(True)
        self.deleteFromMaster.setEnabled(True)
        self.deleteFromMasterAuto.setEnabled(True)
        self.getNonActiveSKUs.setEnabled(True)
        self.getNonActiveSKUs2.setEnabled(True)
        self.updateSections.setEnabled(True)
        self.checkImageFolders.setEnabled(True)

        self.openChromeMailing.setEnabled(True)
        self.shipped.setEnabled(True)
        self.replyToFeedback.setEnabled(True)
        self.paymentReceived.setEnabled(True)
        self.askForFeedback.setEnabled(True)
        self.negativeFeedback.setEnabled(True)
        self.awaitingPayment.setEnabled(True)
        self.sendMail.setEnabled(True)
        self.printShippingLabel.setEnabled(True)
        self.printFromShippingLabel.setEnabled(True)
        self.uploadTracking.setEnabled(True)

        self.checkBoxUSAHealth.setEnabled(True)
        self.checkBoxUKHealth.setEnabled(True)
        self.checkBoxAUSHealth.setEnabled(True)
        self.checkBoxCANADAHealth.setEnabled(True)
        self.openChromeHealth.setEnabled(True)
        self.dateEditHealth.setEnabled(True)
        self.autoEnd.setEnabled(True)
        self.autoInform.setEnabled(True)
        self.manageSoldItem.setEnabled(True)
        self.incremental.setEnabled(True)
        self.sendOffer.setEnabled(True)

        self.editListing.setEnabled(True)
        self.openChromeEditing.setEnabled(True)
        self.mergeExcelFile.setEnabled(True)
        self.configure.setEnabled(True)

        self.edit_title.setEnabled(True)
        self.edit_itemSpecific.setEnabled(True)
        self.edit_desc.setEnabled(True)
        self.edit_images.setEnabled(True)
        self.edit_variation.setEnabled(True)
        self.edit_price.setEnabled(True)
        self.edit_quantity.setEnabled(True)
        self.edit_canada.setEnabled(True)
        self.edit_usa.setEnabled(True)
        self.edit_uk.setEnabled(True)
        self.edit_aus.setEnabled(True)

        for i in range(self.tabWidget.count()):
            if i not in self._disabledTabs:
                self.tabWidget.setTabEnabled(i, True)

    def disableWidgets(self):
        self.correctionWidget.setEnabled(False)
        self.fileWidget.setEnabled(False)
        self.countryWidget.setEnabled(False)
        self.createListings.setEnabled(False)
        self.manualUpload.setEnabled(False)
        self.openChromeListing.setEnabled(False)
        self.openChromeForLogin.setEnabled(False)
        self.addToMasterDB.setEnabled(False)
        self.getFromMaster.setEnabled(False)
        self.deleteFromMaster.setEnabled(False)
        self.deleteFromMasterAuto.setEnabled(False)
        self.getNonActiveSKUs.setEnabled(False)
        self.getNonActiveSKUs2.setEnabled(False)
        self.updateSections.setEnabled(False)
        self.checkImageFolders.setEnabled(False)

        self.openChromeMailing.setEnabled(False)
        self.shipped.setEnabled(False)
        self.replyToFeedback.setEnabled(False)
        self.paymentReceived.setEnabled(False)
        self.askForFeedback.setEnabled(False)
        self.negativeFeedback.setEnabled(False)
        self.awaitingPayment.setEnabled(False)
        self.sendMail.setEnabled(False)
        self.printShippingLabel.setEnabled(False)
        self.printFromShippingLabel.setEnabled(False)
        self.uploadTracking.setEnabled(False)

        self.checkBoxUSAHealth.setEnabled(False)
        self.checkBoxUKHealth.setEnabled(False)
        self.checkBoxAUSHealth.setEnabled(False)
        self.checkBoxCANADAHealth.setEnabled(False)
        self.openChromeHealth.setEnabled(False)
        self.dateEditHealth.setEnabled(False)
        self.autoEnd.setEnabled(False)
        self.autoInform.setEnabled(False)
        self.manageSoldItem.setEnabled(False)
        self.incremental.setEnabled(False)
        self.sendOffer.setEnabled(False)

        self.configure.setEnabled(False)
        self.editListing.setEnabled(False)
        self.openChromeEditing.setEnabled(False)
        self.mergeExcelFile.setEnabled(False)

        self.edit_title.setEnabled(False)
        self.edit_itemSpecific.setEnabled(False)
        self.edit_desc.setEnabled(False)
        self.edit_images.setEnabled(False)
        self.edit_variation.setEnabled(False)
        self.edit_price.setEnabled(False)
        self.edit_quantity.setEnabled(False)
        self.edit_canada.setEnabled(False)
        self.edit_usa.setEnabled(False)
        self.edit_uk.setEnabled(False)
        self.edit_aus.setEnabled(False)

    def disableOtherTabs(self, activeTab):
        for i in range(self.tabWidget.count()):
            if i != activeTab:
                self.tabWidget.setTabEnabled(i, False)

    def completeTask(self):
        try:
            msg = self._bucket.get(block=False)
        except queue.Empty:
            msg = "Unexpected Error : "
        self.enableWidgets()
        # dialouge = showdialog(self, msg, 1)
        # dialouge.show()

class ExcThread(QThread):

    def __init__(self, bucket, target, args = None):
        QThread.__init__(self)
        self._bucket = bucket
        self._target = target
        self._args = args

    def run(self):
        try:
            if self._args:
                returnMsg = self._target(*self._args)
            else:
                returnMsg = self._target()
            self._bucket.put(returnMsg)
        except Exception:
            errorMessage = "Unexpected Error : {}".format(str(sys.exc_info()[1]))
            self._bucket.put(errorMessage)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mW = mainWindowNew("TemporaryUserID", app, None)
    app.exec_()
