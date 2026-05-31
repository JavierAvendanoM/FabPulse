# FabPulse — Session Log Format & Rules

Cada sesión de trabajo genera un log. Este archivo define el formato, las reglas, y el propósito de cada sección.

---

## Propósito de los logs

1. **Memoria técnica** — qué se construyó, qué se decidió, por qué
2. **Evidencia del hackathon** — historia de desarrollo verificable con fechas reales
3. **Contenido de redes sociales** — cada sesión genera posts listos para publicar
4. **Contexto para la siguiente sesión** — el prompt de inicio ya está escrito

---

## Convención de nombre de archivo

```
session-[NN]-[mes][dia].md
```

Ejemplos:
- `session-01-may29.md`
- `session-02-may31.md`
- `session-03-jun02.md`

`[NN]` es un número de dos dígitos que incrementa secuencialmente. Nunca saltearlo.

---

## Estructura del archivo

### 1. Header (obligatorio)

```markdown
# FabPulse — Dev Log

---

## Session [NN] — [Mes] [Dia], [Año]

**Focus:** [Una línea describiendo el tema central de la sesión]
```

### 2. What Was Done (obligatorio)

Lista numerada de lo que se hizo, con narrativa real — no bullet points secos. Cada ítem debe explicar el **qué** y el **por qué**, no solo nombrar la tarea. Incluir snippets de código o output cuando sea relevante.

```markdown
### What Was Done

**1. Título del trabajo**

Párrafo explicando qué se hizo y por qué importa. Mencionar decisiones
de diseño, tradeoffs, o comportamientos no obvios.

```code
// snippet relevante si aplica
```

**2. Siguiente bloque de trabajo**
...
```

### 3. Problemas encontrados y soluciones (condicional)

Incluir solo si hubo problemas reales. Formato tabla con tres columnas.

```markdown
### Problemas encontrados y soluciones

| Problema | Causa | Solución |
|---|---|---|
| Error específico | Por qué ocurrió | Cómo se resolvió |
```

### 4. Files Created (obligatorio)

Tabla completa de todos los archivos nuevos o modificados significativamente.

```markdown
### Files Created

| File | Location | Purpose |
|---|---|---|
| `nombre.py` | `ruta/` | Qué hace |
```

### 5. Decisions Made (obligatorio)

Solo decisiones no-obvias que alguien podría cuestionar. Si la decisión se explica sola, no va aquí.

```markdown
### Decisions Made

| Decision | Rationale |
|---|---|
| Decisión tomada | Por qué esta opción y no la alternativa |
```

### 6. Next Session (obligatorio)

**Siempre incluir el prompt listo para copiar y pegar.** Alguien debería poder abrir una nueva sesión de Claude Code, pegar el prompt, y saber exactamente dónde continuar.

```markdown
### Next Session — [Tema de la próxima sesión]

**Goal:** Una línea con el objetivo concreto.

**Checklist antes de empezar:**
- [ ] Item que el usuario debe verificar
- [ ] Otro prerequisito

**Starting prompt:**
```
Texto del prompt listo para copiar y pegar.
Referencia a CLAUDE.md y archivos relevantes.
```

**Files to have open:** Lista de archivos a tener abiertos
```

### 7. Session metadata (obligatorio)

```markdown
*Session duration: ~X hours*
*"Frase que capture el espíritu de la sesión"*
```

### 8. Social Media (obligatorio)

Tres plataformas, en este orden: LinkedIn → X/Twitter → Instagram.

**LinkedIn:** Tono profesional, historia + resultado técnico concreto, 3–5 párrafos, 5–8 hashtags. Empezar con el emoji `🏗️` o similar.

**X/Twitter:** Formato corto, bullet points con checkmarks `✅`, máximo 280 caracteres por tweet (puede ser hilo si es necesario), 3–4 hashtags.

**Instagram/Reels:** Tono más personal, referencia al journey, CTA "follow the build", 5–8 hashtags.

```markdown
## 📱 Social Media — Session [NN]

### LinkedIn
> [Post completo listo para copiar y pegar]

---

### X / Twitter
> [Tweet listo para copiar y pegar]

---

### Instagram / Reels caption
> [Caption listo para copiar y pegar]
```

---

## Reglas generales

1. **Escribir en pasado** — documenta lo que ya se hizo, no lo que se va a hacer
2. **Ser específico con los errores** — si hubo un bug, nombrar el error exacto y la causa raíz
3. **Incluir output concreto** — `{"status":"ok"}`, `49 files changed`, un número real siempre que sea posible
4. **No repetir lo que ya está en el código** — el log es contexto y decisiones, no una copia del código
5. **El prompt de siguiente sesión es lo más importante** — si alguien pierde contexto, ese prompt es el recovery
6. **Los posts de redes se escriben el mismo día** — la autenticidad del contenido depende de la frescura
7. **Nunca dejar `Next Session` en blanco** — aunque la sesión termine sin plan claro, escribir el estado actual y el siguiente paso lógico

---

## Cuándo crear un nuevo log vs. actualizar uno existente

- **Nuevo log:** Cada vez que se trabaja en el proyecto, independientemente de cuánto se avanzó
- **Actualizar existente:** Solo para corregir errores factuales (typo en un nombre de archivo, fecha incorrecta)
- **No actualizar** para agregar trabajo posterior — eso va en la siguiente sesión

---

## Checklist antes de cerrar una sesión

- [ ] Session log creado con el número correcto
- [ ] Sección "What Was Done" cubre todo lo construido
- [ ] Tabla de problemas y soluciones completada (si aplica)
- [ ] Tabla de archivos creados actualizada
- [ ] Tabla de decisiones completada
- [ ] Prompt de siguiente sesión escrito y probado mentalmente
- [ ] Los tres posts de redes sociales redactados
- [ ] SCHEDULE.md actualizado con checkboxes
- [ ] CLAUDE.md actualizado con "Current Priorities"
- [ ] Git commit realizado con mensaje descriptivo
