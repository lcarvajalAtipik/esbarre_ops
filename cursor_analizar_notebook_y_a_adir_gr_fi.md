# Analizar notebook y añadir gráfica de clientes
_Exported on 04/12/2025 at 15:16:00 CET from Cursor (2.0.34)_

---

**User**

@analisis_clientes.ipynb quiero que entienda sy analices este notebook. 



Quiero que me añadas en una celda una gráfica de la evolución de clientes que dieron al menos una clase ese mes 



---

**Cursor**

Veo que el notebook es muy completo. Déjame ver el final del notebook para entender dónde añadir la nueva celda:

Perfecto, ya entiendo el notebook completamente. Es un análisis muy completo de clientes de esBarre que incluye:

1. **Carga y exploración** de 42,280 registros de visitas
2. **Resumen general** con categorización de tipos de reserva (Bonos, Gympass, ClassPass, etc.)
3. **Análisis de clientes nuevos** por mes y tipo de reserva
4. **Análisis de churn** (clientes que dejaron de venir)

Ahora te añado una nueva sección con la gráfica de **evolución de clientes activos por mes** (clientes únicos que asistieron al menos a una clase cada mes):

```plaintext


->

## 5. 📈 Evolución de Clientes Activos por Mes

Análisis de cuántos clientes únicos asistieron al menos a una clase cada mes.
```

```plaintext


->

# =============================================================================
# EVOLUCIÓN DE CLIENTES ACTIVOS POR MES
# Clientes únicos que asistieron al menos a una clase en cada mes
# =============================================================================

import matplotlib.pyplot as plt
import numpy as np

print("="*70)
print("📈 EVOLUCIÓN DE CLIENTES ACTIVOS POR MES")
print("="*70)
print("(Clientes únicos que asistieron al menos a una clase en cada mes)\n")

# Calcular clientes únicos por mes y ubicación
clientes_por_mes = df.groupby(['Mes_Nombre', 'Nombre de la Ubicacion'])['ID del Cliente'].nunique().reset_index()
clientes_por_mes.columns = ['Mes', 'Ubicacion', 'Clientes Activos']

# Crear pivot table
pivot_clientes_activos = clientes_por_mes.pivot(index='Mes', columns='Ubicacion', values='Clientes Activos').fillna(0).astype(int)

# Calcular total
pivot_clientes_activos['TOTAL'] = pivot_clientes_activos.sum(axis=1)

# Excluir agosto (estudio cerrado)
pivot_clientes_activos = pivot_clientes_activos[~pivot_clientes_activos.index.str.contains('2024-08|2025-08')]

print("📊 Tabla de Clientes Activos por Mes:")
display(pivot_clientes_activos)

# =============================================================================
# GRÁFICA: Evolución de clientes activos
# =============================================================================

fig, ax = plt.subplots(figsize=(16, 8))

# Colores elegantes
color_lopez = '#2E86AB'  # Azul
color_trafalgar = '#A23B72'  # Magenta
color_total = '#1a1a2e'  # Azul oscuro

meses = pivot_clientes_activos.index.tolist()
x = np.arange(len(meses))

# Obtener datos por ubicación
if 'López de Hoyos - esBarre' in pivot_clientes_activos.columns:
    lopez_data = pivot_clientes_activos['López de Hoyos - esBarre'].values
else:
    lopez_data = np.zeros(len(meses))

if 'Trafalgar - esBarré' in pivot_clientes_activos.columns:
    trafalgar_data = pivot_clientes_activos['Trafalgar - esBarré'].values
else:
    trafalgar_data = np.zeros(len(meses))

total_data = pivot_clientes_activos['TOTAL'].values

# Barras apiladas
width = 0.6
bars_lopez = ax.bar(x, lopez_data, width, label='López de Hoyos', color=color_lopez, alpha=0.85, edgecolor='white', linewidth=1)
bars_trafalgar = ax.bar(x, trafalgar_data, width, bottom=lopez_data, label='Trafalgar', color=color_trafalgar, alpha=0.85, edgecolor='white', linewidth=1)

# Línea de total
ax.plot(x, total_data, color=color_total, linewidth=3, marker='o', markersize=8, 
        label='Total', zorder=5, markerfacecolor='white', markeredgewidth=2)

# Añadir valores en la línea de total
for i, total in enumerate(total_data):
    ax.annotate(f'{int(total):,}', (x[i], total), textcoords="offset points", 
                xytext=(0, 12), ha='center', fontsize=10, fontweight='bold', color=color_total,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color_total, alpha=0.9))

# Calcular y mostrar MoM% para total
for i in range(1, len(total_data)):
    if total_data[i-1] > 0:
        mom_pct = ((total_data[i] - total_data[i-1]) / total_data[i-1]) * 100
        color_mom = '#27ae60' if mom_pct >= 0 else '#e74c3c'
        ax.annotate(f'{mom_pct:+.1f}%', (x[i], total_data[i]), textcoords="offset points", 
                    xytext=(0, -25), ha='center', fontsize=8, fontweight='bold', color=color_mom)

# Estilo del gráfico
ax.set_xlabel('Mes', fontsize=13, fontweight='bold', labelpad=10)
ax.set_ylabel('Clientes Activos (únicos)', fontsize=13, fontweight='bold', labelpad=10)
ax.set_title('📈 Evolución de Clientes Activos por Mes\n(Clientes únicos que asistieron al menos a una clase)', 
             fontsize=16, fontweight='bold', pad=20, color='#2c3e50')
ax.set_xticks(x)
ax.set_xticklabels([m[2:] for m in meses], rotation=45, ha='right', fontsize=10)
ax.legend(loc='upper left', fontsize=11, frameon=True, fancybox=True, shadow=True)
ax.grid(True, alpha=0.3, linestyle='--', axis='y')
ax.set_facecolor('#fafbfc')
fig.patch.set_facecolor('white')

# Resumen
max_mes = meses[np.argmax(total_data)]
max_clientes = int(np.max(total_data))
ultimo_mes = meses[-1]
ultimo_clientes = int(total_data[-1])
resumen_text = f'📊 Máximo histórico: {max_clientes:,} clientes ({max_mes}) | Último mes ({ultimo_mes}): {ultimo_clientes:,} clientes'
fig.text(0.5, 0.02, resumen_text, ha='center', fontsize=11, fontweight='bold', 
         color='#2c3e50', bbox=dict(boxstyle='round,pad=0.5', facecolor='#ecf0f1', 
                                     edgecolor='#bdc3c7', alpha=0.9))

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.show()

# =============================================================================
# ESTADÍSTICAS ADICIONALES
# =============================================================================
print("\n📊 ESTADÍSTICAS DE CLIENTES ACTIVOS:")
print("="*60)
print(f"   Promedio mensual (total): {int(total_data.mean()):,} clientes")
print(f"   Máximo: {max_clientes:,} clientes ({max_mes})")
print(f"   Mínimo: {int(np.min(total_data)):,} clientes ({meses[np.argmin(total_data)]})")
print(f"   Último mes ({ultimo_mes}): {ultimo_clientes:,} clientes")

# Tendencia
if len(total_data) >= 3:
    ultimos_3_meses = total_data[-3:]
    tendencia = "📈 Creciente" if ultimos_3_meses[-1] > ultimos_3_meses[0] else "📉 Decreciente"
    print(f"   Tendencia últimos 3 meses: {tendencia}")
```

¡Listo! He añadido una nueva sección al final del notebook (celdas 12 y 13) con la gráfica de **evolución de clientes activos por mes**.

La nueva sección incluye:

1. **📊 Tabla de clientes activos** - Muestra los clientes únicos que asistieron al menos a una clase cada mes, desglosado por ubicación (López de Hoyos y Trafalgar)

