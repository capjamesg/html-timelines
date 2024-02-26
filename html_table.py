import json

import jinja2

with open("table_template.html") as f:
    template = jinja2.Template(f.read())

with open("data.json") as f:
    blog_posts = json.load(f)

rows = ""


def longest_running_colspan_from_now(date_periods, now):
    index = list(date_periods.keys()).index(now)

    longest_running = 0

    for i in range(index, len(date_periods) - 1):
        if date_periods[list(date_periods.keys())[i]] == 0:
            longest_running += 1
        else:
            break

    return longest_running


for key in blog_posts:
    row = f"<tr class='{key.lower()}'><th><a href='https://jamesg.blog/categories/{key.lower()}/'>{key}</a></th>"
    for month in blog_posts[key]:
        if month == "color":
            continue

        colspan = longest_running_colspan_from_now(blog_posts[key], month)
        if isinstance(blog_posts[key][month], dict) and "url" in blog_posts[key][month]:
            row += f"<td><a href='{blog_posts[key][month]['url']}'>&nbsp;</a></td>"
        elif colspan > 0:
            row += f"<td colspan='{colspan}'></td>"
        else:
            row += f"<td></td>"

    row += "</tr>"
    rows += row

rows += "<tr><th></th>"
first_key = list(blog_posts.keys())[0]
for month in blog_posts[first_key]:
    if month == "color":
        continue

    rows += f"<th>{month}</th>"
rows += "</tr>"

css = ""

for item in blog_posts:
    css += f".{item.lower()} td {{background-color: {blog_posts[item]['color']}}}\n"
    css += f".{item.lower()} a {{color: {blog_posts[item]['color']}}}\n"
css += """
#iw-generated-timeline {
    width: 100%;
    border-collapse: collapse;
}
#iw-generated-timeline {width:100%;font-size:smaller; line-height:1.1}
#iw-generated-timeline th {width:8em; text-align:right; padding-right:0.2em}
#iw-generated-timeline td a {display:block; text-align:center; margin-bottom:1px}
#iw-generated-timeline td[colspan] {background:white !important}
"""

output = template.render(rows=rows, css=css)

with open("table.html", "w") as f:
    f.write(output)
