data = {
    "figma_id": "1:1756",
    "font_link": "",
    "template_name": None,
    "background_asset": "https://chroneapp.s3.amazonaws.com/campaign-flyer-template/gif_a.gif",
    "discount": {
        "x": 40,
        "y": 100,
        "color": "white",
        "font": "Sofia, sans-serif",
        "size": 36,
        "weight": None,
    },
    "services": {
        "x": 30,
        "y": 200,
        "color": "white",
        "font": "Sofia, sans-serif",
        "size": 28,
        "weight": None,
    },
    "cta": {
        "x": 60,
        "y": 300,
        "color": "black",
        "font": "Sofia, sans-serif",
        "size": 16,
        "weight": None,
    },
    "biz_name": {
        "x": 40,
        "y": 400,
        "color": "black",
        "font": "Sofia, sans-serif",
        "size": 14,
        "weight": "",
    },
}


def generate_html(data):
    # Check if all required keys are present in the data dictionary
    required_keys = ["background_asset", "discount", "services", "cta", "biz_name"]
    if not all(key in data for key in required_keys):
        return "Error: Missing required data keys."

    # Basic HTML structure
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sofia">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discount Banner</title>
    <style>
        .background {{
            position: relative;
            width: 100vw;
            height: 100vw;
            background-image: url('{data["background_asset"]}');
            background-size: cover;
        }}
        .text-element {{
            position: absolute;
            color: white;
        }}
    </style>
    </head>
    <body>
        <div class="background">
    """

    # Function to create a styled text element
    def create_text_element(class_name, content, position, styles):
        style_string = " ".join(f"{k}: {v};" for k, v in styles.items())
        return f'<div class="text-element" style="top: {(position["y"]/1080)*100}vw; left: {(position["x"]/1080)*100}vw; {style_string}">{content}</div>'

    # Add the text elements
    for key in ["discount", "services", "cta", "biz_name"]:
        element_data = data[key]
        styles = {
            "color": element_data.get("color", "white"),
            "font-family": element_data.get("font", "Arial, sans-serif")
            or "Arial, sans-serif",
            "font-size": f"{(element_data.get('size', '16')/1080)*100 or ' calc((16/1080)*100)'}vw",
            "font-weight": element_data.get("weight", "normal") or "normal",
        }
        html += create_text_element(key, key.upper(), element_data, styles)

    # Close the HTML tags
    html += """
        </div>
    </body>
    </html>
    """

    return html


# Example usage:
html_output = generate_html(data)
print(html_output)
