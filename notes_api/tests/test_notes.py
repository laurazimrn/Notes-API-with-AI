from fastapi.testclient import TestClient
from notes_api.main import app



client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API de Análise"} or "Notes API with Ollama" in response.json()["message"]

def test_create_note():
    response = client.post("/notes/", json={"titulo": "Teste", "conteudo": "Conteúdo da nota"})
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "Teste"
    assert data["conteudo"] == "Conteúdo da nota"
    assert "id" in data

def test_read_notes():
    response = client.get("/notes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_update_note():
    # Primeiro cria uma nota
    create = client.post("/notes/", json={"titulo": "Antigo", "conteudo": "Texto antigo"})
    note_id = create.json()["id"]

    # Atualiza a nota
    response = client.put(f"/notes/{note_id}", json={"titulo": "Novo", "conteudo": "Texto novo"})
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "Novo"
    assert data["conteudo"] == "Texto novo"

def test_delete_note():
    # Cria uma nota
    create = client.post("/notes/", json={"titulo": "Apagar", "conteudo": "Será deletada"})
    note_id = create.json()["id"]

    # Deleta a nota
    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Nota deletada com sucesso"
