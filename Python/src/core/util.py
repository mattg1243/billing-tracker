# General
from decimal import Decimal
from datetime import datetime

# Digest
from digest import ensure_payment_info

# For PDF Handling
from borb.pdf.pdf import PDF
from borb.pdf.page.page import Page
from borb.pdf.document import Document
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.color.color import HexColor, X11Color
from borb.pdf.canvas.layout.table.table import TableCell


# STATEMENT GENERATION
def skele():
    pdf = Document()
    page = Page()
    pdf.append_page(page)
    page_layout = SingleColumnLayout
    page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.02)
    return pdf

# Phone Number Formatter
def phone_formatter(n):
    return format(int(n[:-1]), ",").replace(",", "-") + n[-1]

# Builds Statement Header
def build_statement_header(provider, client, running):
    # Initialize
    header = Table(number_of_rows=11, number_of_columns=3)
    
    # Centered provider name
    header.add(Paragraph(" "))
    header.add(
        Paragraph(
            provider["name"],
            font="Helvetica-Bold",
            horizontal_alignment=Alignment.CENTERED
        )
    )
    header.add(Paragraph(" "))
    
    # Centered provider street address
    header.add(Paragraph(" "))
    header.add(
        Paragraph(
            provider["address"]["street"],
            horizontal_alignment=Alignment.CENTERED
        )
    )
    header.add(Paragraph(" "))
    
    # Centered provider city, state, zip code
    header.add(Paragraph(" "))
    header.add(
        Paragraph(
            provider["address"]["cityState"],
            horizontal_alignment=Alignment.CENTERED
        )
    )
    header.add(Paragraph(" "))
    
    # Format Provider Phone Number
    phone = phone_formatter(provider["phone"])
    print(phone)
    
    # Centered provider phone number
    header.add(Paragraph(" "))
    header.add(
        Paragraph(
            phone,
            horizontal_alignment=Alignment.CENTERED
        )
    )
    header.add(Paragraph(" "))
    
    # Centered provider email address
    header.add(Paragraph(" "))
    header.add(
        Paragraph(
            provider["email"],
            horizontal_alignment=Alignment.CENTERED,
        )
    )
    header.add(Paragraph(" "))
    
    # Empty Lines break
    header.add(Paragraph(" "))
    header.add(Paragraph(" "))
    header.add(Paragraph(" "))
    header.add(Paragraph(" "))
    header.add(Paragraph(" "))
    header.add(Paragraph(" "))
    
    # Left Aligned Client Name
    client_name = client["clientname"]
    header.add(
        Paragraph(
            f"Client Name: {client_name}",
            horizontal_alignment=Alignment.LEFT,
        )
    )
    header.add(Paragraph(" "))
    header.add(Paragraph(" "))
    
    # Left Aligned Statement Date
    now = datetime.now()
    formatted_now = "%d/%d/%d" % (now.month, now.day, now.year)
    header.add(
        Paragraph(
            f"Statement Date: {formatted_now}",
            horizontal_alignment=Alignment.LEFT
        )
    )
    header.add(Paragraph(" "))
    header.add(Paragraph(" "))
    
    # Left Aligned Running Balance
    running = f"%s{running}" % ('$')
    print(running)
    header.add(
        Paragraph(
            f"Balance: {running}",
            horizontal_alignment=Alignment.LEFT
        )
    )
    header.add(Paragraph(" "))
    header.add(Paragraph(" "))
    
    # Line Breaks to Finish Header
    header.add(Paragraph(" "))
    header.add(Paragraph(" "))
    header.add(Paragraph(" "))
    
    # Padding
    header.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    header.no_borders()

    return header

def build_payments_header(provider):
    # Init Payment info table
    payments = Table(number_of_rows=2, number_of_columns=1)
    
    if(ensure_payment_info(provider)):
        payments.add(
            Paragraph(
                provider["paymentInfo"]
            )
        )
    else:
        payments.add(Paragraph(" "))
    
    # Empty Line break
    payments.add(Paragraph(" "))
    
    return payments.no_borders()

def std_event(event):
    if(event == 'Retainer' or event == 'Refund'):
        return False
    else:
        return True

