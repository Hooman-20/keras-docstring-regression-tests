"""Original regression tests for keras-io #2422; no upstream fix is included."""

import os
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

import markdown
import pytest

# Select an unmodified checkout; each checkout is tested in a fresh process.
sys.path.insert(0, str(Path(os.environ["KERAS_IO_CHECKOUT"]) / "scripts"))
import docstrings

PROSE = "Images are augmented during training."
EXAMPLE = "for image in images:\n    if image is not None:\n        augment(image)\n"
INJECTED = (
    "A sample layer.\n\n"
    f"    {PROSE}\n\n"
    "    Args:\n"
    "        factor: Augmentation strength.\n\n"
    "    Example:\n\n"
    "    {{shared_example}}\n"
).replace("{{shared_example}}", "\n```python\n" + EXAMPLE + "```\n")
NORMAL = (
    "A sample layer.\n\n"
    f"    {PROSE}\n\n"
    "    Args:\n"
    "        factor: Augmentation strength.\n"
)


class SampleLayer:
    def __init__(self):
        pass


def render(text):
    # Explicit assignment models runtime injection without compiler dedenting.
    SampleLayer.__doc__ = text
    generator = docstrings.KerasDocumentationGenerator()
    return generator.render_from_object(
        SampleLayer, "study.SampleLayer", "study.SampleLayer"
    )


def html_tree(text):
    html = markdown.markdown(text, extensions=["fenced_code"])
    return ET.fromstring("<root>" + html + "</root>")


@pytest.fixture
def injected_tree():
    return html_tree(render(INJECTED))


def test_injected_prose_is_a_paragraph_not_code(injected_tree):
    paragraphs = ["".join(node.itertext()) for node in injected_tree.findall("./p")]
    assert PROSE in paragraphs
    assert all(
        PROSE not in "".join(node.itertext()) for node in injected_tree.iter("code")
    )


def test_injected_sections_are_recognized(injected_tree):
    # Keras renders section labels as bold paragraphs, not HTML heading tags.
    labels = [node.text for node in injected_tree.findall("./p/strong")]
    assert "Arguments" in labels
    assert "Example" in labels
    arguments = ["".join(node.itertext()) for node in injected_tree.findall("./ul/li")]
    assert "factor: Augmentation strength." in arguments


def test_injected_example_preserves_exact_indentation(injected_tree):
    blocks = [node.text for node in injected_tree.findall("./pre/code")]
    assert EXAMPLE in blocks  # Includes both four-space and eight-space indentation.


def test_normal_docstring_output_is_unchanged():
    # Independent expected output for the ordinary, consistently indented case.
    expected = (
        "### `SampleLayer` class\n\n\n"
        "```python\nstudy.SampleLayer()\n```\n\n\n"
        "A sample layer.\n\n"
        f"{PROSE}\n\n"
        "__Arguments__\n\n- __factor__: Augmentation strength.\n\n\n----\n\n"
    )
    assert render(NORMAL) == expected
