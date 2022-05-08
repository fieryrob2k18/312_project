import users as u
import html

#Definitions:
#Values not final, syntax TBD

# {{variable}} : replace this with a relevant html sequence

# {{loop}}
# //content...
# {{end_loop}}
#loop for continuously looping over data
#TODO: Require specific data variable to loop over (ie {{loop some_struct}})?

# {{if var}}
# //content...
# {{else}} (optional)
# //content...
# {{end_if}}
#places one of the two blocks in the final html

#Takes html data as input, replace all with html strings
#returns modified html string

#sample functions for testing html template functionality
def test1_func():
    return "<h1>This text made by html template{{}}</h1>"


def comments_func():
    return "<h3>No comments currently!</h3>\r\n"
    comments = u.get_comments()
    if len(comments) == 0:
        return "<h3>No comments currently!</h3>\r\n"
    out = ""
    for comment in comments:
        out += "<p>" + html.escape(comment) + "</p>\r\n"
    return out


def users_func():
    users = u.get_users()
    if len(users) == 0:
        return "<h3>No users online currently!</h3>"
    out = "<h3>Users Online:</h3>\r\n"
    for user in users.keys():
        out += "<div class=\"username\"><p>" + html.escape(user) + "</p>\r\n"
        if users[user] == "":
            out += "<img class=\"profileimg\" src=\"default.jpg\"></div>"
        else:
            #assume no bad stuff in profile pictures
            out += "<img class=\"profileimg\" src=\"" + users[user] + "\"></div>"
    return out


#dictionary for storing html template functions
tmpl_dict = {"TEST1": test1_func,
             "users": users_func,
             "comments": comments_func}


#Replace template vars in html with output
#Note that while object is a byte list,
#It does get briefly converted to a string in this function
def renderHtmlTemplate(html):
    #convert to string for string parsing funcs
    #splitting like this avoids replacing user input with {{}}
    #Since each part is looked at only once
    #html is assumed to always be a bytes object
    html_str = html.decode("utf-8")
    parsed_html = html_str.split("{{")
    #we'll reuse html_str for the output
    html_str = ""

    for section in parsed_html:
        #check if the key was found
        key_replaced = False
        for key in tmpl_dict:
            replace_val = key + "}}"
            if section.startswith(replace_val):
                key_replaced = True
                output = tmpl_dict[key]()
                section = section.replace(replace_val, output)
                #under this format there is only one key per section
                break
        #if the value wasn't a proper one, replace with empty str
        #(or there is no key, like at the beginning of a file)
        if not key_replaced:
            idx = section.find("}}")
            if idx > -1:
                #add the 2 to remove brackets as well
                html_str += section[idx+2:]
            else:
                html_str += section
        else:
            html_str += section
    return bytes(html_str, "utf-8")