def build_descrip_table(rows, session, dates, durations, hourly, amounts, new_balance):
    length_of_events = len(dates)
    descrip_table = Table(number_of_rows=rows, number_of_columns=6)
    descrip_table.set_borders_on_all_cells(True, True, True, True)
    for h in ["DATE", "TYPE", "DURATION", "RATE", "AMOUNT", "BALANCE"]:
        descrip_table.add(
            TableCell(
                Paragraph(
                    h,
                    horizontal_alignment=Alignment.LEFT,
                    font_color=X11Color("White"),
                    font_size=10,
                    font="Helvetica",
                ),
                background_color=HexColor("000000"),
            )
        )

    # white
    even_color = HexColor("FFFFFF")

    # Fill Out Table With Events
    iter = 0
    while iter < length_of_events:          # Number of events to iterate through - 16 max on one page 
        # Convert to Working Strings        # If multipaged - only first 16 will be passed into this function
        hourly_rate = str(hourly[iter])     # Then the fn will be called again with the remaining events to be processed being passed in
        amount = str(amounts[iter])         # The length_of_events variable will always refer to how many events are being passed in the current fn call
        balance = str(new_balance[iter])
        
        # Check For Non-Standard Events
        standard = std_event(session[iter])
        
        # Format Datetime Objects
        date = datetime.strftime(dates[iter], "%m-%d-%y")
        
        # Add Dates to Row
        descrip_table.add(TableCell(Paragraph(date), background_color=even_color))
        # Add Event Type
        descrip_table.add(
            TableCell(Paragraph(str(session[iter])), background_color=even_color)
        )
        # Add Event Duration
        if(not standard):
            descrip_table.add(TableCell(Paragraph(" "), background_color=even_color))
        else:
            descrip_table.add(
                TableCell(Paragraph(str(durations[iter])), background_color=even_color)
            )
        # Add Event Rate
        if(not standard):
            descrip_table.add(TableCell(Paragraph(" "), background_color=even_color))
        else:
            descrip_table.add(
                TableCell(Paragraph("$ " + hourly_rate), background_color=even_color)
            )
        # Add Event Cost
        descrip_table.add(
            TableCell(Paragraph("$ " + amount), background_color=even_color)
        )
        # Add Balance After Event
        descrip_table.add(
            TableCell(Paragraph("$ " + balance), background_color=even_color)
        )
        iter += 1

    # If alloted lines is less than the max space
    # Available, fill remaining space with empty rows
    print(rows, iter)
    if iter < rows:
        for row_number in range(iter + 1, rows):
            col_iter = 0
            while col_iter < 6:
                descrip_table.add(
                    TableCell(Paragraph(" "), background_color=even_color)
                )
                col_iter += 1
                if col_iter == 5 and row_number == rows:
                    descrip_table.add(Paragraph("Running Balance: %s" % balance))
                    break
    
    # Set padding on all cells 
    descrip_table.set_padding_on_all_cells(
        Decimal(4), Decimal(4), Decimal(4), Decimal(4)
    )
    descrip_table.no_borders()
    return descrip_table


def generate_statement(CLIENT, PROV, DATES, TYPES, DURATIONS, RATES, AMOUNTS, BALANCE, RUNNING, MULTIPAGE):
    name = CLIENT['clientname']
    print(name)
    
    # Initializing Statement..
    pdf = Document()
    page = Page()
    pdf.append_page(page)
    page_layout = SingleColumnLayout(page, vertical_margin=page.get_page_info().get_height() * Decimal(0.04))
    
    # Append Statement Header
    page_layout.add(build_statement_header(PROV, CLIENT, RUNNING))
    
    # Will Leave an Empty Row if No Payment Info Provided
    page_layout.add(build_payments_header(PROV))
    
    # If single paged - build single description table 
    if(not MULTIPAGE):
        page_layout.add(
            build_descrip_table(22, TYPES, DATES, DURATIONS, RATES, AMOUNTS, BALANCE)
        )
    # Two paged
    elif(len(DATES) < 52):
        # Add 16 events to page 1
        page_layout.add(
            build_descrip_table(28, TYPES[0:26], DATES[0:26], DURATIONS[0:26], RATES[0:26], AMOUNTS[0:26], BALANCE[0:26])
        )
        # Create and Initialize Second Page
        page2 = Page()
        pdf.append_page(page2)
        page2_layout = SingleColumnLayout(page2)
        page2_layout.vertical_margin = page2.get_page_info().get_height() * Decimal(0.02)
        # Add the rest of the events
        page2_layout.add(
            build_descrip_table(33, TYPES[26:], DATES[26:], DURATIONS[26:], RATES[26:], AMOUNTS[26:], BALANCE[26:])
        )
    else:
        # Add 16 events to page 1
        page_layout.add(
            build_descrip_table(28, TYPES[0:26], DATES[0:26], DURATIONS[0:26], RATES[0:26], AMOUNTS[0:26], BALANCE[0:26])
        )
        # Create and Initialize Second Page
        page2 = Page()
        pdf.append_page(page2)
        page2_layout = SingleColumnLayout(page2)
        page2_layout.vertical_margin = page2.get_page_info().get_height() * Decimal(0.02)
        # Add the rest of the events
        page2_layout.add(
            build_descrip_table(39, TYPES[26:58], DATES[26:58], DURATIONS[26:58], RATES[26:58], AMOUNTS[26:58], BALANCE[26:58])
        )
        # Create and Initialize Third Page
        page3 = Page()
        pdf.append_page(page3)
        page3_layout = SingleColumnLayout(page3)
        page3_layout.vertical_margin = page3.get_page_info().get_height() * Decimal(0.02)
        # Add the rest of the events
        page3_layout.add(
            build_descrip_table(39, TYPES[58:], DATES[58:], DURATIONS[58:], RATES[58:], AMOUNTS[58:], BALANCE[58:])
        )
        
        
    # Local path
    with open(f'public/invoices/{name}.pdf', 'wb') as pdf_file:
        PDF.dumps(pdf_file, pdf)
   
   
    """# Heroku path
    with open(f"/app/public/invoices/{cli}.pdf", "wb") as pdf_file:
        PDF.dumps(pdf_file, pdf) """
        
    