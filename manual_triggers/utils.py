import json 
ip='127.0.0.1'
port=8000
module='audit'

url=f'http://{ip}:{port}/{module}/api/'


# Home Screen APIs
company_id='6c087202-057f-438a-8154-000db3e24eed'



def pretty_print_response(response):
    try:
        json_object=response.json()
    except:
        json_object = response
    print('\n\n' + json.dumps(json_object, indent=3))

def wait(name):
    x='-' * 40
    print('\n'+x)
    print(name, ':')
    input(x + '||\n')


def select_option(choice_list, name):
    accept_input = False
    result = ''
    keys = list(choice_list.keys())
    
    while not accept_input:
        print(f'Enter {name}:\n')
        for index, value in enumerate(keys):
            print(index + 1, value)
        y = input("\n")
        try:
            y = int(y)
            if not (y > 0 and y <= len(keys)):
                continue
            print('Selected:', keys[y - 1])
            result = choice_list[keys[y - 1]]
            accept_input = True
        except:
            continue
    return result