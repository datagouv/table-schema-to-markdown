# -*- coding: utf-8 -*-
import io
import json
import logging

from collections import OrderedDict
from datetime import datetime
from unidecode import unidecode

NAME = "name"
TITLE = "title"
DESCRIPTION = "description"
PRIMARY_KEY = "primaryKey"
MISSING_VALUES = "missingValues"

AUTHOR = "author"
CONTRIBUTOR = "contributor"
VERSION = "version"
CREATED = "created"
HOMEPAGE = "homepage"
EXAMPLE = "example"

log = logging.getLogger(__name__)

SCHEMA_PROP_MAP = OrderedDict(
    [
        (AUTHOR, "Auteur"),
        (CONTRIBUTOR, "Contributeurs"),
        (CREATED, "Schéma créé le"),
        (HOMEPAGE, "Site web"),
        (EXAMPLE, "Données d'exemple"),
        (VERSION, "Version"),
    ]
)

TYPE_MAP = {
    "array": "liste",
    "boolean": "booléen",
    "date": "date",
    "datetime": "date et heure",
    "duration": "durée",
    "geojson": "GéoJSON",
    "geopoint": "point géographique",
    "integer": "nombre entier",
    "number": "nombre réel",
    "object": "objet",
    "string": "chaîne de caractères",
    "time": "heure",
    "year": "année",
    "year-month": "année et mois",
}

FORMAT_MAP = {
    "email": "adresse de courriel",
    "uri": "adresse URL",
    "binary": "données binaires encodées en base64",
    "uuid": "identifiant UUID",
}

TYPE_SPECIFIC_MAP = OrderedDict(
    [
        ("decimalChar", "Séparateur décimal («.» par défaut)"),
        ("groupChar", "Séparateur de groupes de chiffres («,» par défaut)"),
        # 'bareNumber' : 'Nombre nu', => Needs a specific treatment
        ("trueValues", "Valeurs considérées comme vraies"),
        ("falseValues", "Valeurs considérées comme fausses"),
    ]
)

CONSTRAINTS_MAP = OrderedDict(
    [
        ("minLength", lambda v: f"Taille minimale : {v}"),
        ("maxLength", lambda v: f"Taille maximale : {v}"),
        ("minimum", lambda v: f"Valeur minimale : {v}"),
        ("maximum", lambda v: f"Valeur maximale : {v}"),
        ("pattern", lambda v: f"Motif : `{v}`"),
        ("enum", lambda v: f"Valeurs autorisées : {', '.join(v)}"),
    ]
)


def format_format(format_val):
    """ Return markdown format information """
    return f"- `{format_val}` {FORMAT_MAP.get(format_val, '')}\n"


def format_type_specific_info(col_content):
    """ Formats and return info relative to type """
    buff = io.StringIO()
    for prop in TYPE_SPECIFIC_MAP:
        if prop in col_content:
            buff.write(f"{TYPE_SPECIFIC_MAP[prop]} : {col_content[prop]}")

    if "bareNumber" in col_content and col_content["bareNumber"] == "false":
        buff.write(
            "Le nombre peut contenir des caractères "
            "supplémentaires (« € », « % » ...)"
        )
    ret = buff.getvalue()
    buff.close()
    return ret


def format_type(col_content):
    buff = io.StringIO()
    # Type
    type_ = col_content.get("type")
    format_ = col_content.get("format")

    if type_:
        type_val = TYPE_MAP.get(type_, f"??{type_}??")
        buff.write(
            "{}{}|".format(
                type_val,
                ""
                if format_ in ["default", None]
                else " (format `{}`)".format(format_),
            )
        )
        # Type specific properties
        buff.write(format_type_specific_info(col_content))

    # RDFType
    rdf_type = col_content.get("rdfType")
    if rdf_type:
        buff.write(f"{rdf_type}|")

    ret = buff.getvalue()
    buff.close()
    return ret


def format_example(col_content):
    example = col_content.get(EXAMPLE)
    if example:
        return f"{example}|"
    return "|"


