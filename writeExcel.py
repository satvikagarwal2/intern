import openpyxl

def writeDataToExcel(listVariable):
    # Define the file name
    filename = 'output.xlsx'
    firstTime = False
    # Create a new workbook if the file doesn't exist
    try:
        workbook = openpyxl.load_workbook(filename)
    except FileNotFoundError:
        workbook = openpyxl.Workbook()
        firstTime = True

    # Select the active sheet
    sheet = workbook.active

    if firstTime:
        # Write the header
        header = ['Temperature', 'Model', 'Buyer Mail', 'Buyer Name', 'Product Title', 'Compnay Name', 'Client Name', 'Mail Type', 'Mail Tone', 'Generated Prompt1', 'Prompt Token', 'Completion Token', 'Total Token', 'Return Option', 'Refund Option', 'Coupon', 'Coupon Code', 'Agent Prompt', 'Generated Prompt2', 'Prompt2 Token', 'Completion2 Token', 'Total2 Token', 'Replied Mail', 'Status']
        sheet.append(header)

    # Write the list at the end of the file
    sheet.append(listVariable)

    # Save the workbook
    workbook.save(filename)