2. **📈 Gráfica de barras apiladas** con:
   - Barras de López de Hoyos (azul) y Trafalgar (magenta) apiladas
   - Línea de total de clientes activos
   - Valores del total encima de cada punto
   - **Variación MoM%** (mes a mes) debajo de cada barra - en verde si es positivo, rojo si es negativo
   - Resumen con el máximo histórico y el último mes

3. **📊 Estadísticas adicionales**:
   - Promedio mensual de clientes activos
   - Máximo y mínimo histórico con sus meses
   - Tendencia de los últimos 3 meses

El estilo visual sigue la misma línea elegante del resto de gráficas del notebook. Solo tienes que ejecutar las celdas 12 y 13 para ver la gráfica. 🎨

---

**User**

vale pues lo que vemos a priori es que los clientes activos empezaron a caer a partir de marzo. En septiembre no volvieron y cuando abrimos en octubre el nuevo local no parece que se haya canibalizado mucho sino que sigue la tendencia decreciente Lopez de hoyos de cada vez menos usuarios activos y sobre todo comparado con el año anterior.



Quiero ahora enfocarme en cómo ha sido la generación de nuevos clientes vs los clientes que se han ido mensualmente. Para contabilizar los churn quiero que contabilices por mes aquellos que en ese mes fueron por última vez y nunca más volvieron. Los que hayan ido alguna vez antes de ese mes son churn old y los que fueron ese mes por primera vez pero nunca volvieron son churn new. 

---

**Cursor**

Voy a añadir ahora una nueva sección al notebook con una tabla y gráficos que muestren, por mes, los clientes nuevos, el churn total y su desglose en churn new vs churn old, junto con el balance neto y stock acumulado.

```plaintext


->

## 6. 🔄 Balance Mensual: Nuevos Clientes vs Churn (New vs Old)

En esta sección analizamos, para cada mes:
- **Clientes nuevos**: primera vez que visitan esBarre ese mes.
- **Churn total**: clientes cuya **última visita** histórica fue en ese mes y nunca han vuelto después.
- **Churn new**: de ese churn, los que **empezaron y terminaron** en el mismo mes (su primera visita y su última visita son ese mes).
- **Churn old**: clientes que ya venían de meses anteriores y para los que ese mes es su última visita.

Así podemos ver si el negocio está creciendo porque entran más de los que se van y si el problema está más en retención de nuevos o en retención de clientes antiguos.
```

```plaintext


->

# =============================================================================
# BALANCE MENSUAL: NUEVOS CLIENTES vs CHURN (NEW vs OLD)
# =============================================================================

import numpy as np

print("="*70)
print("🔄 BALANCE MENSUAL: NUEVOS vs CHURN (New vs Old)")
print("="*70)

# Asegurarnos de tener columnas de mes para primera y última visita
if 'Mes_Ultima_Visita' not in ultima_visita_cliente.columns:
    ultima_visita_cliente['Mes_Ultima_Visita'] = ultima_visita_cliente['Ultima Visita'].dt.to_period('M')
if 'Mes_Primera_Visita' not in ultima_visita_cliente.columns:
    ultima_visita_cliente['Mes_Primera_Visita'] = ultima_visita_cliente['Primera Visita'].dt.to_period('M')

# Mes máximo disponible en el dataset
mes_maximo = df['Fecha de Visita'].dt.to_period('M').max()
print(f"📅 Último mes con datos: {mes_maximo}")

# -----------------------------------------------------------------------------
# 1. NUEVOS CLIENTES POR MES
# -----------------------------------------------------------------------------

# Usamos la tabla de primera visita creada antes
primera_visita_cliente['Mes_Primera_Visita'] = primera_visita_cliente['Primera Visita'].dt.to_period('M')

nuevos_mes = (
    primera_visita_cliente
    .groupby('Mes_Primera_Visita')['ID del Cliente']
    .nunique()
    .reset_index(name='Clientes Nuevos')
)

# -----------------------------------------------------------------------------
# 2. CHURN POR MES, SEPARANDO CHURN NEW vs CHURN OLD
# -----------------------------------------------------------------------------

# Solo consideramos churn "real": meses estrictamente anteriores al último mes
churn_real = ultima_visita_cliente[ultima_visita_cliente['Mes_Ultima_Visita'] < mes_maximo].copy()

# Definición de tipo de churn
# - Churn New: primera y última visita en el mismo mes
# - Churn Old: primera visita en un mes anterior al de la última visita
churn_real['Tipo_Churn'] = np.where(
    churn_real['Mes_Primera_Visita'] == churn_real['Mes_Ultima_Visita'],
    'Churn New',
    'Churn Old'
)

churn_mes = (
    churn_real
    .groupby(['Mes_Ultima_Visita', 'Tipo_Churn'])['ID del Cliente']
    .nunique()
    .unstack(fill_value=0)
    .reset_index()
)

# Asegurar columnas aunque algún mes no tenga de un tipo
for col in ['Churn New', 'Churn Old']:
    if col not in churn_mes.columns:
        churn_mes[col] = 0

churn_mes['Churn Total'] = churn_mes['Churn New'] + churn_mes['Churn Old']

# -----------------------------------------------------------------------------
# 3. COMBINAR NUEVOS vs CHURN EN UNA SOLA TABLA
# -----------------------------------------------------------------------------

nuevos_mes['Mes'] = nuevos_mes['Mes_Primera_Visita'].astype(str)
churn_mes['Mes'] = churn_mes['Mes_Ultima_Visita'].astype(str)

# Solo meses anteriores al último para comparación justa
nuevos_mes_filtrado = nuevos_mes[nuevos_mes['Mes_Primera_Visita'] < mes_maximo].copy()

balance_mes = (
    nuevos_mes_filtrado[['Mes', 'Clientes Nuevos']]
    .merge(
        churn_mes[['Mes', 'Churn New', 'Churn Old', 'Churn Total']],
        on='Mes', how='outer'
    )
    .fillna(0)
)

# Ordenar por mes cronológicamente
balance_mes['Mes_Periodo'] = balance_mes['Mes'].astype('period[M]')
balance_mes = balance_mes.sort_values('Mes_Periodo').reset_index(drop=True)

# Cast a int
for col in ['Clientes Nuevos', 'Churn New', 'Churn Old', 'Churn Total']:
    balance_mes[col] = balance_mes[col].astype(int)

# Calcular balance neto y stock acumulado
balance_mes['Balance Neto'] = balance_mes['Clientes Nuevos'] - balance_mes['Churn Total']
balance_mes['Stock Acumulado'] = balance_mes['Balance Neto'].cumsum()

print("\n📊 Tabla de balance mensual (Nuevos vs Churn):")
display(balance_mes[['Mes', 'Clientes Nuevos', 'Churn New', 'Churn Old', 'Churn Total', 'Balance Neto', 'Stock Acumulado']])

# -----------------------------------------------------------------------------
# 4. GRÁFICO 1: Nuevos vs Churn Total + Balance Neto
# -----------------------------------------------------------------------------

import matplotlib.pyplot as plt

meses = balance_mes['Mes'].tolist()
x = np.arange(len(meses))

fig, ax = plt.subplots(figsize=(18, 9))

color_nuevos = '#2ecc71'   # Verde
color_churn = '#e74c3c'    # Rojo
color_balance = '#34495e'  # Gris azulado

# Barras de nuevos y churn total
width = 0.35
bars_nuevos = ax.bar(x - width/2, balance_mes['Clientes Nuevos'], width,
                     label='Clientes Nuevos', color=color_nuevos, alpha=0.9, edgecolor='white')
bars_churn = ax.bar(x + width/2, balance_mes['Churn Total'], width,
                    label='Churn Total', color=color_churn, alpha=0.85, edgecolor='white')

# Línea de balance neto
ax2 = ax.twinx()
ax2.plot(x, balance_mes['Balance Neto'], color=color_balance, linewidth=3,
         marker='o', markersize=8, label='Balance Neto', markerfacecolor='white', markeredgewidth=2)

# Etiquetas en barras
for bar in bars_nuevos:
    height = bar.get_height()
    ax.annotate(f'+{int(height)}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontsize=9, fontweight='bold', color=color_nuevos)

for bar in bars_churn:
    height = bar.get_height()
    ax.annotate(f'-{int(height)}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontsize=9, fontweight='bold', color=color_churn)

# Etiquetas en la línea de balance neto
for i, val in enumerate(balance_mes['Balance Neto']):
    ax2.annotate(f'{int(val):+}', (x[i], val), textcoords="offset points",
                 xytext=(0, 10), ha='center', fontsize=9, fontweight='bold', color=color_balance)

ax.set_xlabel('Mes', fontsize=13, fontweight='bold')
ax.set_ylabel('Clientes (Nuevos / Churn)', fontsize=13, fontweight='bold')
ax2.set_ylabel('Balance Neto', fontsize=13, fontweight='bold', color=color_balance)
ax2.tick_params(axis='y', labelcolor=color_balance)

ax.set_title('🔄 Balance Mensual: Nuevos Clientes vs Churn Total',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels([m[2:] for m in meses], rotation=45, ha='right')

# Leyenda combinada
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left',
          frameon=True, fancybox=True, shadow=True)

ax.grid(True, axis='y', linestyle='--', alpha=0.3)
ax.set_facecolor('#fafbfc')
fig.patch.set_facecolor('white')

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 5. GRÁFICO 2: Desglose de Churn (New vs Old)
# -----------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(18, 9))

color_churn_new = '#f39c12'   # Naranja
color_churn_old = '#8e44ad'   # Morado

bottom = np.zeros(len(meses))

bars_churn_new = ax.bar(x, balance_mes['Churn New'], width=0.6,
                        label='Churn New (nuevos que no repiten)',
                        color=color_churn_new, alpha=0.9, edgecolor='white')

bars_churn_old = ax.bar(x, balance_mes['Churn Old'], width=0.6,
                        bottom=balance_mes['Churn New'],
                        label='Churn Old (clientes antiguos que se van)',
                        color=color_churn_old, alpha=0.9, edgecolor='white')

# Etiquetas
for i in range(len(meses)):
    total_mes = balance_mes['Churn Total'].iloc[i]
    if total_mes == 0:
        continue
    new_val = balance_mes['Churn New'].iloc[i]
    old_val = balance_mes['Churn Old'].iloc[i]
    ax.annotate(f'{int(total_mes)}', (x[i], total_mes), textcoords="offset points",
                xytext=(0, 8), ha='center', fontsize=9, fontweight='bold', color='#2c3e50')
    # Porcentaje de churn new
    pct_new = new_val / total_mes * 100 if total_mes > 0 else 0
    ax.annotate(f'{pct_new:.0f}% new', (x[i], new_val / 2), textcoords="offset points",
                xytext=(0, 0), ha='center', fontsize=8, color=color_churn_new, fontweight='bold')

ax.set_xlabel('Mes', fontsize=13, fontweight='bold')
ax.set_ylabel('Clientes Churn', fontsize=13, fontweight='bold')
ax.set_title('📉 Desglose de Churn por Mes: New vs Old', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels([m[2:] for m in meses], rotation=45, ha='right')
ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
ax.grid(True, axis='y', linestyle='--', alpha=0.3)
ax.set_facecolor('#fafbfc')
fig.patch.set_facecolor('white')

plt.tight_layout()
plt.show()

# Resumen numérico
print("\n📊 RESUMEN:")
print("="*60)
print(f"   Total clientes nuevos (periodo analizado): {balance_mes['Clientes Nuevos'].sum():,}")
print(f"   Total churn new: {balance_mes['Churn New'].sum():,}")
print(f"   Total churn old: {balance_mes['Churn Old'].sum():,}")
print(f"   Balance neto acumulado: {balance_mes['Balance Neto'].sum():+,,}")
```

