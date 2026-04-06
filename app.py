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
  ArrowUpRight
} from 'lucide-react';
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';

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
    <div className="min-h-screen bg-[#050507] text-slate-100 font-sans">
      {/* SIDEBAR */}
      <aside className="fixed left-0 top-0 h-full w-64 bg-black/40 backdrop-blur-2xl border-r border-white/5 z-50 flex flex-col">
        <div className="p-8">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-br from-purple-600 to-pink-500 rounded-lg shadow-[0_0_15px_rgba(168,85,247,0.5)]" />
            <h1 className="text-xl font-bold tracking-tighter uppercase italic">
              Ortho<span className="text-pink-500">Klin</span>
            </h1>
          </div>
        </div>

        <nav className="flex-1 px-4 space-y-1">
          <NavItem icon={<LayoutDashboard size={18} />} label="Dashboard" active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')} />
          <NavItem icon={<Users size={18} />} label="Pacientes" active={activeTab === 'pacientes'} onClick={() => setActiveTab('pacientes')} />
          <NavItem icon={<TrendingUp size={18} />} label="Faturamento" active={activeTab === 'financas'} onClick={() => setActiveTab('financas')} />
          <NavItem icon={<Settings size={18} />} label="Configurações" active={activeTab === 'settings'} onClick={() => setActiveTab('settings')} />
        </nav>

        <div className="p-6 border-t border-white/5">
          <button className="flex items-center gap-3 text-slate-500 hover:text-pink-500 transition-all text-xs font-bold uppercase tracking-widest">
            <LogOut size={16} /> Sair
          </button>
        </div>
      </aside>

      {/* CONTEÚDO */}
      <main className="ml-64 p-10">
        <header className="flex justify-between items-center mb-12">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-600" size={16} />
            <input type="text" placeholder="BUSCAR INTELIGÊNCIA..." className="bg-white/5 border border-white/10 rounded-md pl-10 pr-4 py-2 text-xs focus:outline-none focus:border-purple-500 w-64 transition-all" />
          </div>
          
          <div className="flex items-center gap-6">
            <Bell size={20} className="text-slate-400 cursor-pointer" />
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-purple-500 to-pink-500 p-[1px]">
              <div className="w-full h-full rounded-full bg-black flex items-center justify-center text-[10px] font-bold">OK</div>
            </div>
          </div>
        </header>

        {/* CARDS KPIS */}
        <div className="grid grid-cols-3 gap-6 mb-10">
          <KPICard label="PENDENTES" value="R$ 12.450" color="purple" />
          <KPICard label="CONVERSÃO" value="74%" color="pink" />
          <KPICard label="TOTAL" value="R$ 89.200" color="white" />
        </div>

        {/* GRÁFICO */}
        <div className="bg-white/5 border border-white/10 rounded-2xl p-8 shadow-2xl">
          <h3 className="text-xs font-bold tracking-[3px] text-slate-500 uppercase mb-8">Performance de Fluxo</h3>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data}>
                <defs>
                  <linearGradient id="grad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#e91e63" stopOpacity={0.4}/>
                    <stop offset="100%" stopColor="#e91e63" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#ffffff05" />
                <XAxis dataKey="name" hide />
                <Tooltip contentStyle={{backgroundColor: '#000', border: '1px solid #333', borderRadius: '8px', fontSize: '12px'}} />
                <Area type="monotone" dataKey="valor" stroke="#e91e63" strokeWidth={3} fill="url(#grad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </main>
    </div>
  );
};

// COMPONENTES AUXILIARES
const NavItem = ({ icon, label, active, onClick }) => (
  <button onClick={onClick} className={`w-full flex items-center gap-4 px-4 py-3 rounded-lg transition-all ${active ? 'bg-gradient-to-r from-purple-600/20 to-transparent text-white border-l-2 border-purple-500' : 'text-slate-500 hover:text-slate-300'}`}>
    {icon} <span className="text-[11px] font-bold uppercase tracking-widest">{label}</span>
  </button>
);

const KPICard = ({ label, value, color }) => (
  <div className="bg-white/5 border border-white/10 p-6 rounded-2xl hover:border-purple-500/50 transition-all group">
    <p className="text-[10px] font-bold text-slate-500 tracking-[2px] mb-2">{label}</p>
    <h2 className={`text-2xl font-black ${color === 'pink' ? 'text-pink-500' : color === 'purple' ? 'text-purple-500' : 'text-white'}`}>{value}</h2>
  </div>
);

export default Dashboard;
