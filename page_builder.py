
def get_page(page_name:str) -> str:
    with open('appui/base.html', 'r') as f:
        # split base html layout on <REQUESTED_PAGE> 
        # should returns array of 2 elements [ 0 => html head , 1 => the end of page ]
        base_headers = f.read().split('<REQUESTED_PAGE>')

    with open(f'appui/pages/{page_name}.html', 'r') as f:
        requested_page = f.read()
    
    return base_headers[0] + requested_page + base_headers[1]
        
