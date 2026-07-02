import subprocess, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class COO:
    def __init__(self):
        self.youtube_adapter = "adapters/youtube_adapter.py"
        self.generator_adapter = "adapters/generator_adapter.py"

    def execute_ceo_order(self, decision):
        """Recibe orden del CEO: {'title':'bounce 15s','style':'bounce'}"""
        print(f"[COO] Orden recibida: {decision['title']}")

        # Paso 1: Generar video - Ejecución Aislada
        cmd_gen = f"python {self.generator_adapter} --style {decision['style']} --output video.mp4"
        result = subprocess.run(cmd_gen, shell=True, capture_output=True)
        if result.returncode != 0:
            self._log_failure("generator", result.stderr.decode())
            return None

        # Paso 2: Subir a YouTube - Ejecución Aislada
        cmd_up = f"python {self.youtube_adapter} --upload video.mp4 --title \"{decision['title']}\""
        result = subprocess.run(cmd_up, shell=True, capture_output=True)
        if result.returncode != 0:
            self._log_failure("uploader", result.stderr.decode())
            return None

        video_id = result.stdout.decode().strip()
        print(f"[COO] Éxito. Video ID: {video_id} | CEO notificado para tracking")
        return video_id

    def _log_failure(self, module, error):
        print(f"[COO] FALLO en {module}: {error}")
        print(f"[COO] Regla 1: Knowledge Debt registrado. CEO debe rediseñar.")

if __name__ == "__main__":
    # Test: COO ejecuta orden manual
    COO().execute_ceo_order({"title":"Test Bounce","style":"bounce"})