Buen análisis el tuyo: efectivamente se ve que el problema principal es que **López de Hoyos se va vaciando** y el nuevo local suma más que canibaliza.

Ya te he añadido una nueva sección (`6. 🔄 Balance Mensual: Nuevos Clientes vs Churn (New vs Old)`) al final del notebook con:

- **Tabla mensual** con:
  - **Clientes Nuevos**
  - **Churn New** (primera y última visita en el mismo mes)
  - **Churn Old** (ya venían de antes y ese mes es su última visita)
  - **Churn Total**, **Balance Neto** y **Stock Acumulado**
- **Gráfico 1**: barras de *Nuevos* vs *Churn Total* por mes y una **línea de Balance Neto**.
- **Gráfico 2**: barras apiladas solo de churn con desglose **New vs Old** y porcentaje de churn que es de “nuevos que no repiten”.

Para verlo, ejecuta las nuevas celdas 14 y 15 del notebook (las que están bajo el título `## 6. 🔄 Balance Mensual: Nuevos Clientes vs Churn (New vs Old)`).

---

**User**

pero para esto quiero que solo analices lopez de hoyos

---

**Cursor**

```plaintext
# Usamos la tabla de primera visita creada antes
primera_visita_cliente['Mes_Primera_Visita'] = primera_visita_cliente['Primera Visita'].dt.to_period('M')

nuevos_mes = (
    primera_visita_cliente
    .groupby('Mes_Primera_Visita')['ID del Cliente']
    .nunique()
    .reset_index(name='Clientes Nuevos')
)


->

# Usamos la tabla de primera visita creada antes (SOLO LÓPEZ DE HOYOS)
primera_visita_lopez = primera_visita_cliente[primera_visita_cliente['Ubicacion Primera Visita'] == 'López de Hoyos - esBarre'].copy()
primera_visita_lopez['Mes_Primera_Visita'] = primera_visita_lopez['Primera Visita'].dt.to_period('M')

nuevos_mes = (
    primera_visita_lopez
    .groupby('Mes_Primera_Visita')['ID del Cliente']
    .nunique()
    .reset_index(name='Clientes Nuevos')
)

```

Error L18 unexpected token: probably notebook parser complaining? But we just updated; maybe okay. Still need second edit for churn_real filter by Lopez.

```plaintext
# Solo consideramos churn "real": meses estrictamente anteriores al último mes
churn_real = ultima_visita_cliente[ultima_visita_cliente['Mes_Ultima_Visita'] < mes_maximo].copy()


->

# Solo consideramos churn "real": meses estrictamente anteriores al último mes (SOLO LÓPEZ DE HOYOS)
churn_real = ultima_visita_cliente[(ultima_visita_cliente['Mes_Ultima_Visita'] < mes_maximo) &
                                   (ultima_visita_cliente['Ultima Ubicacion'] == 'López de Hoyos - esBarre')].copy()

```

Perfecto, ajustamos todo a **López de Hoyos**.

### 🛠 Qué he cambiado

En la celda de código del bloque `## 6. 🔄 Balance Mensual: Nuevos Clientes vs Churn (New vs Old)` he hecho dos ajustes:

1. **Nuevos clientes por mes**: ahora solo cuenta los que empiezan en López de Hoyos.
   - Antes usaba todos los clientes de `primera_visita_cliente`.
   - Ahora filtra primero por ubicación:

```python
# Usamos la tabla de primera visita creada antes (SOLO LÓPEZ DE HOYOS)
primera_visita_lopez = primera_visita_cliente[primera_visita_cliente['Ubicacion Primera Visita'] == 'López de Hoyos - esBarre'].copy()
primera_visita_lopez['Mes_Primera_Visita'] = primera_visita_lopez['Primera Visita'].dt.to_period('M')

nuevos_mes = (
    primera_visita_lopez
    .groupby('Mes_Primera_Visita')['ID del Cliente']
    .nunique()
    .reset_index(name='Clientes Nuevos')
)
```

