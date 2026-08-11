import pytest
from generator.script_generator import generate_multidomain_script, generate_ai_script

def test_generate_multidomain_script_python():
    script = generate_multidomain_script("Tutorial de Pandas en Python")
    assert script["title"] == "Tutorial de Pandas en Python"
    assert len(script["scenes"]) >= 5
    assert any(s["type"] == "editor" for s in script["scenes"])

def test_generate_multidomain_script_docker():
    script = generate_multidomain_script("Docker para principiantes")
    assert "Docker" in script["title"]
    assert any("Dockerfile" in s.get("filename", "") for s in script["scenes"] if s["type"] == "editor")

def test_generate_ai_script_fallback():
    script = generate_ai_script("Git y GitHub comandos basicos")
    assert "Git" in script["title"]
    assert len(script["scenes"]) >= 5
