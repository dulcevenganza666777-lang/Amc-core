import json
import os
import glob

class ObjectiveEngine:
    """
    Motor de decisiones: Calcula el Top 5 de EBV (Expected Business Value).
    Cumple: Regla 1 Derecho a no decidir, Regla 3 Explicabilidad
    """
    def __init__(self, workspace="AMC-Core"):
        self.workspace = workspace
        self.snapshots_dir = os.path.join(workspace, "knowledge", "snapshots")
        self.confidence_threshold = self._get_threshold() # Umbrales evolutivos
        
    def _get_threshold(self):
        # Regla 4: Umbrales evolutivos 80%→65%
        video_count = len(glob.glob(os.path.join(self.workspace, "knowledge", "*.db")))
        if video_count < 30: return 0.80 # Bootstrap
        elif video_count < 100: return 0.75 # Aprendizaje
        elif video_count < 300: return 0.70 # Consolidación
        else: return 0.65 # Maduro

    def get_latest_snapshots(self):
        os.makedirs(self.snapshots_dir, exist_ok=True)
        list_of_files = glob.glob(os.path.join(self.snapshots_dir, '*.json'))
        if not list_of_files: return []
        return sorted(list_of_files, key=os.path.getctime, reverse=True)

    def calculate_ebv(self, evidence):
        """Regla 3: Explicabilidad. Devuelve evidencia + predicción + riesgo"""
        scores = []
        for vid in evidence:
            views = vid.get('view_count', 0)
            likes = vid.get('like_count', 0)
            duration = vid.get('duration', 23)
            # EBV = Impacto * Confianza - Riesgo
            impact = (views * 0.6) + (likes * 10 * 0.3) + ((23 - abs(23 - duration)) * 0.1)
            evidence_conf = min(len(evidence) / 50, 1.0) # Regla 0: Múltiples fuentes
            prediction_conf = 0.5 # TODO: learning_engine.py
            risk = 0.1 if "spiral" not in vid.get('title','').lower() else 0.4 # Repetir = riesgo
            ebv = impact * evidence_conf * prediction_conf * (1 - risk)
            scores.append({
                "title": vid.get('title'), 
                "ebv": ebv,
                "explicacion": f"Impacto:{impact:.0f} x Evidencia:{evidence_conf:.2f} x Pred:{prediction_conf:.2f} x Riesgo:{risk:.2f}"
            })
        return sorted(scores, key=lambda x: x['ebv'], reverse=True)[:5]

    def run(self):
        files = self.get_latest_snapshots()
        if not files:
            print("[CEO] NO DECISIÓN: No hay evidencia (snapshots). Regla 1 respetada.")
            return None
            
        with open(files[0], 'r') as f:
            data = json.load(f)
            evidence = data.get('evidence', [])
            
        top5 = self.calculate_ebv(evidence)
        if not top5 or top5[0]['ebv'] < self.confidence_threshold:
            print(f"[CEO] NO DECISIÓN: EBV máximo {top5[0]['ebv']:.2f} < umbral {self.confidence_threshold:.2f}")
            print("[CEO] Acción: Diseñar experimento. Regla 1 respetada.")
            return None
        return top5

if __name__ == "__main__":
    engine = ObjectiveEngine(workspace=".")
    top_5 = engine.run()
    if top_5:
        print("--- TOP 5 DECISIONES SEGÚN EBV ---")
        for i, decision in enumerate(top_5, 1):
            print(f"{i}. {decision['title']} (Score: {decision['ebv']:.2f})")
            print(f" └─ {decision['explicacion']}")