2. **Churn por mes (new/old)**: ahora solo considera clientes cuya **última visita fue en López de Hoyos**.

```python
# Solo consideramos churn "real": meses estrictamente anteriores al último mes (SOLO LÓPEZ DE HOYOS)
churn_real = ultima_visita_cliente[(ultima_visita_cliente['Mes_Ultima_Visita'] < mes_maximo) &
                                   (ultima_visita_cliente['Ultima Ubicacion'] == 'López de Hoyos - esBarre')].copy()
```

Con esto, toda la tabla y los dos gráficos de la sección 6 quedan **100% centrados en López de Hoyos** (nuevos, churn new, churn old, balance y stock acumulado). Solo tienes que volver a ejecutar la celda 15 para ver los números ya filtrados.

```python
# Usamos la tabla de primera visita creada antes (SOLO LÓPEZ DE HOYOS)
primera_visita_lopez = primera_visita_cliente[primera_visita_cliente['Ubicacion Primera Visita'] == 'López de Hoyos - esBarre'].copy()
primera_visita_lopez['Mes_Primera_Visita'] = primera_visita_lopez['Primera Visita'].dt.to_period('M')

nuevos_mes = (
    primera_visita_lopez
    .groupby('Mes_Primera_Visita')['ID del Cliente']
    .nunique()
    .reset_index(name='Clientes Nuevos')
)
```

```python
# Solo consideramos churn "real": meses estrictamente anteriores al último mes (SOLO LÓPEZ DE HOYOS)
churn_real = ultima_visita_cliente[(ultima_visita_cliente['Mes_Ultima_Visita'] < mes_maximo) &
                                   (ultima_visita_cliente['Ultima Ubicacion'] == 'López de Hoyos - esBarre')].copy()
```

---

**User**

---------------------------------------------------------------------------

ValueError                                Traceback (most recent call last)

Cell In[150], line 225

    223 print(f"   Total churn new: {balance_mes['Churn New'].sum():,}")

    224 print(f"   Total churn old: {balance_mes['Churn Old'].sum():,}")

--> 225 print(f"   Balance neto acumulado: {balance_mes['Balance Neto'].sum():+,,}")



ValueError: Cannot specify ',' with ','.

---

**Cursor**

Voy a corregir el formato del `print` que calcula el balance neto acumulado para que el formato numérico sea válido, y así puedas ejecutar la celda sin errores.

```plaintext
print("\n📊 RESUMEN:")
print("="*60)
print(f"   Total clientes nuevos (periodo analizado): {balance_mes['Clientes Nuevos'].sum():,}")
print(f"   Total churn new: {balance_mes['Churn New'].sum():,}")
print(f"   Total churn old: {balance_mes['Churn Old'].sum():,}")
print(f"   Balance neto acumulado: {balance_mes['Balance Neto'].sum():+,,}")

->

print("\n📊 RESUMEN:")
print("="*60)
print(f"   Total clientes nuevos (periodo analizado): {balance_mes['Clientes Nuevos'].sum():,}")
print(f"   Total churn new: {balance_mes['Churn New'].sum():,}")
print(f"   Total churn old: {balance_mes['Churn Old'].sum():,}")
# Balance neto acumulado con formato signo + separador de miles
balance_acumulado = balance_mes['Balance Neto'].sum()
print(f"   Balance neto acumulado: {balance_acumulado:+,}")
```

El error viene del formato `:+,,` en el `f-string`, que usa dos comas y Python no lo admite.

Ya he corregido la celda: ahora se guarda primero el valor en `balance_acumulado` y se imprime así:

```python
# Balance neto acumulado con formato signo + separador de miles
balance_acumulado = balance_mes['Balance Neto'].sum()
print(f"   Balance neto acumulado: {balance_acumulado:+,}")
```

Vuelve a ejecutar la celda 15 y el resumen debería salir sin errores.

```python
# Balance neto acumulado con formato signo + separador de miles
balance_acumulado = balance_mes['Balance Neto'].sum()
print(f"   Balance neto acumulado: {balance_acumulado:+,}")
```

---

**User**

como se mira el churn normalmente teniendo en cuenta que no sabes si los que han dejado de venir en octubre, septiembre o noviembre no sabes si volveran?

---

**Cursor**

Buena pregunta, es el “truco” del churn: **el futuro no lo sabes**, así que siempre hay que decidir una convención.

### 💡 Ideas clave

- **1. Definir una ventana de inactividad (X días/meses)**  
  - Se considera *churn* un cliente que **lleva sin venir más de X días** desde su última visita.  
  - Ejemplo: X = 60 días. Con datos hasta 30‑nov, un cliente cuya última visita fue el 1‑sept ya lleva 90 días sin venir ⇒ lo clasificas como churn.  
  - En cambio, alguien que vino el 15‑nov no puede ser churn todavía, porque no ha pasado la ventana de 60 días.

- **2. Tratar los últimos meses como “datos incompletos”**  
  - Normalmente se **excluye el último mes (o los últimos 2)** del cálculo de churn “cerrado”, porque todavía hay clientes que podrían volver.  
  - En tu caso podrías:  
    - Calcular churn “real” hasta **septiembre** (por ejemplo),  
    - Y etiquetar octubre y noviembre como **“churn provisional / early warning”**, pero no mezclarlos con el churn cerrado.

- **3. Churn por periodo vs. churn acumulado**  
  - **Churn mensual**: de los clientes activos al inicio del mes, ¿qué % cumple criterio de inactividad X días al final del periodo de observación?  
  - **Retención/cohortes**: coges clientes que empezaron en un mes (ej. cohorte de marzo) y miras qué % sigue activo 1, 2, 3… meses después. Esto evita el problema de los meses recientes porque siempre comparas dentro de ventanas completas.

- **4. Cómo aplicarlo a tu caso (recomendación práctica)**  
  - Define una regla sencilla: por ejemplo **“churn = 60 días sin visita”**.  
  - Calcula churn **por mes de última visita** solo para meses en los que hayan pasado ya esos 60 días completos (en tus datos, hasta septiembre si quieres ir conservador).  
  - Marca **octubre y noviembre** como meses “abiertos” donde sólo miras **tendencia de inactividad**, no churn definitivo.

Si quieres, en el notebook puedo ajustarte la lógica actual de churn para que use una ventana de X días (ej. 60 o 90) y que automáticamente marque los últimos meses como “abiertos” en las tablas y gráficos.

---

**User**

pues hagamos mejor para churn old Churn del mes = nº de clientes que llevan 60 días sin asistir, excluyendo agosto

---

**Cursor**

```plaintext
# -----------------------------------------------------------------------------
# 2. CHURN POR MES, SEPARANDO CHURN NEW vs CHURN OLD
# -----------------------------------------------------------------------------

# Solo consideramos churn "real": meses estrictamente anteriores al último mes (SOLO LÓPEZ DE HOYOS)
churn_real = ultima_visita_cliente[(ultima_visita_cliente['Mes_Ultima_Visita'] < mes_maximo) &
                                   (ultima_visita_cliente['Ultima Ubicacion'] == 'López de Hoyos - esBarre')].copy()

# Definición de tipo de churn
# - Churn New: primera y última visita en el mismo mes
# - Churn Old: primera visita en un mes anterior al de la última visita
churn_real['Tipo_Churn'] = np.where(


->

# -----------------------------------------------------------------------------
# 2. CHURN POR MES, SEPARANDO CHURN NEW vs CHURN OLD (DEFINICIÓN 60 DÍAS)
# -----------------------------------------------------------------------------

# Churn "real" para López de Hoyos:
# clientes cuya última visita fue en ese local y llevan al menos 60 días sin venir,
# excluyendo los meses de agosto (estudio cerrado).
UMBRAL_CHURN_DIAS = 60
churn_real = ultima_visita_cliente[
    (ultima_visita_cliente['Ultima Ubicacion'] == 'López de Hoyos - esBarre') &
    (ultima_visita_cliente['Dias_Sin_Visita'] >= UMBRAL_CHURN_DIAS)
].copy()

# Excluir meses de agosto
churn_real = churn_real[~churn_real['Mes_Ultima_Visita'].astype(str).isin(['2024-08', '2025-08'])]

# Definición de tipo de churn
# - Churn New: primera y última visita en el mismo mes
# - Churn Old: primera visita en un mes anterior al de la última visita
churn_real['Tipo_Churn'] = np.where(

```

