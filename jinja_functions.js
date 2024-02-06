function get_img_url(url, data) {
    if (url === null) {
        return null;
    }

    if (!url.endsWith('.webp')) {
        return `${url}?v=${data['data_version']}`;
    }

    let url_splits = url.split('/');
    let base_url = url_splits.slice(0, -1).join('/');
    let splits = url_splits[url_splits.length - 1].split('.');
    
    if (!data['is_mobile']) {
        return `${base_url}/${splits[0]}_new.webp?v=${data['data_version']}`;
    } else {
        return `${base_url}/${splits[0]}_new_min.webp?v=${data['data_version']}`;
    }
}

function get_animation_classes(anim_name, section_name, data) {
    let ret_str = "";
    if (!data['design'] || !data['design'][section_name] || !data['design'][section_name]['animation'] || !data['design'][section_name]['animation'][anim_name]) {
        return ret_str;
    }

    let animation = data['design'][section_name]['animation'][anim_name];
    let name = animation['name'];
    if (name !== undefined && name !== null) {
        ret_str = name;
        let args = animation['args'];
        if (args !== undefined && args !== null) {
            for (let key in args) {
                ret_str = `${ret_str} ${ret_str}__${key}_${args[key]}`;
            }
        }
    }

    return ret_str;
}

function get_animations_in_page(data) {
    let anims = new Set();
    for (let section in data['design']) {
        if (data['design'][section]['animation'] !== undefined && data['design'][section]['animation'] !== null) {
            for (let anim in data['design'][section]['animation']) {
                anims.add(data['design'][section]['animation'][anim]['name']);
            }
        }
    }

    let animPaths = Array.from(anims).map(anim => `landing_page/animations/${anim}.html`);
    return animPaths;
}

function get_font_face(data) {
    let font_scheme = data['font_scheme'];
    let font_face_root = "";
    let bf = font_scheme['body_font'];
    if (bf['type'] !== undefined && bf['type'] !== null && bf['type'] !== 'css') {
        font_face_root += `
        @font-face {
          font-family: "${bf['name']}";
          font-style: normal;
          font-weight: 400;
          src: url(${bf['link']}) format("${bf['type']}");
          unicode-range: U+000-5FF;
        }
        `;
    }
    bf = font_scheme['head_font'];
    if (bf['type'] !== undefined && bf['type'] !== null && bf['type'] !== 'css') {
        font_face_root += `
        @font-face {
          font-family: "${bf['name']}";
          font-style: normal;
          font-weight: 400;
          src: url(${bf['link']}) format("${bf['type']}");
          unicode-range: U+000-5FF;
        }
        `;
    }

    font_face_root += `
    :root{
      --body-font:"${font_scheme['body_font']['name']}", ${font_scheme['body_font']['family']};
      --head-font:"${font_scheme['head_font']['name']}", ${font_scheme['head_font']['family']};
    }
    `;

    return font_face_root;
}

function extract_alpha(input_str) {
    return Array.from(input_str).filter(char => char.match(/[a-z]/i)).join('').toLowerCase();
}

function get_header_anchor(section_id, host, type = null) {
    if (type === 'external') {
        if (host.includes('localhost')) {
            return 'http://' + host + '/' + section_id;
        } else {
            return 'https://' + host + '/' + section_id;
        }
    } else {    
        if (host.includes('localhost')) {
            return 'http://' + host + '#' + section_id;
        } else {
            return 'https://' + host + '#' + section_id;
        }
    }
}

function get_style_property(prop_name, section_type, data) {
    let section_design = data['design'][section_type];
    if (section_design !== undefined && section_design !== null) {
        let style = section_design['style'];
        if (style !== undefined && style !== null) {
            let prop_value = style[prop_name];
            if (prop_value !== undefined && prop_value !== null) {
                return prop_value;
            }
        }
    }
    return "";
}

function get_font_style_classes(font_scheme) {
    if (font_scheme === null || font_scheme === undefined) {
        return "";
    }

    let classes = "";
    let font_scale = {
        "para_font": {
            "symbol": "p",
            "line_height": 1.5,
            "size": {
                "sm": 12,
                "md": 14,
                "lg": 16,
                "xl": 18
            }
        },
        "label_font": {
            "symbol": "l",
            "line_height": 1.2,
            "size": {
                "sm": 12,
                "md": 14,
                "lg": 16,
                "xl": 18
            }
        },
        "head_font": {
            "symbol": "h",
            "line_height": 1.2,
            "size": {
                "xs": 20,
                "sm": 24,
                "md": 28,
                "lg": 32,
                "xl": 36,
                "xxl": 40
            }
        },
        "display_font": {
            "symbol": "d",
            "line_height": 1.2,
            "size": {
                "xs": 24,
                "sm": 28,
                "md": 32,
                "lg": 36,
                "xl": 40
            }
        }
    };

    classes += "@media only screen and (min-width: 601px) {\n";
    for (let f_name in font_scheme) {
        let detail = font_scale[f_name];
        if (detail === undefined || detail === null) {
            if (f_name === 'body_font') {
                detail = font_scale['para_font'];
            } else {
                continue;
            }
        }

        let sizes = detail['size'];
        for (let sz in sizes) {
            let f_size_scale = font_scheme[f_name]['font_size_scale'];
            if (f_size_scale === undefined || f_size_scale === null) {
                f_size_scale = 1.0;
            }
            let fsize = sizes[sz] * f_size_scale;
            classes += `.font-${detail['symbol']}-${sz} { font-size : ${Math.round(fsize)}px;  line-height : ${detail['line_height']}; font-family : '${font_scheme[f_name]['name']}', ${font_scheme[f_name]['family']}; }\n\t`;
        }
    }

    classes += "\n}\n@media only screen and (max-width: 600px) {\n";

    for (let f_name in font_scheme) {
        let detail = font_scale[f_name];
        if (detail === undefined || detail === null) {
            if (f_name === 'body_font') {
                detail = font_scale['para_font'];
            } else {
                continue;
            }
        }

        let sizes = detail['size'];
        for (let sz in sizes) {
            let f_size_scale = font_scheme[f_name]['font_size_scale'];
            if (f_size_scale === undefined || f_size_scale === null) {
                f_size_scale = 1.0;
            }
            let fsize = sizes[sz] * f_size_scale;
            classes += `.font-m-${detail['symbol']}-${sz} { font-size : ${Math.round(fsize)}px;  line-height : ${detail['line_height']}; font-family : '${font_scheme[f_name]['name']}', ${font_scheme[f_name]['family']}; }\n\t`;
        }
    }

    classes += "\n}\n";
    return classes;
}

function dict_to_json(service) {
    return JSON.stringify(service);
}
