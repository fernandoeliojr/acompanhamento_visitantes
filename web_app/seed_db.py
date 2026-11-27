from app import app
from models import db, Visitor

sample_visitors = [
    {
        "data_chegada": "2026-11-22", "culto": "Domingo Noite - 19h", "nome": "Lucas Gabriel Souza",
        "whatsapp": "(11) 98765-4321", "email": "lucas.souza@gmail.com", "bairro": "Centro",
        "faixa_etaria": "Jovem (18-29)", "tem_filhos": False, "como_conheceu": "Convite de Amigo",
        "acolhedor": "Mariana Recepção", "autorizou_contato": True, "fase_atual": "Dias 8 a 14",
        "status_geral": "Ativo", "observacoes": "Interesse em grupo de Jovens / LIFE"
    },
    {
        "data_chegada": "2026-11-22", "culto": "Domingo Manhã - 10h", "nome": "Camila Santos Ferreira",
        "whatsapp": "(11) 97654-3210", "email": "camila.ferreira@hotmail.com", "bairro": "Jardim das Flores",
        "faixa_etaria": "Adulto (30-49)", "tem_filhos": True, "como_conheceu": "Instagram da Igreja",
        "acolhedor": "Carlos Apoio", "autorizou_contato": True, "fase_atual": "Dias 3 a 7",
        "status_geral": "Ativo", "observacoes": "Casada, 1 filho. Pediu oração"
    }
]

with app.app_context():
    for v_data in sample_visitors:
        v = Visitor(**v_data)
        db.session.add(v)
    db.session.commit()
    print("Database seeded with sample data.")