Perfecto, hemos cambiado la definición para que encaje con lo que pides.

### 🔁 Nueva lógica de churn (solo López de Hoyos)

En la sección `## 6. 🔄 Balance Mensual: Nuevos Clientes vs Churn (New vs Old)` ahora:

- **Solo miramos López de Hoyos** (`Ultima Ubicacion == 'López de Hoyos - esBarre'`).
- Consideramos **churn “real”** solo a los clientes que:
  - Llevan **al menos 60 días sin venir** (`Dias_Sin_Visita >= 60`).
  - Y además **su mes de última visita NO es agosto** (2024-08 ni 2025-08).

El bloque de churn ha quedado así:

```python
# 2. CHURN POR MES, SEPARANDO CHURN NEW vs CHURN OLD (DEFINICIÓN 60 DÍAS)

# Churn "real" para López de Hoyos:
# clientes cuya última visita fue en ese local y llevan al menos 60 días sin venir,
# excluyendo los meses de agosto (estudio cerrado).
UMBRAL_CHURN_DIAS = 60
churn_real = ultima_visita_cliente[
    (ultima_visita_cliente['Ultima Ubicacion'] == 'López de Hoyos - esBarre') &
    (ultima_visita_cliente['Dias_Sin_Visita'] >= UMBRAL_CHURN_DIAS)
].copy()

# Excluir meses de agosto
churn_real = churn_real[~churn_real['Mes_Ultima_Visita'].astype(str).isin(['2024-08', '2025-08'])]

# Definición de tipo de churn
# - Churn New: primera y última visita en el mismo mes
# - Churn Old: primera visita en un mes anterior al de la última visita
churn_real['Tipo_Churn'] = np.where(
    churn_real['Mes_Primera_Visita'] == churn_real['Mes_Ultima_Visita'],
    'Churn New',
    'Churn Old'
)
```

Es decir, **“churn del mes” = número de clientes cuya última visita fue ese mes, llevan ≥60 días sin venir y son de López de Hoyos**, con agosto fuera.  
Vuelve a ejecutar la celda 15 y verás la tabla y los gráficos ya con esta nueva definición.

```python
# 2. CHURN POR MES, SEPARANDO CHURN NEW vs CHURN OLD (DEFINICIÓN 60 DÍAS)

# Churn "real" para López de Hoyos:
# clientes cuya última visita fue en ese local y llevan al menos 60 días sin venir,
# excluyendo los meses de agosto (estudio cerrado).
UMBRAL_CHURN_DIAS = 60
churn_real = ultima_visita_cliente[
    (ultima_visita_cliente['Ultima Ubicacion'] == 'López de Hoyos - esBarre') &
    (ultima_visita_cliente['Dias_Sin_Visita'] >= UMBRAL_CHURN_DIAS)
].copy()

# Excluir meses de agosto
churn_real = churn_real[~churn_real['Mes_Ultima_Visita'].astype(str).isin(['2024-08', '2025-08'])]

# Definición de tipo de churn
# - Churn New: primera y última visita en el mismo mes
# - Churn Old: primera visita en un mes anterior al de la última visita
churn_real['Tipo_Churn'] = np.where(
    churn_real['Mes_Primera_Visita'] == churn_real['Mes_Ultima_Visita'],
    'Churn New',
    'Churn Old'
)
```

---

**User**

vale quiero ahora que empecemos un análisis enfocado en las reservas. .Por favor ignora los datos de Agosto. Quiero que analicemos:



Evolución de las reservas totales , misma gráfica que la evolución de clientes activos por mes. 



Evolución de las reservas por persona.



Evolución de las reservas, haciendo stack diferenciando de las reservas de los nuevos clientes vs los que ya habían reservado un mes anterior.



Evolución de las reservas por tipo_reserva, para entender cómo han evolucionado según sea bono , clase suelta etc

---

**Cursor**

```plaintext


->

## 7. 📊 Análisis de Reservas (sin agosto)

En esta sección analizamos las **reservas (visitas)** excluyendo siempre los meses de agosto (estudio cerrado):

- **Evolución de las reservas totales**: mismo estilo que la gráfica de clientes activos (barras por local + línea de total).
- **Evolución de las reservas por persona**: cuántas reservas hace de media cada cliente activo por mes.
- **Evolución de reservas de clientes nuevos vs recurrentes**: stack de reservas de clientes que empiezan ese mes vs los que ya habían reservado antes.
- **Evolución de reservas por `tipo_reserva`**: bonos, clase suelta, Gympass, ClassPass, invitaciones, etc.
```

