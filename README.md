# 🚚 Digital Twin: Optimizador de Flota AGV (Arauco Challenge)

Simulación avanzada de alta fidelidad para la toma de decisiones estratégicas en la automatización del transporte de lotes de Plywood.

## 🚀 Guía de Inicio Rápido

Ejecuta los siguientes comandos en tu terminal para configurar el entorno y arrancar el Digital Twin:

```bash
# 1. Crear entorno virtual de Python
python -m venv venv

# 2. Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias requeridas
pip install -r requirements.txt

# 4. Ejecutar la simulación
streamlit run simulation.py
```

*Nota: El servidor se levantará automáticamente por defecto en el puerto no convencional `8505` configurado en `.streamlit/config.toml`.*

---

## 🧠 Arquitectura y Decisiones Técnicas

Este desarrollo aplica técnicas de desarrollo premium integrando modelado físico y visualización fluida:
1. **Optimización de Flota (MILP):** Resuelve dinámicamente el balance de línea para satisfacer 60 lotes/h.
2. **Visualización Híbrida:** Utiliza un Canvas HTML5 interpolado por splines cuadráticas de Bezier para asegurar 60 FPS fluidos sin el overhead reactivo de Streamlit.
