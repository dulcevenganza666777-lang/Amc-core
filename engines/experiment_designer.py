#!/usr/bin/env python3
"""
Experiment Designer - Regla 1: Derecho a no decidir
Si confianza < umbral, diseña test barato para ganar evidencia.
"""
class ExperimentDesigner:
    def design_test(self, low_conf_decision):
        """Ejemplo: Si bounce tiene conf 65%, test: Subir 2 shorts 8s sin edición"""
        print(f"[Experiment] Conf baja para: {low_conf_decision}")
        print("[Experiment] Test: 2 variantes 8s, $0 costo, mide hook 1s")
        print("[Experiment] Si 1 gana >40% ret, subir conf a 80%")
        return {"test_type":"A/B_cheap", "cost":0, "metric":"retention_3s"}
        
if __name__ == "__main__":
    ExperimentDesigner().design_test("bounce_v2")
