import sqlite3
from datetime import datetime

db = 'knowledge/knowledge_base.db'

def get_brain_stage():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM internal_videos WHERE status='publico'")
    total = cur.fetchone()[0]
    conn.close()
    
    if total <= 30: return "Bootstrap", 80
    elif total <= 100: return "Aprendizaje", 75
    elif total <= 300: return "Consolidación", 70
    else: return "Maduro", 65

def calculate_ebv(evidence, prediction, risk):
    # EBV = (Evidence * Prediction * (100 - Risk)) / 10000
    return round((evidence * prediction * (100 - risk)) / 10000, 2)

def evaluate_decisions():
    stage, min_conf = get_brain_stage()
    print(f"[Constitution] Etapa: {stage} | Confianza mínima: {min_conf}%")
    
    # Decisión 1: Bounce a 23:00hrs
    evidence_1 = 86 # 1 video propio + 0 competencia, pero 1K views
    prediction_1 = 74 # Histórico: 22/30 aciertos = 74%
    risk_1 = 15 # Bajo riesgo, solo tiempo
    ebv_1 = calculate_ebv(evidence_1, prediction_1, risk_1)
    
    # Decisión 2: Spiral a 02:00hrs 
    evidence_2 = 91 # 2 videos, 71.4% ret alta
    prediction_2 = 74
    risk_2 = 95 # Alto: duplicate_spiral = 95% riesgo FAIL
    ebv_2 = calculate_ebv(evidence_2, prediction_2, risk_2)
    
    # Decisión 3: Mantener igual
    evidence_3 = 50
    prediction_3 = 50 
    risk_3 = 0
    ebv_3 = calculate_ebv(evidence_3, prediction_3, risk_3)
    
    decisions = [
        {"name": "Particles bounce 2 @ 23:00hrs", "evidence": evidence_1, "prediction": prediction_1, "risk": risk_1, "ebv": ebv_1},
        {"name": "Spiral nuevo @ 02:00hrs", "evidence": evidence_2, "prediction": prediction_2, "risk": risk_2, "ebv": ebv_2},
        {"name": "Mantener igual / no publicar", "evidence": evidence_3, "prediction": prediction_3, "risk": risk_3, "ebv": ebv_3},
    ]
    
    # Ordenar por EBV
    decisions = sorted(decisions, key=lambda x: x['ebv'], reverse=True)
    
    print("\n[Evaluator] === TOP 5 DECISIONES POR EBV ===")
    for i, d in enumerate(decisions[:5], 1):
        status = "APROBADA" if d['prediction'] >= min_conf and d['risk'] < 80 else "REQUIERE CEO"
        print(f"{i}. {d['name']}")
        print(f" Evidence: {d['evidence']}% | Prediction: {d['prediction']}% | Risk: {d['risk']}%")
        print(f" EBV: {d['ebv']} | Status: {status}\n")
    
    return decisions[0]

if __name__ == "__main__":
    best = evaluate_decisions()
    print(f"[CEO] ACCIÓN: Ejecutar '{best['name']}' | EBV: {best['ebv']}")
