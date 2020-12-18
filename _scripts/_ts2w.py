"""generate widget boilerplate updater for python and typescript

"""
import json
import re
import shutil
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import List

from bs4.dammit import UnicodeDammit
from yaml import safe_dump

HERE = Path(__file__).parent
ROOT = HERE.parent
JLPM = shutil.which("jlpm")
ENC = dict(encoding="utf-8")

RE_PY_TRAITS = re.compile(
    r"""(# BEGIN SCHEMAGEN:TRAITS (.*?)\n(.*)# END SCHEMAGEN:TRAITS)""",
    flags=re.M | re.S,
)
RE_TS_PROPERTIES = re.compile(
    r"""(// BEGIN SCHEMAGEN:PROPERTIES (.*?)\n(.*)// END SCHEMAGEN:PROPERTIES)""",
    flags=re.M | re.S,
)


def prop_to_trait(prop_name, prop, add_tag=True, add_help=True):
    """translate a schema to a traitlets trait"""
    # pylint: disable=too-many-locals,too-many-branches
    trait = "Any"
    args = []
    kwargs = []
    tags = []

    ptype = prop.get("type")
    any_of = prop.get("anyOf")

    if any_of:
        trait = "Union"
        args += [
            "[{}]".format(
                ", ".join(
                    prop_to_trait("", any_of_prop, add_tag=False, add_help=False)
                    for any_of_prop in any_of
                )
            )
        ]
    elif ptype == "object":
        trait = "Dict"
    elif ptype == "boolean":
        trait = "Bool"
    elif ptype == "string":
        const = prop.get("const")
        if const is not None:
            trait = "Enum"
            args += [f"'{const}'"]
        else:
            trait = "Unicode"
    elif ptype == "number":
        fmt = prop.get("format")
        if fmt == "int":
            trait = "Int"
        elif fmt == "float":
            trait = "Float"
        else:
            trait = "Union"
            args += ["[T.Float(), T.Int()]"]
    elif ptype == "array":
        trait = "Union"
        args += ["[T.Tuple(), T.Enum([None])]"]
    else:
        print(
            prop_name,
            "\n-----------------------------\n",
            safe_dump(prop, default_flow_style=False),
            "\n-----------------------------\n",
        )

    if add_help and prop.get("description"):
        dammit = UnicodeDammit(prop["description"])
        kwargs += [f"""help='''{dammit.unicode_markup}'''"""]

    if add_tag:
        # might need more tags
        tags += ["sync=True"]
        kwargs += ["allow_none=True", "default_value=None"]

    arg_str = ", ".join(args)
    kwarg_str = ", ".join(kwargs)
    all_args = [a for a in [arg_str, kwarg_str] if a]
    all_arg_str = ", ".join(all_args)
    tag_str = f""".tag({", ".join(tags)})""" if tags else ""

    return f"""T.{trait}({all_arg_str}){tag_str}"""


def update_py(schema, path):
    """update a python file chunk from a schema"""
    txt = path.read_text(**ENC)

    for match in re.findall(RE_PY_TRAITS, txt):
        old, dfn = match[:2]

        root = schema["definitions"][dfn]

        traits = []

        for prop_name, prop in root["properties"].items():
            trait = f"{prop_name} = {prop_to_trait(prop_name, prop)}"
            traits += [trait]

        ind = "\n    "
        new = (
            f"""# BEGIN SCHEMAGEN:TRAITS {dfn}\n"""
            f"""    {ind.join(traits)}\n"""
            f"""    # END SCHEMAGEN:TRAITS\n"""
        )
        txt = txt.replace(old, new)

    path.write_text(txt, **ENC)
    subprocess.check_call(["black", str(path)])


def update_ts(schema, path):
    """update a typescript file from schema"""
    txt = path.read_text(**ENC)

    for match in re.findall(RE_TS_PROPERTIES, txt):
        old, dfn = match[:2]
        root = schema["definitions"][dfn]

        str_props = ", ".join([f"'{p}'" for p in root["properties"].keys()])
        new = (
            f"""// BEGIN SCHEMAGEN:PROPERTIES {dfn}\n"""
            f"""  {str_props}\n"""
            f"""  // END SCHEMAGEN:PROPERTIES\n"""
        )
        txt = txt.replace(old, new)

    path.write_text(txt, **ENC)
    subprocess.check_call([JLPM, "prettier", "--write", str(path)])


def ts_to_widget(schema_path: Path, target_paths: List[Path]):
    """generate widget files"""
    schema = json.loads(schema_path.read_text(**ENC))

    for path in target_paths:
        if path.suffix == ".py":
            update_py(schema, path)
        elif path.suffix == ".ts":
            update_ts(schema, path)

    return 0


def parser():
    """parse command line arguments"""
    p = ArgumentParser("update widget boilerplate from JSON schema")
    p.add_argument("schema", help="the JSON Schema source")
    p.add_argument("targets", nargs="+", help="the .ts or .py files to update")
    return p


def main():
    """main CLI entrypoint"""
    args = parser().parse_args()
    return ts_to_widget(
        schema_path=Path(args.schema), target_paths=[Path(t) for t in args.targets]
    )


if __name__ == "__main__":
    sys.exit(main())