```plaintext


->

# =============================================================================
# 7. ANÁLISIS DE RESERVAS (EXCLUYENDO AGOSTO)
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt

print("="*70)
print("📊 ANÁLISIS DE RESERVAS (sin agosto)")
print("="*70)

# Filtrar datos excluyendo agosto 2024 y 2025
meses_excluir = ['2024-08', '2025-08']
df_res = df[~df['Mes_Nombre'].isin(meses_excluir)].copy()

# Asegurar columnas de periodo de mes
if 'Mes_Periodo' not in df_res.columns:
    df_res['Mes_Periodo'] = df_res['Fecha de Visita'].dt.to_period('M')

# -----------------------------------------------------------------------------
# 1. EVOLUCIÓN DE LAS RESERVAS TOTALES (POR LOCAL + TOTAL)
# -----------------------------------------------------------------------------

reservas_mes_loc = (
    df_res
    .groupby(['Mes_Nombre', 'Nombre de la Ubicacion'])
    .size()
    .reset_index(name='Reservas')
)

pivot_reservas_loc = reservas_mes_loc.pivot(index='Mes_Nombre',
                                            columns='Nombre de la Ubicacion',
                                            values='Reservas').fillna(0).astype(int)

# Orden cronológico por mes
años_meses_orden = pivot_reservas_loc.index.astype('period[M]').sort_values()
pivot_reservas_loc = pivot_reservas_loc.loc[años_meses_orden.astype(str)]

# Calcular total
pivot_reservas_loc['TOTAL'] = pivot_reservas_loc.sum(axis=1)

print("\n📊 Reservas totales por mes y local (sin agosto):")
display(pivot_reservas_loc)

fig, ax = plt.subplots(figsize=(16, 8))

color_lopez = '#2E86AB'
color_trafalgar = '#A23B72'
color_total = '#1a1a2e'

meses = pivot_reservas_loc.index.tolist()
x = np.arange(len(meses))

lopez_data = pivot_reservas_loc.get('López de Hoyos - esBarre', pd.Series(0, index=meses)).values
trafalgar_data = pivot_reservas_loc.get('Trafalgar - esBarré', pd.Series(0, index=meses)).values
total_data = pivot_reservas_loc['TOTAL'].values

width = 0.6
bars_lopez = ax.bar(x, lopez_data, width, label='López de Hoyos', color=color_lopez,
                    alpha=0.85, edgecolor='white', linewidth=1)
ax.bar(x, trafalgar_data, width, bottom=lopez_data, label='Trafalgar',
       color=color_trafalgar, alpha=0.85, edgecolor='white', linewidth=1)

ax.plot(x, total_data, color=color_total, linewidth=3, marker='o', markersize=8,
        label='Total reservas', zorder=5, markerfacecolor='white', markeredgewidth=2)

for i, total in enumerate(total_data):
    ax.annotate(f'{int(total):,}', (x[i], total), textcoords='offset points',
                xytext=(0, 10), ha='center', fontsize=9, fontweight='bold', color=color_total,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=color_total, alpha=0.9))

ax.set_xlabel('Mes', fontsize=13, fontweight='bold')
ax.set_ylabel('Reservas (visitas)', fontsize=13, fontweight='bold')
ax.set_title('📊 Evolución de Reservas Totales por Mes (sin agosto)', fontsize=16,
             fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels([m[2:] for m in meses], rotation=45, ha='right')
ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
ax.grid(True, axis='y', linestyle='--', alpha=0.3)
ax.set_facecolor('#fafbfc')
fig.patch.set_facecolor('white')

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 2. EVOLUCIÓN DE LAS RESERVAS POR PERSONA
# -----------------------------------------------------------------------------

reservas_mes = df_res.groupby('Mes_Nombre').size()
clientes_mes = df_res.groupby('Mes_Nombre')['ID del Cliente'].nunique()

reservas_por_cliente = (reservas_mes / clientes_mes).rename('Reservas por Cliente')
reservas_por_cliente = reservas_por_cliente.loc[años_meses_orden]

print("\n📊 Reservas por cliente y mes (media):")
display(reservas_por_cliente.to_frame())

fig, ax = plt.subplots(figsize=(14, 7))

ax.plot(reservas_por_cliente.index.tolist(), reservas_por_cliente.values,
        marker='o', linewidth=3, color='#2c3e50')

for x_tick, val in zip(reservas_por_cliente.index.tolist(), reservas_por_cliente.values):
    ax.annotate(f'{val:.2f}', (x_tick, val), textcoords='offset points',
                xytext=(0, 8), ha='center', fontsize=9, fontweight='bold', color='#2c3e50')

ax.set_xlabel('Mes', fontsize=13, fontweight='bold')
ax.set_ylabel('Reservas por cliente (media)', fontsize=13, fontweight='bold')
ax.set_title('📈 Evolución de Reservas por Cliente Activo (sin agosto)', fontsize=16,
             fontweight='bold', pad=20)
ax.set_xticks(reservas_por_cliente.index.tolist())
ax.set_xticklabels([m[2:] for m in reservas_por_cliente.index.tolist()], rotation=45, ha='right')
ax.grid(True, axis='y', linestyle='--', alpha=0.3)
ax.set_facecolor('#fafbfc')
fig.patch.set_facecolor('white')

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 3. EVOLUCIÓN DE RESERVAS: CLIENTES NUEVOS vs RECURRENTES
# -----------------------------------------------------------------------------

# Aseguramos columna de Mes_Primera_Visita en primera_visita_cliente
if 'Mes_Primera_Visita' not in primera_visita_cliente.columns:
    primera_visita_cliente['Mes_Primera_Visita'] = primera_visita_cliente['Primera Visita'].dt.to_period('M')

map_primera_visita = primera_visita_cliente.set_index('ID del Cliente')['Mes_Primera_Visita']

df_res['Mes_Primera_Visita'] = df_res['ID del Cliente'].map(map_primera_visita)
df_res['Segmento_Reserva'] = np.where(
    df_res['Mes_Periodo'] == df_res['Mes_Primera_Visita'],
    'Nuevos',
    'Recurrentes'
)

reservas_segmento = (
    df_res
    .groupby(['Mes_Periodo', 'Segmento_Reserva'])
    .size()
    .unstack(fill_value=0)
)

reservas_segmento = reservas_segmento.loc[años_meses_orden]
reservas_segmento['TOTAL'] = reservas_segmento.sum(axis=1)

print("\n📊 Reservas por segmento (Nuevos vs Recurrentes) y mes:")
display(reservas_segmento)

fig, ax = plt.subplots(figsize=(16, 8))

x = np.arange(len(reservas_segmento.index))
meses_seg = [str(p) for p in reservas_segmento.index]

color_nuevos = '#f39c12'
color_recurrentes = '#3498db'
color_total_seg = '#1a1a2e'

nuevos_data = reservas_segmento['Nuevos'].values
recurrentes_data = reservas_segmento['Recurrentes'].values
total_seg = reservas_segmento['TOTAL'].values

width = 0.6
ax.bar(x, recurrentes_data, width, label='Recurrentes', color=color_recurrentes,
       alpha=0.85, edgecolor='white', linewidth=1)
ax.bar(x, nuevos_data, width, bottom=recurrentes_data, label='Nuevos',
       color=color_nuevos, alpha=0.9, edgecolor='white', linewidth=1)

ax.plot(x, total_seg, color=color_total_seg, linewidth=3, marker='o', markersize=8,
        label='Total reservas', zorder=5, markerfacecolor='white', markeredgewidth=2)

for i, total in enumerate(total_seg):
    ax.annotate(f'{int(total):,}', (x[i], total), textcoords='offset points',
                xytext=(0, 10), ha='center', fontsize=9, fontweight='bold', color=color_total_seg)

ax.set_xlabel('Mes', fontsize=13, fontweight='bold')
ax.set_ylabel('Reservas (visitas)', fontsize=13, fontweight='bold')
ax.set_title('🔄 Evolución de Reservas: Clientes Nuevos vs Recurrentes (sin agosto)',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels([m[2:] for m in meses_seg], rotation=45, ha='right')
ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
ax.grid(True, axis='y', linestyle='--', alpha=0.3)
ax.set_facecolor('#fafbfc')
fig.patch.set_facecolor('white')

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 4. EVOLUCIÓN DE RESERVAS POR TIPO_RESERVA
# -----------------------------------------------------------------------------

reservas_tipo = (
    df_res
    .groupby(['Mes_Periodo', 'tipo_reserva'])
    .size()
    .unstack(fill_value=0)
)

# Ordenar columnas por total descendente
orden_cols = reservas_tipo.sum().sort_values(ascending=False).index
reservas_tipo = reservas_tipo[orden_cols]
reservas_tipo = reservas_tipo.loc[años_meses_orden]

print("\n📊 Reservas por tipo_reserva y mes:")
display(reservas_tipo.astype(int))

fig, ax = plt.subplots(figsize=(18, 9))

colores_area = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6',
                '#1abc9c', '#e67e22', '#34495e']

ax.stackplot(range(len(reservas_tipo.index)),
             [reservas_tipo[col].values for col in reservas_tipo.columns],
             labels=reservas_tipo.columns,
             colors=colores_area[:len(reservas_tipo.columns)],
             alpha=0.85, edgecolor='white', linewidth=0.5)

# Línea de total
totales_tipo = reservas_tipo.sum(axis=1).values
ax.plot(range(len(reservas_tipo.index)), totales_tipo,
        color='#2c3e50', linewidth=3, linestyle='--', marker='o',
        markersize=6, label='Total reservas', zorder=5)

for i, total in enumerate(totales_tipo):
    ax.annotate(f'{int(total):,}', (i, total), textcoords='offset points',
                xytext=(0, 8), ha='center', fontsize=9, fontweight='bold', color='#2c3e50')

ax.set_xlabel('Mes', fontsize=13, fontweight='bold')
ax.set_ylabel('Reservas (visitas)', fontsize=13, fontweight='bold')
ax.set_title('📊 Evolución de Reservas por tipo_reserva (sin agosto)', fontsize=16,
             fontweight='bold', pad=20)
ax.set_xticks(range(len(reservas_tipo.index)))
ax.set_xticklabels([str(p)[2:] for p in reservas_tipo.index], rotation=45, ha='right')
ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), frameon=True,
          fancybox=True, shadow=True, title='tipo_reserva')
ax.grid(True, axis='y', linestyle='--', alpha=0.3)
ax.set_facecolor('#fafbfc')
fig.patch.set_facecolor('white')

plt.tight_layout(rect=[0, 0.02, 0.8, 1])
plt.show()
```

