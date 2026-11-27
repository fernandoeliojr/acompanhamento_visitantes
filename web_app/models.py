from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

VISITOR_PHASES = ['Dia 0', 'Até 48h', 'Dias 3 a 7', 'Dias 8 a 14', 'Dias 15 a 29', 'Dia 30']

PHASE_SYNONYMS = {
    'até 48 horas': 'Até 48h',
    'ate 48 horas': 'Até 48h',
    'até 48h': 'Até 48h',
    'ate 48h': 'Até 48h',
    'dia 0': 'Dia 0',
    'dias 3 a 7': 'Dias 3 a 7',
    'dias 8 a 14': 'Dias 8 a 14',
    'dias 15 a 29': 'Dias 15 a 29',
    'dia 30': 'Dia 30'
}

STAGE_DESCRIPTIONS = {
    'Dia 0': 'Recepção e Boas-Vindas',
    'Até 48h': 'Primeiro Contato & Cartão',
    'Dias 3 a 7': 'Apresentação Grupo LIFE',
    'Dias 8 a 14': 'Conexão com Líder',
    'Dias 15 a 29': 'Acompanhamento Genuíno',
    'Dia 30': 'Consolidação e Integração'
}

def normalize_phase(phase_name):
    if not phase_name:
        return None
    cleaned = phase_name.strip().lower()
    return PHASE_SYNONYMS.get(cleaned, phase_name)

def get_timeline_stages(fase_atual):
    normalized_current = normalize_phase(fase_atual)

    current_index = -1
    for i, phase in enumerate(VISITOR_PHASES):
        if normalize_phase(phase) == normalized_current:
            current_index = i
            break

    stages = []
    for i, phase in enumerate(VISITOR_PHASES):
        if current_index == -1:
            status = 'upcoming'
            is_current = False
            is_completed = False
        elif i < current_index:
            status = 'completed'
            is_current = False
            is_completed = True
        elif i == current_index:
            status = 'current'
            is_current = True
            is_completed = False
        else:
            status = 'upcoming'
            is_current = False
            is_completed = False

        stages.append({
            'name': phase,
            'description': STAGE_DESCRIPTIONS.get(phase, ''),
            'index': i,
            'step': i + 1,
            'status': status,
            'is_current': is_current,
            'is_completed': is_completed
        })

    return stages

class Visitor(db.Model):
    __tablename__ = 'visitors'

    id = db.Column(db.Integer, primary_key=True)
    data_chegada = db.Column(db.String(20), nullable=False)
    culto = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    whatsapp = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    bairro = db.Column(db.String(100), nullable=True)
    faixa_etaria = db.Column(db.String(20), nullable=True)
    tem_filhos = db.Column(db.Boolean, default=False)
    como_conheceu = db.Column(db.String(100), nullable=True)
    acolhedor = db.Column(db.String(100), nullable=True)
    autorizou_contato = db.Column(db.Boolean, default=False, nullable=False)
    fase_atual = db.Column(db.String(50), nullable=True)
    status_geral = db.Column(db.String(50), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    @property
    def timeline_stages(self):
        return get_timeline_stages(self.fase_atual)

    @property
    def timeline_progress_pct(self):
        stages = self.timeline_stages
        for s in stages:
            if s['is_current']:
                return int((s['index'] / (len(VISITOR_PHASES) - 1)) * 100)
        if all(s['is_completed'] for s in stages):
            return 100
        return 0

    def __repr__(self):
        return f'<Visitor {self.nome}>'
