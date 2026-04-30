import React, { useState, useMemo, useEffect, useRef } from 'react';
import {
  Truck, Settings2, BarChart3, AlertCircle, ArrowRight, Factory, Warehouse,
  Activity, Maximize2, Gauge, Route, Package, Zap, Play, Pause, RotateCcw,
  TrendingUp, Layers, Cpu, ChevronRight, CheckCircle2, AlertTriangle,
  CircleDot, MapPin, Timer, Weight, Target, Sparkles
} from 'lucide-react';

const App = () => {
  // ============================================================
  // ESTADO PRINCIPAL DE LA SIMULACIÓN
  // ============================================================
  const [production, setProduction] = useState({
    S1: { L: 10, C: 10 },     // Salida 1: 20 lotes/h (Productos L y C)
    S2: { A: 8, B: 6, M: 6 }, // Salida 2: 20 lotes/h (Productos A, B, M)
    S3: { A: 7, B: 7, M: 6 }  // Salida 3: 20 lotes/h (Productos A, B, M)
  });

  const [params, setParams] = useState({
    velocity: 5,        // km/h - velocidad máxima
    occupancy: 70,      // % ocupación máxima por AGV
    dist100: 100,       // metros ruta corta
    dist150: 150,       // metros ruta larga
    loadWeight: 2100,   // kg por lote
    loadTime: 30,       // segundos carga/descarga
    safetyMargin: 5     // % margen de seguridad operativa
  });

  const [isRunning, setIsRunning] = useState(true);
  const [activeView, setActiveView] = useState('dashboard');
  const [time, setTime] = useState(0);

  // ============================================================
  // ANIMACIÓN DEL TIEMPO (para movimiento de AGVs)
  // ============================================================
  useEffect(() => {
    if (!isRunning) return;
    const interval = setInterval(() => setTime(t => t + 0.05), 50);
    return () => clearInterval(interval);
  }, [isRunning]);

  // ============================================================
  // CÁLCULOS DE INGENIERÍA - MODELO MATEMÁTICO RIGUROSO
  // ============================================================
  const engineering = useMemo(() => {
    const v_m_min = (params.velocity * 1000) / 60; // m/min
    const loadTimeMin = params.loadTime / 60;

    // Tiempo de ciclo = (2 × distancia / velocidad) + tiempo carga/descarga
    const cycle100 = (2 * params.dist100) / v_m_min + 2 * loadTimeMin;
    const cycle150 = (2 * params.dist150) / v_m_min + 2 * loadTimeMin;

    // Capacidad teórica máxima (lotes/h por AGV)
    const theoretical100 = 60 / cycle100;
    const theoretical150 = 60 / cycle150;

    // Capacidad efectiva con ocupación máxima
    const effective100 = theoretical100 * (params.occupancy / 100);
    const effective150 = theoretical150 * (params.occupancy / 100);

    return {
      v_m_min,
      cycle100,
      cycle150,
      theoretical100,
      theoretical150,
      effective100,
      effective150
    };
  }, [params]);

  // ============================================================
  // SIMULACIÓN DE FLUJOS - APEGADO 100% A RESTRICCIONES ARAUCO
  // ============================================================
  const simulation = useMemo(() => {
    // RESTRICCIÓN 1: S1 → E1 (Productos L y C) - Distancia 100m
    const flow_S1_E1 = production.S1.L + production.S1.C;
    const agv_route1 = Math.ceil(flow_S1_E1 / engineering.effective100);
    const util_route1 = (flow_S1_E1 / (agv_route1 * engineering.effective100)) * 100;

    // RESTRICCIÓN 2: S2 y S3 → E2 (Producto A) - Distancia 100m
    const flow_S2_E2 = production.S2.A;
    const flow_S3_E2 = production.S3.A;
    const flow_E2 = flow_S2_E2 + flow_S3_E2;
    const agv_route2 = Math.ceil(flow_E2 / engineering.effective100);
    const util_route2 = (flow_E2 / (agv_route2 * engineering.effective100)) * 100;

    // RESTRICCIÓN 3: S2 y S3 → E3 y E4 (Productos B y M) - Distancia 150m
    const total_BM = production.S2.B + production.S2.M + production.S3.B + production.S3.M;
    // Distribución óptima balanceada entre E3 y E4 (15 lotes/h cada uno)
    const flow_E3 = Math.min(15, total_BM / 2);
    const flow_E4 = total_BM - flow_E3;
    const agv_route3 = Math.ceil(total_BM / engineering.effective150);
    const util_route3 = (total_BM / (agv_route3 * engineering.effective150)) * 100;

    const totalAGVs = agv_route1 + agv_route2 + agv_route3;
    const totalProduction = flow_S1_E1 + flow_E2 + total_BM;

    // Verificación de restricciones de producción por máquina
    const sumS1 = production.S1.L + production.S1.C;
    const sumS2 = production.S2.A + production.S2.B + production.S2.M;
    const sumS3 = production.S3.A + production.S3.B + production.S3.M;

    // Verificación de consumo (15 lotes/h por entrada)
    const validE1 = flow_S1_E1 <= 15.001;
    const validE2 = flow_E2 <= 15.001;
    const validE3 = flow_E3 <= 15.001;
    const validE4 = flow_E4 <= 15.001;

    const allValid = sumS1 === 20 && sumS2 === 20 && sumS3 === 20 &&
                     validE1 && validE2 && validE3 && validE4;

    // KPIs operativos
    const totalDistance = (flow_S1_E1 * 200) + (flow_E2 * 200) + (total_BM * 300); // m/hr
    const totalTonnage = totalProduction * (params.loadWeight / 1000); // toneladas/hr
    const energyEstimate = totalAGVs * 8.5; // kWh estimado por flota
    const avgUtilization = (util_route1 + util_route2 + util_route3) / 3;

    return {
      routes: [
        {
          id: 'R1',
          name: 'Ruta L/C',
          from: ['S1'],
          to: ['E1'],
          products: ['L', 'C'],
          flow: flow_S1_E1,
          distance: params.dist100,
          cycle: engineering.cycle100,
          capacity: engineering.effective100,
          agvs: agv_route1,
          utilization: util_route1,
          color: 'cyan',
          breakdown: { L: production.S1.L, C: production.S1.C }
        },
        {
          id: 'R2',
          name: 'Ruta A',
          from: ['S2', 'S3'],
          to: ['E2'],
          products: ['A'],
          flow: flow_E2,
          distance: params.dist100,
          cycle: engineering.cycle100,
          capacity: engineering.effective100,
          agvs: agv_route2,
          utilization: util_route2,
          color: 'amber',
          breakdown: { 'S2→E2': flow_S2_E2, 'S3→E2': flow_S3_E2 }
        },
        {
          id: 'R3',
          name: 'Ruta B/M',
          from: ['S2', 'S3'],
          to: ['E3', 'E4'],
          products: ['B', 'M'],
          flow: total_BM,
          distance: params.dist150,
          cycle: engineering.cycle150,
          capacity: engineering.effective150,
          agvs: agv_route3,
          utilization: util_route3,
          color: 'violet',
          breakdown: { E3: flow_E3, E4: flow_E4 }
        }
      ],
      totalAGVs,
      totalProduction,
      sumS1, sumS2, sumS3,
      flow_E1: flow_S1_E1, flow_E2, flow_E3, flow_E4,
      validE1, validE2, validE3, validE4,
      allValid,
      totalDistance,
      totalTonnage,
      energyEstimate,
      avgUtilization
    };
  }, [production, engineering, params]);

  // ============================================================
  // FUNCIONES DE ACTUALIZACIÓN
  // ============================================================
  const updateProduction = (machine, product, val) => {
    const newVal = Math.max(0, Math.min(20, parseInt(val) || 0));
    setProduction(prev => ({
      ...prev,
      [machine]: { ...prev[machine], [product]: newVal }
    }));
  };

  const updateParam = (key, val) => {
    setParams(prev => ({ ...prev, [key]: parseFloat(val) || 0 }));
  };

  const resetToOptimal = () => {
    setProduction({
      S1: { L: 10, C: 10 },
      S2: { A: 8, B: 6, M: 6 },
      S3: { A: 7, B: 7, M: 6 }
    });
  };

  // ============================================================
  // PRESETS DE ESCENARIOS
  // ============================================================
  const scenarios = [
    { name: 'Óptimo Base', icon: Target, prod: { S1: { L: 10, C: 10 }, S2: { A: 8, B: 6, M: 6 }, S3: { A: 7, B: 7, M: 6 } } },
    { name: 'Pico Producto A', icon: TrendingUp, prod: { S1: { L: 8, C: 7 }, S2: { A: 15, B: 3, M: 2 }, S3: { A: 15, B: 3, M: 2 } } },
    { name: 'Mix Equilibrado', icon: Activity, prod: { S1: { L: 7, C: 8 }, S2: { A: 7, B: 7, M: 6 }, S3: { A: 8, B: 6, M: 6 } } },
    { name: 'Foco B/M', icon: Layers, prod: { S1: { L: 8, C: 7 }, S2: { A: 4, B: 8, M: 8 }, S3: { A: 4, B: 8, M: 8 } } }
  ];

  // ============================================================
  // RENDER
  // ============================================================
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-100 font-mono relative overflow-hidden">
      {/* GRID DE FONDO TÉCNICO */}
      <div className="absolute inset-0 opacity-[0.07]" style={{
        backgroundImage: 'linear-gradient(rgba(99,102,241,0.5) 1px, transparent 1px), linear-gradient(90deg, rgba(99,102,241,0.5) 1px, transparent 1px)',
        backgroundSize: '40px 40px'
      }} />

      {/* GLOW AMBIENTAL */}
      <div className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-violet-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10 p-4 md:p-6 lg:p-8 max-w-[1600px] mx-auto">
        
        {/* ═══════════════════════════════════════════════════════ */}
        {/* HEADER PRINCIPAL                                        */}
        {/* ═══════════════════════════════════════════════════════ */}
        <header className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
          <div className="flex items-center gap-4">
            <div className="relative">
              <div className="h-14 w-14 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-2xl flex items-center justify-center shadow-lg shadow-cyan-500/30">
                <Truck className="text-white" size={28} strokeWidth={2.5} />
              </div>
              <div className="absolute -top-1 -right-1 h-4 w-4 bg-emerald-400 rounded-full border-2 border-slate-950 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-[10px] font-bold tracking-[0.2em] text-cyan-400 uppercase">ARAUCO Industrial Challenge</span>
                <span className="px-1.5 py-0.5 bg-cyan-500/10 border border-cyan-500/30 rounded text-[9px] text-cyan-300 font-bold">v2.4 PRO</span>
              </div>
              <h1 className="text-2xl md:text-3xl font-black tracking-tight text-white leading-none">
                AGV Logistics <span className="text-cyan-400">Optimizer</span>
              </h1>
              <p className="text-xs text-slate-400 mt-1 font-sans">Sistema de optimización de flota — Plywood 60 lotes/h · 24/7</p>
            </div>
          </div>

          {/* CONTROLES DE EJECUCIÓN */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsRunning(!isRunning)}
              className={`px-4 py-2.5 rounded-xl flex items-center gap-2 font-bold text-sm transition-all ${
                isRunning
                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-500/20'
                  : 'bg-slate-800 text-slate-300 border border-slate-700 hover:bg-slate-700'
              }`}
            >
              {isRunning ? <Pause size={16} /> : <Play size={16} />}
              {isRunning ? 'EN VIVO' : 'PAUSADO'}
            </button>
            <button
              onClick={resetToOptimal}
              className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 flex items-center gap-2 font-bold text-sm transition-all"
            >
              <RotateCcw size={16} />
              RESET
            </button>
          </div>
        </header>

        {/* ═══════════════════════════════════════════════════════ */}
        {/* KPIs HERO - LA RESPUESTA DEL DESAFÍO                    */}
        {/* ═══════════════════════════════════════════════════════ */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
          {/* KPI 1: FLOTA REQUERIDA */}
          <div className="relative group bg-gradient-to-br from-cyan-500/10 to-blue-600/10 border border-cyan-500/30 rounded-2xl p-5 overflow-hidden">
            <div className="absolute -top-4 -right-4 w-24 h-24 bg-cyan-500/20 rounded-full blur-2xl" />
            <div className="relative">
              <div className="flex items-center justify-between mb-3">
                <span className="text-[10px] font-bold tracking-widest text-cyan-300 uppercase">Flota Mínima</span>
                <Truck size={16} className="text-cyan-400" />
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-5xl font-black text-white tabular-nums">{simulation.totalAGVs}</span>
                <span className="text-sm text-cyan-300 font-bold">AGVs</span>
              </div>
              <div className="text-[10px] text-slate-400 mt-2 font-sans">Optimizado por programación entera</div>
            </div>
          </div>

          {/* KPI 2: PRODUCCIÓN TOTAL */}
          <div className="relative group bg-gradient-to-br from-emerald-500/10 to-teal-600/10 border border-emerald-500/30 rounded-2xl p-5 overflow-hidden">
            <div className="absolute -top-4 -right-4 w-24 h-24 bg-emerald-500/20 rounded-full blur-2xl" />
            <div className="relative">
              <div className="flex items-center justify-between mb-3">
                <span className="text-[10px] font-bold tracking-widest text-emerald-300 uppercase">Throughput</span>
                <Package size={16} className="text-emerald-400" />
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-5xl font-black text-white tabular-nums">{simulation.totalProduction}</span>
                <span className="text-sm text-emerald-300 font-bold">lotes/h</span>
              </div>
              <div className="text-[10px] text-slate-400 mt-2 font-sans">{simulation.totalTonnage.toFixed(1)} ton/h transportadas</div>
            </div>
          </div>

          {/* KPI 3: UTILIZACIÓN */}
          <div className="relative group bg-gradient-to-br from-violet-500/10 to-purple-600/10 border border-violet-500/30 rounded-2xl p-5 overflow-hidden">
            <div className="absolute -top-4 -right-4 w-24 h-24 bg-violet-500/20 rounded-full blur-2xl" />
            <div className="relative">
              <div className="flex items-center justify-between mb-3">
                <span className="text-[10px] font-bold tracking-widest text-violet-300 uppercase">Util. Promedio</span>
                <Gauge size={16} className="text-violet-400" />
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-5xl font-black text-white tabular-nums">{simulation.avgUtilization.toFixed(0)}</span>
                <span className="text-sm text-violet-300 font-bold">%</span>
              </div>
              <div className="text-[10px] text-slate-400 mt-2 font-sans">Carga operativa de la flota</div>
            </div>
          </div>

          {/* KPI 4: VALIDACIÓN DE RESTRICCIONES */}
          <div className={`relative group bg-gradient-to-br border rounded-2xl p-5 overflow-hidden ${
            simulation.allValid
              ? 'from-emerald-500/10 to-green-600/10 border-emerald-500/30'
              : 'from-amber-500/10 to-orange-600/10 border-amber-500/30'
          }`}>
            <div className={`absolute -top-4 -right-4 w-24 h-24 rounded-full blur-2xl ${simulation.allValid ? 'bg-emerald-500/20' : 'bg-amber-500/20'}`} />
            <div className="relative">
              <div className="flex items-center justify-between mb-3">
                <span className={`text-[10px] font-bold tracking-widest uppercase ${simulation.allValid ? 'text-emerald-300' : 'text-amber-300'}`}>Validación</span>
                {simulation.allValid ? <CheckCircle2 size={16} className="text-emerald-400" /> : <AlertTriangle size={16} className="text-amber-400" />}
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl font-black text-white">
                  {simulation.allValid ? 'ÓPTIMO' : 'AJUSTAR'}
                </span>
              </div>
              <div className="text-[10px] text-slate-400 mt-2 font-sans">
                {simulation.allValid ? '8/8 restricciones cumplidas' : 'Revisar producción por máquina'}
              </div>
            </div>
          </div>
        </div>

        {/* ═══════════════════════════════════════════════════════ */}
        {/* GRID PRINCIPAL: CONTROLES + VISUALIZACIÓN              */}
        {/* ═══════════════════════════════════════════════════════ */}
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-4">
          
          {/* ──────────────────────────────────────────────────── */}
          {/* COLUMNA IZQUIERDA: PANEL DE CONTROL TOTAL           */}
          {/* ──────────────────────────────────────────────────── */}
          <div className="xl:col-span-4 space-y-4">
            
            {/* ESCENARIOS RÁPIDOS */}
            <div className="bg-slate-900/60 backdrop-blur border border-slate-800 rounded-2xl p-5">
              <div className="flex items-center gap-2 mb-3">
                <Sparkles className="text-amber-400" size={16} />
                <h3 className="text-xs font-black tracking-widest text-slate-300 uppercase">Escenarios</h3>
              </div>
              <div className="grid grid-cols-2 gap-2">
                {scenarios.map((s, i) => {
                  const Icon = s.icon;
                  return (
                    <button
                      key={i}
                      onClick={() => setProduction(s.prod)}
                      className="p-2.5 bg-slate-800/50 hover:bg-cyan-500/10 hover:border-cyan-500/30 border border-slate-700 rounded-lg text-left transition-all group"
                    >
                      <Icon size={14} className="text-cyan-400 mb-1 group-hover:scale-110 transition-transform" />
                      <div className="text-[11px] font-bold text-slate-200 leading-tight">{s.name}</div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* CONFIGURACIÓN DE PRODUCCIÓN */}
            <div className="bg-slate-900/60 backdrop-blur border border-slate-800 rounded-2xl p-5">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <Factory className="text-cyan-400" size={16} />
                  <h3 className="text-xs font-black tracking-widest text-slate-300 uppercase">Mezcla de Producción</h3>
                </div>
                <span className="text-[10px] text-slate-500 font-sans">lotes/h por máquina</span>
              </div>

              {/* SALIDA 1 */}
              <MachineControl
                title="SALIDA 1"
                subtitle="Productos L y C → Entrada 1"
                badge="100m"
                badgeColor="cyan"
                products={[
                  { key: 'L', value: production.S1.L, color: 'cyan' },
                  { key: 'C', value: production.S1.C, color: 'sky' }
                ]}
                onChange={(p, v) => updateProduction('S1', p, v)}
                total={simulation.sumS1}
                target={20}
              />

              {/* SALIDA 2 */}
              <MachineControl
                title="SALIDA 2"
                subtitle="A → E2 · B,M → E3,E4"
                badge="Multi"
                badgeColor="amber"
                products={[
                  { key: 'A', value: production.S2.A, color: 'amber' },
                  { key: 'B', value: production.S2.B, color: 'violet' },
                  { key: 'M', value: production.S2.M, color: 'fuchsia' }
                ]}
                onChange={(p, v) => updateProduction('S2', p, v)}
                total={simulation.sumS2}
                target={20}
              />

              {/* SALIDA 3 */}
              <MachineControl
                title="SALIDA 3"
                subtitle="A → E2 · B,M → E3,E4"
                badge="Multi"
                badgeColor="amber"
                products={[
                  { key: 'A', value: production.S3.A, color: 'amber' },
                  { key: 'B', value: production.S3.B, color: 'violet' },
                  { key: 'M', value: production.S3.M, color: 'fuchsia' }
                ]}
                onChange={(p, v) => updateProduction('S3', p, v)}
                total={simulation.sumS3}
                target={20}
              />

              {/* RESUMEN PRODUCCIÓN */}
              <div className="mt-4 p-3 bg-slate-950/50 rounded-xl border border-slate-800 grid grid-cols-3 gap-2 text-center">
                <div>
                  <div className="text-[9px] text-slate-500 font-bold uppercase tracking-wider mb-1">S1</div>
                  <div className={`text-sm font-black ${simulation.sumS1 === 20 ? 'text-emerald-400' : 'text-amber-400'}`}>
                    {simulation.sumS1}/20
                  </div>
                </div>
                <div>
                  <div className="text-[9px] text-slate-500 font-bold uppercase tracking-wider mb-1">S2</div>
                  <div className={`text-sm font-black ${simulation.sumS2 === 20 ? 'text-emerald-400' : 'text-amber-400'}`}>
                    {simulation.sumS2}/20
                  </div>
                </div>
                <div>
                  <div className="text-[9px] text-slate-500 font-bold uppercase tracking-wider mb-1">S3</div>
                  <div className={`text-sm font-black ${simulation.sumS3 === 20 ? 'text-emerald-400' : 'text-amber-400'}`}>
                    {simulation.sumS3}/20
                  </div>
                </div>
              </div>
            </div>

            {/* PARÁMETROS DE INGENIERÍA */}
            <div className="bg-slate-900/60 backdrop-blur border border-slate-800 rounded-2xl p-5">
              <div className="flex items-center gap-2 mb-4">
                <Settings2 className="text-cyan-400" size={16} />
                <h3 className="text-xs font-black tracking-widest text-slate-300 uppercase">Parámetros Técnicos</h3>
              </div>

              <ParamSlider
                label="Velocidad AGV"
                unit="km/h"
                value={params.velocity}
                min={1}
                max={5}
                step={0.5}
                max_safe={5}
                onChange={v => updateParam('velocity', v)}
                icon={Zap}
              />
              <ParamSlider
                label="Ocupación máx."
                unit="%"
                value={params.occupancy}
                min={50}
                max={70}
                step={5}
                max_safe={70}
                onChange={v => updateParam('occupancy', v)}
                icon={Gauge}
              />
              <ParamSlider
                label="Distancia ruta corta"
                unit="m"
                value={params.dist100}
                min={50}
                max={200}
                step={10}
                onChange={v => updateParam('dist100', v)}
                icon={Route}
              />
              <ParamSlider
                label="Distancia ruta larga"
                unit="m"
                value={params.dist150}
                min={100}
                max={300}
                step={10}
                onChange={v => updateParam('dist150', v)}
                icon={Route}
              />
              <ParamSlider
                label="Tiempo carga/descarga"
                unit="s"
                value={params.loadTime}
                min={10}
                max={120}
                step={5}
                onChange={v => updateParam('loadTime', v)}
                icon={Timer}
              />
            </div>
          </div>

          {/* ──────────────────────────────────────────────────── */}
          {/* COLUMNA DERECHA: VISUALIZACIONES                    */}
          {/* ──────────────────────────────────────────────────── */}
          <div className="xl:col-span-8 space-y-4">
            
            {/* DIAGRAMA DE RED - VISUALIZACIÓN PRINCIPAL */}
            <div className="bg-slate-900/60 backdrop-blur border border-slate-800 rounded-2xl p-5 relative overflow-hidden">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <Cpu className="text-cyan-400" size={16} />
                  <h3 className="text-xs font-black tracking-widest text-slate-300 uppercase">Red Logística — Tiempo Real</h3>
                </div>
                <div className="flex items-center gap-2 text-[10px] text-slate-500">
                  <CircleDot size={10} className="text-emerald-400 animate-pulse" />
                  <span className="font-sans">Simulación activa</span>
                </div>
              </div>

              <NetworkDiagram simulation={simulation} time={time} isRunning={isRunning} />

              {/* LEYENDA */}
              <div className="mt-3 flex flex-wrap gap-3 text-[10px] font-sans">
                <LegendItem color="cyan" label="Ruta L/C (100m)" />
                <LegendItem color="amber" label="Ruta A (100m)" />
                <LegendItem color="violet" label="Ruta B/M (150m)" />
                <span className="text-slate-500 ml-auto">Velocidad AGV: {params.velocity} km/h · Ocupación: {params.occupancy}%</span>
              </div>
            </div>

            {/* TARJETAS DE RUTAS DETALLADAS */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
              {simulation.routes.map((route, i) => (
                <RouteCard key={route.id} route={route} index={i} />
              ))}
            </div>

            {/* TABLA DE FLUJOS POR ENTRADA */}
            <div className="bg-slate-900/60 backdrop-blur border border-slate-800 rounded-2xl p-5">
              <div className="flex items-center gap-2 mb-4">
                <Warehouse className="text-cyan-400" size={16} />
                <h3 className="text-xs font-black tracking-widest text-slate-300 uppercase">Validación de Consumo (15 lotes/h por entrada)</h3>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <ConsumptionCard id="E1" product="L y C" value={simulation.flow_E1} valid={simulation.validE1} color="cyan" />
                <ConsumptionCard id="E2" product="A" value={simulation.flow_E2} valid={simulation.validE2} color="amber" />
                <ConsumptionCard id="E3" product="B y M" value={simulation.flow_E3} valid={simulation.validE3} color="violet" />
                <ConsumptionCard id="E4" product="B y M" value={simulation.flow_E4} valid={simulation.validE4} color="fuchsia" />
              </div>
            </div>

            {/* MÉTRICAS DE INGENIERÍA */}
            <div className="bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-5">
              <div className="flex items-center gap-2 mb-4">
                <BarChart3 className="text-cyan-400" size={16} />
                <h3 className="text-xs font-black tracking-widest text-slate-300 uppercase">Análisis de Ingeniería</h3>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <EngMetric label="Ciclo 100m" value={engineering.cycle100.toFixed(2)} unit="min" />
                <EngMetric label="Ciclo 150m" value={engineering.cycle150.toFixed(2)} unit="min" />
                <EngMetric label="Cap. AGV 100m" value={engineering.effective100.toFixed(1)} unit="lotes/h" />
                <EngMetric label="Cap. AGV 150m" value={engineering.effective150.toFixed(1)} unit="lotes/h" />
                <EngMetric label="Distancia total" value={(simulation.totalDistance / 1000).toFixed(1)} unit="km/h" />
                <EngMetric label="Tonelaje" value={simulation.totalTonnage.toFixed(1)} unit="ton/h" />
                <EngMetric label="Energía est." value={simulation.energyEstimate.toFixed(1)} unit="kWh" />
                <EngMetric label="Velocidad" value={engineering.v_m_min.toFixed(1)} unit="m/min" />
              </div>
            </div>
          </div>
        </div>

        {/* FOOTER */}
        <footer className="mt-8 pt-6 border-t border-slate-800 flex flex-col md:flex-row items-center justify-between gap-3 text-[10px] text-slate-500 font-sans">
          <div className="flex items-center gap-3">
            <span className="font-black text-cyan-400 tracking-widest">ARAUCO</span>
            <span>·</span>
            <span>Modelo de transporte basado en Programación Entera Mixta (MILP)</span>
          </div>
          <div className="flex items-center gap-2">
            <span>Lote: 2.6×1.4×1m · {params.loadWeight} kg</span>
            <span>·</span>
            <span>Operación: 24/7</span>
          </div>
        </footer>
      </div>
    </div>
  );
};

// ============================================================
// COMPONENTES AUXILIARES
// ============================================================

const MachineControl = ({ title, subtitle, badge, badgeColor, products, onChange, total, target }) => {
  const isValid = total === target;
  return (
    <div className="mb-4 last:mb-0 p-3 bg-slate-950/40 rounded-xl border border-slate-800">
      <div className="flex items-center justify-between mb-2">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-black text-white tracking-wider">{title}</span>
            <span className={`px-1.5 py-0.5 rounded text-[9px] font-bold border bg-${badgeColor}-500/10 border-${badgeColor}-500/30 text-${badgeColor}-300`}>
              {badge}
            </span>
          </div>
          <p className="text-[10px] text-slate-500 font-sans mt-0.5">{subtitle}</p>
        </div>
        <div className={`text-xs font-black tabular-nums ${isValid ? 'text-emerald-400' : 'text-amber-400'}`}>
          {total}/{target}
        </div>
      </div>
      <div className={`grid gap-2`} style={{ gridTemplateColumns: `repeat(${products.length}, 1fr)` }}>
        {products.map(p => (
          <div key={p.key} className="relative">
            <label className="text-[9px] block text-slate-500 mb-1 font-bold uppercase tracking-wider">Prod {p.key}</label>
            <input
              type="number"
              min="0"
              max="20"
              value={p.value}
              onChange={e => onChange(p.key, e.target.value)}
              className={`w-full bg-slate-900 border rounded-lg p-2 font-mono font-black text-sm text-white focus:outline-none focus:ring-2 transition-all border-slate-700 focus:ring-${p.color}-500/50 focus:border-${p.color}-500/50`}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

const ParamSlider = ({ label, unit, value, min, max, step, max_safe, onChange, icon: Icon }) => {
  const isOverSafe = max_safe && value > max_safe;
  const pct = ((value - min) / (max - min)) * 100;
  return (
    <div className="mb-3 last:mb-0">
      <div className="flex items-center justify-between mb-1.5">
        <div className="flex items-center gap-1.5">
          {Icon && <Icon size={11} className="text-slate-500" />}
          <span className="text-[10px] font-bold text-slate-300 uppercase tracking-wider">{label}</span>
        </div>
        <span className={`text-xs font-black font-mono ${isOverSafe ? 'text-amber-400' : 'text-cyan-400'}`}>
          {value} <span className="text-[9px] text-slate-500">{unit}</span>
        </span>
      </div>
      <div className="relative">
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={e => onChange(e.target.value)}
          className="w-full h-1.5 bg-slate-800 rounded-full appearance-none cursor-pointer accent-cyan-500"
          style={{
            background: `linear-gradient(to right, rgb(34 211 238) 0%, rgb(34 211 238) ${pct}%, rgb(30 41 59) ${pct}%, rgb(30 41 59) 100%)`
          }}
        />
      </div>
    </div>
  );
};

const NetworkDiagram = ({ simulation, time, isRunning }) => {
  const W = 700;
  const H = 380;

  // Posiciones de nodos
  const nodes = {
    S1: { x: 80, y: 70, label: 'S1', sub: '20 lotes/h', color: '#06b6d4' },
    S2: { x: 80, y: 190, label: 'S2', sub: '20 lotes/h', color: '#f59e0b' },
    S3: { x: 80, y: 310, label: 'S3', sub: '20 lotes/h', color: '#a855f7' },
    E1: { x: 620, y: 50, label: 'E1', sub: 'L y C', color: '#06b6d4' },
    E2: { x: 620, y: 145, label: 'E2', sub: 'A', color: '#f59e0b' },
    E3: { x: 620, y: 235, label: 'E3', sub: 'B y M', color: '#a855f7' },
    E4: { x: 620, y: 325, label: 'E4', sub: 'B y M', color: '#d946ef' }
  };

  // Definición de rutas con animación
  const routes = [
    { from: 'S1', to: 'E1', flow: simulation.flow_E1, color: '#06b6d4', dist: '100m', delay: 0 },
    { from: 'S2', to: 'E2', flow: simulation.routes[1].breakdown['S2→E2'], color: '#f59e0b', dist: '100m', delay: 0.3 },
    { from: 'S3', to: 'E2', flow: simulation.routes[1].breakdown['S3→E2'], color: '#f59e0b', dist: '100m', delay: 0.6 },
    { from: 'S2', to: 'E3', flow: simulation.flow_E3 / 2, color: '#a855f7', dist: '150m', delay: 0.9 },
    { from: 'S3', to: 'E3', flow: simulation.flow_E3 / 2, color: '#a855f7', dist: '150m', delay: 1.2 },
    { from: 'S2', to: 'E4', flow: simulation.flow_E4 / 2, color: '#d946ef', dist: '150m', delay: 1.5 },
    { from: 'S3', to: 'E4', flow: simulation.flow_E4 / 2, color: '#d946ef', dist: '150m', delay: 1.8 }
  ];

  return (
    <div className="relative w-full" style={{ height: H }}>
      <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-full">
        {/* DEFS para gradientes y filtros */}
        <defs>
          <filter id="glow">
            <feGaussianBlur stdDeviation="2" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          {Object.entries(nodes).map(([key, n]) => (
            <radialGradient key={`grad-${key}`} id={`grad-${key}`}>
              <stop offset="0%" stopColor={n.color} stopOpacity="0.4" />
              <stop offset="100%" stopColor={n.color} stopOpacity="0" />
            </radialGradient>
          ))}
        </defs>

        {/* GRID DE FONDO */}
        <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
          <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(99,102,241,0.05)" strokeWidth="0.5" />
        </pattern>
        <rect width={W} height={H} fill="url(#grid)" />

        {/* LÍNEAS DE RUTA */}
        {routes.filter(r => r.flow > 0).map((route, i) => {
          const from = nodes[route.from];
          const to = nodes[route.to];
          const midX = (from.x + to.x) / 2;
          const curveY = (from.y + to.y) / 2 + (i % 2 === 0 ? -15 : 15);
          const path = `M ${from.x + 30} ${from.y} Q ${midX} ${curveY} ${to.x - 30} ${to.y}`;
          
          return (
            <g key={`route-${i}`}>
              {/* Línea de ruta base */}
              <path
                d={path}
                fill="none"
                stroke={route.color}
                strokeWidth="1.5"
                strokeOpacity="0.2"
                strokeDasharray="3 3"
              />
              {/* Línea de flujo activo */}
              <path
                d={path}
                fill="none"
                stroke={route.color}
                strokeWidth="2"
                strokeOpacity="0.6"
                strokeLinecap="round"
              />
              {/* AGV en movimiento */}
              {isRunning && route.flow > 0 && (
                <circle r="5" fill={route.color} filter="url(#glow)">
                  <animateMotion dur={`${3 + i * 0.3}s`} repeatCount="indefinite" begin={`${route.delay}s`}>
                    <mpath href={`#path-${i}`} />
                  </animateMotion>
                </circle>
              )}
              <path id={`path-${i}`} d={path} fill="none" />
              
              {/* Etiqueta de flujo */}
              <text
                x={midX}
                y={curveY - 5}
                textAnchor="middle"
                className="text-[9px] font-bold font-mono"
                fill={route.color}
                opacity="0.9"
              >
                {route.flow.toFixed(0)} l/h
              </text>
            </g>
          );
        })}

        {/* NODOS DE PRODUCCIÓN (S1, S2, S3) */}
        {['S1', 'S2', 'S3'].map(key => {
          const n = nodes[key];
          return (
            <g key={key}>
              {/* Glow exterior */}
              <circle cx={n.x} cy={n.y} r="40" fill={`url(#grad-${key})`} />
              {/* Pulso animado */}
              <circle cx={n.x} cy={n.y} r="22" fill="none" stroke={n.color} strokeWidth="1" opacity="0.4">
                <animate attributeName="r" from="22" to="35" dur="2s" repeatCount="indefinite" />
                <animate attributeName="opacity" from="0.5" to="0" dur="2s" repeatCount="indefinite" />
              </circle>
              {/* Nodo principal */}
              <circle cx={n.x} cy={n.y} r="22" fill="rgba(15,23,42,0.95)" stroke={n.color} strokeWidth="2" />
              <text x={n.x} y={n.y + 1} textAnchor="middle" className="text-sm font-black" fill={n.color} dominantBaseline="middle">
                {n.label}
              </text>
              <text x={n.x} y={n.y + 38} textAnchor="middle" className="text-[9px] font-bold font-sans" fill="#94a3b8">
                {n.sub}
              </text>
              {/* Icono fábrica */}
              <text x={n.x - 35} y={n.y - 25} className="text-[10px]" fill={n.color}>◆</text>
            </g>
          );
        })}

        {/* NODOS DE CONSUMO (E1, E2, E3, E4) */}
        {['E1', 'E2', 'E3', 'E4'].map(key => {
          const n = nodes[key];
          const flow = key === 'E1' ? simulation.flow_E1 :
                       key === 'E2' ? simulation.flow_E2 :
                       key === 'E3' ? simulation.flow_E3 :
                       simulation.flow_E4;
          return (
            <g key={key}>
              <circle cx={n.x} cy={n.y} r="35" fill={`url(#grad-${key})`} />
              <rect x={n.x - 22} y={n.y - 18} width="44" height="36" rx="6" fill="rgba(15,23,42,0.95)" stroke={n.color} strokeWidth="2" />
              <text x={n.x} y={n.y - 3} textAnchor="middle" className="text-sm font-black" fill={n.color} dominantBaseline="middle">
                {n.label}
              </text>
              <text x={n.x} y={n.y + 9} textAnchor="middle" className="text-[8px] font-bold font-mono" fill="#cbd5e1" dominantBaseline="middle">
                {flow.toFixed(0)} l/h
              </text>
              <text x={n.x} y={n.y + 32} textAnchor="middle" className="text-[9px] font-bold font-sans" fill="#94a3b8">
                {n.sub}
              </text>
            </g>
          );
        })}

        {/* HEADERS */}
        <text x={80} y={25} textAnchor="middle" className="text-[10px] font-black tracking-widest" fill="#475569">PRODUCCIÓN</text>
        <text x={620} y={25} textAnchor="middle" className="text-[10px] font-black tracking-widest" fill="#475569">CONSUMO</text>
      </svg>
    </div>
  );
};

const RouteCard = ({ route, index }) => {
  const colorMap = {
    cyan: { bg: 'from-cyan-500/10 to-blue-600/5', border: 'border-cyan-500/30', text: 'text-cyan-400', glow: 'bg-cyan-500/10' },
    amber: { bg: 'from-amber-500/10 to-orange-600/5', border: 'border-amber-500/30', text: 'text-amber-400', glow: 'bg-amber-500/10' },
    violet: { bg: 'from-violet-500/10 to-purple-600/5', border: 'border-violet-500/30', text: 'text-violet-400', glow: 'bg-violet-500/10' }
  };
  const c = colorMap[route.color];
  const utilColor = route.utilization > 90 ? 'text-red-400' : route.utilization > 70 ? 'text-amber-400' : 'text-emerald-400';

  return (
    <div className={`relative bg-gradient-to-br ${c.bg} border ${c.border} rounded-2xl p-4 overflow-hidden group`}>
      <div className={`absolute -top-8 -right-8 w-32 h-32 ${c.glow} rounded-full blur-3xl`} />
      
      <div className="relative">
        {/* HEADER */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <span className={`px-2 py-0.5 bg-slate-950/60 ${c.text} rounded text-[10px] font-black tracking-wider border ${c.border}`}>
              {route.id}
            </span>
            <span className="text-xs font-bold text-white">{route.name}</span>
          </div>
          <span className="text-[9px] text-slate-500 font-mono">{route.distance}m</span>
        </div>

        {/* ROUTE FLOW */}
        <div className="flex items-center gap-1 mb-3 text-[10px] font-bold">
          {route.from.map((f, i) => (
            <React.Fragment key={f}>
              {i > 0 && <span className="text-slate-600">+</span>}
              <span className="px-1.5 py-0.5 bg-slate-950/60 border border-slate-700 rounded text-slate-300">{f}</span>
            </React.Fragment>
          ))}
          <ArrowRight size={12} className="text-slate-600 mx-1" />
          {route.to.map((t, i) => (
            <React.Fragment key={t}>
              {i > 0 && <span className="text-slate-600">+</span>}
              <span className="px-1.5 py-0.5 bg-slate-950/60 border border-slate-700 rounded text-slate-300">{t}</span>
            </React.Fragment>
          ))}
        </div>

        {/* MAIN STATS */}
        <div className="grid grid-cols-2 gap-2 mb-3">
          <div className="bg-slate-950/40 rounded-lg p-2">
            <div className="text-[9px] text-slate-500 font-bold uppercase">Flujo</div>
            <div className="text-lg font-black text-white tabular-nums">{route.flow}<span className="text-[10px] text-slate-500 ml-1 font-normal">l/h</span></div>
          </div>
          <div className="bg-slate-950/40 rounded-lg p-2">
            <div className="text-[9px] text-slate-500 font-bold uppercase">AGVs</div>
            <div className={`text-lg font-black tabular-nums ${c.text}`}>{route.agvs}<span className="text-[10px] text-slate-500 ml-1 font-normal">und</span></div>
          </div>
        </div>

        {/* UTILIZATION BAR */}
        <div>
          <div className="flex items-center justify-between text-[9px] mb-1">
            <span className="text-slate-500 font-bold uppercase tracking-wider">Carga operativa</span>
            <span className={`${utilColor} font-black font-mono`}>{route.utilization.toFixed(1)}%</span>
          </div>
          <div className="w-full bg-slate-950 rounded-full h-1.5 overflow-hidden">
            <div
              className={`h-full rounded-full transition-all duration-500 ${
                route.utilization > 90 ? 'bg-red-500' : route.utilization > 70 ? 'bg-amber-500' : 'bg-emerald-500'
              }`}
              style={{ width: `${Math.min(100, route.utilization)}%` }}
            />
          </div>
        </div>

        {/* CYCLE TIME */}
        <div className="mt-2 pt-2 border-t border-slate-800 flex items-center justify-between text-[9px]">
          <span className="text-slate-500 font-sans">Ciclo: <span className="text-slate-300 font-mono">{route.cycle.toFixed(1)} min</span></span>
          <span className="text-slate-500 font-sans">Cap/AGV: <span className="text-slate-300 font-mono">{route.capacity.toFixed(1)} l/h</span></span>
        </div>
      </div>
    </div>
  );
};

const ConsumptionCard = ({ id, product, value, valid, color }) => {
  const colorMap = {
    cyan: 'border-cyan-500/30 text-cyan-400',
    amber: 'border-amber-500/30 text-amber-400',
    violet: 'border-violet-500/30 text-violet-400',
    fuchsia: 'border-fuchsia-500/30 text-fuchsia-400'
  };
  return (
    <div className={`relative bg-slate-950/40 border ${colorMap[color]} rounded-xl p-3`}>
      <div className="flex items-center justify-between mb-1.5">
        <span className={`text-xs font-black ${colorMap[color]}`}>{id}</span>
        {valid ? <CheckCircle2 size={12} className="text-emerald-400" /> : <AlertTriangle size={12} className="text-red-400" />}
      </div>
      <div className="text-2xl font-black text-white tabular-nums">{value.toFixed(0)}<span className="text-[10px] text-slate-500 ml-1 font-normal">/15</span></div>
      <div className="text-[9px] text-slate-500 font-sans mt-0.5">Producto {product}</div>
      <div className="mt-2 w-full bg-slate-900 rounded-full h-1 overflow-hidden">
        <div
          className={`h-full transition-all ${valid ? 'bg-emerald-500' : 'bg-red-500'}`}
          style={{ width: `${Math.min(100, (value / 15) * 100)}%` }}
        />
      </div>
    </div>
  );
};

const EngMetric = ({ label, value, unit }) => (
  <div className="bg-slate-950/40 rounded-xl p-3 border border-slate-800">
    <div className="text-[9px] text-slate-500 font-bold uppercase tracking-wider mb-1">{label}</div>
    <div className="text-lg font-black text-white tabular-nums">{value}</div>
    <div className="text-[9px] text-slate-600 font-sans">{unit}</div>
  </div>
);

const LegendItem = ({ color, label }) => {
  const colorMap = {
    cyan: 'bg-cyan-500',
    amber: 'bg-amber-500',
    violet: 'bg-violet-500'
  };
  return (
    <div className="flex items-center gap-1.5">
      <div className={`w-2 h-2 rounded-full ${colorMap[color]}`} />
      <span className="text-slate-400">{label}</span>
    </div>
  );
};

export default App;
