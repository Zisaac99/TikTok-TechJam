from application import app
from application.forms import *
from application.models import *
from flask import render_template, request, flash, redirect, json, jsonify, url_for, make_response, send_file
from flask_login import login_user, login_required, current_user, logout_user, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from application.routes import *
import math
import random
from datetime import datetime
from application import *

# Used to add or minus using str amounts as using float will lead to inaccuracies
# It is already assumed that the max dp for the str amounts is 2dp
def addOrMinusMoney(currAmount, addAmount, type):
    currSplit = currAmount.split(".")
    addSplit = str(addAmount).split(".")
    centsMax = 100

    currDollars = int(currSplit[0])

    if len(currSplit) > 1 and len(currSplit[1]) == 1:
        currCents = int(currSplit[1]) * 10
    elif len(currSplit) > 1 and len(currSplit[1]) > 1:
        currCents = int(currSplit[1])
    else:
        currCents = 0

    addDollars = int(addSplit[0])

    if len(addSplit) > 1 and len(addSplit[1]) == 1:
        addCents = int(addSplit[1]) * 10
    elif len(addSplit) > 1 and len(addSplit[1]) > 1:
        addCents = int(addSplit[1])
    else:
        addCents = 0

    newDollars = 0
    newCents = 0

    if type == "add":
        newDollars = currDollars + addDollars
        newCents = currCents + addCents

        if newCents > centsMax:
            newCents -= centsMax
            newDollars += 1
    else:
        newDollars = currDollars - addDollars
        newCents = currCents - addCents

        if newCents < 0:
            newCents += centsMax
            newDollars -= 1

    return str(f"{newDollars}.{newCents}")
          


def generateDummyData():
    types = ["Withdrawal","Deposit","Transfer"]
    # randAmount = str(round(random.uniform(1, 10000),2))
    # randDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = [Transaction(type = types[random.randint(0,2)], amount = str(round(random.uniform(1, 10000),2)), date = datetime.now(), fk_user_id = 1) for i in range(100)]

    db.session.bulk_save_objects(data)
    db.session.commit()

def ssp_transaction(id,value,col,ot,p,pp):
    # Try-except to prevent crashes
    try:
        query = Transaction.query
        # Get the total number of records from the Job table
        total_count = query.filter_by(fk_user_id = id).count()

        # Create an array to store the dictionary of data for each row later
        trans = []

        query = query.filter_by(fk_user_id = id)
        # If the user search for a value in the datatable's search box we search for it throughout all the columns
        if value != '':
            query = query.filter(
                    Transaction.transaction_id.like(f'%{value}%') |
                    Transaction.amount.like(f'%{value}%') |
                    Transaction.type.like(f'%{value}%') |
                    Transaction.date.like(f'%{value}%'))

        # Order a column ascendingly/descendingly depending on what the user chooses
        if ot == 'asc':
            query = query.order_by(col.asc())
        else:
            query = query.order_by(col.desc())

        # Get the total number of recoreds after all the filtering
        filtered_count = query.count()
        # Check if pagination is selected. By default pagination will be selected. This is just incase pagination is somehow turned off
        if p == -1: # If the number of records needed to be return is -1 we do not need pagination
            # Get all the filtered records
            query = query.all()
            result = query
        else: # Pagination is needed
            # Get all the filtered records and paginate it based on the current page and number of rows to be displayed for that page
            query = query.paginate(page=p, per_page=pp)
            result = query.items

        # Loop through the filtered records
        for i in range(len(result)):
            trans.append({
                'date': result[i].date,
                'amount': result[i].amount,
                'type': result[i].type,
                'accountId': result[i].accountId
            })

        # Return the total count, filtered count, and data in the form of an array that stores the dictionary of each row
        return [total_count,filtered_count,trans]  
    except Exception as error: # If there is an error we catch and print it
        # Rollback if an error occured
        db.session.rollback()
        print(f'Error:{error}')
        return 0

# Generate dummy data
@app.route('/generate', methods = ["POST"])
def generate():
    try:
        generateDummyData()
        return jsonify({'Success': "100 Dummy transaction's data was successfully generated!"})
    except Exception as e:
        return jsonify({'Error': str(e)})
    
@app.route('/api/ssp_transaction', methods=['GET']) 
def api_ssp_transaction():
    userid = current_user.user_id

    # Get the information sent from the job page table
    request_values = request.values

    # How many times the table has been drawn
    draw = int(request_values['draw'])

    # Get the search value in the search box
    search = str(request_values['search[value]'])

    # Store the columns of the datatables in an array
    columns = [Transaction.date, Transaction.amount, Transaction.type, Transaction.accountId]

    # Get the integer which tells us which column needs to be ordered
    # if 'order[0][column]' in request_values:
    if 'order[0][column]' in request_values:
        column_to_order = int(request_values['order[0][column]'])
    else:
        column_to_order = 0
    
    # Order type of the column
    if 'order[0][column]' in request_values:
        order_type = str(request_values['order[0][dir]'])
    else:
        order_type = 'asc'

    # Number of records per page in the table
    per_page = int(request_values['length'])

    # Get the current page
    page = math.trunc(int(request_values['start'])/per_page) + 1
    
    # Pass the needed parameters to the ssp_job_api
    # and get the results needed to return to the table
    results = ssp_transaction(userid,search,columns[column_to_order],order_type,page,per_page)

    # Get the entries from the results
    job = results[2]

    # We need to return the current draw number, total number of records in the table,
    # total number of records filtered, and the data to be displayed
    return jsonify({'draw':draw,'recordsTotal':results[0],'recordsFiltered':results[1],'data':job})

@app.route('/api/add_code', methods=['POST'])
def api_add_code():
    try:
        code = request.values['code']
        amount = request.values['amount']
        
        codeExist = Code.query.filter_by(code = code).first()

        if codeExist:
            return jsonify({"Error":f"Code: {code} already exists in the database"})

        if float(amount) < 0:
            return jsonify({"Error":"Amount cannot be negative!"})
        
        amtSplit = amount.split(".")
        if len(amtSplit) > 1 and len(amtSplit[1]) > 2:
            return jsonify({"Error":"Amount must at max be 2dp!"})
            
        new_code = Code(code = code, amount = amount, isActivated = False)
        db.session.add(new_code)
        db.session.commit()
        return jsonify({"Success":f"Code: {code} of ${amount} was successfully created"})
    except Exception as e:
        return jsonify({'Error':str(e)})
    
@app.route('/api/add_atm', methods=['POST'])
def api_add_atm():
    try:
        atm = request.values['atm']
        withdraw = request.values['withdraw']

        atmExist = ATM.query.filter_by(atmNumber = atm).first()

        if "." in withdraw:
            return jsonify({"Error":"Withdrawl amount must not contain decimals!"})

        withdraw = int(withdraw)

        if withdraw < 0:
            return jsonify({"Error":"ATM max withdrawl amount cannot be negative!"})

        if atmExist:
            atmExist.withdrawAmount = ATM.withdrawAmount + withdraw
            db.session.commit()
            return jsonify({"Success":f"ATM: {atm} has been topped up with with ${withdraw}."})

        new_atm = ATM(atmNumber = atm, withdrawAmount = withdraw)
        db.session.add(new_atm)
        db.session.commit()
        return jsonify({"Success":f"ATM: {atm} with max withdrawl amount of ${withdraw} was successfully created"})
    except Exception as e:
        return jsonify({'Error':str(e)})