He añadido una nueva sección completa de reservas en el notebook, siguiendo exactamente lo que pedías.

### ✅ Qué tienes ahora en la sección `## 7. 📊 Análisis de Reservas (sin agosto)`

1. **Evolución de las reservas totales (sin agosto)**  
   - Barras apiladas por local (`López de Hoyos` y `Trafalgar`)  
   - Línea con el **total de reservas por mes**  
   - Etiquetas con el número total de reservas en cada mes.

2. **Evolución de las reservas por persona**  
   - Cálculo: \( \text{reservas del mes} / \text{clientes únicos del mes} \).  
   - Gráfico de línea con la **media de reservas por cliente activo** cada mes (sin agosto) y la tabla correspondiente.

3. **Evolución de reservas de clientes nuevos vs recurrentes**  
   - Marca cada reserva como:
     - **`Nuevos`** si el mes de la reserva coincide con el mes de su primera visita.
     - **`Recurrentes`** si ya habían venido antes.  
   - Gráfico de barras apiladas (Nuevos vs Recurrentes) + línea de total de reservas y tabla con los datos.

4. **Evolución de reservas por `tipo_reserva`**  
   - Tabla con reservas por mes y `tipo_reserva` (Bonos, Clase Suelta, Gympass, ClassPass, Invitaciones, Descuentos, etc.), sin agosto.  
   - Gráfico de **stacked area** por tipo de reserva + línea de total.

Solo tienes que ejecutar las nuevas celdas 16 y 17 del notebook para ver todas las tablas y gráficas.

---

**User**

corre las celdas cuando las metas para asegurarte está todo okey

---

**Cursor**

```plaintext
reservas_por_cliente = (reservas_mes / clientes_mes).rename('Reservas por Cliente')
reservas_por_cliente = reservas_por_cliente.loc[años_meses_orden]


->

reservas_por_cliente = (reservas_mes / clientes_mes).rename('Reservas por Cliente')
# Ordenar usando los mismos meses que en pivot_reservas_loc (convertimos PeriodIndex -> str)
reservas_por_cliente = reservas_por_cliente.loc[años_meses_orden.astype(str)]

```

Buen apunte, el error venía justo de ahí: estabas indexando una serie con un `PeriodIndex` cuando su índice era de strings.

He ajustado la celda 17 para que:

- Conserve el orden cronológico de `años_meses_orden`,  
- Pero convierta ese `PeriodIndex` a `str` antes de indexar `reservas_por_cliente`, que tiene índice de tipo string:

```python
reservas_por_cliente = (reservas_mes / clientes_mes).rename('Reservas por Cliente')
# Ordenar usando los mismos meses que en pivot_reservas_loc (convertimos PeriodIndex -> str)
reservas_por_cliente = reservas_por_cliente.loc[años_meses_orden.astype(str)]
```

No puedo ejecutar yo mismo las celdas desde aquí, pero con este cambio el `KeyError` que muestras debería desaparecer. Ejecuta de nuevo la celda 17 y, si sale otro traceback, pégamelo y lo vamos puliendo hasta que todo corra limpio.

```python
reservas_por_cliente = (reservas_mes / clientes_mes).rename('Reservas por Cliente')
# Ordenar usando los mismos meses que en pivot_reservas_loc (convertimos PeriodIndex -> str)
reservas_por_cliente = reservas_por_cliente.loc[años_meses_orden.astype(str)]
```

---

**User**

perfecto añade la evolución de la media de reservas, teniendo en cuenta que la media de un mes es la de ese mes junto con sus anteriores

---

**Cursor**

```plaintext
reservas_por_cliente = (reservas_mes / clientes_mes).rename('Reservas por Cliente')
# Ordenar usando los mismos meses que en pivot_reservas_loc (convertimos PeriodIndex -> str)
reservas_por_cliente = reservas_por_cliente.loc[años_meses_orden.astype(str)]

print("\n📊 Reservas por cliente y mes (media):")
display(reservas_por_cliente.to_frame())

fig, ax = plt.subplots(figsize=(14, 7))

ax.plot(reservas_por_cliente.index.tolist(), reservas_por_cliente.values,
        marker='o', linewidth=3, color='#2c3e50')

for x_tick, val in zip(reservas_por_cliente.index.tolist(), reservas_por_cliente.values):
    ax.annotate(f'{val:.2f}', (x_tick, val), textcoords='offset points',
                xytext=(0, 8), ha='center', fontsize=9, fontweight='bold', color='#2c3e50')

ax.set_xlabel('Mes', fontsize=13, fontweight='bold')
ax.set_ylabel('Reservas por cliente (media)', fontsize=13, fontweight='bold')
ax.set_title('📈 Evolución de Reservas por Cliente Activo (sin agosto)', fontsize=16,
             fontweight='bold', pad=20)
ax.set_xticks(reservas_por_cliente.index.tolist())
ax.set_xticklabels([m[2:] for m in reservas_por_cliente.index.tolist()], rotation=45, ha='right')
ax.grid(True, axis='y', linestyle='--', alpha=0.3)
ax.set_facecolor('#fafbfc')
fig.patch.set_facecolor('white')

plt.tight_layout()
plt.show()


->

reservas_por_cliente = (reservas_mes / clientes_mes).rename('Reservas por Cliente')
# Ordenar usando los mismos meses que en pivot_reservas_loc (convertimos PeriodIndex -> str)
reservas_por_cliente = reservas_por_cliente.loc[años_meses_orden.astype(str)]

print("\n📊 Reservas por cliente y mes (media):")
display(reservas_por_cliente.to_frame())

# Media acumulada: cada mes es la media de ese mes y todos los anteriores
reservas_media_acumulada = reservas_por_cliente.expanding().mean().rename('Media acumulada')

fig, ax = plt.subplots(figsize=(14, 7))

# Línea de media mensual
ax.plot(reservas_por_cliente.index.tolist(), reservas_por_cliente.values,
        marker='o', linewidth=2, color='#95a5a6', label='Media mensual')

# Línea de media acumulada (mes actual + anteriores)
ax.plot(reservas_media_acumulada.index.tolist(), reservas_media_acumulada.values,
        marker='o', linewidth=3, color='#2c3e50', label='Media acumulada')

# Anotaciones solo en la media acumulada para que el gráfico sea más limpio
for x_tick, val in zip(reservas_media_acumulada.index.tolist(), reservas_media_acumulada.values):
    ax.annotate(f'{val:.2f}', (x_tick, val), textcoords='offset points',
                xytext=(0, 8), ha='center', fontsize=9, fontweight='bold', color='#2c3e50')

ax.set_xlabel('Mes', fontsize=13, fontweight='bold')
ax.set_ylabel('Reservas por cliente (media)', fontsize=13, fontweight='bold')
ax.set_title('📈 Reservas por Cliente Activo\nMedia mensual vs Media acumulada (sin agosto)', fontsize=16,
             fontweight='bold', pad=20)
ax.set_xticks(reservas_por_cliente.index.tolist())
ax.set_xticklabels([m[2:] for m in reservas_por_cliente.index.tolist()], rotation=45, ha='right')
ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
ax.grid(True, axis='y', linestyle='--', alpha=0.3)
ax.set_facecolor('#fafbfc')
fig.patch.set_facecolor('white')

plt.tight_layout()
plt.show()

```

He añadido justo lo que pides sobre la media de reservas.

