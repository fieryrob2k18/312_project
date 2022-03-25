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
def renderHtmlTemplate(html):
    return html