def format_constraints(col_content):
    """ Converts type and constraints information into Markdown """
    buff = io.StringIO()

    constraints = col_content.get("constraints")
    if constraints:
        required = None
        if constraints.get("required"):
            required = "Valeur obligatoire"
        elif not constraints.get("required", True):
            required = "Valeur optionnelle"
        constraint_str_list = list(
            filter(
                None,
                [
                    required,
                    "Valeur unique" if constraints.get("unique") else None
                ]
            )
        )

        # minLength, maxLength, minimum, maximum, pattern, enum
        for prop in [prop for prop in CONSTRAINTS_MAP if prop in constraints]:
            constraint_str_list.append(
                CONSTRAINTS_MAP[prop](constraints[prop])
            )

        buff.write(", ".join(constraint_str_list))

    ret = buff.getvalue()
    buff.close()
    return ret


def format_property(name, value):
    if name == CREATED:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%d/%m/%Y")
    if name == MISSING_VALUES:
        if value == [""]:
            return ""
        return ", ".join(map(lambda v: f'`"{v}"`', value))
    if name == PRIMARY_KEY:
        return ", ".join(value) if isinstance(value, list) else value
    return value


def format_name(field_json):
    buff = io.StringIO()

    field_name = field_json.get("name")
    buff.write(
        f"|{field_name if field_name else 'Erreur : nom manquant'}"
    )

    title = field_json.get("title")
    if title:
        buff.write(f" ({title})")

    buff.write("|")

    ret = buff.getvalue()
    buff.close()
    return ret


def convert_source(source, out_fd, style='table'):
    log.info("Loading schema from %r", source)
    with open(source, encoding="utf-8") as f:
        schema = json.load(f)
    convert_json(schema, out_fd, style)


def write_property(
    schema_json,
    property_name,
    out_fd,
    prefix="",
    suffix="\n\n"
):
    if property_name in schema_json:
        property_value = format_property(
            property_name,
            schema_json[property_name]
        )
        if property_value != "":
            out_fd.write(prefix + property_value + suffix)


def make_link_suitable(field_prop):
    # replacing specific characters with dashes to make the inner links work
    to_rep = [
        ".", "_", "'", "&", "/", ":", ";", "?", "@", "=", "+", "$", "*", " "
    ]
    for c in to_rep:
        field_prop = field_prop.replace(c, '-')
    return unidecode(field_prop.lower(), "utf-8")


