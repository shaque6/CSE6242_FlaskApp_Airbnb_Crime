def popup_html(row_num, df_airbnb):
    i = row_num
    name=df_airbnb['name'].iloc[i]
    price=df_airbnb['price'].iloc[i]
    roomtype=df_airbnb['room_type'].iloc[i]
    accom=df_airbnb['accommodates'].iloc[i]
    beds=int(df_airbnb['beds'].iloc[i])
    baths=df_airbnb['bathrooms_text'].iloc[i]
    link=df_airbnb['listing_url'].iloc[i]



    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"

    html = """<!DOCTYPE html>
<html>

<head>
<h4 style="margin-bottom:10"; width="200px"><a href="{}">{}</a></h4>""".format(link, name) + """

</head>
    <table style="height: 20px; width: 200px; border:1px solid black">
<tbody>
<tr style = "border:1px solid black">
<td style = "border:1px solid black">Price Per Night:</td>
<td style = "border:1px solid black">&nbsp; {}</td>""" .format(price) + """
</tr>

<tr style = "border:1px solid black">
<td style = "border:1px solid black">Room Type:</td>
<td style = "border:1px solid black">&nbsp; {}</td>""" .format(roomtype) + """
</tr>

<tr style = "border:1px solid black">
<td style = "border:1px solid black">Accommodates:</td>
<td style = "border:1px solid black">&nbsp; {}</td>""" .format(accom) + """
</tr>

<tr style = "border:1px solid black">
<td style = "border:1px solid black">Beds:</td>
<td style = "border:1px solid black">&nbsp; {}</td>""" .format(beds) + """
</tr>

<tr style = "border:1px solid black">
<td style = "border:1px solid black">Baths:</td>
<td style = "border:1px solid black">&nbsp; {}</td>""" .format(baths) + """
</tr>

</tbody>
</table>
</html>
"""
    return html