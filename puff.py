import requests

data = [{'emp_id': 1.0, 'device_id': 'ABB00', 'name': 'Shubham', 'Address': 'XYZ',
        "Friends": ['happy', 'Amit','shona','goli']},
        {'emp_id': 2.0, 'device_id': 'ABB01', 'name': 'Gaurav', 'Address': 'ABC',
        "Friends": ['garry', 'harry','marry','cherry']}
        ]
# print(data)
dic = {}
frnd = []

for value in data:
    dic[value.get('name')+'_friends'] = []  # Put that variable in another dictionary with new variable
    f = value['Friends']
    # if value.get('name')+'_friends' in dic:
    dic[value.get('name')+'_friends'].append(f)
print(dic)

# for value in data:
#        f = value['Friends']        # Extract data from json field 'Friends'
#        frnd.append(f)              # Stores it in the variable
#        dic[value.get('name')+'_friends'] = frnd  # Put that variable in another dictionary with new variable
# print(dic)

## to mail the dictionary
def mail(json_data):
       url = 'http://13.233.236.200:8080/service-email/MailService'
       # payload = "{\n\t\"user\":\"whirlybirdmailer\",\n\t\"password\":\"monster@123\"," \
       #           "\n\t\"to\":[\"shubhammishra125006@gmail.com\"],\n\t\"cc\":[],\n\t\"bcc\":[],\n\t\"subject\":\"mail for the test\"," \
       #           "\n\t\"message_body\":\"<h2>Dear team,</h2><p>Please find the Daily Generation details as below " \
       #           "\n\"\n}"
       payload = "{\n\"user\":\"whirlybirdmailer\",\n\"password\":\"monster@123\"," \
                 "\n\"to\":[\"shubham@gmail.com\"],\n\t\"cc\":[],\n\t\"bcc\":[],\n\"subject\":\"mail for the test\"," \
                 "\n\t\"message_body\":\"<h2>Dear team,</h2><p>Please find the Daily Generation details as below " \
                 "\n\"\n}"
       headers = {
              'Content-Type': 'application/json',
              'Content-Type': 'text/plain'
       }
       Postresponse = requests.request("POST", url, headers=headers, data=payload)
       print(Postresponse.text.encode('utf8'))

# mail(dic)