En la sección de **“Evolución de las reservas por persona”** ahora se calcula y se dibuja:

- `reservas_por_cliente`: **media mensual** de reservas por cliente activo.
- `reservas_media_acumulada`: **media acumulada**, donde la media de cada mes es la de ese mes junto con todos los anteriores (`expanding().mean()`).

El gráfico ahora muestra **dos líneas**:
- Gris: media mensual.
- Azul oscuro: media acumulada (con etiquetas numéricas).

Solo tienes que volver a ejecutar la celda 17 y verás la evolución de la media acumulada de reservas.

---

**User**

vale vamos a empezar de nuevo en otro notebook. Comencemos con un análisis de las reservas. 

---

**Cursor**

```plaintext


->

# 📊 Análisis de Reservas - esBarre

Este notebook se centra **solo en las reservas (visitas)**, partiendo del mismo fichero de Mindbody.

En este análisis vamos a:
- Cargar y preparar los datos de reservas.
- Excluir agosto (mes cerrado) para que no distorsione la serie.
- Ver la evolución de las reservas por mes y por local.
- Calcular reservas por persona (media) y su evolución.

Más adelante podremos añadir: reservas por tipo de reserva, por canal, nuevos vs recurrentes, etc.
```

```plaintext


->

# 1. Importar librerías y configurar entorno

import json
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', None)

print("✅ Librerías cargadas")
```

```plaintext


->

# 2. Cargar datos de Mindbody (visitas / reservas)

RUTA_FICHERO = 'Detailed Visit Information.json'

with open(RUTA_FICHERO, 'r') as f:
    data = json.load(f)

reservas = pd.DataFrame(data)

print(f"✅ Datos cargados: {len(reservas):,} registros")
print(f"📋 Columnas disponibles ({len(reservas.columns)}):")
for i, col in enumerate(reservas.columns, 1):
    print(f"  {i:2}. {col}")

reservas.head(3)
```

```plaintext


->

# 3. Preparar fechas y columnas auxiliares

# Convertir columnas de fecha
reservas['Fecha de Visita'] = pd.to_datetime(reservas['Fecha de Visita'], format='mixed')
reservas['Fecha y Hora de Creacion UTC'] = pd.to_datetime(reservas['Fecha y Hora de Creacion UTC'], format='mixed')

# Columnas de año/mes
reservas['Año'] = reservas['Fecha de Visita'].dt.year
reservas['Mes'] = reservas['Fecha de Visita'].dt.month
reservas['Año-Mes'] = reservas['Fecha de Visita'].dt.to_period('M')
reservas['Mes_Nombre'] = reservas['Fecha de Visita'].dt.strftime('%Y-%m')

# Excluir diciembre 2025 si quieres ser consistente con el otro notebook
reservas = reservas[~((reservas['Año'] == 2025) & (reservas['Mes'] == 12))]

# Excluir agosto (estudio cerrado)
reservas = reservas[reservas['Mes'] != 8]

print("✅ Fechas preparadas, agosto y dic-2025 excluidos")
print(f"📅 Rango de fechas: {reservas['Fecha de Visita'].min().date()} a {reservas['Fecha de Visita'].max().date()}")
```

```plaintext


->

# 4. Resumen general rápido de reservas

print("="*60)
print("📊 RESUMEN GENERAL DE RESERVAS")
print("="*60)

print(f"Total de reservas (visitas): {len(reservas):,}")
print(f"Clientes únicos: {reservas['ID del Cliente'].nunique():,}")
print(f"Clases distintas: {reservas['ID de la Clase'].nunique():,}")
print(f"Locales: {reservas['Nombre de la Ubicacion'].nunique():,}\n")

print("🏢 Reservas por local:")
res_por_local = reservas['Nombre de la Ubicacion'].value_counts()
for loc, n in res_por_local.items():
    clientes_loc = reservas[reservas['Nombre de la Ubicacion'] == loc]['ID del Cliente'].nunique()
    print(f"  - {loc}: {n:,} reservas | {clientes_loc:,} clientes")

print("\n📅 Reservas por mes (total):")
res_por_mes = reservas.groupby('Mes_Nombre').size()
display(res_por_mes.to_frame('Reservas'))
```

```plaintext


->

# 5. Evolución de reservas totales por mes y por local

# Agrupar reservas por mes y local
res_mes_loc = (
    reservas
    .groupby(['Año-Mes', 'Nombre de la Ubicacion'])
    .size()
    .reset_index(name='Reservas')
)

pivot_res_mes_loc = res_mes_loc.pivot(index='Año-Mes', columns='Nombre de la Ubicacion', values='Reservas').fillna(0)

# Orden cronológico
pivot_res_mes_loc = pivot_res_mes_loc.sort_index()

# Calcular total
pivot_res_mes_loc['TOTAL'] = pivot_res_mes_loc.sum(axis=1)

print("📊 Tabla de reservas por mes y local:")
display(pivot_res_mes_loc.astype(int))

# Gráfico similar al de clientes activos
fig, ax = plt.subplots(figsize=(16, 8))

meses = [str(p) for p in pivot_res_mes_loc.index]
x = np.arange(len(meses))

color_lopez = '#2E86AB'
color_trafalgar = '#A23B72'
color_total = '#1a1a2e'

lopez_data = pivot_res_mes_loc.get('López de Hoyos - esBarre', pd.Series(0, index=pivot_res_mes_loc.index)).values
trafalgar_data = pivot_res_mes_loc.get('Trafalgar - esBarré', pd.Series(0, index=pivot_res_mes_loc.index)).values
total_data = pivot_res_mes_loc['TOTAL'].values

width = 0.6
ax.bar(x, lopez_data, width, label='López de Hoyos', color=color_lopez, alpha=0.85, edgecolor='white')
ax.bar(x, trafalgar_data, width, bottom=lopez_data, label='Trafalgar', color=color_trafalgar, alpha=0.85, edgecolor='white')

ax.plot(x, total_data, color=color_total, linewidth=3, marker='o', markersize=8,
        label='Total reservas', zorder=5, markerfacecolor='white', markeredgewidth=2)

for i, total in enumerate(total_data):
    ax.annotate(f'{int(total):,}', (x[i], total), textcoords='offset points',
                xytext=(0, 10), ha='center', fontsize=9, fontweight='bold', color=color_total)

ax.set_xlabel('Mes', fontsize=13, fontweight='bold')
ax.set_ylabel('Reservas (visitas)', fontsize=13, fontweight='bold')
ax.set_title('📊 Evolución de Reservas Totales por Mes (sin agosto)', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels([m[2:] for m in meses], rotation=45, ha='right')
ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
ax.grid(True, axis='y', linestyle='--', alpha=0.3)
ax.set_facecolor('#fafbfc')
fig.patch.set_facecolor('white')

plt.tight_layout()
plt.show()
```

Perfecto, ya tienes un nuevo notebook llamado `analisis_reservas.ipynb` con las primeras piezas del análisis de reservas.

En ese notebook he añadido:

- **Celda 0 (markdown)**: título y objetivos del análisis de reservas.
- **Celda 1**: importación de librerías y configuración de pandas / matplotlib.
- **Celda 2**: carga del fichero `Detailed Visit Information.json` a un `DataFrame` llamado `reservas`.
- **Celda 3**: preparación de fechas, creación de columnas de año/mes, exclusión de **agosto** y de **diciembre 2025**.
- **Celda 4**: resumen general rápido (totales, por local y por mes).
- **Celda 5**: tabla y gráfica de **evolución de reservas totales por mes y por local**, con barras apiladas y línea de total.

Siguiente paso: abre `analisis_reservas.ipynb` y ejecuta las celdas 0–5 en orden; a partir de ahí podemos añadir reservas por persona, nuevos vs recurrentes y tipos de reserva en este notebook limpio.

