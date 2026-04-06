import React, { useState } from 'react';
import { 
  LayoutDashboard, 
  Users, 
  TrendingUp, 
  Settings, 
  Bell, 
  Search, 
  LogOut, 
  Plus,
  ArrowUpRight,
  MoreVertical
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';

// Mock Data para o Gráfico Futurista
const data = [
  { name: 'Seg', valor: 400 },
  { name: 'Ter', valor: 300 },
  { name: 'Qua', valor: 600 },
  { name: 'Qui', valor: 800 },
  { name: 'Sex', valor: 500 },
  { name: 'Sáb', valor: 900 },
  { name: 'Dom', valor: 700 },
];

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="min-h-screen bg-[#050507] text-slate-100 font-sans selection:bg-purple-500/30">
      
      {/* SIDEBAR FIXA - GLASSMORPHISM */}
      <aside className="fixed left-0 top-0 h-full w-64 bg-black/20 backdrop-blur-xl border-r border-white/10 z-50 flex flex-col">
        <div className="p-8">
          <div className="flex items-center gap-3 group cursor-pointer">
            <div className="w-10 h-10 bg-gradient-to-tr from-purple-600 to-pink-500 rounded-xl blur-[2px] group-hover:blur-none transition-all duration-500 shadow-[0_0_20px_rgba(168,85,247,0.4)]" />
            <h1 className="text-xl font-bold tracking-tighter bg-gradient-to-r from-white to-white/60 bg-clip-text text-transparent uppercase">
              OrthoKlin<span className="text-pink-500">.</span>
            </h1>
          </div>
        </div>

        <nav className="flex-1 px-4 space-y-2">
          <NavItem icon={<LayoutDashboard size={20} />} label="Dashboard" active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')} />
          <NavItem icon={<Users size={20} />} label="Pacientes" active={activeTab === 'pacientes'} onClick={() => setActiveTab('pacientes')} />
          <NavItem icon={<TrendingUp size={20} />} label="Faturamento" active={activeTab === 'finanças'} onClick={() => setActiveTab('finanças')} />
          <NavItem icon={<Settings size={20} />} label="Configurações" active={activeTab === 'settings'} onClick={() => setActiveTab('settings')} />
        </nav>

        <div className="p-4 border-t border-white/5">
          <button className="flex items-center gap-3 px-4 py-3 w-full text-slate-400 hover:text-pink-400 transition-colors duration-300">
            <LogOut size={20} />
            <span className="font-medium text-sm tracking-wide">Sair do Sistema</span>
          </button>
        </div>
      </aside>

      {/* ÁREA PRINCIPAL */}
      <main className="ml-64 p-8">
        
        {/* TOPBAR */}
        <header className="flex justify-between items-center mb-10">
          <div className="relative group">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-purple-400 transition-colors" size={18} />
            <input 
              type="text" 
              placeholder="Pesquisar inteligência..." 
              className="bg-white/5 border border-white/10 rounded-full pl-10 pr-6 py-2.5 w-80 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:bg-white/10 transition-all placeholder:text-slate-600 text-sm"
            />
          </div>

          <div className="flex items-center gap-6">
            <button className="relative p-2 bg-white/5 rounded-full hover:bg-white/10 transition-all border border-white/10 group">
              <Bell size={20} className="text-slate-400 group-hover:text-white" />
              <span className="absolute top-0 right-0 w-2.5 h-2.5 bg-pink-500 rounded-full border-2 border-[#050507]" />
            </button>
            <div className="flex items-center gap-3 pl-4 border-l border-white/10">
              <div className="text-right">
                <p className="text-xs text-slate-500 font-medium uppercase tracking-widest leading-none">Admin</p>
                <p className="text-sm font-bold">Dr. Ortho</p>
              </div>
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 p-[2px]">
                <div className="w-full h-full rounded-full bg-black flex items-center justify-center overflow-hidden">
                  <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="Avatar" />
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* GRID DE KPIS */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
