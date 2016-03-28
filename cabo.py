import csv, sys

TAB = '  '

def is_num(x):
	try:
		x = float(x)
	except ValueError:
		return False
	return True

def get_chargees(row):
	inds = [i for i in range(4, len(row))]
	c = [row[i] for i in inds]
	return [x for x in c if x != '']

def get_charges(sheet):
	charges = []
	with open(sheet,'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter = ',')
		for row in reader:
			chargees = get_chargees(row)
			charge = {
				'item': row[1],
				'payer': row[2],
				'amount': row[3],
				'chargees': chargees,
				'num_chargees': len(chargees),
				'day': row[0]
			}
			if charge['num_chargees'] != 0  and is_num(charge['amount']):
				charge['amount'] = float(charge['amount'])
				charges.append(charge)
	return charges

# calculate dict key: ower, values: list of charges owed
def calculate_owing(person, charges):
	owe_dict = {}
	my_charges = [c for c in charges if c['payer'] == person]
	for charge in my_charges:
		chargees = [chargee for chargee in charge['chargees'] if chargee != person]
		for chargee in chargees:
			if chargee not in owe_dict.keys():
				owe_dict[chargee] = []
			owe_dict[chargee].append(charge)
	return owe_dict

def charge_string(charge):
	return str(charge['amount']/charge['num_chargees'])+' for '+charge['item']+' on '+charge['day']

def charge_amount(charge):
	return charge['amount']/charge['num_chargees']

def get_amount_owed(charges):
	return sum([charge_amount(c) for c in charges])

# create printout of who owes you what
def print_owing(person, owing):
	amount_owed = get_amount_owed([item for sublist in owing.values() for item in sublist])
	print '\n=== '+person+' is owed $'+str(amount_owed)+' ==='
	for chargee in owing.keys():
		amount = get_amount_owed(owing[chargee])
		print TAB+chargee+' owes you '+str(amount)
		for charge in owing[chargee]:
			print TAB*2+'* '+charge_string(charge)


# dict keys: payers values: list of charges owed
def calculate_owes(person, charges):
	owes = {}
	for charge in charges:
		if person in charge['chargees'] and charge['payer'] != person:
			if charge['payer'] not in owes.keys():
				owes[charge['payer']] = []
			owes[charge['payer']].append(charge)
	return owes

def print_owes(person, owes):
	owed_amount = get_amount_owed([item for sublist in owes.values() for item in sublist])
	print '\n>>> '+person+' owes $' + str(owed_amount) + ' <<<'
	for payer in owes.keys():
		amount = get_amount_owed(owes[payer])
		print TAB+'You owe '+payer+' $'+str(amount)
		for charge in owes[payer]:
			print TAB*2+'* '+charge_string(charge)

if __name__ == '__main__':
	SHEET = sys.argv[1]
	charges = get_charges(SHEET)
	PAYERS = list(set([charge['payer'] for charge in charges]))
	PAYEES = [charge['chargees'] for charge in charges]
	PAYEES = list(set([item for sublist in PAYEES for item in sublist]))
	for person in PAYERS:
		owing = calculate_owing(person, charges)
		print_owing(person, owing)

	print '\n############# How much each person owes #############'
	for person in PAYEES:
		owes = calculate_owes(person, charges)
		print_owes(person, owes)
