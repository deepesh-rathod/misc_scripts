import re

sp_msg = "Cha-Ching!\nYou have a booking request from {cust_type} on your website.\nName - {name}\nMessage - {message}\nPlease call/text them on {phone} immediately to fix an appointment.\n\nCheers,\nTeam Chrone"

form_data = {
    "name" : "Deepesh test",
    "phone" : "7987215728"
}

def get_sp_msg(sp_msg,form_data):
    pattern = r'{[^}]*}'
    variables = re.findall(pattern, sp_msg)
    for variable in variables:
        variable=variable.replace('{','').replace('}','')
        if variable not in form_data.keys():
            # send slack notif
            print(f"{variable} not present")
            if variable=='service':
                form_data[variable] = "Not Selected"
            elif variable=='message':
                form_data[variable] = "No message"
            elif variable=='cust_type':
                form_data[variable] = "a client"
            else:
                form_data[variable] = "-"
    
    for key,value in form_data.items():
        sp_msg = sp_msg.replace(f"{{{key}}}",f"{value}")
    
    return sp_msg