def convert_json(schema_json, out_fd, style):
    """ Converts table schema data to markdown """

    # Header
    if NAME in schema_json:
        write_property(schema_json, NAME, out_fd, "## ")
        write_property(schema_json, TITLE, out_fd)
    else:
        write_property(schema_json, TITLE, out_fd, "## ")
    write_property(schema_json, DESCRIPTION, out_fd)

    for property_name in SCHEMA_PROP_MAP.keys():
        prefix = "- {} : ".format(SCHEMA_PROP_MAP[property_name])
        write_property(schema_json, property_name, out_fd, prefix, "\n")

    write_property(
        schema_json,
        MISSING_VALUES,
        out_fd,
        "- Valeurs manquantes : ",
        "\n"
    )
    write_property(
        schema_json,
        PRIMARY_KEY,
        out_fd,
        "- Clé primaire : `",
        "`\n"
    )

    # Foreign keys constraint is more complex
    # than a list of strings, more work required.

    out_fd.write("\n")

    fields = schema_json.get("fields")

    if fields:
        out_fd.write("### Modèle de données\n\n")
        if style == 'table':
            # GitHub Flavored Markdown table header
            headers = ["Nom", "Type", "Description", "Exemple", "Propriétés"]
            out_fd.write("|" + "|".join(headers) + "|\n")
            out_fd.write("|" + "|".join("-" * len(headers)) + "|\n")
            for field in fields:
                convert_field(field, out_fd)

        elif style == 'page':

            out_fd.write("\n##### Liste des propriétés")
            out_fd.write("\n\n| Propriété | Type | Obligatoire |")
            out_fd.write("\n| -- | -- | -- |")

            for field in fields:
                field_name = field.get("name")
                field_title = field.get("title")
                if field_title is not None:
                    strUrl = (
                        f"[{field_name}]"
                        f"(#{make_link_suitable(field_title)}"
                        f"-propriete-{make_link_suitable(field_name)})"
                    )
                else:
                    strUrl = (
                        f"[{field_name}]"
                        f"(#propriete-{make_link_suitable(field_name)})"
                    )

                field_type = field.get("type")
                field_format = field.get("format")
                field_constraints = field.get("constraints")
                strFormat = ""
                if field_format is not None:
                    strFormat = f"(format `{field.get('format')}`)"

                field_title = field.get("title")
                listenums = []
                intervals = ""
                sizes = ""
                pattern = ""

                if field_constraints and field_constraints.get("required"):
                    required = "Oui"
                else:
                    required = "Non"

                out_fd.write(
                    f"\n| {strUrl} | {TYPE_MAP[field_type]} "
                    f"{strFormat} | {required} |"
                )

            out_fd.write("\n")

            for field in fields:
                field_name = field.get("name")
                field_description = field.get("description")
                field_type = field.get("type")
                field_example = field.get("example")
                field_constraints = field.get("constraints")
                field_format = field.get("format")
                field_title = field.get("title")
                listenums = []
                intervals = ""
                sizes = ""
                pattern = ""

                required = None
                if field_constraints:
                    if field_constraints.get("required"):
                        required = "Valeur obligatoire"
                    else:
                        required = "Valeur optionnelle"

                    if field_constraints.get("minLength"):
                        sizes = (
                            f"Plus de {field_constraints['minLength']} "
                            "caractères"
                        )

                    if field_constraints.get("maxLength"):
                        if sizes:
                            sizes = (
                                f"Entre {field_constraints['minLength']} "
                                f"et {field_constraints['maxLength']} "
                                "caractères"
                            )
                        else:
                            sizes = (
                                f"Moins de {field_constraints['maxLength']} "
                                "caractères"
                            )

                    if field_constraints.get("minimum"):
                        intervals = (
                            "Valeur supérieure à "
                            f"{field_constraints['minimum']}"
                        )

                    if field_constraints.get("maximum"):
                        if intervals:
                            intervals = (
                                f"Valeur entre {field_constraints['minimum']}"
                                f" et {field_constraints['maximum']}"
                            )
                        else:
                            intervals = (
                                "Valeur inférieure à : "
                                f"{field_constraints['maximum']}"
                            )

                    if field_constraints.get("pattern"):
                        pattern = str(field_constraints['pattern'])

                    if field_constraints.get("enum"):
                        listenums = field_constraints["enum"]

                out_fd.write("\n#### ")
                if field_title is not None:
                    out_fd.write(f"{field_title} - ")
                out_fd.write(f"Propriété `{field_name}`")
                out_fd.write(f"\n\n> *Description : {field_description}*")
                if field_example:
                    out_fd.write(f"<br/>*Exemple : {field_example}*")
                if required is not None:
                    out_fd.write(f"\n- {required}")
                else:
                    out_fd.write("\n- Valeur optionnelle")
                out_fd.write(f"\n- Type : {TYPE_MAP[field_type]}")
                if field_format is not None:
                    out_fd.write(f" (format `{field_format}`)")
                if len(listenums) > 0:
                    out_fd.write("\n- Valeurs autorisées : ")
                    for enum in listenums:
                        # to prevent weird display due
                        # to markdown quoting mechanism
                        out_fd.write(
                            "\n    - {}".format(
                                "\\" + enum if isinstance(enum, str) and enum.startswith(">")
                                else enum
                            )
                        )
                if intervals != "":
                    out_fd.write(f"\n- {intervals}")
                if sizes != "":
                    out_fd.write(f"\n- {sizes}")
                if pattern != "":
                    out_fd.write(f"\n- Motif : `{pattern}`")
                out_fd.write("\n")


def format_description(field_json):
    description = field_json.get("description")
    if description:
        return f"{description}|"
    return ""


def convert_field(field_json, out_fd):
    """ Convert JSON content describing a column to Markdown"""

    out_fd.write(format_name(field_json))
    out_fd.write(format_type(field_json))
    out_fd.write(format_description(field_json))
    out_fd.write(format_example(field_json))
    out_fd.write(format_constraints(field_json))

    out_fd.write("|\n")


def sources_to_markdown(schema_json):
    if "sources" not in schema_json:
        return None
    md = "## Socle juridique du schéma\n"
    for source in schema_json["sources"]:
        if not all(k in source for k in ["title", "path"]):
            return None
        md += f"- [{source['title']}]({source['path']})\n"
    return md
